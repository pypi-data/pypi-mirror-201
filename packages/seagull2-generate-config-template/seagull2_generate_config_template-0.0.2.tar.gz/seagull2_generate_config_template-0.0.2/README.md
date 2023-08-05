
# 简介
海鸥Ⅱ根据模板生成配置文件

# 打包py

## 安装打包工具 
```
 python -m pip install --user --upgrade setuptools wheel
 ```

## 打包
```
python .\setup.py sdist bdist_wheel
```
### [setup.py 参考](https://docs.python.org/3.8/distutils/setupscript.html#writing-the-setup-script)

## 测试
```
cd
```
## 安装上传工具
```
python -m pip install --user --upgrade twine
```
## 上传（默认上传到pypi，需要登录）
```
python m twine upload dist/*
```
# 安装
```
pip install seagull2_generate_config_template
```
