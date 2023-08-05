# JupyterToLib

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

JupyterToLib is a Python library that enables you to easily transform your Jupyter notebooks into fully-functional Python modules. With this tool, you can take your data science code to the next level by transforming your notebooks into modules that can be easily imported and reused in other projects. Moreover, the script optimization feature of JupyterToLib allows you to remove unnecessary comments and empty lines, reducing the size of your code and improving its readability and maintainability. With JupyterToLib, you can breathe life into your data science projects and simplify your workflow quickly and easily.

## Installation

You can install JupyterToLib using pip:

''' pip install JupyterToLib '''


## Usage

Here's an example of how to use JupyterToLib to convert a Jupyter notebook to a Python module:

```python
from JupyterToLib import jupyter_to_py

TR = jupyter_to_py.JupyterToLib()
TR.ProcessLib("path/to/your/notebook.ipynb", "path/to/output/module.py")
```

To optimize your Python scripts by removing comments and empty lines, you can use the remove_comments_and_empty_lines method:

```python
from JupyterToLib import jupyter_to_py

TR = jupyter_to_py.JupyterToLib()
TR.remove_comments_and_empty_lines("path/to/your/script.py")
```

## License
JupyterToLib is distributed under the MIT License, which means you are free to use it in your personal and commercial projects.

## Contributing
If you'd like to contribute to JupyterToLib, please feel free to submit a pull request or open an issue. We welcome contributions from the community and are always looking for ways to improve the library.

## Contact
If you have any questions or feedback, please don't hesitate to contact us at jcvsl94@gmail.com. We'd love to hear from you!
