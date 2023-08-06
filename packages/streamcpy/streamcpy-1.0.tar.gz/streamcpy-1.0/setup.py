from setuptools import setup, Extension

module1 = Extension('streamcpy',
                    sources = ['streamcpy.c'])

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

classifier = """
License :: OSI Approved :: GPL License
Programming Language :: C
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development
Typing :: Typed
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

setup (name='streamcpy',
       version='1.0',
       author='littlebutt',
       author_email='luogan1996@icloud.com',
       license='GPL-3.0 license',
       description = "The Stream Api in Python",
       long_description=long_description,
       url='https://github.com/littlebutt/streamcpy',
       classifiers=classifier,
       ext_modules=[module1])