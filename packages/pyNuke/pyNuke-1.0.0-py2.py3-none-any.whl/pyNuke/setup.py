from setuptools import setup

setup(
    name='pyNuke',
    version='1.0.0',    
    description='A Discord Nuke. Meant to be used with good intent for testing purposes.',
    author='Tiago Coelho',
    author_email='melaochapanao@gmail.com',
    license='The Unlicense',
    packages=['pyNuke'],
    install_requires=['discord.py'],

    classifiers=["Development Status :: 4 - Beta", 'Intended Audience :: Developers', "Programming Language :: Python",    "Programming Language :: Python :: 3",    "Programming Language :: Python :: 3.6",    "Programming Language :: Python :: 3.7",    "Programming Language :: Python :: 3.8", 'Programming Language :: Python :: 3.9'],
)