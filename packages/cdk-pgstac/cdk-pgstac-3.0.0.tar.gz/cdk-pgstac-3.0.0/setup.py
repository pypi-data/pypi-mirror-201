import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-pgstac",
    "version": "3.0.0",
    "description": "A set of constructs deploying pgSTAC with CDK",
    "license": "ISC",
    "url": "https://github.com/developmentseed/cdk-pgstac.git",
    "long_description_content_type": "text/markdown",
    "author": "Anthony Lukach<anthony@developmentseed.org>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/developmentseed/cdk-pgstac.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_pgstac",
        "cdk_pgstac._jsii"
    ],
    "package_data": {
        "cdk_pgstac._jsii": [
            "cdk-pgstac@3.0.0.jsii.tgz"
        ],
        "cdk_pgstac": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.46.0, <3.0.0",
        "aws-cdk.aws-apigatewayv2-integrations-alpha>=2.47.0.a0, <3.0.0",
        "aws-cdk.aws-lambda-python-alpha>=2.47.0.a0, <3.0.0",
        "constructs>=10.1.113, <11.0.0",
        "jsii>=1.69.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
