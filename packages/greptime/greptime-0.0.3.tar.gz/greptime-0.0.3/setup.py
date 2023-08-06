import setuptools

long_desc = open("README.md").read()
required = ["numpy"] # Comma seperated dependent libraries name

setuptools.setup(
    name="greptime",
    version="0.0.3",
    author="discord9",
    author_email="zglzy29yzdk@gmail.com",
    license="Apache License 2.0",
    description="A mock test library for greptimedb's scripting feature",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/GreptimeTeam/greptime_py_mock",
    # project_urls is optional
    project_urls={
        "Bug Tracker": "https://github.com/GreptimeTeam/greptime_py_mock/issues",
    },
    key_words="greptime",
    install_requires=required,
    packages=["greptime"],
    python_requires=">=3.6",
)
# build:
# python -m build
# upload to testpypi
# python -m twine upload --repository testpypi dist/*
# upload to pypi
# python -m twine upload dist/*