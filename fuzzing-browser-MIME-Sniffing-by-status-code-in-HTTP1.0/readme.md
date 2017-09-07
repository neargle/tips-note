# firefox任意版本在HTTP1.0且HTTP状态码为304的情况下, 任何Content-type都会解析为html

此Tip是我们不小心试出来的，不知道之前有没有人发现过。

## 目录：

```
├── fuzz.html : fuzz用html文件
├── http_status_code_in_query.php : 会根据`?payload=`返回http响应的php脚本
```

## 记录

1. firefox任意版本在HTTP1.0且HTTP状态码为304的情况下, 任何Content-type都会解析html
返回包为:
```
HTTP/1.0 304 Not Modified
Date: Tue, 05 Sep 2017 12:26:32 GMT
Server: Apache/2.4.23 (Unix) OpenSSL/1.0.2h PHP/7.0.9 mod_perl/2.0.8-dev Perl/v5.16.3
Connection: close

<img src=1 onerror=alert('304+Not+Modified')>
```
2. response body必须得以html标签起始

## 图

![](https://github.com/neargle/tips-note/blob/master/fuzzing-browser-MIME-Sniffing-by-status-code-in-HTTP1.0/firefox.png)

## thx

- wolf
- evi1m0
