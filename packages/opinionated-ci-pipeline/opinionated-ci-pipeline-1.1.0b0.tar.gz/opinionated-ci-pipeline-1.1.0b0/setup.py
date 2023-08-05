import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "opinionated-ci-pipeline",
    "version": "1.1.0.b0",
    "description": "CI/CD on AWS with feature-branch builds, developer-environment deployments, and build status notifications.",
    "license": "MIT",
    "url": "https://github.com/merapar/opinionated-ci-pipeline.git",
    "long_description_content_type": "text/markdown",
    "author": "Maciej Radzikowski<maciej.radzikowski@merapar.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/merapar/opinionated-ci-pipeline.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "opinionated_ci_pipeline",
        "opinionated_ci_pipeline._jsii"
    ],
    "package_data": {
        "opinionated_ci_pipeline._jsii": [
            "opinionated-ci-pipeline@1.1.0-beta.0.jsii.tgz"
        ],
        "opinionated_ci_pipeline": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.63.0, <3.0.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.75.0, <2.0.0",
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
