<?php
/**
 * Digital-Buro — traitement du formulaire de contact (/contact/).
 *
 * - Répond en JSON quand le formulaire est envoyé en JavaScript (fetch),
 *   sinon redirige vers /merci/ (ou vers le formulaire en cas d'erreur).
 * - Protections anti-spam : champ piège, délai minimal, limite par IP, filtre de liens.
 * - Aucune donnée n'est stockée sur le serveur : la demande est envoyée par e-mail.
 *
 * Compatible PHP 7.2+ (hébergement mutualisé OVH).
 */
declare(strict_types=1);
date_default_timezone_set('Europe/Brussels');

/* ------------------------------------------------------------------ Réglages */
const TO_EMAIL   = 'digital-buro@skynet.be';   // destinataire des demandes
const FROM_EMAIL = 'site@digital-buro.be';     // expéditeur : une adresse du domaine du site (délivrabilité / SPF)
const SITE_NAME  = 'Digital-Buro';
const THANKS_URL = '/merci/';
const FORM_URL   = '/contact/';

const SUBJECTS = [
    'reparation' => 'Réparation / devis',
    'cartouches' => 'Cartouches & toners',
    'achat'      => 'Achat de matériel',
    'entreprise' => 'Entreprise / intervention sur site',
    'sav'        => 'Service après-vente / réclamation',
    'autre'      => 'Autre demande',
    'rappel'     => 'Demande de rappel',
];

header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');

$wantsJson = isset($_SERVER['HTTP_ACCEPT']) && strpos((string) $_SERVER['HTTP_ACCEPT'], 'application/json') !== false;

function respond(bool $ok, string $message = '', int $code = 200): void
{
    global $wantsJson;
    if ($wantsJson) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $message], JSON_UNESCAPED_UNICODE);
    } else {
        header('Location: ' . ($ok ? THANKS_URL : FORM_URL . '?erreur=1#formulaire'), true, 303);
    }
    exit;
}

function field(string $key, int $max): string
{
    $v = isset($_POST[$key]) && is_string($_POST[$key]) ? $_POST[$key] : '';
    $v = trim(str_replace("\0", '', $v));
    return function_exists('mb_substr') ? mb_substr($v, 0, $max, 'UTF-8') : substr($v, 0, $max);
}

function oneLine(string $v): string
{
    return trim((string) preg_replace('/[\r\n\t]+/', ' ', $v));
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: ' . FORM_URL, true, 303);
    exit;
}

// Anti-spam 1 : champ piège, invisible pour les visiteurs
if (field('site_web', 200) !== '') {
    respond(true, 'OK');
}

// Anti-spam 2 : envoi trop rapide après l'affichage de la page (robots)
$ts = (int) field('ts', 20);
if ($ts > 0 && (microtime(true) * 1000 - $ts) < 2500) {
    respond(false, 'Merci de patienter quelques secondes avant l’envoi.', 429);
}

// Anti-spam 3 : un envoi toutes les 30 secondes maximum par adresse IP
$ip = (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
$lock = rtrim(sys_get_temp_dir(), '/\\') . DIRECTORY_SEPARATOR . 'dbcontact_' . md5($ip);
if (is_file($lock) && (time() - (int) filemtime($lock)) < 30) {
    respond(false, 'Merci de patienter quelques secondes avant un nouvel envoi.', 429);
}

$nom       = oneLine(field('nom', 120));
$email     = oneLine(field('email', 180));
$telephone = oneLine(field('telephone', 40));
$sujetKey  = oneLine(field('sujet', 30));
$appareil  = oneLine(field('appareil', 160));
$message   = field('message', 5000);
$sujet     = SUBJECTS[$sujetKey] ?? SUBJECTS['autre'];

if ($nom === '' || ($telephone === '' && $email === '')) {
    respond(false, 'Indiquez votre nom et un téléphone ou une adresse e-mail.', 422);
}
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'Merci de vérifier votre adresse e-mail.', 422);
}
if ($telephone !== '' && (!preg_match('/^[+()0-9 .-]{7,40}$/', $telephone) || strlen(preg_replace('/[^0-9]/', '', $telephone)) < 7)) {
    respond(false, 'Merci de vérifier votre numéro de téléphone.', 422);
}
if ($sujetKey === 'rappel' && $telephone === '') {
    respond(false, 'Le numéro de téléphone est nécessaire pour vous rappeler.', 422);
}

// Anti-spam 4 : trop de liens dans le message
if (preg_match_all('~https?://~i', $message) > 3) {
    respond(true, 'OK');
}

$line = str_repeat('-', 52);
$body  = "Nouvelle demande envoyée depuis le site " . SITE_NAME . "\n{$line}\n";
$body .= "Nom       : {$nom}\n";
$body .= "E-mail    : {$email}\n";
$body .= 'Téléphone : ' . ($telephone !== '' ? $telephone : '—') . "\n";
$body .= "Sujet     : {$sujet}\n";
$body .= 'Appareil  : ' . ($appareil !== '' ? $appareil : '—') . "\n";
$body .= "{$line}\n\n{$message}\n\n{$line}\n";
$body .= 'Envoyé le ' . date('d/m/Y à H:i') . "\n";
$body .= $email !== '' ? "Répondre à cet e-mail ou rappeler le client.\n" : "Rappeler le client au numéro indiqué.\n";

$subjectLine = '=?UTF-8?B?' . base64_encode("[Site] {$sujet} — {$nom}") . '?=';
$fromName    = '=?UTF-8?B?' . base64_encode('Site ' . SITE_NAME) . '?=';

$headers  = "From: {$fromName} <" . FROM_EMAIL . ">\r\n";
if ($email !== '') $headers .= "Reply-To: {$email}\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: 8bit\r\n";
$headers .= "X-Mailer: DigitalBuro-Site\r\n";

$sent = @mail(TO_EMAIL, $subjectLine, $body, $headers, '-f' . FROM_EMAIL);

if ($sent) {
    @touch($lock);
    respond(true, 'Merci ! Votre demande est bien envoyée.');
}
respond(false, "L'envoi a échoué. Appelez-nous au 02 534 47 02 ou écrivez à " . TO_EMAIL . '.', 500);
