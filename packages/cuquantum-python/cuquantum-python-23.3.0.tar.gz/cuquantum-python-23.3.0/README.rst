***********************
NVIDIA cuQuantum Python
***********************

NVIDIA cuQuantum Python provides Python bindings and high-level object-oriented models for accessing the full functionalities of NVIDIA cuQuantum SDK from Python.

Installation
============

.. code-block:: bash

   pip install -v cuquantum-python

.. note::

   Starting cuQuantum 22.11, this package is a meta package pointing to ``cuquantum-python-cuXX``,
   where XX is the CUDA major version (currently CUDA 11 & 12 are supported).
   The meta package will attempt to infer and install the correct ``-cuXX`` wheel. However,
   in situations where the auto-detection fails, this package currently points to ``cuquantum-python-cu11``
   with a warning raised (if the verbosity flag ``-v`` is set, as shown above). This behavior
   is subject to change in the future, and users are encouraged to install the new wheels that
   come *with* the ``-cuXX`` suffix.

Citing cuQuantum
================

Pleae click this Zenodo badge to see the citation format: |DOI|

.. |DOI| image:: https://zenodo.org/badge/435003852.svg
    :target: https://zenodo.org/badge/latestdoi/435003852
