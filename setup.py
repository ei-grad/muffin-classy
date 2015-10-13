"""
Muffin-Classy
-------------

Class based views for Muffin
"""
from setuptools import setup

setup(
    name='Muffin-Classy',
    version='0.7.0-dev0',
    url='https://github.com/apiguy/muffin-classy',
    license='BSD',
    author='Freedom Dumlao',
    author_email='freedomdumlao@gmail.com',
    description='Class based views for Muffin',
    long_description=__doc__,
    py_modules=['muffin_classy'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Muffin>=0.9'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test_classy'
)
