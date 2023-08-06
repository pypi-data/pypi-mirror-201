from setuptools import setup, find_packages
import importlib


def get_requirements():
    with open('requirements.txt', 'r') as f:
        ret = [line.strip() for line in f.readlines()]
        print("requirements:", ret)
    return ret


setup(
    name='zltk',
    # packages = ['zltk'], # this must be the same as the name above
    version='0.0.0',
    description='A collection of commonly used functions.',
    author='Zhili Cheng',
    url='https://github.com/chengzl18/zltk',
    author_email='chengzl22@mails.tsinghua.edu.cn',
    download_url='https://github.com/chengzl18/zltk/archive/master.zip',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=['tokenizer', 'Chinese'],
    python_requires=">=3.6.0",
    install_requires=get_requirements(),
    packages=find_packages(),
    package_data={'': ['*.yaml']}
)


required_list = []
for package in required_list:
    try:
        m = importlib.import_module(package)
    except ModuleNotFoundError:
        print("\n"+"="*30+"  WARNING  "+"="*30)
        print(f"{package} is not found on your environment, please install it manually.")
        print("We do not install it for you because the environment sometimes needs special care.")
