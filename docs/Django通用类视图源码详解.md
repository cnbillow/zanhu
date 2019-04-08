## Django通用类视图源码详解

![img](https://upload-images.jianshu.io/upload_images/6993533-e1cc1955aded941c.png)

| 属性/方法                          | 含义                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| model①                             | 指定模型类                                                   |
| tempalta_name                      | 指定模板文件，默认是`模型类名_list`，在当前应用的模板文件夹下 |
| queryset②                          | 指定一个经过过滤的对象列表，将取代`model`提供的值            |
| context_object_name                | 定义queryset结果集在模板中的名字，默认是`object_list`或`模型类名_list` |
| paginate_by                        | 对象分页                                                     |
| ordering                           | 排序查询集对象，str或元组                                    |
| `get_ordering(self)`               | 排序查询集对象 [源码]                                        |
| `get_paginate_by(self, queryset)`  | 对象分页 [源码]                                              |
| `get_queryset(self)`③              | 获取此视图的对象列表，必须是可迭代或者可以使查询集，默认返回`queryset`属性，可以通过**重写**该方法实现动态过滤 [源码](http://ccbv.co.uk/projects/Django/2.1/django.views.generic.list/ListView/#get_queryset) |
| `get_context_data(self, **kwargs)` | 返回显示对象的上下文数据,通过**覆盖**该方法返回额外的上下文 [源码] |



说明

![img](https://upload-images.jianshu.io/upload_images/6993533-098ed1d26164267a.png)

| 属性/方法                          | 含义                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| model                              | 同上                                                         |
| template_name                      | 同上                                                         |
| success_url                        | 删除成功后跳转的url路径                                      |
| queryset                           | 同上                                                         |
| context_object_name                | 同上                                                         |
| slug_url_kwarg                     | 通过url传入的要删除的对象主键id，默认值为slug                |
| pk_url_kwarg                       | 通过url传入的要删除的对象主键id，默认值为pk                  |
| `get_object(self, queryset=None)`  | 返回要删除的对象，[源码](http://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/DeleteView/#get_object) |
| `get_queryset(self)`               | 获取此视图的对象                                             |
| `get_context_data(self, **kwargs)` | 将单个对象插入到上下文中                                     |

**参考**

1. [class-based-views flattened-index](https://docs.djangoproject.com/en/2.2/ref/class-based-views/flattened-index/)
2. [Django 2.1 ListView](http://ccbv.co.uk/projects/Django/2.1/django.views.generic.list/ListView/)
3. [Django 2.1 DeleteView](http://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/DeleteView/)