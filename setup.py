"""
Muffin-Classy
-------------

Class based views for Muffin
"""
from setuptools import setup

setup(
    name='Muffin-Classy',
    version='0.0.0-0',
    url='https://github.com/ei-grad/muffin-classy',
    license='BSD',
    author='Andrew Grigorev',
    author_email='andrew@ei-grad.ru',
    description='Class based views for Muffin',
    long_description=__doc__,
    py_modules=['muffin_classy'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'aiohttp'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests'
)
