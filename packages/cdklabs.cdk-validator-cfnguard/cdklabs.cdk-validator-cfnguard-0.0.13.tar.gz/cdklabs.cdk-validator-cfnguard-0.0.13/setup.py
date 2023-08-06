import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdklabs.cdk-validator-cfnguard",
    "version": "0.0.13",
    "description": "@cdklabs/cdk-validator-cfnguard",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/cdk-validator-cfnguard.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-validator-cfnguard.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdklabs.cdk_validator_cfnguard",
        "cdklabs.cdk_validator_cfnguard._jsii"
    ],
    "package_data": {
        "cdklabs.cdk_validator_cfnguard._jsii": [
            "cdk-validator-cfnguard@0.0.13.jsii.tgz"
        ],
        "cdklabs.cdk_validator_cfnguard": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.71.0, <3.0.0",
        "jsii>=1.80.0, <2.0.0",
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
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
