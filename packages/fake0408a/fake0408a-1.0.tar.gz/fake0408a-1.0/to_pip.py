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


def create_package_dir(package_name, package_version, python_files):
    tmp_dir = tempfile.mkdtemp()
    package_dir = os.path.join(tmp_dir, f"{package_name}-{package_version}")
    os.makedirs(package_dir)

    for file in python_files:
        file_name = os.path.basename(file)
        if os.path.exists(os.path.join(package_dir, file_name)):
            print(f"Error: File {file_name} already exists in the package directory.")
            sys.exit(1)
        with open(file) as src, open(os.path.join(package_dir, file_name), "w") as dest:
            dest.write("#!/usr/bin/env python\n")
            dest.write(src.read())
        os.system(f"chmod +x {os.path.join(package_dir, os.path.basename(file))}")

    if os.path.exists("requirements.txt"):
        shutil.copy("requirements.txt", os.path.join(package_dir, "requirements.txt"))

    return package_dir


def write_setup_py(package_dir, package_name, package_version, python_files):
    modules = ", ".join([f"'{os.path.basename(file).split('.')[0].replace('-', '_')}'" for file in python_files])
    entry_points = ", ".join(
        [
            f"{os.path.basename(file).split('.')[0].replace('-', '_')} = {os.path.basename(file).split('.')[0].replace('-', '_')}:main"
            for file in python_files
        ]
    )

    setup_py = f"""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="{package_name}",
    version="{package_version}",
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


def handle_readme(package_dir, package_name):
    if os.path.exists("README.md"):
        shutil.copy("README.md", os.path.join(package_dir, "README.md"))
    else:
        with open(os.path.join(package_dir, "README.md"), "w") as f:
            f.write(f"# {package_name}\n\nThis is a placeholder README.md file.")


def create_pypirc_file(pypi_username, pypi_password):
    pypirc_content = f"""
[distutils]
index-servers =
  pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: {pypi_username}
password: {pypi_password}
"""
    with open(os.path.expanduser("~/.pypirc"), "w") as f:
        f.write(pypirc_content)


def to_pip(python_files, package_name, package_version, pypi_username=None, pypi_password=None):
    if not python_files:
        usage()

    package_dir = create_package_dir(package_name, package_version, python_files)
    write_setup_py(package_dir, package_name, package_version, python_files)
    handle_readme(package_dir, package_name)

    if pypi_username and pypi_password:
        create_pypirc_file(pypi_username, pypi_password)

    # Build the package before uploading
    build_exit_code = os.system(f"cd {package_dir} && python setup.py sdist bdist_wheel")
    if build_exit_code != 0:
        print("Error: Failed to build the package.")
        sys.exit(1)
    exit_code = os.system(f"cd {package_dir} && twine upload --config-file ~/.pypirc dist/*")
    if exit_code != 0:
        print("Error: Failed to upload the package.")
        sys.exit(1)


def to_pip_args():
    args = parse_args()

    if not args.python_files:
        usage()

    to_pip(args.python_files, args.package_name, args.package_version, args.pypi_username, args.pypi_password)


def main():
    to_pip_args()


if __name__ == "__main__":
    main()
