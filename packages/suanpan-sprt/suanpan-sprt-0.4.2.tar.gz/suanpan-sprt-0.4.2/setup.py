from setuptools import setup
import pathlib
import os


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

package_root = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(package_root, "sprt", "version.py")) as fp:
    exec(fp.read(), version)
version = version["__version__"]

with open(os.path.join(package_root, "requirements.txt")) as fp:
    requires = fp.readlines()

setup(
    name='suanpan-sprt',
    packages=['sprt'],
    version=version,
    description='A framework for invoking functions over HTTP',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Guangyuan Lu',
    author_email='mocheng.lgy@xuelangyun.com',
    url='https://gitlab-sp.xuelangyun.com/xuelang-group/suanpan-functional-python',
    keywords=['suanpan', 'faas', 'functions'],

    install_requires=requires,
    python_requires=">=3.7",
    classifiers=[],
    entry_points={
      "console_scripts": [
        "sprt=sprt.__main__:main",
      ]
    },
)
