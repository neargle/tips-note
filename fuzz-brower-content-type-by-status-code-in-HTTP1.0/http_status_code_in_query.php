<?php
$payload = @$_GET["payload"];
$payload = ($payload) ? $payload : "304 Not Modified";
header("Content-Type: binary/octet-stream");
header("HTTP/1.0 " .$payload);
?>

<img src=1 onerror=alert(1)>444444
