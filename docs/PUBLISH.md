# Publication Guide | 发布指南

This document provides guidelines on how to publish a Python package to PyPI, so that other developers can install the package using `pip install`. | 本文档提供了如何发布 Python 包到 PyPI 的指南，以便其他开发者可以使用 `pip install` 来安装该包。

## Publication Steps | 发布步骤

### 1. Prepare for Publication | 1. 准备发布

Make sure you have a [PyPI](https://pypi.org/) account. If not, please register one first. | 确保你已经有一个 [PyPI](https://pypi.org/) 账号。如果没有，请先注册一个。

```bash
# Install necessary packaging tools | 安装必要的打包工具
pip install build twine
```

### 2. Test Local Package | 2. 测试本地包

Before publishing, you can test the package locally: | 在发布前，可以先在本地测试这个包：

```bash
# Enter package directory | 进入包目录
cd /path/to/backend-starter

# Create development installation | 创建开发安装
pip install -e .

# Test package functionality | 测试包功能
# ...

# After testing, uninstall | 测试完成后，卸载
pip uninstall <package-name>
```

### 3. Build Package | 3. 构建包

```bash
# Build package | 构建包
python -m build
```

This will create source distribution (.tar.gz) and wheel distribution (.whl) files in the `dist/` directory. | 这将在 `dist/` 目录下创建源代码分发包（.tar.gz）和轮子分发包（.whl）。

### 4. Publish to PyPI | 4. 发布到 PyPI

```bash
# First test on TestPyPI (optional but recommended) | 先在 TestPyPI 上测试发布（可选但推荐）
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Publish to official PyPI | 发布到正式 PyPI
twine upload dist/*
```

You will be asked to enter your PyPI username and password during publication. | 发布时会要求输入你的 PyPI 用户名和密码。

### 5. Verify Publication | 5. 验证发布

After publishing, you can verify that the package is available using the following command: | 发布后，你可以使用以下命令验证包是否可用：

```bash
pip install <package-name>
```

## Updating the Package | 更新包

### Update Steps | 更新步骤

1. Modify code and test | 修改代码并测试
2. Update version number in `setup.py` or `pyproject.toml` | 更新 `setup.py` 或 `pyproject.toml` 中的版本号
3. Rebuild and republish | 重新构建并发布

```bash
# Clean previous builds | 清理之前的构建
rm -rf dist/ build/ *.egg-info/

# Rebuild | 重新构建
python -m build

# Publish updated version | 发布更新后的版本
twine upload dist/*
```

## Notes | 注意事项

1. Ensure the following information is correct in `setup.py` or `pyproject.toml`: | 在 `setup.py` 或 `pyproject.toml` 中确保以下信息正确:
   - name (`name`) | 名称 (`name`)
   - version (`version`) | 版本 (`version`)
   - description (`description`) | 描述 (`description`)
   - repository URL (`url`) | 仓库地址 (`url`)
   - author (`author`) | 作者 (`author`)
   - license (`license`) | 许可证 (`license`)

2. Package names must be unique on PyPI, make sure your package name is not already taken. | 包名称在 PyPI 上必须是唯一的，确保你的包名没有被占用。

3. Consider adding a detailed README.md as the long description for your package. | 考虑添加详细的 README.md，作为包的长描述。

4. Use Semantic Versioning to manage your version numbers. | 使用语义化版本控制（Semantic Versioning）来管理你的版本号。

## Troubleshooting | 疑难解答

If you encounter problems during the publication process: | 如果发布过程中遇到问题:

- Make sure your PyPI account email is verified | 确保你的 PyPI 账号电子邮件已验证
- Check if the package name conflicts with existing packages | 检查包名是否与现有包冲突
- If upload fails, check the error message and resolve the corresponding issue | 如果上传失败，检查错误消息并解决相应问题
- Use `twine check dist/*` to verify that your distribution packages meet PyPI requirements | 使用 `twine check dist/*` 来验证你的分发包是否符合 PyPI 要求

For more help, please refer to the [PyPI documentation](https://packaging.python.org/tutorials/packaging-projects/). | 如需更多帮助，请参考 [PyPI 文档](https://packaging.python.org/tutorials/packaging-projects/)。 