"""
Flask-Session
-------------

Flask-Session is an extension for Flask that adds support for
Server-side Session to your application.

Links
`````

* `development version
  <https://github.com/fengsp/flask-session/zipball/master#egg=Flask-dev>`_

"""
with open("README.md", "r") as fh:
    long_description = fh.read()

from setuptools import setup

setup(
    name='Flask-Session-Refresh-Option',
    version='0.1.2',
    url='https://github.com/luismigsantana/flask-session-not-refresh-option',
    license='BSD',
    author='Luis Miguel Santana',
    author_email='miguelsantanna.ms@gmail.com',
    long_description_content_type="text/markdown",
    description='Adds server-side session support to your Flask application',
    long_description=long_description,
    packages=['flask_session'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
        'cachelib'
    ],
    test_suite='test_session',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
