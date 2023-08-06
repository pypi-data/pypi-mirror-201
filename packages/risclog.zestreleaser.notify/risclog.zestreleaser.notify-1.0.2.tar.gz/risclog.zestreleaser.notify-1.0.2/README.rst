============================
risclog.zestreleaser.notify
============================

.. image:: https://github.com/risclog-solution/risclog.zestreleaser.notify/workflows/Test/badge.svg?branch=master
     :target: https://github.com/risclog-solution/risclog.zestreleaser.notify/actions?workflow=Test
     :alt: CI Status


.. image:: https://img.shields.io/pypi/v/risclog.zestreleaser.notify.svg
        :target: https://pypi.python.org/pypi/risclog.zestreleaser.notify


This package provides a plugin for zest.releaser that offers to notify about a
new release in a configured channel (actually only Keybase_ is supported).

.. _Keybase: https://keybase.io

To use, add a section to your ~/.pypirc like the following::

    [risclog.zestreleaser.notify]
    keybase = https://bots.keybase.io/webhookbot/<CHANNELID>


* Free software: MIT license


Features
--------

Run tests::

    $ ./pytest


Credits
-------

This package was created with Cookiecutter_ and the `risclog-solution/risclog-cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`risclog-solution/risclog-cookiecutter-pypackage`: https://github.com/risclog-solution/risclog-cookiecutter-pypackage


This package uses AppEnv_ for running tests inside this package.

.. _AppEnv: https://github.com/flyingcircusio/appenv
