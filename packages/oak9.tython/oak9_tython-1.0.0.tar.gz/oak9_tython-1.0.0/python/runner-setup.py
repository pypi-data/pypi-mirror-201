from setuptools import setup, find_packages

package_data = {}

for package in find_packages():
    package_data[package] = ["*.pyi"]

setup_args = dict(
    name='oak9.tython',
    version='0.0.1b',
    description='oak9 tython framework',
    license='Open Source',
    packages=find_packages(),
    package_data=package_data,
    author='oak9',
    author_email='oak9@oak9.io'
)

if __name__ == '__main__':
    setup(**setup_args)
