相关技术
===

south
---

TechDict/app/tech_dict/scripts/south_migrate.py

执行此脚本时 必须在项目目录下 而不是scripts 下.
此脚本在有数据库表结构更改时使用 使用工具: South
使用方法:

###通用做法

1.在数据库变更前
    python scripts/south_migrate.py truncate paper_edu
    此操作会删掉app里面south相关信息(包括数据库和文件)
2.在数据库变更前
    python scripts/south_migrate.py init paper_edu
    此操作会--fake旧数据库
3.数据库变更
    python scripts/south_migrate.py auto paper_edu
    此操作会更改数据库表结构,删除south相关信息(包括数据库和文件)

###针对于git上面别人代码

1.git pull 之前
    python scripts/south_migrate.py init app1,app2,app3

2.git pull 之后
    python scripts/south_migrate.py auto app1,app2,app3
