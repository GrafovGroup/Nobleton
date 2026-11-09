<?php
/** WHC-only handler. Deploy to /api/inquiry.php; never serve as a static asset. */
declare(strict_types=1);
namespace Nobleton;
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
$allowedOrigins = ['https://nobleton.ca', 'https://www.nobleton.ca', 'https://nobleton.dimagrafov.chatgpt.site'];
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $allowedOrigins, true)) {
    header('Access-Control-Allow-Origin: ' . $origin);
    header('Vary: Origin');
    header('Access-Control-Allow-Methods: POST, OPTIONS');
    header('Access-Control-Allow-Headers: Accept, Content-Type');
}
function scalar(string $key): string { return isset($_POST[$key]) && is_string($_POST[$key]) ? trim($_POST[$key]) : ''; }
function respond(int $status, string $error = ''): never {
    http_response_code($status);
    $ok = $status === 200;
    if (str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json')) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'error' => $error]);
    } elseif ($ok) {
        header('Location: https://nobleton.ca/' . (scalar('preferred_language') === 'fr-CA' ? 'fr/' : '') . 'thank-you/', true, 303);
    } else {
        header('Content-Type: text/html; charset=utf-8');
        $fr = scalar('preferred_language') === 'fr-CA';
        echo '<!doctype html><html lang="'.($fr?'fr-CA':'en-CA').'"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nobleton.ca</title><main style="max-width:650px;margin:10vh auto;padding:25px;font:18px/1.6 system-ui"><h1>'.($fr?'La demande n’a pas pu être envoyée.':'Your request could not be sent.').'</h1><p>'.($fr?'Vérifiez les champs et votre consentement, puis réessayez. Vous pouvez aussi contacter directement le professionnel.':'Check the fields and consent, then try again. You can also contact the professional directly.').'</p><a href="https://nobleton.ca/'.($fr?'fr/':'').'contact/">'.($fr?'Options de contact':'Contact options').'</a></main></html>';
    }
    exit;
}
if ($origin !== '' && !in_array($origin, $allowedOrigins, true)) respond(403, 'origin');
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') { http_response_code(204); exit; }
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { header('Allow: POST'); respond(405, 'method'); }
if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 16384) respond(413, 'size');
if (scalar('company_url') !== '') respond(400, 'invalid');
$kind = scalar('kind');
$destinations = ['realtor' => 'realtor@nobleton.ca', 'valuation' => 'realtor@nobleton.ca', 'mortgage' => 'mortgage@nobleton.ca'];
if (!isset($destinations[$kind]) || scalar('consent') !== 'yes') respond(422, 'validation');
$name = scalar('name'); $email = scalar('email'); $phone = scalar('phone'); $address = scalar('address'); $message = scalar('message');
if ($name === '' || strlen($name) > 300 || strlen($email) > 180 || !filter_var($email, FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n\x00]/', $email.$name.$phone) || strlen($phone) > 80 || strlen($address) > 750 || strlen($message) > 7500 || ($kind === 'valuation' && $address === '') || ($kind !== 'valuation' && $message === '')) respond(422, 'validation');
$topic = scalar('topic');
if ($kind === 'mortgage' && !in_array($topic, ['consultation','question','purchase','renewal','refinance','investment'], true)) respond(422, 'validation');
// Only hashes and counters are stored. No inquiry contents are saved here.
$rateDir = dirname(__DIR__, 2) . '/.nobleton-inquiry-rate';
if (!is_dir($rateDir) && !@mkdir($rateDir, 0700, true) && !is_dir($rateDir)) respond(503, 'unavailable');
$client = hash('sha256', (__FILE__) . ($_SERVER['REMOTE_ADDR'] ?? 'unknown'));
$rateFile = $rateDir . '/' . $client . '.json';
$handle = @fopen($rateFile, 'c+');
if (!$handle || !flock($handle, LOCK_EX)) respond(503, 'unavailable');
$now = time(); $record = json_decode(stream_get_contents($handle), true);
if (!is_array($record) || $now - ($record['start'] ?? 0) >= 3600) $record = ['start' => $now, 'count' => 0];
if ($record['count'] >= 4) { flock($handle, LOCK_UN); fclose($handle); respond(429, 'rate_limit'); }
$record['count']++; rewind($handle); ftruncate($handle, 0); fwrite($handle, json_encode($record)); fflush($handle); flock($handle, LOCK_UN); fclose($handle); @chmod($rateFile, 0600);
// Bound retention of expired counters without logging IP addresses.
foreach (glob($rateDir.'/*.json') ?: [] as $old) { if (@filemtime($old) < $now - 86400) @unlink($old); }
$source = scalar('source_page');
if (!preg_match('~^/(?:fr/)?(?:ask-realtor|home-evaluation|mortgage-consultation)/$~', $source)) $source = 'Not supplied';
$language = scalar('preferred_language') === 'fr-CA' ? 'fr-CA' : 'en-CA';
$both = scalar('both') === 'yes';
$to = $both ? 'realtor@nobleton.ca, mortgage@nobleton.ca' : $destinations[$kind];
$body = "Nobleton.ca inquiry\n\nType: $kind\nTopic: $topic\nName: $name\nEmail: $email\nPhone: $phone\nProperty address: $address\nLanguage: $language\nSource page: $source\n\nMessage:\n$message\n\nConsent: visitor agreed to contact about this inquiry.\nOptional contact by both professionals: ".($both?'Yes':'No')."\n";
$headers = ['From' => 'Nobleton.ca <info@nobleton.ca>', 'Reply-To' => $email, 'MIME-Version' => '1.0', 'Content-Type' => 'text/plain; charset=UTF-8'];
if (!mail($to, 'Nobleton.ca: ' . $kind . ' inquiry', $body, $headers)) respond(503, 'delivery');
respond(200);
