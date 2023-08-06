from setuptools import setup, find_packages

setup(
    name='nate_indi',
    version='0.1',
    description='A Python package for making API requests',
    url='https://github.com/my-username/my-package',
    author='My Name',
    author_email='myemail@example.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pandas_ta'],
    entry_points={"console_scripts": ["test=nate_indi.macd:macdResult"]}

)



