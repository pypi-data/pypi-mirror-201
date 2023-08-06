from setuptools import setup, find_packages

setup(
    name='simplerabbit',
    version='1.0.0',
    author='Phuong Do',
    author_email='phdo@energidanmark.dk',
    description='A Python library for sending and receiving messages using RabbitMQ',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pika==1.3.1',
    ],
)

