from setuptools import setup

setup(
    name='umedsmsclient',
    version='1.0.0',
    description='A Python client library for sending and scheduling sms messages via Fire Text Sms API',
    author='Hasitha Widanagamachchi',
    author_email='haztha@gmail.com',
    url='https://github.com/hasithaprageeth/umed-sms-client',
    packages=['umedsmsclient'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)