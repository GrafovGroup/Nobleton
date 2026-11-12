<?php
declare(strict_types=1);
require __DIR__.'/../server/idx/lib.php';
$checks=0;
function check(bool $condition,string $name):void{global $checks;$checks++;if(!$condition)throw new RuntimeException($name);}
$sample=['ListingKey'=>'TEST1','CityRegion'=>'Nobleton','ContractStatus'=>'Available','ListOfficeName'=>'TEST BROKERAGE','TransactionType'=>'For Sale','ListPrice'=>1200000,'BedroomsTotal'=>4,'BathroomsTotalInteger'=>3,'PropertySubType'=>'Detached','PublicRemarks'=>'<script>example</script>'];
check(idx_permitted($sample),'available eligible');
foreach(['DDFYN','InternetEntireListingDisplayYN']as $field)check(!idx_permitted(array_replace($sample,[$field=>false])),'opt out');
check(!idx_permitted(array_replace($sample,['ContractStatus'=>'Sold'])),'sold excluded');
check(!idx_permitted(array_replace($sample,['CityRegion'=>'King City'])),'geography');
$out=idx_public_row($sample+['PrivateRemarks'=>'secret','InternetAddressDisplayYN'=>false,'StreetName'=>'Hidden','Media'=>[['MediaURL'=>'javascript:alert(1)'],['MediaURL'=>'https://example.com/photo.jpg','MediaType'=>'image/jpeg']]]);
check(!isset($out['PrivateRemarks'])&&!isset($out['StreetName']),'private fields and address');
check(count($out['photos'])===1,'photo URL');
check($out['PublicRemarks']===$sample['PublicRemarks'],'unchanged remarks');
check(idx_search([$sample],['min'=>'1300000'])['total']===0,'price filter');
check(idx_search([$sample],['deal'=>'lease'])['total']===0,'lease filter');
check(idx_search([$sample],['beds'=>'4','baths'=>'3'])['total']===1,'bed bath filter');
$many=[];for($i=0;$i<120;$i++)$many[]=array_replace($sample,['ListingKey'=>'TEST'.$i]);
check(count(idx_search($many,[])['listings'])===12,'result bound');
check(count(idx_search($many,['page'=>'10'])['listings'])===12,'pagination');
foreach([['min'=>['bad']],['beds'=>'oops'],['sort'=>'sql'],['id'=>"foo'"],['type'=>['bad']]]as $bad){$thrown=false;try{idx_search([$sample],$bad);}catch(InvalidArgumentException $e){$thrown=true;}check($thrown,'validation');}
check(idx_fields('<edmx:Edmx xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx"><edmx:DataServices><Schema xmlns="http://docs.oasis-open.org/odata/ns/edm"><EntityType Name="Property"><Property Name="ListingKey" Type="Edm.String"/></EntityType></Schema></edmx:DataServices></edmx:Edmx>','Property')===['ListingKey'],'metadata');
echo "IDX unit checks: $checks passed\n";
