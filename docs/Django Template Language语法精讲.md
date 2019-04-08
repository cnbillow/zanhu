## 一、模板继承

**base.html**文件，比如上方的导航栏

```python
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>
<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>
    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

其它功能模块的html文件

```python
{% extends "base.html" %}

{% block title %}My amazing blog{% endblock %}

{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```

## 二、变量

使用方式，不能以_开头

```python
{{ variable }}
```

`.`或获取变量的属性

循环字典

```python
{% for k, v in defaultdict.items %}
    Do something with k and v here...
{% endfor %}
```

## 三、过滤器

`{{ value|add:"2" }}`	字符串或列表相加，注意：字符串是变成整数相加
`{{ first|add:second }}`		
`{{ value|addslashes }}`		单引号前面加上/ 比如把 I'm using Django 变成 I\\'m using Django
`{{ value|capfirst }}`	首字母大写	
`{{ value|center:"15" }}`	15个占位符居中对齐

`{{ value|ljust:"10" }}`		10个占位符左对齐
`{{ value|rjust:"10" }}`		10个占位符右对齐

`{{ value|cut:" " }}`	移除掉所有的空格，如要移除所有的A, {{ value|cut: "A" }}
`{{ value|date:"D d M Y" }}` 	[参考](https://docs.djangoproject.com/en/2.1/ref/templates/builtins/#date)
`{{ value|default:"nothing" }}` 	如果value是False的话，使用默认值
`{{ value|default_if_none:"nothing" }}` 	如果value是None的话，使用默认值
`{{ value|dictsort:"name" }}`	对列表中的多个字典进行排序

例如

```python
[
    {'name': 'zed', 'age': 19},
    {'name': 'amy', 'age': 22},
    {'name': 'joe', 'age': 31},
]
```

结果是

```python
[
    {'name': 'amy', 'age': 22},
    {'name': 'joe', 'age': 31},
    {'name': 'zed', 'age': 19},
]
```

再举个栗子

```python
[
    {'title': '1984', 'author': {'name': 'George', 'age': 45}},
    {'title': 'Timequake', 'author': {'name': 'Kurt', 'age': 75}},
    {'title': 'Alice', 'author': {'name': 'Lewis', 'age': 33}},
]
```

使用`dicsort`

```python
{% for book in books|dictsort:"author.age" %}
    * {{ book.title }} ({{ book.author.name }})
{% endfor %}
```

结果是

```python
* Alice (Lewis)
* 1984 (George)
* Timequake (Kurt)
```

再再举个栗子，列表中的元组也是可以排序的

```python
[
	('c', 'string'),
    ('a', '42'),
    ('b', 'foo'),
]
```

使用`dictsortreversed`反向排序

```python
{{ value|dictsortreversed:0 }}  # 注意要是数字下标0，不是字符串"0"
```

结果是

```python
[
    ('c', 'string'),
    ('b', 'foo'),
    ('a', '42'),
]
```

`{{ value|divisibleby:"3" }}`	value能否被3整除，返回True或者False
`{{ value|filesizeformat }}`	文件大小变成人类直观可读的方式，value是123456789，变成117.7MB
`{{ value|first }}`	返回列表的第一个元素或字符串的第一个字符
`{{ value|last }}`	返回列表的最后一个元素回字符串的最后一个字符
`floatformat`	[各种格式化](https://docs.djangoproject.com/en/2.1/ref/templates/builtins/#floatformat)
`force_escape`	再关闭转义的区域，强制启用转义
`{{ value|get_digit:"2" }}` 从右边往左取第2为，如果是123456789？

`{{ value|join:" // " }}`	使用字符串连接列表 ['a', 'b', 'c']变成了 "a // b // c"

`json_script`	Django 2.1版本里面唯一一个新增的

举个栗子

```python
{{ value|json_script:"hello-data" }}
```

如果value的值是字典{'hello': 'world'}，结果将神奇的变成

```javascript
<script id="hello-data" type="application/json">{"hello": "world"}</script>
```

然后可以在JS里面接收这个值

```javascript
var value = JSON.parse(document.getElementById('hello-data').textContent);
```

`{{ value|length }}` 	返回列表或字符串的长度
`{{ value|length_is:"4" }}`	返回True或者False
`{{ value|linebreaks }}` 	比如，将Python/nDjango变成`<p>Python<br>Django</p>`
`{{ value|linebreaksbr }}`	比如，将Python/nDjango变成`Python<br>Django`
`{{ value|linenumbers }}`

举个栗子，value是

```
one
two
three
```

结果是

```python
1. one
2. two
3. three
```

 `{{ value|make_list }}`		将数字或字符串循环到列表
`{{ value|random }}`		字符串或列表中随机获取一个

`{{ value|safe }}`	对value关闭自动转义

`{{ some_list|safeseq|join:", " }}`		对列表中每一个对象关闭自动转义，然后字符串拼接
`{{ value|slice:":2" }}`		获取列表的前两个元素，或字符串的前2为
`{{ value|slugify }}`	支持英文的slug
`{{ value|stringformat:"E" }}`	科学计数法表示
`{{ value|striptags }}`	过滤掉html中的标签
`{{ blog_date|timesince:comment_date }}` 	人性化的时间显示
`{{ value|title }}`	标题大写
`{{ value|truncatechars:9 }}` 	截取字符串，超过6后面会变成 `...`
`{{ value|truncatechars_html:9 }}`	截取html标签中的字符串，超过6后面变成`...`
`{{ value|truncatewords:2 }}`	截取字单词，超过6后面会变成 `...`
`{{ value|truncatewords_html:2 }}`	截取html标签中的单词，超过6后面变成`...`
`{{ value|upper }}`		字母变大写

`{{ name|lower }}`		字母变小写

`{{ value|urlencode }}`		url编码

把`https://www.example.org/`变成`https%3A%2F%2Fwww.example.org%2F`
`{{ value|urlizetrunc:15 }}`

把`Check out www.djangoproject.com`	变成`Check out <a href="http://www.djangoproject.com" rel="nofollow">www.djangopr...</a>`
`{{ value|wordcount }}`		统计单词个数
`{{ value|wordwrap:5 }}`		每一行限定多少个，多了就换行

## 四、标签

for循环标签

```python
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
```

以及for ... empty

```python
{% thumbnail article.image "1920x1080" as im %}
    <img src="{{ im.url }}" alt="文章图片" class="card-img-top">
{% empty %}
    <img class="card-img-top" src="http://placehold.it/1920x1080" alt="图片大小">
{% endthumbnail %}
```

if, elif, and else

```python
{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% endif %}
```

加上条件判断 **`==`, `!=`, `<`, `>`, `<=`, `>=`, `in`, `not in`, `is`, 以及 `is not`**

```python
{% if athlete_list and coach_list or cheerleader_list %}
{% if somevar == "x" %}
  This appears if variable somevar equals the string "x"
{% endif %}
```

判断是否是否相等`ifequal` and `ifnotequal`  (Django 2.1文档提示将在之后的版本中移除此功能)

{% ifequal a b %} ... {% endifequal %}
{% if a == b %} ... {% endif %}

注释内容comment；不能嵌套！

```python
<p>Rendered text with {{ pub_date|date:"c" }}</p>
{% comment "Optional note" %}
    <p>Commented out text with {{ create_date|date:"c" }}</p>
{% endcomment %}
```

csrf_token, 这个不解释

cycle 循环常量或变量

```python
{% for o in some_list %}
    <tr class="{% cycle 'row1' rowvalue2 'row3' %}">
        ...
    </tr>
{% endfor %}
```

extends继承父模板

```
{% extends "./base2.html" %}
{% extends "../base1.html" %}
{% extends "./my/base3.html" %}
```

filter过滤器，使用单个或多个过滤器

```python
{% filter force_escape|lower %}
    This text will be HTML-escaped, and will appear in all lowercase.
{% endfilter %}
```

firstof 输出第一个为True的值

```
{% firstof var1 var2 var3 %}
```

ifchange用法

include 加载模板或内容到当前的上下文

```python
{% include "foo/bar.html" %}
{% include template_name %}
```

load 加载模板标签

lorem 随机展示内容

```python
{% lorem [count] [method] [random] %}
# method 有 w(单词), p(html段落), b(文本段落)
```

now 展示当前日期或时间

```python
{% now "jS F Y H:i" %}
```

resetcycle 重置为第一个开始循环

```
{% for coach in coach_list %}
    <h1>{{ coach.name }}</h1>
    {% for athlete in coach.athlete_set.all %}
        <p class="{% cycle 'odd' 'even' %}">{{ athlete.name }}</p>
    {% endfor %}
    {% resetcycle %}
{% endfor %}
```

结果如下

```
<h1>José Mourinho</h1>
<p class="odd">Thibaut Courtois</p>
<p class="even">John Terry</p>
<p class="odd">Eden Hazard</p>

<h1>Carlo Ancelotti</h1>
<p class="odd">Manuel Neuer</p>
<p class="even">Thomas Müller</p>
```

spaceless移除html中的空格、tab和换行

```python
{% spaceless %}
    <p>
        <a href="foo/">Foo</a>
    </p>
{% endspaceless %}
```

verbatim  在区域内禁止Django模板引擎

```
{% verbatim %}
    {{if dying}}Still alive.{{/if}}
{% endverbatim %}
```

with 重命名并缓存变量，这样的话`business.employees.count`不会查询数据库多次

```python
{% with total=business.employees.count %}
    {{ total }} employee{{ total|pluralize }}
{% endwith %}

{% with alpha=1 beta=2 %}
    ...
{% endwith %}
```

block, autoescape, url也属于标签

## 五、注释

使用`{# #}`

```python
{# greeting #}hello
{# {% if foo %}bar{% else %} #}
```

## 六、自动HTML转义

安全起见，默认开启自动转义；有如下2种方式关闭

- 对于变量

```python
{{ article.get_markdown|safe }}
```

- 对于block(区域)

```python
Auto-escaping is on by default. Hello {{ name }}

{% autoescape off %}
    This will not be auto-escaped: {{ data }}.

    Nor this: {{ other_data }}
    {% autoescape on %}
        Auto-escaping applies again: {{ name }}
    {% endautoescape %}
{% endautoescape %}
```

- 在已关闭转义的区域中启用转义

```python
{% autoescape off %}
    {{ title|escape }}
{% endautoescape %}
```



## 七、方法调用

比如QuerySet中的方法

```python
{% for tag in article.tags.all %}
    <a href="#"><span class="badge badge-info">{{ tag }}</span></a>
{% endfor %}
```

## 八、自定义标签和过滤器

举例，在`INSTALLED_APPS`中添加`django.contrib.humanize`

在前端模板上方导入

```python
{% load humanize %}
```

使用过滤器

```python
{{ news.created_at|naturaltime }}
{{ 45000|intcomma }}
```
