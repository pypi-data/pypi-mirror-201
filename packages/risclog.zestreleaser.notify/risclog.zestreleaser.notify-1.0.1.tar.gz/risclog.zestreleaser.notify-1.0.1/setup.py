#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    author='riscLOG Solution GmbH',
    author_email='info@risclog.de',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: German',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='Notify about new release in keybase channel.',
    install_requires=[
        'pydantic[dotenv]',
        # Add your dependencies here
        'zest.releaser >= 5.0',
        'requests',
        'six'
    ],
    extras_require={
        'docs': [
            'Sphinx',
        ],
        'test': [
            'pytest-cache',
            'pytest-cov',
            'pytest-flake8',
            'pytest-rerunfailures',
            'pytest-sugar',
            'pytest',
            'coverage',
            # https://github.com/PyCQA/flake8/issues/1419#issuecomment-947243876
            'flake8<4',
            'mock',
            'requests',
        ],
    },
    entry_points={
        'zest.releaser.releaser.after': [
            'notify=risclog.zestreleaser.notify:notify',
        ]
    },
    license='MIT license',
    long_description=readme,
    include_package_data=True,
    keywords='risclog.zestreleaser.notify',
    name='risclog.zestreleaser.notify',
    packages=find_packages('src'),
    namespace_packages=['risclog', 'risclog.zestreleaser'],
    package_dir={'': 'src'},
    url='https://github.com/risclog-solution/risclog.zestreleaser.notify',
    version='1.0.1',
    zip_safe=False,
)
