from setuptools import setup, find_namespace_packages

setup(
    name='vab',
    version='1.0.0',
    description='very helpful assistant bot',
    url='https://github.com/VadimTrubay/vab.git',
    author='Trubay_Vadim',
    author_email='vadnetvadnet@ukr.net',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['numexpr', 'colorama'],
    entry_points={'console_scripts': ['vab=vab.main:main']},
    package_data={'vab': ['vab/*.txt', 'vab/*.bin']}
)