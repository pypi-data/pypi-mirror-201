from setuptools import setup, find_namespace_packages

setup(
    name='lgvad',
    version='1.0.0',
    description='very helpful lottery',
    url='https://github.com/VadimTrubay/lgvad.git',
    author='Trubay_Vadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['colorama'],
    entry_points={'console_scripts': ['lgvad=lgvad.main:main']}
)