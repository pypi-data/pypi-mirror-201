#!/usr/bin/env python
import argparse
import os
import shutil
import sys
import tempfile


def usage():
    print(
        f"Usage: python -m to_pip -n <package_name> -v <package_version> [-u <pypi_username> -p <pypi_password>] <python_files>"
    )
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--package_name", help="Package name", required=True)
    parser.add_argument("-v", "--package_version", help="Package version", required=True)
    parser.add_argument("-u", "--pypi_username", help="PyPI username", default="")
    parser.add_argument("-p", "--pypi_password", help="PyPI password", default="")
    parser.add_argument("python_files", nargs="*", help="Python files to include")
    return parser.parse_args()


def to_pip():
    args = parse_args()

    if not args.python_files:
        usage()

    tmp_dir = tempfile.mkdtemp()
    package_dir = os.path.join(tmp_dir, f"{args.package_name}-{args.package_version}")
    os.makedirs(package_dir)

    for file in args.python_files:
        with open(file) as src, open(
                os.path.join(package_dir, os.path.basename(file)), "w"
        ) as dest:
            dest.write("#!/usr/bin/env python\n")
            dest.write(src.read())
        os.system(f"chmod +x {os.path.join(package_dir, os.path.basename(file))}")

    if os.path.exists("requirements.txt"):
        shutil.copy("requirements.txt", os.path.join(package_dir, "requirements.txt"))

    modules = ", ".join([f"'{os.path.basename(file).split('.')[0].replace('-', '_')}'" for file in args.python_files])
    entry_points = ", ".join(
        [
            f"{os.path.basename(file).split('.')[0].replace('-', '_')} = {os.path.basename(file).split('.')[0].replace('-', '_')}:main"
            for file in args.python_files
        ]
    )

    setup_py = f"""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="{args.package_name}",
    version="{args.package_version}",
    packages=find_packages(),
    py_modules=[{modules}],
    install_requires=requirements,
    entry_points={{
        'console_scripts': [
            '{entry_points}',
        ],
    }},
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
"""

    with open(os.path.join(package_dir, "setup.py"), "w") as f:
        f.write(setup_py)

    if os.path.exists("README.md"):
        shutil.copy("README.md", os.path.join(package_dir, "README.md"))

    os.system(f"cd {package_dir} && python setup.py sdist bdist_wheel")

    if args.pypi_username and args.pipy_password:
        pypirc_content = f"""
[distutils]
index-servers =
  pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: {args.pipy_username}
password: {args.pipy_password}
"""
        with open(os.path.expanduser("~/.pypirc"), "w") as f:
            f.write(pypirc_content)

    os.system(f"cd {package_dir} && twine upload dist/*")


def main():
    to_pip()


if __name__ == "__main__":
    main()