from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='kkssh',
    version='0.11',
    description='ssh client',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author='xingkun',
    author_email='xingkunliu@qq.com',
    url='https://github.com/Beim/kkssh',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='ssh client',
    install_requires=[
        'paramiko',
    ],
    entry_points={
        'console_scripts': [
            'kkssh = kkssh.main:main'
        ]
    },
)
