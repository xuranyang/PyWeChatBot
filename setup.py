from setuptools import find_packages, setup

VERSION = '0.0.8'

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='PyWeChatBot',
    version=VERSION,
    author='xuranyang',
    author_email='xuranyang96@gmail.com',
    description='WeChatBot Send Message',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/xuranyang/PyWeChatBot',
    keywords=['wechat', 'bot', 'wechatbot', 'wechat bot'],
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    python_requires='>=3.7',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    package_data={'': ['*.csv', '*.txt', '.toml']},
    include_package_data=True,
)
