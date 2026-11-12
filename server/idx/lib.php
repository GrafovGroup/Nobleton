<?php
declare(strict_types=1);

// Only this directory, installed outside the document root, holds feed credentials/data.
const IDX_DIR = '/home/nvfglyl5/nobleton-private';
const IDX_ROOT = 'https://query.ampre.ca/odata/';
const IDX_MAX_AGE = 3600;

function idx_request(string $resource, array $query = []): array {
    $token = trim((string) @file_get_contents(IDX_DIR . '/idx-token'));
    if (!preg_match('/^[A-Za-z0-9_.-]+$/D', $token) || strlen($token) < 50) throw new RuntimeException('credential_missing');
    $url = IDX_ROOT . $resource . ($query ? '?' . http_build_query($query, '', '&', PHP_QUERY_RFC3986) : '');
    $ch = curl_init($url);
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER=>true, CURLOPT_FOLLOWLOCATION=>false,
        CURLOPT_CONNECTTIMEOUT=>10, CURLOPT_TIMEOUT=>60, CURLOPT_ENCODING=>'', CURLOPT_PROTOCOLS=>CURLPROTO_HTTPS,
        CURLOPT_HTTPHEADER=>['Authorization: Bearer ' . $token, 'Accept: '.($resource==='$metadata'?'application/xml':'application/json')],
        CURLOPT_USERAGENT=>'Nobleton.ca IDX/1.0']);
    $body = curl_exec($ch); $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE); curl_close($ch);
    if ($status === 401 || $status === 403) {
        @unlink(IDX_DIR . '/idx-cache.json');
        throw new RuntimeException('authorization_' . $status);
    }
    if ($status !== 200 || !is_string($body)) throw new RuntimeException('upstream_' . $status);
    if ($resource === '$metadata') return ['xml'=>$body];
    $data = json_decode(preg_replace('/^\x{FEFF}/u','',$body) ?? $body, true);
    if(json_last_error()!==JSON_ERROR_NONE) throw new RuntimeException('upstream_json_format');
    if (!is_array($data) || !isset($data['value']) || !is_array($data['value'])) throw new RuntimeException('upstream_format');
    return $data;
}

function idx_fields(string $xml, string $entity): array {
    $doc = simplexml_load_string($xml, 'SimpleXMLElement', LIBXML_NONET);
    if ($doc === false) throw new RuntimeException('metadata_format');
    $nodes = $doc->xpath('//*[local-name()="EntityType" and @Name="' . $entity . '"]/*[local-name()="Property"]');
    return array_map(static fn($n)=>(string)$n['Name'], $nodes ?: []);
}

function idx_permitted(array $row): bool {
    if (($row['CityRegion'] ?? '') !== 'Nobleton' || ($row['ContractStatus'] ?? '') !== 'Available') return false;
    foreach (['InternetEntireListingDisplayYN','DDFYN'] as $key) {
        if (array_key_exists($key,$row) && in_array($row[$key],[false,0,'0','N','No','false'],true)) return false;
    }
    return !empty($row['ListingKey']) && !empty($row['ListOfficeName']);
}

function idx_public_row(array $row): array {
    $keys = ['ListingKey','ListingId','ListPrice','TransactionType','PropertyType','PropertySubType','City','CityRegion',
        'UnparsedAddress','StreetNumber','StreetName','StreetSuffix','StreetDirSuffix','UnitNumber','PostalCode',
        'BedroomsTotal','BedroomsAboveGrade','BedroomsBelowGrade','BathroomsTotalInteger','ParkingTotal',
        'LivingAreaRange','LotSizeArea','LotSizeUnits','PublicRemarks','ListOfficeName','CoListOfficeName',
        'ModificationTimestamp','OriginalEntryTimestamp','ListPriceUnit','InternetAddressDisplayYN'];
    $out = array_intersect_key($row,array_flip($keys));
    if (isset($row['InternetAddressDisplayYN']) && in_array($row['InternetAddressDisplayYN'],[false,0,'0','N','No','false'],true)) {
        foreach (['UnparsedAddress','StreetNumber','StreetName','StreetSuffix','StreetDirSuffix','UnitNumber','PostalCode'] as $key) unset($out[$key]);
    }
    $photos=[];
    foreach (($row['Media'] ?? []) as $photo) {
        $url = $photo['MediaURL'] ?? '';
        if (!is_string($url) || strlen($url)>4000 || !filter_var($url,FILTER_VALIDATE_URL) || parse_url($url,PHP_URL_SCHEME)!=='https') continue;
        if (isset($photo['MediaType']) && !in_array($photo['MediaType'],['image/jpeg','image/png','image/webp'],true)) continue;
        $photos[]=['url'=>$url,'order'=>(int)($photo['Order']??0),'size'=>(string)($photo['ImageSizeDescription']??'')];
    }
    usort($photos,static fn($a,$b)=>$a['order']<=>$b['order']);
    $out['photos']=array_values(array_unique(array_column($photos,'url')));
    return $out;
}

function idx_sync(): void {
    umask(0077);
    $lock=fopen(IDX_DIR . '/idx-sync.lock','c');
    if (!$lock || !flock($lock,LOCK_EX|LOCK_NB)) throw new RuntimeException('sync_locked');
    try {
        $xml=idx_request('$metadata')['xml'];
        $fields=idx_fields($xml,'Property'); $mediaFields=idx_fields($xml,'Media');
        $required=['ListingKey','CityRegion','ContractStatus','ListOfficeName','ListPrice'];
        if (array_diff($required,$fields)) throw new RuntimeException('required_fields_unavailable');
        $wanted=['ListingId','ListPrice','TransactionType','PropertyType','PropertySubType','City','CityRegion','ContractStatus',
            'UnparsedAddress','StreetNumber','StreetName','StreetSuffix','StreetDirSuffix','UnitNumber','PostalCode',
            'BedroomsTotal','BedroomsAboveGrade','BedroomsBelowGrade','BathroomsTotalInteger','ParkingTotal',
            'LivingAreaRange','LotSizeArea','LotSizeUnits','PublicRemarks','ListOfficeName','CoListOfficeName',
            'ModificationTimestamp','OriginalEntryTimestamp','ListPriceUnit','InternetAddressDisplayYN','InternetEntireListingDisplayYN','DDFYN'];
        $select=array_values(array_unique(array_merge($required,array_intersect($wanted,$fields))));
        $photoSelect=array_values(array_intersect(['MediaKey','ResourceRecordKey','MediaURL','MediaType','Order','ImageSizeDescription'],$mediaFields));
        if (array_diff(['MediaKey','ResourceRecordKey','MediaURL'],$photoSelect)) throw new RuntimeException('media_fields_unavailable');
        $photoFilter=[];
        $photoFilter[]="ResourceName eq 'Property'";
        if(in_array('MediaType',$photoSelect,true)) $photoFilter[]="MediaType eq 'image/jpeg'";
        if(in_array('ImageSizeDescription',$photoSelect,true)) $photoFilter[]="ImageSizeDescription eq 'Large'";
        $all=[]; $last=''; $complete=false;
        for($batch=0;$batch<100;$batch++) {
            $filter="CityRegion eq 'Nobleton' and ContractStatus eq 'Available'";
            if($last!=='') $filter.=" and ListingKey gt '".str_replace("'","''",$last)."'";
            $data=idx_request('Property',['$filter'=>$filter,'$select'=>implode(',',$select),'$orderby'=>'ListingKey','$top'=>100]);
            $rows=$data['value'];
            foreach($rows as $row) if(idx_permitted($row)) $all[(string)$row['ListingKey']]=$row;
            if(count($rows)<100 && empty($data['@odata.nextLink'])) {$complete=true;break;}
            $next=(string)($rows[count($rows)-1]['ListingKey']??'');
            if(!$next || $next===$last) throw new RuntimeException('pagination_stalled');
            $last=$next;
        }
        if(!$complete) throw new RuntimeException('sync_limit');
        // Separate Media requests: this approved feed returns an empty body for $expand.
        // Refresh all photographs each time, including photo-only changes.
        foreach(array_chunk(array_keys($all),20) as $keys){
            $keyFilter='('.implode(' or ',array_map(static fn($key)=>"ResourceRecordKey eq '".str_replace("'","''",(string)$key)."'",$keys)).')';
            $lastMedia='';$mediaComplete=false;
            for($batch=0;$batch<100;$batch++){
                $filter=implode(' and ',$photoFilter).' and '.$keyFilter;
                if($lastMedia!=='')$filter.=" and MediaKey gt '".str_replace("'","''",$lastMedia)."'";
                $data=idx_request('Media',['$filter'=>$filter,'$select'=>implode(',',$photoSelect),'$orderby'=>'MediaKey','$top'=>1000]);
                foreach($data['value'] as $photo){$key=(string)($photo['ResourceRecordKey']??'');if(isset($all[$key]))$all[$key]['Media'][]=$photo;}
                if(count($data['value'])<1000 && empty($data['@odata.nextLink'])){$mediaComplete=true;break;}
                $next=(string)($data['value'][count($data['value'])-1]['MediaKey']??'');
                if(!$next||$next===$lastMedia)throw new RuntimeException('media_pagination_stalled');$lastMedia=$next;
            }
            if(!$mediaComplete)throw new RuntimeException('media_sync_limit');
        }
        $payload=['updatedAt'=>gmdate('c'),'listings'=>array_values(array_map('idx_public_row',$all))];
        $tmp=IDX_DIR.'/idx-cache.tmp';
        if(file_put_contents($tmp,json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_THROW_ON_ERROR),LOCK_EX)===false || !rename($tmp,IDX_DIR.'/idx-cache.json')) throw new RuntimeException('cache_write');
        file_put_contents(IDX_DIR.'/idx-health.json',json_encode(['ok'=>true,'checkedAt'=>gmdate('c')]));
    } finally {flock($lock,LOCK_UN);fclose($lock);}
}

function idx_cache(?int $now=null): array {
    $file=IDX_DIR.'/idx-cache.json';
    $data=json_decode((string)@file_get_contents($file),true);
    $updated=is_array($data)?strtotime($data['updatedAt']??''):false;
    if(!$updated || ($now??time())-$updated>IDX_MAX_AGE || !isset($data['listings'])) throw new RuntimeException('temporarily_unavailable');
    return $data;
}

function idx_search(array $rows,array $params): array {
    $deal=$params['deal']??'sale';
    if(!in_array($deal,['sale','lease','all'],true)) throw new InvalidArgumentException('invalid_filter');
    $number=static function($key,$max)use($params):float {
        $v=$params[$key]??'';
        if($v==='')return 0;
        if(!is_scalar($v)||!is_numeric($v)||$v<0||$v>$max)throw new InvalidArgumentException('invalid_filter');
        return (float)$v;
    };
    $min=$number('min',1000000000);$max=$number('max',1000000000);$beds=$number('beds',20);$baths=$number('baths',20);
    $type=$params['type']??'';if(!is_string($type)||strlen($type)>80)throw new InvalidArgumentException('invalid_filter');
    $id=$params['id']??'';if(!is_string($id)||!preg_match('/^[A-Za-z0-9_-]{0,80}$/D',$id))throw new InvalidArgumentException('invalid_filter');
    $sort=$params['sort']??'newest';if(!in_array($sort,['newest','price-asc','price-desc'],true))throw new InvalidArgumentException('invalid_filter');
    $result=array_values(array_filter($rows,static function($r)use($deal,$min,$max,$beds,$baths,$type,$id){
        if($id!=='')return ($r['ListingKey']??'')===$id;
        $transaction=strtolower((string)($r['TransactionType']??''));
        if($deal==='sale'&&!str_contains($transaction,'sale'))return false;
        if($deal==='lease'&&!str_contains($transaction,'lease')&&!str_contains($transaction,'rent'))return false;
        $price=(float)($r['ListPrice']??0);
        return (!$min||$price>=$min)&&(!$max||$price<=$max)&&(!$beds||(float)($r['BedroomsTotal']??$r['BedroomsAboveGrade']??0)>=$beds)
            &&(!$baths||(float)($r['BathroomsTotalInteger']??0)>=$baths)&&(!$type||($r['PropertySubType']??'')===$type);
    }));
    usort($result,static function($a,$b)use($sort){
        $cmp=$sort==='price-asc'?($a['ListPrice']??0)<=>($b['ListPrice']??0):($sort==='price-desc'?($b['ListPrice']??0)<=>($a['ListPrice']??0):strcmp($b['OriginalEntryTimestamp']??$b['ModificationTimestamp']??'',$a['OriginalEntryTimestamp']??$a['ModificationTimestamp']??''));
        return $cmp?:strcmp($a['ListingKey'],$b['ListingKey']);
    });
    $page=max(1,(int)$number('page',10000));$size=12;
    $types=array_values(array_unique(array_filter(array_column($rows,'PropertySubType'))));sort($types);
    return ['total'=>count($result),'page'=>$page,'pageSize'=>$size,'types'=>$types,'listings'=>array_slice($result,($page-1)*$size,$size)];
}
