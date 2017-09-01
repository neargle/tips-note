<?php

function startsWith($url, $domain) {
     $length = strlen($domain);
     return (substr($url, 0, $length) === $domain);
}

$referrer = @$_SERVER['HTTP_REFERER'];

if (startsWith($referrer, "http://10.101.122.75:8082")) {
    $js_code = 'function jquery() { return "security content";}';
    echo $js_code;
} else {
    $js_code = 'function jquery() { return "nothing";}';
    echo $js_code;
}

