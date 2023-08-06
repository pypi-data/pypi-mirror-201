from setuptools import setup, find_packages


setup(
    name='pypalert',
    version='1.3.0',
    license='MIT',
    author="sanlien",
    author_email='paul_chen@sanlien.com',
    description='A library can get Sanlien S303 modbus ',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='S303 modbus',

)
