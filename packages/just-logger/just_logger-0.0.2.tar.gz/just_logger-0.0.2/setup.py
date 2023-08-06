from setuptools import setup
    
    
def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name='just_logger', # 项目名称
    version='0.0.2', # 版本
    author='Baoming Yu', # 作者
    author_email='dingxuanliang@icloud.com', # 联系邮箱
    url='https://github.com/Baoming520/just-logger', # 项目url
    description='A logging tool is used to record all kinds of logs during program running.', # 简单描述
    long_description=readme(), # 长描述
    long_description_content_type="text/markdown", # 长描述格式
    packages=['just_logger'], # 要打包的package
    package_data={}, # 要包含的数据文件
    install_requires=[], # 本库依赖的库
)