<?php
/**
 * Contact + callback. PHP 7.4+; real mail() transport on the hosting server.
 * Recipient is fixed. A success means the mail server accepted the message.
 */
declare(strict_types=1);
require_once __DIR__ . '/form-validation.php';
date_default_timezone_set('Europe/Brussels');
const TO_EMAIL = 'digital-buro@skynet.be';
const FROM_EMAIL = 'site@digital-buro.be';
const SUBJECTS = ['reparation'=>'Réparation / devis','cartouches'=>'Cartouches & toners',
    'achat'=>'Achat de matériel','entreprise'=>'Entreprise / intervention',
    'sav'=>'Service après-vente','autre'=>'Autre demande','rappel'=>'Demande de rappel'];

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
$wantsJson = strpos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;
function escape(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }
function respond(bool $ok, string $message, int $code=200): void {
    global $wantsJson;
    if ($wantsJson) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok'=>$ok,'message'=>$message], JSON_UNESCAPED_UNICODE);
    } elseif ($ok) {
        header('Location: /merci/', true, 303);
    } else {
        http_response_code($code);
        header('Content-Type: text/html; charset=utf-8');
        echo '<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Votre demande — Digital-Buro</title><link rel="stylesheet" href="/assets/css/style.css"><main class="container section"><h1 class="h2">Votre demande n’a pas été envoyée</h1><p class="lead">'.escape($message).'</p><p><a class="btn btn--primary" href="/api/contact.php?form=1">Revenir au formulaire</a></p><p><a href="tel:+3225344702">02 534 47 02</a> · <a href="mailto:'.TO_EMAIL.'">'.TO_EMAIL.'</a></p></main></html>';
    }
    exit;
}
function field(string $name, int $limit): string {
    $value = $_POST[$name] ?? '';
    if (!is_string($value) || strlen($value) > $limit || strpos($value, "\0") !== false) {
        respond(false, 'Un champ dépasse la taille autorisée ou contient des caractères non valides.', 422);
    }
    return trim($value);
}
function start_form_session(): void {
    session_name('db_form');
    session_set_cookie_params(['lifetime'=>0,'path'=>'/api/','secure'=>!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off',
        'httponly'=>true,'samesite'=>'Lax']);
    if (!session_start(['use_strict_mode'=>true])) respond(false, 'Le formulaire est indisponible. Appelez le magasin.', 503);
}
function token(): string {
    if (empty($_SESSION['form_token']) || time()-($_SESSION['form_time'] ?? 0)>3600) {
        $_SESSION['form_token'] = bin2hex(random_bytes(32));
        $_SESSION['form_time'] = time();
    }
    return $_SESSION['form_token'];
}

$method = $_SERVER['REQUEST_METHOD'] ?? '';
if ($method === 'GET' && (isset($_GET['token']) || isset($_GET['form']))) {
    start_form_session();
    $token = token();
    session_write_close();
    if (isset($_GET['token'])) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok'=>true,'token'=>$token]);
        exit;
    }
    header('Content-Type: text/html; charset=utf-8');
    echo '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Contact — Digital-Buro</title><link rel="stylesheet" href="/assets/css/style.css"></head><body><main class="container section" style="max-width:680px"><a href="/contact/">← Contact et horaires</a><h1 class="h1">Contacter Digital-Buro</h1><p class="lead">Votre nom et votre téléphone sont obligatoires.</p><form class="form" method="post" action="/api/contact.php"><div class="field"><label for="nom">Nom</label><input class="field__input" id="nom" name="nom" autocomplete="name" minlength="2" maxlength="120" required></div><div class="field"><label for="telephone">Téléphone</label><input class="field__input" id="telephone" name="telephone" type="tel" autocomplete="tel" maxlength="40" required></div><div class="field"><label for="email">E-mail (facultatif)</label><input class="field__input" id="email" name="email" type="email" autocomplete="email" maxlength="180"></div><div class="field"><label for="message">Votre demande (facultatif)</label><textarea class="field__input" id="message" name="message" maxlength="5000"></textarea></div><input type="hidden" name="form_token" value="'.escape($token).'"><input type="hidden" name="sujet" value="autre"><div class="form__hp" aria-hidden="true"><label for="site_web">Ne pas remplir</label><input name="site_web" id="site_web" tabindex="-1" autocomplete="off"></div><p class="form__legal">Vos coordonnées servent à répondre à votre demande. <a href="/confidentialite/">Confidentialité</a>.</p><button class="btn btn--primary" type="submit">Envoyer la demande</button></form></main></body></html>';
    exit;
}
if ($method !== 'POST') { header('Location: /contact/', true, 303); exit; }
if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0)>24000) respond(false, 'Demande trop volumineuse.', 413);
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '' && parse_url($origin, PHP_URL_HOST) !== parse_url('http://'.($_SERVER['HTTP_HOST'] ?? ''), PHP_URL_HOST)) {
    respond(false, 'Rechargez le formulaire depuis notre site.', 403);
}
if (field('site_web',200) !== '') respond(false, 'Votre demande a été refusée. Contactez le magasin par téléphone.', 422);

start_form_session();
$postedToken=field('form_token',64);
if ($postedToken==='' || empty($_SESSION['form_token']) || !hash_equals($_SESSION['form_token'],$postedToken)
    || time()-($_SESSION['form_time'] ?? 0)>3600) {
    respond(false, 'La session du formulaire a expiré. Rechargez la page puis réessayez.', 403);
}
if (time()-($_SESSION['form_time'] ?? time())<2) {
    respond(false, 'Merci de patienter deux secondes avant de réessayer.', 429);
}
$nom=field('nom',480);
$email=field('email',180);
$telephone=normalized_contact_phone(field('telephone',40));
$sujetKey=field('sujet',30);
$appareil=field('appareil',160);
$message=field('message',20000);
if (!preg_match('//u',$message) || preg_match_all('/./us',$message)>5000) respond(false,'Votre message doit contenir au maximum 5 000 caractères.',422);
if (!valid_contact_name($nom)) respond(false, 'Indiquez votre nom sans chiffres ni caractères spéciaux (accents, espaces, apostrophes et traits d’union acceptés).',422);
if ($telephone===null) respond(false, 'Indiquez un téléphone valide : numéro belge ou numéro international avec + et l’indicatif du pays.',422);
if ($email!=='' && (!filter_var($email,FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/',$email))) respond(false,'Vérifiez votre adresse e-mail.',422);
if (preg_match('/[\r\n]/',$appareil) || !isset(SUBJECTS[$sujetKey])) respond(false,'Vérifiez le sujet de votre demande.',422);
if (preg_match_all('~https?://~i',$message)>3) respond(false,'Votre message contient trop de liens. Décrivez votre demande sans ces liens.',422);

// Atomic limits: at most 5 accepted submissions/hour, 30 seconds between attempts.
// File contains hashed-IP identifier + timestamps only, no message or contact data.
$ip=(string)($_SERVER['REMOTE_ADDR'] ?? '');
$lockPath=rtrim(sys_get_temp_dir(),'/\\').DIRECTORY_SEPARATOR.'dbcontact_v2_'.hash('sha256',$ip);
$handle=@fopen($lockPath,'c+');
if (!$handle || !flock($handle,LOCK_EX)) respond(false,'Le formulaire est temporairement indisponible. Appelez le magasin.',503);
$state=json_decode(stream_get_contents($handle),true) ?: [];
$now=time();
$recent=array_values(array_filter($state['sent'] ?? [],function($t)use($now){return is_int($t) && $now-$t<3600;}));
if (count($recent)>=5 || $now-(int)($state['attempt'] ?? 0)<30) {
    header('Retry-After: 30');
    respond(false,'Trop de demandes rapprochées. Patientez avant de réessayer ou appelez le magasin.',429);
}
$state=['attempt'=>$now,'sent'=>$recent];
rewind($handle);ftruncate($handle,0);fwrite($handle,json_encode($state));fflush($handle);

$sujet=SUBJECTS[$sujetKey];
$body="Demande depuis le site Digital-Buro\n\nNom : {$nom}\nTéléphone : {$telephone}\nE-mail : {$email}\nSujet : {$sujet}\nAppareil : {$appareil}\n\n{$message}\n\nEnvoyé le ".date('d/m/Y à H:i')."\n";
$subject='=?UTF-8?B?'.base64_encode("[Site] {$sujet} — {$nom}").'?=';
$from=getenv('DB_MAIL_FROM') ?: FROM_EMAIL;
if (!filter_var($from,FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/',$from)) respond(false,'Configuration d’envoi indisponible. Appelez le magasin.',503);
$headers=['From'=>'Digital-Buro <'.$from.'>','MIME-Version'=>'1.0','Content-Type'=>'text/plain; charset=UTF-8','Content-Transfer-Encoding'=>'8bit'];
if ($email!=='') $headers['Reply-To']=$email;
try { $sent=@mail(TO_EMAIL,$subject,$body,$headers); } catch (Throwable $e) { $sent=false; }
if (!$sent) {
    error_log('Digital-Buro contact: mail transport refused a message.');
    respond(false,'L’envoi a échoué. Appelez le 02 534 47 02 ou écrivez à '.TO_EMAIL.'.',503);
}
$state['sent'][]=$now;
rewind($handle);ftruncate($handle,0);fwrite($handle,json_encode($state));
flock($handle,LOCK_UN);fclose($handle);
unset($_SESSION['form_token'],$_SESSION['form_time']);
session_write_close();
respond(true,'Merci ! Votre demande a été transmise au magasin.');

