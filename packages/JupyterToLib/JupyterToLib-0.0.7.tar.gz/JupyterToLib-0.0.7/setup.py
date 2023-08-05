from setuptools import setup, find_packages

setup(
    name='JupyterToLib',
    version='0.0.7',
    packages=find_packages(),
    license='MIT',
    author='Jose Carlos Del Valle',
    author_email='jcvsl94@gmail.com',
    description='A Python package that transforms your Jupyter notebooks into Python modules and optimizes your scripts by removing comments and empty lines.',
    long_description='JupyterToLib is a Python library that enables you to easily transform your Jupyter notebooks into fully-functional Python modules. With this tool, you can take your data science code to the next level by transforming your notebooks into modules that can be easily imported and reused in other projects. Moreover, the script optimization feature of JupyterToLib allows you to remove unnecessary comments and empty lines, reducing the size of your code and improving its readability and maintainability. With JupyterToLib, you can breathe life into your data science projects and simplify your workflow quickly and easily.',
    long_description_content_type='text/markdown',
    url='https://github.com/jcval94/JupyterToLib.git',
    install_requires=[
        'nbformat>=5.1.3',
    ],
)
