import os

php_code_format = '''
<?php
$payload = {status_code};
http_response_code($payload);
die("console.log($payload);");
'''

status_code_lst = [
    200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 
    300, 301, 302, 303, 304, 305, 306, 307, 308
]


for status_code in status_code_lst:
    code_str = str(status_code)
    with open("fuzzfile/{}.php".format(status_code), "w") as f:
        f.write(php_code_format.format(status_code=code_str))
