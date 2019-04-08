> 注意命令的执行用户，[root@zanhu ~]#表示root用户，[zanhu@zanhu ~]$表示zanhu用户

## 一、ECS+RDS初始化设置

待更新...

## 二、CentOS 7初始化配置

### 2.1 创建组和用户

```shell
[root@zanhu ~]# groupadd zanhu
[root@zanhu ~]# useradd -m zanhu -g zanhu
[root@zanhu ~]# passwd zanhu
```

zanhu家目录赋予执行权限，非常重要！！！

```shell
[zanhu@zanhu ~]$ chmod +x /home/zanhu/
```

### 2.2 安装系统依赖

有Python, MySQL的依赖，Elasticsearch对Java依赖，django-compressor的压缩需要的bizp2-devel等

```shell
[root@zanhu ~]# yum -y install zlib-devel mysql-devel libffi-devel bzip2-devel openssl-devel java
```

### 2.3 安装git/redis/nginx/uwsgi/supervisor

后面要用的一次装好

```shell
[root@zanhu ~]# yum -y  install git redis nginx uwsgi supervisor
```

### 2.3 设置开机启动

保证实例重启后服务依然运行

```shell
[root@zanhu ~]# systemctl enable redis nginx supervisord uwsgi
Created symlink from /etc/systemd/system/multi-user.target.wants/redis.service to /usr/lib/systemd/system/redis.service.
Created symlink from /etc/systemd/system/multi-user.target.wants/nginx.service to /usr/lib/systemd/system/nginx.service.
Created symlink from /etc/systemd/system/multi-user.target.wants/supervisord.service to /usr/lib/systemd/system/supervisord.service.
Created symlink from /etc/systemd/system/multi-user.target.wants/uwsgi.service to /usr/lib/systemd/system/uwsgi.service.
[root@zanhu ~]#
```

## 四、安装Python3

### 4.1 六条命令一梭哈

一条条来不容易出问题，阿里云的服务器下载`Python-3.7.2.tar.xz`很慢，可以先浏览器下载了再传到服务器上，后面下载`elasticsearch-2.4.6.tar.gz`也是一样。

```shell
[root@zanhu ~]# wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
[root@zanhu ~]# tar -xvf Python-3.7.2.tar.xz
[root@zanhu ~]# cd Python-3.7.2
[root@zanhu ~]# ./configure --prefix=/usr/local/python3
[root@zanhu ~]# make
[root@zanhu ~]# make install
```

### 4.2 创建软链接

```shell
[root@zanhu ~]# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
[root@zanhu ~]# ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

### 4.3 验证安装结果

```shell
[root@zanhu ~]# python3 -V
Python 3.7.2
[root@zanhu ~]# pip3 -V
pip 18.1 from /usr/local/python3/lib/python3.7/site-packages/pip (python 3.7)
[root@zanhu ~]# whereis python3
python3: /usr/bin/python3 /usr/local/python3
[root@zanhu ~]# whereis pip3
pip3: /usr/bin/pip3
[root@zanhu ~]#
```

## 五、MySQL安装和配置（用RDS的略过）

### 5.1 下载并导入MySQL的yum源

穷的时候买不起**RDS**，就在ECS上装个`MySQL 8.0`凑合下

```shell
[root@zanhu ~]# wget https://dev.mysql.com/get/mysql80-community-release-el7-2.noarch.rpm
[root@zanhu ~]# rpm -ivh mysql80-community-release-el7-2.noarch.rpm
[root@zanhu ~]# yum -y install mysql-server
```

### 5.2 启动服务并设置开机启动

```shell
[root@zanhu ~]# systemctl start mysqld
[root@zanhu ~]# systemctl enable mysqld
```

### 5.3 创建数据库和用户

在`/var/log/mysqld.log`中找到**临时密码**

```shell
[root@zanhu ~]# more /var/log/mysqld.log | grep temporary
2019-04-06T14:01:57.443425Z 5 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: jahbfeusA9!j
[root@zanhu ~]#
```

然后`root`连接到数据库，`'root'@'localhost'`表示只允许`root`用户本地连接

```shell
[root@zanhu ~]# mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.15

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

修改`root`密码

```mysql
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'zAnhu6.6';
Query OK, 0 rows affected (0.00 sec)

mysql>
```

再创建数据库和用户，注意是2个数据库，`test_zannhu`是跑测试用例需要的数据库

```mysql
mysql> create database zanhu charset utf8;
Query OK, 1 row affected, 1 warning (0.01 sec)

mysql> create database test_zanhu charset utf8;
Query OK, 1 row affected, 1 warning (0.01 sec)

mysql>  create user 'zanhu'@'localhost' identified by 'zAnhu6.6';
Query OK, 0 rows affected (0.01 sec)

mysql>
```

### 5.4 安全和权限设置

继续，给赞乎用户赋予`zanhu`和`test_zanhu`数据库的所有权限，**并且只允许通过localhost连接**，一不将`3306`端口暴露给公网，二不设置弱密码，多层安全防护。

```mysql
mysql> grant all on zanhu.* to 'zanhu'@'localhost';
Query OK, 0 rows affected (0.01 sec)

mysql> grant all on test_zanhu.* to 'zanhu'@'localhost';
Query OK, 0 rows affected (0.01 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)

mysql> exit
Bye
[root@zanhu ~]#
```

## 六、安装Elasticsearch

### 6.1 切换到zanhu用户

elasticsearch服务不能使用root用户运行

```shell
[zanhu@zanhu ~]$ wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.6/elasticsearch-2.4.6.tar.gz
[zanhu@zanhu ~]$ tar -xvf elasticsearch-2.4.6.tar.gz
[zanhu@zanhu ~]$ touch elasticsearch_running.log
[zanhu@zanhu ~]$ ./elasticsearch-2.4.6/bin/elasticsearch > elasticsearch_running.log 2>&1 &
[zanhu@zanhu ~]$
```

### 6.2 验证安装结果

```shell
[zanhu@zanhu ~]$ curl http://localhost:9200/
{
  "name" : "Damballah",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "epKEXYosQBWrDHQbL3bPBw",
  "version" : {
    "number" : "2.4.6",
    "build_hash" : "5376dca9f70f3abef96a77f4bb22720ace8240fd",
    "build_timestamp" : "2017-07-18T12:17:44Z",
    "build_snapshot" : false,
    "lucene_version" : "5.5.4"
  },
  "tagline" : "You Know, for Search"
}
[zanhu@zanhu ~]$
```

## 七、项目发布

### 7.1 上传代码

这里我是从自己GitHub的**私有**仓库`clone`过来，大家可以上传自己的代码

```shell
[zanhu@zanhu ~]$ git clone https://github.com/liaogx/zanhu.git
```

创建logs文件夹，用于存放`uwsgi`和`daphne`生成的日志

```shell
[zanhu@zanhu ~]$ cd zanhu
[zanhu@zanhu zanhu]$ mkdir logs
```

### 7.2 安装项目需要的包

部署到生产环境的时候，因为就一个项目在服务器上，就使用真实的Python3环境，**不需要pipenv了**

使用`root`安装，其它用户权限不够，`requirements.txt`文件如下，生产环境需要的包

```shell
python-slugify==3.0.1
redis==3.2.1
celery==4.2.1
django==2.1.7
django-redis==4.10.0
django-allauth==0.39.1
django-environ==0.4.5
django-crispy-forms==1.7.2
django-compressor==2.2
mysqlclient==1.4.2.post1
django-contrib-comments==1.9.1
django-markdownx==2.0.28
channels==2.1.7
sorl-thumbnail==12.5.0
django-taggit==1.1.0
channels-redis==2.3.3
awesome-slugify==1.6.5
argon2-cffi==19.1.0
pillow==5.4.1
python3-openid==3.1.0
requests-oauthlib==1.2.0
requests==2.21.0
django-haystack==2.8.1
elasticsearch==2.4.1
```

安装，root用户的pip源会自动使用阿里云，飞快

```shell
[root@zanhu ~]# pip3 install -r /home/zanhu/zanhu/requirements.txt
```

### 7.3 生成数据表

回到`zanhu`用户，migrate一下

```shell
[zanhu@zanhu zanhu]$ pwd
/home/zanhu/zanhu
[zanhu@zanhu zanhu]$ python3 manage.py migrate
......
```

### 7.4 collect静态文件

```shell
[zanhu@zanhu zanhu]$ python3 manage.py collectstatic

99 static files copied to '/home/zanhu/zanhu/zanhu/static'.
[zanhu@zanhu zanhu]$
```

### 7.5 压缩静态文件

```shell
[zanhu@zanhu zanhu]$ python3 manage.py compress --force
......
Compressing... done
Compressed 13 block(s) from 61 template(s) for 1 context(s).
[zanhu@zanhu zanhu]$
```

### 7.6 添加GitHub的client_id和secret

这步别忘了，不然网站无法使用GitHub注册。这里我以自己视频中讲解的为例，大家灵活变通

```mysql
[zanhu@zanhu zanhu]$ mysql -u root -p
Enter password:

mysql> use zanhu;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> insert into socialaccount_socialapp values (1, 'GitHub', 'GitHub', '9393a29720306c652566', '620f2137713131c9644cf3e878e1555933afd2cea', '');
Query OK, 1 row affected (0.01 sec)

mysql>
mysql> insert into socialaccount_socialapp_sites values (1, 1, 1);
Query OK, 1 row affected (0.01 sec)

mysql> exit
Bye
[zanhu@zanhu zanhu]$
```

对应的，这是我GitHub上`OAuth Apps`认证的设置

![img](https://liaogx-public-img.oss-cn-shanghai.aliyuncs.com/imooc/zanhu_oauth_github_explanation.png)

## 八、nginx+uwsgi+daphne配置

### 8.1 nginx配置

下面是nginx的配置，`/etc/nginx/nginx.conf`

```shell
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    upstream channels-backend {  # websocket请求转发配置
        server localhost:8000;
    }

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
            include	uwsgi_params;  # uwsgi_params at /etc/nginx
            uwsgi_pass unix:/run/zanhu_uwsgi.sock;  # sock文件，与/etc/uwsgi.d/zanhu_uwsgi.ini中定义的相同
        }

        location /static/ {
            root  /home/zanhu/zanhu/zanhu;  # static文件所在的目录路径
        }

        location /media/ {
            root   /home/zanhu/zanhu/zanhu;  # media文件所在的目录路径
        }

        location /ws/ {  # /ws/用于区分http请求和websocket
            proxy_pass http://channels-backend;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $server_name;
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
}
```

### 8.2 uwsgi配置

下面是uwsgi的配置，`uwsgi.service`服务

```shell
[Unit]
Description=zanhu uWSGI service

[Service]
ExecStart=/usr/local/python3/bin/uwsgi --emperor /etc/uwsgi.d
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

和`zanhu_uwsgi.ini`文件

```shell
[uwsgi]
# Django manage.py 所在文件夹路径
chdir = /home/zanhu/zanhu
module = config.wsgi:application
# 启用master进程管理
master = true
# 绑定的 UNIX socket
socket = /run/zanhu_uwsgi.sock
# uwsgi的进程数
processes = 1
# uWSGI进程的用户标识
uid = zanhu
# uWSGI进程的组标识
gid = zanhu
# 最大请求处理数，之后重新生成进程
max-requests = 5000
# 退出时清理环境
vacuum = true
# python的安裝路径
home = /usr/local/python3/
# 设置 UNIX socket的所有者和权限
chown-socket = zanhu:nginx
chmod-socket = 660
# 日志中加入时间戳
log-date = true
logto = /home/zanhu/zanhu/logs/uwsgi.log
```

### 8.3 daphne配置

daphne的配置，supervisor通过读取`zanhu_daphne.ini`的配置，管理daphne进程

```shell
[program:daphne]
socket = tcp://localhost:8000  # 与Nginx的TCP Socket连接
# 项目目录
directory = /home/zanhu/zanhu
# 每个进程都需要独立的socket文件
command = /usr/local/python3/bin/daphne --root-path=/home/zanhu/zanhu config.asgi:application
stdout_logfile = /home/zanhu/zanhu/logs/daphne.log
# 给每个进程命名，便于管理
process_name = asgi_worker%(process_num)s
# 启动的进程数，设置成云服务器的vCPU数
numprocs = 1
# 设置自启和重启
autostart = true
autorestart = true
redirect_stderr = True
stopasgroup = true
```

## 九、启动服务并检查日志

### 9.1 启动nginx

```shell
[root@zanhu ~]# cp /home/zanhu/zanhu/nginx.conf /etc/nginx/nginx.conf
[root@zanhu ~]# systemctl start nginx
```

### 9.2 启动uwsgi

先Python环境中安装uwsgi，然后启动uwsgi

```shell
[root@zanhu ~]# pip3 install uwsgi
[root@zanhu ~]# cp /home/zanhu/zanhu/uwsgi.service /etc/systemd/system/
[root@zanhu ~]# cp /home/zanhu/zanhu/zanhu_uwsgi.ini /etc/uwsgi.d/
[root@zanhu ~]# systemctl daemon-reload
[root@zanhu ~]# systemctl restart uwsgi
```

### 9.3 启动supervisord

也就是启动了daphe进程

```shell
[root@zanhu ~]# cp /home/zanhu/zanhu/zanhu_daphne.ini /etc/supervisord.d/
[root@zanhu ~]# systemctl start supervisord
[root@zanhu ~]# supervisorctl update
[root@zanhu ~]# supervisorctl reload
```

### 9.4 更改日志权限

非常重要！！！给日志增加可读权限。并启动`redis`服务，别漏了

```shell
[root@zanhu ~]# chmod +r /home/zanhu/zanhu/logs/*
[root@zanhu ~]# systemctl start redis
```

### 9.5 检查日志

- `uwsgi.log`

```shell
[zanhu@zanhu ~]$ tail -5  zanhu/logs/uwsgi.log
[pid: 30345|app: 0|req: 139/139] 180.164.101.207 () {46 vars in 930 bytes} [Sun Apr  7 00:09:36 2019] GET /accounts/login/?next=/notifications/latest-notifications/%3F_%3D1554566976945 => generated 6247 bytes in 13 msecs (HTTP/1.1 200) 7 headers in 344 bytes (1 switches on core 0)
[pid: 30345|app: 0|req: 140/140] 180.164.101.207 () {48 vars in 923 bytes} [Sun Apr  7 00:09:37 2019] GET /accounts/login/?next=/ => generated 5009 bytes in 14 msecs (HTTP/1.1 200) 7 headers in 352 bytes (1 switches on core 0)
[pid: 30345|app: 0|req: 141/141] 180.164.101.207 () {46 vars in 878 bytes} [Sun Apr  7 00:09:37 2019] GET /notifications/latest-notifications/?_=1554566977949 => generated 0 bytes in 2 msecs (HTTP/1.1 302) 7 headers in 274 bytes (1 switches on core 0)
[pid: 30345|app: 0|req: 142/142] 180.164.101.207 () {46 vars in 930 bytes} [Sun Apr  7 00:09:37 2019] GET /accounts/login/?next=/notifications/latest-notifications/%3F_%3D1554566977949 => generated 6247 bytes in 12 msecs (HTTP/1.1 200) 7 headers in 344 bytes (1 switches on core 0)
[pid: 30345|app: 0|req: 143/143] 180.164.101.207 () {46 vars in 944 bytes} [Sun Apr  7 00:09:38 2019] GET /accounts/github/login/?process=login&next=%2F => generated 0 bytes in 15 msecs (HTTP/1.1 302) 8 headers in 551 bytes (1 switches on core 0)
```

- `daphne.log`

```shell
[zanhu@zanhu ~]$ tail -5  zanhu/logs/daphne.log
127.0.0.1:42906 - - [07/Apr/2019:00:31:28] "WSDISCONNECT /ws/notifications/" - -
127.0.0.1:42912 - - [07/Apr/2019:00:31:39] "WSCONNECTING /ws/notifications/" - -
127.0.0.1:42912 - - [07/Apr/2019:00:31:39] "WSREJECT /ws/notifications/" - -
127.0.0.1:42912 - - [07/Apr/2019:00:31:39] "WSDISCONNECT /ws/notifications/" - -
127.0.0.1:42918 - - [07/Apr/2019:00:31:50] "WSCONNECTING /ws/notifications/" - -
```

- `nginx access.log`，root用户才有权限查看，下同。

```shell
[root@zanhu ~]# tail -5 /var/log/nginx/access.log
180.164.101.207 - - [07/Apr/2019:00:41:32 +0800] "GET /static/CACHE/css/bootstrap.min.css.map HTTP/1.1" 404 3043 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36" "-"
180.164.101.207 - - [07/Apr/2019:00:41:32 +0800] "GET /static/fonts/font-awesome-4.7.0/fonts/fontawesome-webfont.woff2?v=4.7.0&b3114982de95 HTTP/1.1" 200 77160 "http://39.98.252.127/static/CACHE/css/7be88d97718d.css" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36" "-"
180.164.101.207 - - [07/Apr/2019:00:41:32 +0800] "GET /static/CACHE/js/8b4fbd1ef7c0.js HTTP/1.1" 200 423351 "http://39.98.252.127/messages/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36" "-"
180.164.101.207 - - [07/Apr/2019:00:41:33 +0800] "GET /notifications/latest-notifications/?_=1554568893315 HTTP/1.1" 200 94 "http://39.98.252.127/messages/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36" "-"
180.164.101.207 - - [07/Apr/2019:00:41:33 +0800] "GET /static/img/favicon.png HTTP/1.1" 200 17052 "http://39.98.252.127/messages/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36" "-"
[root@zanhu ~]#
```

- `nginx error.log`，没有报错，爽！

```shell
[root@zanhu ~]# tail -5 /var/log/nginx/error.log

```

- `supervisor.log`，root用户才有权限查看

```shell
[root@zanhu ~]# tail -10 /var/log/supervisor/supervisord.log
2019-04-06 23:24:18,396 INFO success: asgi_worker0 entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
2019-04-06 23:24:29,561 INFO waiting for asgi_worker0 to die
2019-04-06 23:24:29,725 INFO stopped: asgi_worker0 (exit status 0)
2019-04-06 23:24:29,729 CRIT Supervisor running as root (no user in config file)
2019-04-06 23:24:29,729 WARN Included extra file "/etc/supervisord.d/zanhu_daphne.ini" during parsing
2019-04-06 23:24:29,730 INFO RPC interface 'supervisor' initialized
2019-04-06 23:24:29,730 CRIT Server 'unix_http_server' running without any HTTP authentication checking
2019-04-06 23:24:29,730 INFO supervisord started with pid 30359
2019-04-06 23:24:30,732 INFO spawned: 'asgi_worker0' with pid 30365
2019-04-06 23:24:32,371 INFO success: asgi_worker0 entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
[root@zanhu ~]#
```

有提示`CRIT Server 'unix_http_server' running without any HTTP authentication checking`，可以在`/etc/supervisord.conf`中给`unix_http_server`设置用户名和密码，就这样也没事。

## 十、赢取白富美，出任CTO...

完。