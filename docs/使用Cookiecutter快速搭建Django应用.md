## 一、[Cookiecutter](https://github.com/audreyr/cookiecutter)介绍

Cookiecutter是一款快速建立**工程模板**的Python命令行工具，它可以让你选择已有的模板来快速搭建工程项目，例如使用[cookiecutter-django](https://github.com/pydanny/cookiecutter-django)创建Django项目，同时也支持C/C++/C#/Golang/Java/JS/PHP等语言：

![img](https://liaogx-public-img.oss-cn-shanghai.aliyuncs.com/imooc/cookiecutter_support_language.png)

## 二、安装Cookiecutter

在Python环境中使用pip安装：

```shell
$ pip install cookiecutter
```

然后到你想要创建项目的目录，执行如下命令：

```shell
$ cookiecutter https://github.com/pydanny/cookiecutter-django.git
```

配置过程如下：

```shell
project_name [My Awesome Project]: myproject  # 项目名称
project_slug [myproject]: app01  # slug
description [Behold My Awesome Project!]: This is the first application!  # 项目描述
author_name [Daniel Roy Greenfeld]: __Jack__  # 作者
domain_name [example.com]: imooc.com  # 部署的域名
email [__jack__@example.com]: imooc@imooc.com  # 邮箱
version [0.1.0]:  # 版本号，默认为0.1.0
Select open_source_license:  # 选择项目License
1 - MIT
2 - BSD
3 - GPLv3
4 - Apache Software License 2.0
5 - Not open source
Choose from 1, 2, 3, 4, 5 (1, 2, 3, 4, 5) [1]: 5
timezone [UTC]: Asia/Shanghai  # Django settings中的TIME_ZONE
windows [n]: n # 是否是Windows环境
use_pycharm [n]: y  # 是否使用Pycharm开发
use_docker [n]: y  # 是否使用Docker容器
Select postgresql_version:  # 选择Postgres数据库版本，cookiecutter-django默认只支持Postgres
1 - 10.5
2 - 10.4
3 - 10.3
4 - 10.2
5 - 10.1
6 - 9.6
7 - 9.5
8 - 9.4
9 - 9.3
Choose from 1, 2, 3, 4, 5, 6, 7, 8, 9 (1, 2, 3, 4, 5, 6, 7, 8, 9) [1]: 1
Select js_task_runner:  # js运行方式
1 - None
2 - Gulp
Choose from 1, 2 (1, 2) [1]: 1
custom_bootstrap_compilation [n]: n  # 是否自定义bootstrap压缩
use_compressor [n]: n  # 是否使用压缩
use_celery [n]: n  # 是否使用celery，一个异步任务队列
use_mailhog [n]: n  # 是否使用mailhog，Django项目中发送邮件的，也可以使用Mailgun代替
use_sentry [n]: n  # 是否使用whitenoise
use_whitenoise [n]: y  # 是否使用bootstrap压缩
use_heroku [n]: n  # 是否使用heroku，heroku是国外著名的云服务厂商之一，提供PaaS
use_travisci [n]: n  # 是否使用travisci，类似于jekins，用于DevOps中的持续集成与发布
keep_local_envs_in_vcs [y]: y  # 对于本地环境变量使用版本控制
debug [n]: y  # 是否开启debug模式，settings中配置
 [SUCCESS]: Project initialized, keep up the good work!
[root@shiyanlou ~]#
```

安装完成后，完整项目结构如下：

```shell
[root@shiyanlou ~]# cd app01/
[root@shiyanlou app01]# tree  # 如果没有，先yum install tree
.
├── app01
│   ├── conftest.py
│   ├── contrib
│   │   ├── __init__.py
│   │   └── sites
│   │       ├── __init__.py
│   │       └── migrations
│   │           ├── 0001_initial.py
│   │           ├── 0002_alter_domain_unique.py
│   │           ├── 0003_set_site_domain_and_name.py
│   │           └── __init__.py
│   ├── __init__.py
│   ├── static  # 静态文件
│   │   ├── css
│   │   │   └── project.css
│   │   ├── fonts
│   │   ├── images
│   │   │   └── favicons
│   │   │       └── favicon.ico
│   │   ├── js
│   │   │   └── project.js
│   │   └── sass
│   │       ├── custom_bootstrap_vars.scss
│   │       └── project.scss
│   ├── templates  # 模板
│   │   ├── 403_csrf.html
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── account
│   │   │   ├── account_inactive.html
│   │   │   ├── base.html
│   │   │   ├── email_confirm.html
│   │   │   ├── email.html
│   │   │   ├── login.html
│   │   │   ├── logout.html
│   │   │   ├── password_change.html
│   │   │   ├── password_reset_done.html
│   │   │   ├── password_reset_from_key_done.html
│   │   │   ├── password_reset_from_key.html
│   │   │   ├── password_reset.html
│   │   │   ├── password_set.html
│   │   │   ├── signup_closed.html
│   │   │   ├── signup.html
│   │   │   ├── verification_sent.html
│   │   │   └── verified_email_required.html
│   │   ├── base.html
│   │   ├── pages
│   │   │   ├── about.html
│   │   │   └── home.html
│   │   └── users
│   │       ├── user_detail.html
│   │       ├── user_form.html
│   │       └── user_list.html
│   └── users  # 用户模块
│       ├── adapters.py
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── __init__.py
│       ├── migrations
│       │   ├── 0001_initial.py
│       │   └── __init__.py
│       ├── models.py
│       ├── tests
│       │   ├── factories.py
│       │   ├── __init__.py
│       │   ├── test_forms.py
│       │   ├── test_models.py
│       │   ├── test_urls.py
│       │   └── test_views.py
│       ├── urls.py
│       └── views.py
├── compose  # docker compose
│   ├── local  # 开发环境
│   │   └── django
│   │       ├── Dockerfile
│   │       └── start
│   └── production  # 生产环境
│       ├── caddy  # caddy用于https部署
│       │   ├── Caddyfile
│       │   └── Dockerfile
│       ├── django  # django应用容器
│       │   ├── Dockerfile
│       │   ├── entrypoint
│       │   └── start
│       └── postgres  # 数据库容器
│           ├── Dockerfile
│           └── maintenance
│               ├── backup
│               ├── backups
│               ├── restore
│               └── _sourced
│                   ├── constants.sh
│                   ├── countdown.sh
│                   ├── messages.sh
│                   └── yes_no.sh
├── config  # Django的配置
│   ├── __init__.py
│   ├── settings
│   │   ├── base.py
│   │   ├── __init__.py
│   │   ├── local.py  # 开发环境
│   │   ├── production.py  # 生产环境
│   │   └── test.py  # 测试环境
│   ├── urls.py
│   └── wsgi.py
├── docs # 项目文档
│   ├── conf.py
│   ├── deploy.rst
│   ├── docker_ec2.rst
│   ├── index.rst
│   ├── __init__.py
│   ├── install.rst
│   ├── make.bat
│   ├── Makefile
│   └── pycharm
│       ├── configuration.rst
│       └── images
│           ├── 1.png
│           ├── 2.png
│           ├── 3.png
│           ├── 4.png
│           ├── 7.png
│           ├── 8.png
│           ├── f1.png
│           ├── f2.png
│           ├── f3.png
│           ├── f4.png
│           ├── issue1.png
│           └── issue2.png
├── locale
│   └── README.rst
├── local.yml
├── manage.py
├── merge_production_dotenvs_in_dotenv.py
├── production.yml
├── pytest.ini
├── README.rst
├── requirements  # 包和模块
│   ├── base.txt  # 必备的
│   ├── local.txt  # 开发环境，可能包含一些测试用的包
│   └── production.txt  # 生产环境
└── setup.cfg

34 directories, 109 files
[root@shiyanlou app01]#
```

因为我没有把Celery/Mailhog/Sentry等等都选上，所以东西还算比较少，现在应该知道Cookiecutter的作用了。

## 三、安装和配置Postgresql

### 3.1 安装Postgresql

从CentOS源安装，三条命令一梭哈：

```shell
$ sudo yum install postgresql-server postgresql-contrib
$ sudo postgresql-setup initdb  # 初始化
$ sudo systemctl start postgresql  # 启动服务
$ sudo systemctl enable postgresql # 可选，设置开机启动
```

### 3.2 Postgresql安全配置

一顿操作猛如虎：

```shell
[root@shiyanlou ~]# sudo passwd postgres  # 更改系统用户postgres的密码
Changing password for user postgres.
New password:
BAD PASSWORD: The password contains the user name in some form
Retype new password:
passwd: all authentication tokens updated successfully.
[root@shiyanlou ~]# su - postgres  # 更改数据库用户postgres的密码
-bash-4.2$ psql -d template1 -c "ALTER USER postgres WITH PASSWORD 'Im00c.';"
ALTER ROLE
-bash-4.2$ exit
logout
[root@shiyanlou ~]#
```

### 3.3 创建数据库和用户

类似于MySQL，不过使用cookiecutter-django默认使用PostgreSQL

```shell
[root@shiyanlou ~]# su - postgres
Last login: Thu Jan 31 22:41:31 CST 2019 on pts/0
-bash-4.2$ psql postgres
psql (9.2.24)
Type "help" for help.

postgres=# createdb imooc  # 创建数据库imooc
postgres-# create role user01 with login encrypted password 'passw0rD.' created  # 用户
postgres-# grant all privileges on database imooc to user01  # 给用户赋权
postgres-# \q
-bash-4.2$ exit
logout
[root@shiyanlou ~]#
```

cookiecutter-django使用环境变量([django-environ](https://github.com/joke2k/django-environ))来管理保密配置，`SECRET_KET`，数据库用户名密码等并没有写在代码中，使用如下命令配置环境变量：

```shell
$ export DATABASE_URL=postgres://user01:passw0rD.@localhost:5432/imooc
```

提示：PostgreSQL数据库连接字符串`postgres://用户名:密码@数据库地址:端口/库名`

## 四、安装包

### 4.1 pipenv创建环境

```sh
[root@shiyanlou ~]# cd app01/
[root@shiyanlou app01]# pipenv --python 3.7
Creating a virtualenv for this project…
Pipfile: /root/app01/Pipfile
Using /usr/bin/python3 (3.7.2) to create virtualenv…
⠙ Creating virtual environment...Using base prefix '/usr/local/python3'
New python executable in /root/.local/share/virtualenvs/app01-DYWCxUWF/bin/python3
Also creating executable in /root/.local/share/virtualenvs/app01-DYWCxUWF/bin/python
Installing setuptools, pip, wheel...
done.
Running virtualenv with interpreter /usr/bin/python3
✔ Successfully created virtual environment!
Virtualenv location: /root/.local/share/virtualenvs/app01-DYWCxUWF
Creating a Pipfile for this project…
[root@shiyanlou app01]#
```

### 4.2 安装包并lock

安装前先将`requirements/local.txt`中的

```shell
psycopg2==2.7.4 --no-binary psycopg2  # https://github.com/psycopg/psycopg2
```

改成

```shell
psycopg2 --no-binary psycopg2  # https://github.com/psycopg/psycopg2
```

否则会安装失败。（我是CentOS Linux release 7.6.1810 (Core)）

```shell
[root@shiyanlou app01]# pipenv install -r requirements/local.txt --skip-lock
Requirements file provided! Importing into Pipfile…
Installing dependencies from Pipfile…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 28/28 — 00:00:13
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
[root@shiyanlou app01]#
```

如何有提示`An error occurred while installing xxx`，重新运行一遍就行了，因为`pipenv`不稳定。

然后`pipenv lock`，很慢！无需等待可以进行后面的步骤

```shell
[root@shiyanlou app01]# pipenv lock
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
⠦ Locking...
```

然后使用Django shell生成数据表，运行项目。

## 五、优点和局限

cookiecutter的主要局限来自于它的优点，太模板化的东西会导致灵活性不足。而且目前可用的各种模板质量参差不齐，不过主流的项目模板都是非常棒的，比如各种前后端框架，机器学习等等，有很多人在维护和更新。

一个框架搭到什么程度比较合适，这就不能一概而论了。

如果你要做一个Django应用，模板里默认就集成了用户注册和登录功能，有时候你觉得太棒了我刚好需要，有时候你觉得我没这样的需求，还得从新建好的项目一点一点删掉没用的代码还可能改错导致跑不起来。

其实我认为cookiecutter也是一个很好的学习渠道，使用cookiecutter新建项目你可以看到别人是如何组织代码，如何管理配置，如何管理依赖等等，比如Python写的项目，理论上你可以把代码扔在任何目录，大拿扔的好看，自己扔的就很丑。

最后再提一点，cookiecutter支持自定义模板，你也可以把自己常用的项目功能打包成模板，后续只要有重用需求，cookiecutter一下，立马开始业务功能的cooding，岂不妙哉？

[文章参考]

[让你的项目模板化和专业化 - Cookiecutter](https://betacat.online/posts/2017-08-16/cookiecutter-intro/)

[How to create a Django Application using Cookiecutter](https://swapps.com/blog/how-to-create-a-django-application-using-cookiecutter/)

[How to Install PostgreSQL Relational Databases on CentOS 7](https://www.linode.com/docs/databases/postgresql/how-to-install-postgresql-relational-databases-on-centos-7/)