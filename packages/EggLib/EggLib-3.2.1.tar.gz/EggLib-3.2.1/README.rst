=====================================
EggLib documentation!
=====================================

.. image:: ./doc/logo/banner.png
   :target: https://egglib.org
   :alt: EggLib Logo

|PythonVersions| |PypiPackage|

.. contents:: Table of Contents
   :depth: 3


About
=====

EggLib is a Python library, largely implemented in C++, for evolutionary
genetics and genomics. Main features are sequence data management,
sequence polymorphism analysis, and coalescent simulations. EggLib is a
flexible Python module with a performant underlying C++ library and
allows fast and intuitive development of Python programs and scripts.

**EggLib home page:** `<https://www.egglib.org>`_


Installation
============

EggLib is available on pip. For more information on installing EggLib or
downloading source code please refer to the installation section of the
documentation: `<https://egglib.org/install.html>`_.

Cloning
=======

You can clone the whole package using::

    git clone https://gitlab.com/demita/egglib.githttps://doi.org/10.1111/1755-0998.13672

For example, this lets you access to the current version on development::

    cd egglib
    git checkout dev

Building local documentation
============================

To generate the documentation locally, you should clone the repository,
and run this (assuming the package has been installed)::

    python setup.py build_sphinx
    python setup.py build_pdf

The first command generates the html documentation (available in the
``doc/build/html`` directory) and the second generates three pdf
documents containing the main sections of the documentation (in the
``doc/build/latex`` directory).

To generate documentation, one needs:

* A LaTex processor, containing the following packages: anyfontsize,
  amsmath, fncychap, capt-of, needspace, framed, upquote, wrapfig (and
  possibly others).
* ``python3-sphinx``
* ``python3-svgwrite``
* ``latexmk``

Citation
========

Siol M., T. Coudoux, S. Ravel and S. De Mita. 2022. EggLib 3: A python package for population genetics and genomics.
*Mol Ecol. Res.* **22**:3176-3187. `<https://doi.org/10.1111/1755-0998.13672>`_

De Mita S. and M. Siol. 2012. EggLib: processing, analysis and simulation tools for population genetics and genomics.
*BMC Genet.* **13**:27. `Open access <http://www.biomedcentral.com/1471-2156/13/27/abstract>`_

License
=======

EggLib is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.

EggLib is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

`<https://www.egglib.org/licence.html>`_

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-blue.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+

.. |PypiPackage| image:: https://badge.fury.io/py/EggLib.svg
   :target: https://pypi.org/project/EggLib
   :alt: PyPi package
