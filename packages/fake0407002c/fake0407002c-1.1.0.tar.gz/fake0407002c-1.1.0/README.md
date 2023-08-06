# to-pip

`to-pip` is a tool that makes it easy to convert a set of Python files into a Python package that can be uploaded to PyPI. It can also upload the package to PyPI for you, if you provide your PyPI credentials. 

## Usage

### Web Interface

Github:
[https://github.com/bohachu/to_pip](https://github.com/bohachu/to_pip)

Web interface:
[http://to-pip.falra.net](http://to-pip.falra.net)

You can use the web interface of `to-pip` [here](https://to-pip-jqvkl3xr3a-uc.a.run.app). Simply upload your Python files, enter your package name and version, and click "Create Package". If you provide your PyPI credentials, you can also choose to upload the package to PyPI directly from the web interface.

### Command Line Interface

You can also use the `to-pip` command-line tool to create a package from your Python files. To use it, simply install the `to-pip` package using pip:

```
pip install to-pip
```

Then, run the `to-pip` command with the following arguments:

```
python -m to_pip -n <package_name> -v <package_version> [-u <pypi_username> -p <pypi_password>] <python_files>
```

Here is what each argument means:

- `-n` or `--package_name`: The name of your package.
- `-v` or `--package_version`: The version of your package in `x.x.x` format.
- `-u` or `--pypi_username` (optional): Your PyPI username. If you provide this, `to-pip` will upload your package to PyPI for you.
- `-p` or `--pypi_password` (optional): Your PyPI password. If you provide this, `to-pip` will upload your package to PyPI for you.
- `<python_files>`: The Python files that you want to include in your package.

### Package Usage

Once you have created your package, you can install it using pip:

```
pip install <package_name>
```

After installing the package, you can use any functions or classes defined in your Python files as normal. 

### Example

Let's say you have two Python files, `hello.py` and `world.py`, that you want to package into a package called `helloworld` with version `1.0.0`. Here's how you would use `to-pip` to create the package:

```
python -m to_pip -n helloworld -v 1.0.0 hello.py world.py
```
