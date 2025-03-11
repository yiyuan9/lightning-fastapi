# Alembic Versions

这个目录用于存放数据库迁移版本文件。

当你修改数据库模型后，使用以下命令生成新的迁移版本：

```bash
alembic revision --autogenerate -m "描述此次变更"
```

然后应用迁移：

```bash
alembic upgrade head
```

注意：此目录初始为空，首次运行项目时会自动生成初始迁移文件。 