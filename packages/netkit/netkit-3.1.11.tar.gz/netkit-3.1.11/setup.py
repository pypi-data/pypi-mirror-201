
from setuptools import setup, find_packages
setup(
    name='netkit',
    version='3.1.11',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=[],
    python_requires='>=3',
    scripts=[],
    url='https://github.com/dantezhu/netkit',
    license='MIT',
    author='dantezhu',
    author_email='zny2008@gmail.com',
    description='useful kit for network programming',
)
