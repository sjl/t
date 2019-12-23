try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='t',
    version='1.2.0',
    author='Steve Losh',
    author_email='steve@stevelosh.com',
    url='https://hg.sr.ht/~sjl/t',
    py_modules=['t'],
    entry_points={
        'console_scripts': [
            't = t:_main',
        ],
    },
)
