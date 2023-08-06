from setuptools import setup

setup(
    name='theheartbeat',
    version='0.1.0',
    description='A Python module for uploading files and folders to Amazon S3.',
    author='Shubham Kumar',
    author_email='shubham@ioanyt.com',
    packages=['heartbeat'],
    install_requires=['requests'],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
