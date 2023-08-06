from setuptools import setup

with open("readme.md","r",encoding="utf-8") as f:
    long_description=f.read()

setup(
    name='pandasrw',# 需要打包的名字,即本模块要发布的名字
    version='0.0.3',#版本
    description='A pandas IO library for efficiently load and dump excel、csv、pkl', # 简要描述
    py_modules=['pandasrw'],   #  需要打包的模块
    author='storm', # 作者名
    #long_description="pandasrw提升了pandas读写excel、csv、pickle文件的性能和易用性。https://github.com/stormtozero/pandasio",
    author_email='41915460@163.com',   # 作者邮件
    url='https://github.com/stormtozero/pandasrw', # 项目地址,一般是代码托管的网站
    requires=['pandas','polars','xlwings','chardet','xlsx2csv',"openpyxl"], # 依赖包,如果没有,可以不要
    license='MIT'
)

