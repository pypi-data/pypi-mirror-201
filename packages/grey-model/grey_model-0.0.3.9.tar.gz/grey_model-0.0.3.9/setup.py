from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.0.3.9'
DESCRIPTION = '灰色系统包，目前只有一个功能，未来会有很多！'
LONG_DESCRIPTION = '我需要很长的时间去完善，目前只是一个占位，将在未来完善，也许是一年以后啦~，现在我要带上耳机，数学分析'

# Setting up
setup(
    include_package_data=True,
    name="grey_model",
    version=VERSION,
    author="Yiming Zeng",
    author_email="romtance@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['statsmodels',
                      'matplotlib',
                      'pandas',
                      'numpy',
                      'pmdarima'],
    keywords=['python','grey model','prediction'],
    url='http://math.halashuo.cn/',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)