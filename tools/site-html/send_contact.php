<?php
/**
 * Digital-Buro contact/callback, adapted from the supplied reservation mailer.
 * PHP 7.4+; mail() sends HTML to the fixed shop address.
 * All limits apply on the server, including requests made without JavaScript.
 */
declare(strict_types=1);
require_once __DIR__ . '/form-validation.php';
date_default_timezone_set('Europe/Brussels');

const TO_EMAIL = 'digital-buro@skynet.be';
const FROM_EMAIL = 'site@digital-buro.be';
const MIN_FILL_SECONDS = 2;
const TOKEN_TTL_SECONDS = 3600;
const IP_COOLDOWN_SECONDS = 30;
const IP_MAX_PER_HOUR = 5;
const PHONE_MAX_PER_HOUR = 3;
const GLOBAL_MAX_PER_HOUR = 30;
const GLOBAL_MAX_PER_DAY = 100;
const DUPLICATE_WINDOW_SECONDS = 600;
const SUBJECTS = [
    'reparation'=>'Réparation / devis', 'cartouches'=>'Cartouches & toners',
    'achat'=>'Achat de matériel', 'entreprise'=>'Entreprise / intervention',
    'sav'=>'Service après-vente', 'autre'=>'Autre demande', 'rappel'=>'Demande de rappel',
];

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');
$wantsJson = strpos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;
$rateHandle = null;

function escape(string $value): string {
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function encoded_subject(string $value): string {
    $words = [];
    $buffer = '';
    foreach (preg_split('//u', $value, -1, PREG_SPLIT_NO_EMPTY) as $character) {
        if (strlen($buffer) + strlen($character) > 42) {
            $words[] = '=?UTF-8?B?'.base64_encode($buffer).'?=';
            $buffer = '';
        }
        $buffer .= $character;
    }
    if ($buffer !== '') $words[] = '=?UTF-8?B?'.base64_encode($buffer).'?=';
    return implode(' ', $words);
}

function respond(bool $ok, string $message, int $code = 200, string $error = ''): void {
    global $wantsJson, $rateHandle;
    if (is_resource($rateHandle)) {
        flock($rateHandle, LOCK_UN);
        fclose($rateHandle);
        $rateHandle = null;
    }
    if ($wantsJson) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok'=>$ok, 'message'=>$message, 'error'=>$error], JSON_UNESCAPED_UNICODE);
    } elseif ($ok) {
        header('Location: merci.html', true, 303);
    } else {
        http_response_code($code);
        header('Content-Type: text/html; charset=utf-8');
        echo '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Votre demande — Digital-Buro</title><link rel="stylesheet" href="assets/css/style.css"></head><body><main class="container section"><h1 class="h2">Votre demande n’a pas été envoyée</h1><p class="lead">'.escape($message).'</p><p><a class="btn btn--primary" href="send_contact.php?form=1">Revenir au formulaire</a></p><p><a href="tel:+3225344702">02 534 47 02</a> · <a href="mailto:'.TO_EMAIL.'">'.TO_EMAIL.'</a></p></main></body></html>';
    }
    exit;
}

function field(string $name, int $byteLimit): string {
    $value = $_POST[$name] ?? '';
    if (!is_string($value) || strlen($value) > $byteLimit || strpos($value, "\0") !== false || preg_match('//u', $value) !== 1) {
        respond(false, 'Un champ contient des caractères non valides ou dépasse la taille autorisée.', 422, 'validation');
    }
    return trim($value);
}

function start_form_session(): void {
    $directory = str_replace('\\', '/', dirname($_SERVER['SCRIPT_NAME'] ?? '/send_contact.php'));
    $path = rtrim($directory, '/') . '/';
    session_name('db_html_form');
    session_set_cookie_params([
        'lifetime'=>0, 'path'=>$path,
        'secure'=>!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off',
        'httponly'=>true, 'samesite'=>'Lax',
    ]);
    if (!session_start(['use_strict_mode'=>true, 'use_only_cookies'=>true])) {
        respond(false, 'Le formulaire est indisponible. Appelez le magasin.', 503, 'unavailable');
    }
}

function form_token(): string {
    if (empty($_SESSION['form_token']) || time() - ($_SESSION['form_time'] ?? 0) > TOKEN_TTL_SECONDS) {
        $_SESSION['form_token'] = bin2hex(random_bytes(32));
        $_SESSION['form_time'] = time();
    }
    return $_SESSION['form_token'];
}

function reject_limit(int $seconds): void {
    header('Retry-After: '.max(1, $seconds));
    respond(false, 'Trop de demandes rapprochées. Patientez avant de réessayer ou appelez le 02 534 47 02.', 429, 'rate_limit');
}

function persist_limits(array $state): void {
    global $rateHandle;
    $json = json_encode($state);
    if (!is_string($json) || !rewind($rateHandle) || !ftruncate($rateHandle, 0)
        || fwrite($rateHandle, $json) !== strlen($json) || !fflush($rateHandle)) {
        respond(false, 'Le formulaire est temporairement indisponible. Appelez le magasin.', 503, 'unavailable');
    }
}

$method = $_SERVER['REQUEST_METHOD'] ?? '';
if ($method === 'GET' && (isset($_GET['token']) || isset($_GET['form']))) {
    start_form_session();
    $token = form_token();
    $waitMs = max(0, MIN_FILL_SECONDS - (time() - $_SESSION['form_time'])) * 1000;
    session_write_close();
    if (isset($_GET['token'])) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok'=>true, 'token'=>$token, 'wait_ms'=>$waitMs ? $waitMs + 100 : 0]);
        exit;
    }
    header('Content-Type: text/html; charset=utf-8');
    echo '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Contact — Digital-Buro</title><link rel="stylesheet" href="assets/css/style.css"></head><body><main class="container section" style="max-width:680px"><a href="contact.html">← Contact et horaires</a><h1 class="h1">Contacter Digital-Buro</h1><p class="lead">Votre nom et votre téléphone sont obligatoires.</p><form class="form" method="post" action="send_contact.php"><div class="field"><label for="nom">Nom</label><input class="field__input" id="nom" name="nom" autocomplete="name" minlength="2" maxlength="120" required></div><div class="field"><label for="telephone">Téléphone</label><input class="field__input" id="telephone" name="telephone" type="tel" autocomplete="tel" maxlength="40" required></div><div class="field"><label for="email">E-mail (facultatif)</label><input class="field__input" id="email" name="email" type="email" autocomplete="email" maxlength="180"></div><div class="field"><label for="appareil">Appareil (facultatif)</label><input class="field__input" id="appareil" name="appareil" maxlength="160"></div><div class="field"><label for="message">Votre demande (facultatif)</label><textarea class="field__input" id="message" name="message" maxlength="5000"></textarea></div><input type="hidden" name="form_token" value="'.escape($token).'"><input type="hidden" name="sujet" value="autre"><div class="form__hp" aria-hidden="true"><label for="site_web">Ne pas remplir</label><input name="site_web" id="site_web" tabindex="-1" autocomplete="off"></div><p class="form__legal">Vos coordonnées servent à répondre à votre demande. <a href="confidentialite.html">Confidentialité</a>.</p><button class="btn btn--primary" type="submit">Envoyer la demande</button></form></main></body></html>';
    exit;
}
if ($method === 'GET') {
    header('Location: contact.html', true, 303);
    exit;
}
if ($method !== 'POST') {
    header('Allow: GET, POST');
    respond(false, 'Méthode de requête non autorisée.', 405, 'method');
}
if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 24000 || !empty($_FILES)) {
    respond(false, 'Demande trop volumineuse ou pièce jointe non autorisée.', 413, 'validation');
}
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '') {
    $parsed = parse_url($origin);
    $host = parse_url('http://'.($_SERVER['HTTP_HOST'] ?? ''));
    $port = $parsed['port'] ?? (($parsed['scheme'] ?? '') === 'https' ? 443 : 80);
    $expectedPort = $host['port'] ?? (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' ? 443 : 80);
    if (!is_array($parsed) || !in_array($parsed['scheme'] ?? '', ['http', 'https'], true)
        || strtolower($parsed['host'] ?? '') !== strtolower($host['host'] ?? '') || $port !== $expectedPort) {
        respond(false, 'Rechargez le formulaire depuis notre site.', 403, 'session');
    }
}
if (field('site_web', 200) !== '') {
    respond(false, 'Votre demande a été refusée. Contactez le magasin par téléphone.', 422, 'spam');
}
start_form_session();
$postedToken = field('form_token', 64);
if ($postedToken === '' || empty($_SESSION['form_token']) || !hash_equals($_SESSION['form_token'], $postedToken)
    || time() - ($_SESSION['form_time'] ?? 0) > TOKEN_TTL_SECONDS) {
    respond(false, 'La session du formulaire a expiré. Rechargez la page puis réessayez.', 403, 'session');
}
if (time() - ($_SESSION['form_time'] ?? time()) < MIN_FILL_SECONDS) {
    reject_limit(MIN_FILL_SECONDS);
}
$nom = field('nom', 480);
$email = field('email', 180);
$telephone = normalized_contact_phone(field('telephone', 40));
$sujetKey = field('sujet', 30);
$appareil = field('appareil', 640);
$message = field('message', 20000);
if (!valid_contact_name($nom) || $telephone === null) {
    respond(false, 'Indiquez un nom sans chiffres et un numéro de téléphone valide.', 422, 'validation');
}
if ($email !== '' && (!filter_var($email, FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/', $email))) {
    respond(false, 'Vérifiez votre adresse e-mail.', 422, 'validation');
}
if (!isset(SUBJECTS[$sujetKey]) || preg_match('/[\r\n]/', $appareil)
    || preg_match_all('/./us', $appareil) > 160 || preg_match_all('/./us', $message) > 5000) {
    respond(false, 'Vérifiez le sujet, l’appareil et la longueur de votre message.', 422, 'validation');
}
if (preg_match_all('~(?:https?://|www\.)~i', $message) > 3) {
    respond(false, 'Votre message contient trop de liens. Décrivez votre demande sans ces liens.', 422, 'spam');
}
$from = getenv('DB_MAIL_FROM') ?: FROM_EMAIL;
if (!filter_var($from, FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/', $from)) {
    respond(false, 'Configuration d’envoi indisponible. Appelez le magasin.', 503, 'unavailable');
}

// One shared, locked file caps the mailbox even when robots change IP/session.
// It contains salted fingerprints and timestamps, never the message or contacts.
$storePath = rtrim(sys_get_temp_dir(), '/\\').DIRECTORY_SEPARATOR
    .'db_html_contact_v1_'.substr(hash('sha256', __DIR__), 0, 16).'.json';
$rateHandle = @fopen($storePath, 'c+');
if (!$rateHandle) respond(false, 'Le formulaire est temporairement indisponible. Appelez le magasin.', 503, 'unavailable');
@chmod($storePath, 0600);
if (!flock($rateHandle, LOCK_EX | LOCK_NB)) reject_limit(5);
$raw = stream_get_contents($rateHandle);
$state = $raw === '' ? ['secret'=>bin2hex(random_bytes(32)), 'attempts'=>[]] : json_decode($raw, true);
if (!is_array($state) || !is_string($state['secret'] ?? null) || !is_array($state['attempts'] ?? null)) {
    respond(false, 'La protection du formulaire est indisponible. Appelez le magasin.', 503, 'unavailable');
}
$now = time();
$state['attempts'] = array_values(array_filter($state['attempts'], function ($entry) use ($now) {
    return is_array($entry) && is_int($entry['t'] ?? null) && $now - $entry['t'] < 86400;
}));
$ipHash = hash_hmac('sha256', (string)($_SERVER['REMOTE_ADDR'] ?? ''), $state['secret']);
$phoneHash = hash_hmac('sha256', $telephone, $state['secret']);
$fingerprint = hash_hmac('sha256', json_encode([$nom, $telephone, $email, $sujetKey, $appareil, $message]), $state['secret']);
$hourly = $ipHourly = $phoneHourly = 0;
$lastIp = 0;
foreach ($state['attempts'] as $entry) {
    if ($now - $entry['t'] < 3600) {
        $hourly++;
        if (($entry['ip'] ?? '') === $ipHash) $ipHourly++;
        if (($entry['phone'] ?? '') === $phoneHash) $phoneHourly++;
    }
    if (($entry['ip'] ?? '') === $ipHash) $lastIp = max($lastIp, $entry['t']);
    if (!empty($entry['sent']) && ($entry['fingerprint'] ?? '') === $fingerprint
        && $now - $entry['t'] < DUPLICATE_WINDOW_SECONDS) {
        respond(false, 'Cette demande a déjà été envoyée. Le magasin vous répondra pendant ses heures d’ouverture.', 409, 'duplicate');
    }
}
if (count($state['attempts']) >= GLOBAL_MAX_PER_DAY || $hourly >= GLOBAL_MAX_PER_HOUR
    || $ipHourly >= IP_MAX_PER_HOUR || $phoneHourly >= PHONE_MAX_PER_HOUR) {
    reject_limit(3600);
}
if ($now - $lastIp < IP_COOLDOWN_SECONDS) reject_limit(IP_COOLDOWN_SECONDS - ($now - $lastIp));
$state['attempts'][] = ['t'=>$now, 'ip'=>$ipHash, 'phone'=>$phoneHash, 'fingerprint'=>$fingerprint, 'sent'=>false];
persist_limits($state);
unset($_SESSION['form_token'], $_SESSION['form_time']);
session_write_close();

$sujet = SUBJECTS[$sujetKey];
$title = $sujetKey === 'rappel' ? 'Nouvelle demande de rappel' : 'Nouvelle demande depuis le site';
$rows = ['Nom'=>escape($nom), 'Téléphone'=>escape($telephone),
    'E-mail'=>$email === '' ? 'Non renseigné' : escape($email), 'Sujet'=>escape($sujet),
    'Appareil / besoin'=>$appareil === '' ? 'Non renseigné' : escape($appareil)];
$table = '';
foreach ($rows as $label => $value) {
    $table .= '<tr><th style="text-align:left;padding:12px;border-bottom:1px solid #e1e4ec;color:#646b78">'.$label.'</th><td style="padding:12px;border-bottom:1px solid #e1e4ec;overflow-wrap:anywhere;word-break:break-word">'.$value.'</td></tr>';
}
$html = '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Demande — Digital-Buro</title></head><body style="margin:0;padding:24px;background:#f3f4f7;font-family:Arial,sans-serif;color:#14214a"><div style="max-width:600px;margin:auto;background:#fff;padding:24px;border-radius:12px"><div style="padding:20px;background:#14214a;color:#fff;border-radius:8px"><strong style="font-size:24px">DIGITAL-BURO</strong><h1 style="font-size:20px;margin:12px 0 0">'.escape($title).'</h1></div><p>Une personne vous a contacté via le site Digital-Buro.</p><table style="width:100%;border-collapse:collapse">'.$table.'</table><h2 style="font-size:18px">Message</h2><div style="padding:16px;background:#fff3ec;border-left:4px solid #f46623;overflow-wrap:anywhere">'.($message === '' ? 'Aucun message particulier.' : nl2br(escape($message))).'</div><p style="font-size:12px;color:#646b78;margin-top:24px">Envoyé le '.date('d/m/Y à H:i').' depuis le formulaire de digital-buro.be.</p></div></body></html>';
$subject = encoded_subject('[Site] '.$sujet.' — '.$nom);
$headers = ['From'=>'Digital-Buro <'.$from.'>', 'MIME-Version'=>'1.0',
    'Content-Type'=>'text/html; charset=UTF-8', 'Content-Transfer-Encoding'=>'quoted-printable'];
if ($email !== '') $headers['Reply-To'] = $email;
try { $sent = @mail(TO_EMAIL, $subject, quoted_printable_encode($html), $headers); }
catch (Throwable $error) { $sent = false; }
if (!$sent) {
    error_log('Digital-Buro HTML contact: mail transport refused a message.');
    respond(false, 'L’envoi a échoué. Appelez le 02 534 47 02 ou écrivez à '.TO_EMAIL.'.', 503, 'send_failed');
}
$state['attempts'][count($state['attempts']) - 1]['sent'] = true;
persist_limits($state);
respond(true, 'Merci ! Votre demande a été transmise au magasin.');
