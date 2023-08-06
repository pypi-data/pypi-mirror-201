import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dvadmin-sms",
    version="1.0.1",
    author="DVAdmin",
    author_email="liqiang@django-vue-admin.com",
    description="一款适用于django-vue-admin基于阿里云、腾讯云、华为云等官方短信服务开发的短信发送插件，快速整合各端的短信服务插件。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/huge-dream/dvadmin-uniapp",
    packages=setuptools.find_packages(),
    python_requires='>=3.7, <4',
    install_requires=[
        "alibabacloud_dysmsapi20170525>=2.0.23",  # 阿里云
        "tencentcloud-sdk-python>=3.0.854",  # 腾讯云
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
