from setuptools import find_packages, setup

setup(
    name='cgdb_client',
    packages=find_packages(include=["cgdb", "cgdb.exceptions", "cgdb.managers", "cgdb.resources", "cgdb.utils"]),
    version='0.5.2',
    install_requires=["pandas==1.1.5", "requests==2.27.0"],
    description='CGDB Client',
    author='CzechGlobe',
    author_email='it@czechglobe.cz',
    license='MIT',
)
