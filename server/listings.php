<?php
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header('X-Robots-Tag: noindex, nofollow');
if(($_SERVER['REQUEST_METHOD']??'')!=='GET'){http_response_code(405);header('Allow: GET');echo '{"error":"method_not_allowed"}';exit;}
// This feed is approved for Nobleton.ca only. Do not enable cross-origin previews.
$origin=$_SERVER['HTTP_ORIGIN']??'';
if($origin!==''&&$origin!=='https://nobleton.ca'){http_response_code(403);echo '{"error":"origin_not_allowed"}';exit;}
try{
    require '/home/nvfglyl5/nobleton-private/idx/lib.php';
    $data=idx_cache();
    $result=idx_search($data['listings'],$_GET);
    $result['updatedAt']=$data['updatedAt'];
    echo json_encode($result,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_THROW_ON_ERROR);
}catch(InvalidArgumentException $e){http_response_code(400);echo '{"error":"invalid_filter"}';}
catch(Throwable $e){http_response_code(503);header('Retry-After: 900');echo '{"error":"temporarily_unavailable"}';}
