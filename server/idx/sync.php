<?php
declare(strict_types=1);
if(PHP_SAPI!=='cli'){http_response_code(404);exit;}
require __DIR__.'/lib.php';
try {idx_sync();echo "IDX sync: OK\n";}
catch(Throwable $e){
    // Deliberately no token, upstream response or listing data in diagnostics.
    $code=$e instanceof RuntimeException?$e->getMessage():'sync_failed';
    if(!preg_match('/^[a-z0-9_]+$/D',$code))$code='sync_failed';
    file_put_contents(IDX_DIR.'/idx-health.json',json_encode(['ok'=>false,'checkedAt'=>gmdate('c'),'code'=>$code]));
    fwrite(STDERR,"IDX sync: $code\n");exit(1);
}
