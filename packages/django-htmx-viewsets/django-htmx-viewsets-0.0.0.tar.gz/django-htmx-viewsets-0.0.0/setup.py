#!/usr/bin/env python
import sys
from setuptools import find_packages, setup
#from src.django_htmx_viewsets import __version__


install_requires = [
    'django>=3.2,<5.0',
    'django-htmx>=1.0.0,<2.0.0',
    #tests:
]


tests_require = [
    *install_requires,
    'django-debug-toolbar>=3.8.0',
    'django-extensions>=3.2.0',
    'psycopg2-binary>=2.9.0',
    'Werkzeug>=2.2.0',
]


setup(
    name='django-htmx-viewsets',
    #version=__version__,
    author="Snake-Soft",
    author_email="info@snake-soft.com",
    description="Viewsets for Django using HTMX, Chartjs and DataTables",
    long_description=open('README.md').read(),
    license='GPL3',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
)
