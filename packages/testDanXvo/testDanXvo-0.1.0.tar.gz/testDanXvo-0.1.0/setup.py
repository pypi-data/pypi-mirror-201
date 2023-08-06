from setuptools import setup, find_packages

setup(
    name="testDanXvo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "my_script=my_package.my_script:main",
        ],
    },
)
