<?php
$payload = $_SERVER["PHP_SELF"];
$payload = @substr($payload, -3);
$payload = ($payload) ? $payload : 404 ;
http_response_code($payload);
die("document.write($payload);");
