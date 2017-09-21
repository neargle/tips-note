# Fuzz 尖括号跟什么字符可以使html正常解析？

## 结果

并不能正常解析...
需要像: `<% contenteditable onresize=alert(document.domain)>` in ie, Fuzz更多的熟悉和方法才可正常执行
and it is another story...
