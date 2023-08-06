from setuptools import find_packages, setup
setup(
    name='webexpython',
    packages=find_packages(include=['webexpython']),
    version='0.2.15',
    description='Python tools for Cisco Webex',
    author='Josh Kittle - josh.kittle@gmail.com',
    license='MIT',
    install_requires=['requests'],
    setup_requires=[],
)
