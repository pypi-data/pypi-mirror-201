from setuptools import setup, find_packages
version_fn = 'src/ddd_struct/version.py'
with open(version_fn, 'r') as f:
    verstr = f.read()
version = verstr.split('=')[1]
version = version.replace("'", "").strip()


setup(
    name="ddd-struct",
    version=version,
    author="wangziling100",
    author_email="wangziling100@163.com",
    description="Data structures",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=['retry2', 'ddd-interface'],
)