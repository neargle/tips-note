# Fuzz 尖括号跟什么字符可以使html正常解析？

## 结果

并不能正常解析...

需要像: `<% contenteditable onresize=alert(document.domain)>`, Fuzz更多的属性和方法才可以获得想要的bypass tip。

but it is another story...
