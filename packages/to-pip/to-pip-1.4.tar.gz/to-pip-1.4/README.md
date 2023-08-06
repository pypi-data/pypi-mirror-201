# To-pip

`to-pip` is a command line tool that helps you create Python packages from your Python files and upload them to PyPI with ease.

## Installation

To install `to-pip`, use the following command:

```bash
python -m pip install to-pip
```

## Usage

To use `to-pip`, simply run the following command:

```bash
python -m to_pip -n <package_name> -v <package_version> [-u <pypi_username> -p <pypi_password>] <python_files>
```

Where:
- `<package_name>` is the name of your package.
- `<package_version>` is the version of your package.
- `<pypi_username>` is your PyPI username (optional).
- `<pypi_password>` is your PyPI password (optional).
- `<python_files>` are the Python files you want to include in your package.

For example, if you have a file `hello.py` that you want to include in your package, you can run the following command:

```bash
python -m to_pip -n hello-world -v 0.1.0 hello.py
```

This will create a package called `hello-world` with version `0.1.0`, and containing the `hello.py` file.

If you have multiple Python files that you want to include in your package, you can specify them all as arguments:

```bash
python -m to_pip -n hello-world -v 0.1.0 hello.py world.py
```

By default, `to-pip` will create a console script for each Python file you include in your package. For example, if you include `hello.py` and `world.py`, `to-pip` will create two console scripts called `hello` and `world`. You can run these scripts from the command line once you install your package.

## Uploading to PyPI

If you want to upload your package to PyPI, you can provide your PyPI credentials using the `-u` and `-p` options:

```bash
python -m to_pip -n hello-world -v 0.1.0 -u <pypi_username> -p <pypi_password> hello.py
```

This will upload your package to PyPI once it is created.

## License

`to-pip` is distributed under the MIT License. See `LICENSE` for more information.