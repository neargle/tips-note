# 使用Fuzz的方式对“Chrome XSS Auditor”与“HTTP状态码”的关系进行研究

```
- fuzzfile
│   ── 200.php
│   ├── 201.php
│   ├── 202.php
│   ├── 203.php
│   ├── ***.php
│   └── 308.php
├── generate_phpfile.py
├── readme.md
├── status_code_in_phpself.php
├── test.html
├── test_chrome_js_outside_execute.html
├── test_chrome_xss_adult.html
└── xss.php
```

- fuzzfile : python脚本生成的php文件所放的文件夹
- generate_phpfile.py : 生成返回不同状态码的php脚本的python脚本
- status_code_in_phpself.php : 最初使用这个脚本获取`_SERVER["PHP_SELF"]`或get请求来更改状态码
- test.html : html 测试文件
- test_chrome_js_outside_execute.html : Fuzz那些状态码内的内容可以在`<script src=`里面执行
- test_chrome_xss_adult.html : Fuzz那些状态码内的内容可以bypass XSS auditor
- xss.php : 拥有XSS的php环境

## 测试结果

1. fuzz失败，基于http status_code不能bypass Chrome XSS auditor
2. Chrome XSS auditor 对`<script src=`内url的判断和HTTP status_code没有关系,只要是其他域的都会block。`http://0.0.0.0:8081/xss.php?x=%3Cscript%20src=%22http://0.0.0.0:8082/fuzzfile/308.php%22%3E`。
3. script标签不闭合可能会产生问题
4. 当`<script src=`内url有get请求时，即使是自己的域也会block。`<script%20src="http://0.0.0.0:8081//fuzzfile/308.php?x">`。
5. 以下状态码页面中的内容可以在`<script src=`内执行: [
    200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 
    300, 301, 302, 303, 304, 305, 306, 307, 308
]
