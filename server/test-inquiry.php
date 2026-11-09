<?php
/** CLI-only delivery stub: never sends messages. */
namespace Nobleton;
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
$case = $argv[1] ?? 'realtor';
$expected = ['realtor'=>200,'valuation'=>200,'mortgage'=>200,'both'=>200,'missing_consent'=>422,'bad_email'=>422,'bad_address'=>422,'bad_topic'=>422,'bad_origin'=>403,'honeypot'=>400,'delivery_failure'=>503,'method'=>405,'options'=>204][$case] ?? 500;
$calls=0;
function mail($to,$subject,$body,$headers): bool {
    global $case,$calls;
    $calls++;
    $recipient = $case==='both'?'realtor@nobleton.ca, mortgage@nobleton.ca':($case==='mortgage'?'mortgage@nobleton.ca':'realtor@nobleton.ca');
    if($to!==$recipient || $headers['Reply-To']!=='validation@example.invalid') throw new \RuntimeException('Routing/header failure');
    if(!str_contains($body,'Source page: /ask-realtor/')) throw new \RuntimeException('Source attribution failure');
    return $case!=='delivery_failure';
}
$_SERVER=['REQUEST_METHOD'=>'POST','HTTP_ACCEPT'=>'application/json','HTTP_ORIGIN'=>'https://nobleton.ca','REMOTE_ADDR'=>'cli-test-'.getmypid()];
$_POST=['kind'=>'realtor','name'=>'Validation fixture','email'=>'validation@example.invalid','message'=>'Automated validation; delivery is stubbed.','consent'=>'yes','source_page'=>'/ask-realtor/','preferred_language'=>'fr-CA','topic'=>'consultation'];
if($case==='valuation'){$_POST['kind']='valuation';$_POST['address']='Test fixture address';unset($_POST['message']);}
if($case==='mortgage')$_POST['kind']='mortgage';
if($case==='both')$_POST['both']='yes';
if($case==='missing_consent')unset($_POST['consent']);
if($case==='bad_email')$_POST['email']="user@example.invalid\r\nBcc: other@example.invalid";
if($case==='bad_address')$_POST['kind']='valuation';
if($case==='bad_topic'){$_POST['kind']='mortgage';$_POST['topic']='unsupported';}
if($case==='bad_origin')$_SERVER['HTTP_ORIGIN']='https://example.invalid';
if($case==='honeypot')$_POST['company_url']='spam';
if($case==='method')$_SERVER['REQUEST_METHOD']='GET';
if($case==='options')$_SERVER['REQUEST_METHOD']='OPTIONS';
register_shutdown_function(function()use($expected,$case){global $calls;$wantCalls=in_array($case,['realtor','valuation','mortgage','both','delivery_failure'],true)?1:0;if(http_response_code()!==$expected||$calls!==$wantCalls){fwrite(STDERR,"FAIL $case\n");exit(1);}echo " PASS $case\n";});
require __DIR__.'/inquiry.php';
