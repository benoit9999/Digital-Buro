<?php
/** Optional Google Places (New) adapter. Disabled without explicit server config.
 * No API key in public files; no reviews cache (Places storage restrictions).
 * Keep the static, attributed reviews as the fallback in all cases.
 */
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex, nofollow');
function unavailable(): void {
    http_response_code(503);
    echo json_encode(['ok' => false, 'fallback' => 'static']);
    exit;
}
if (getenv('DB_PLACES_ENABLED') !== '1') unavailable();
$key = getenv('DB_PLACES_API_KEY');
$place = getenv('DB_PLACES_ID');
if (!$key || !$place || !preg_match('/^[a-zA-Z0-9_-]+$/', $place) || !function_exists('curl_init')) unavailable();
// Rate limit requests without storing any Places content.
$lock = sys_get_temp_dir() . DIRECTORY_SEPARATOR . 'digital-buro-places-rate';
$handle = @fopen($lock, 'c+');
if (!$handle || !flock($handle, LOCK_EX)) unavailable();
$previous = (int) stream_get_contents($handle);
if (time() - $previous < 30) { flock($handle, LOCK_UN); fclose($handle); unavailable(); }
rewind($handle); ftruncate($handle, 0); fwrite($handle, (string) time());
flock($handle, LOCK_UN); fclose($handle);
$ch = curl_init('https://places.googleapis.com/v1/places/' . rawurlencode($place) . '?languageCode=fr');
curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER=>true, CURLOPT_CONNECTTIMEOUT=>3, CURLOPT_TIMEOUT=>6,
 CURLOPT_HTTPHEADER=>['X-Goog-Api-Key: ' . $key, 'X-Goog-FieldMask: rating,userRatingCount,reviews,googleMapsUri,attributions']]);
$body=curl_exec($ch);$code=curl_getinfo($ch,CURLINFO_HTTP_CODE);curl_close($ch);
if ($code !== 200 || !is_string($body)) unavailable();
$data=json_decode($body,true);
if (!is_array($data)) unavailable();
$reviews=[];
foreach (($data['reviews'] ?? []) as $review) {
 $reviews[]=['author'=>$review['authorAttribution']['displayName'] ?? '',
  'author_url'=>$review['authorAttribution']['uri'] ?? '', 'rating'=>$review['rating'] ?? null,
  'date'=>$review['publishTime'] ?? null, 'text'=>$review['text']['text'] ?? '',
  'source'=>$review['googleMapsUri'] ?? ($data['googleMapsUri'] ?? '')];
}
echo json_encode(['ok'=>true,'rating'=>$data['rating'] ?? null,'count'=>$data['userRatingCount'] ?? null,
 'reviews'=>$reviews,'attributions'=>$data['attributions'] ?? [],'source'=>$data['googleMapsUri'] ?? '',
 'attribution'=>'Google Maps'],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
