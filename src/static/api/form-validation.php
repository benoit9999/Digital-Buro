<?php
declare(strict_types=1);

function valid_contact_name(string $name): bool
{
    return strlen($name) <= 480
        && preg_match_all('/./us', $name) <= 120
        && preg_match('/^\p{L}[\p{L}\p{M} .\x{2019}\x{0027}\-]*\p{L}\p{M}*$/u', $name) === 1
        && preg_match_all('/\p{L}/u', $name) >= 2;
}

/** Format plausibility, not proof of ownership or that the line is assigned. */
function normalized_contact_phone(string $value): ?string
{
    if (!preg_match('/^[+0-9 ()\.\-]{7,40}$/', $value)) return null;
    $phone = preg_replace('/[ ()\.\-]/', '', $value);
    if (strpos($phone, '00') === 0) $phone = '+' . substr($phone, 2);
    if (strpos($phone, '+320') === 0) $phone = '+32' . substr($phone, 4);
    if (strpos($phone, '0') === 0) {
        if (!preg_match('/^0(?:4[5-9][0-9]{7}|[1-9][0-9]{7})$/', $phone)) return null;
        $phone = '+32' . substr($phone, 1);
    }
    if (!preg_match('/^\+[1-9][0-9]{7,14}$/', $phone)) return null;
    if (strpos($phone, '+32') === 0 && !preg_match('/^\+32(?:4[5-9][0-9]{7}|[1-9][0-9]{7})$/', $phone)) return null;
    if (strpos($phone, '+33') === 0 && !preg_match('/^\+33[1-9][0-9]{8}$/', $phone)) return null;
    if (preg_match('/([0-9])\1{6,}/', $phone) || preg_match('/(?:12345678|87654321)$/', $phone)) return null;
    return $phone;
}
