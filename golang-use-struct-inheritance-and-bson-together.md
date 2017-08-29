# golang定义struct使用继承时如何和bson及json库兼容

情况如下：

```go
type Example struct {
    ID        bson.ObjectId `bson:"_id,omitempty"      json:"_id,omitempty"`
    baseModel
}
```

1. 使用小写开头的基结构体，可以使转换而成的bson或json结构不带baseModel
2. 在自动转化为bson时，例如mgo.v2在insert的时候如果带有小写的基结构体，程序会爆以下错误:

```
reflect.Value.Interface: cannot return value obtained from unexported field or method
```

解决方法：

```go
type Example struct {
    ID        bson.ObjectId `bson:"_id,omitempty"      json:"_id,omitempty"`
    baseModel `bson:",inline"`
}
```

定义bson为inline，则在自动转换的时候，mgo.v2不会用反射去猜测baseModel的结构。

官方解释：

> inline     Inline the field, which must be a struct or a map,
>            causing all of its fields or keys to be processed as if
>            they were part of the outer struct. For maps, keys must
>            not conflict with the bson keys of other struct fields.
