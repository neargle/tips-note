# 专门用于sql注入等扫描器的url去重和比较 Python url类

[./url_filter.py 代码](./url_filter.py)

## 对比依据

目前主要的区别在于相同的get参数即使值不同也会判断为相等，例如：`http://example.com/x?a=1&b=2 == http://example.com/x?a=1&b=3`
