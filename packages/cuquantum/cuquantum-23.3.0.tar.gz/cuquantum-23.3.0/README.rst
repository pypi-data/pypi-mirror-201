**************************************************************************************
cuQuantum SDK: A High-Performance Library for Accelerating Quantum Information Science
**************************************************************************************

`NVIDIA cuQuantum SDK <https://developer.nvidia.com/cuquantum-sdk>`_ is a high-performance library for quantum information science and beyond.
Currently its primary target is *quantum circuit simulations* and it consists of two major components:

* cuStateVec: a high-performance library for state vector computations
* cuTensorNet: a high-performance library for tensor network computations

In addition to C APIs, cuQuantum also provides Python APIs via `cuQuantum Python`_.

.. _cuQuantum Python: https://pypi.org/project/cuquantum-python/

Documentation
=============

Please refer to https://docs.nvidia.com/cuda/cuquantum/index.html for the cuQuantum documentation.

Installation
============

.. code-block:: bash

   pip install -v cuquantum

.. note::

   Starting cuQuantum 22.11, this package is a meta package pointing to ``cuquantum-cuXX``,
   where XX is the CUDA major version (currently CUDA 11 & 12 are supported).
   The meta package will attempt to infer and install the correct ``-cuXX`` wheel. However,
   in situations where the auto-detection fails, this package currently points to ``cuquantum-cu11``
   with a warning raised (if the verbosity flag ``-v`` is set, as shown above). This behavior
   is subject to change in the future, and users are encouraged to install the new wheels that
   come *with* the ``-cuXX`` suffix.

.. note::

   To use cuQuantum's Python APIs, please directly install `cuQuantum Python`_.

Citing cuQuantum
================

Pleae click this Zenodo badge to see the citation format: |DOI|

.. |DOI| image:: https://zenodo.org/badge/435003852.svg
    :target: https://zenodo.org/badge/latestdoi/435003852
