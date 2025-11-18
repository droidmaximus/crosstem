Crosstem Documentation
======================

A comprehensive Python package for morphological analysis combining derivational stemming, inflectional analysis, and cross-lingual etymology.

.. image:: https://badge.fury.io/py/crosstem.svg
   :target: https://badge.fury.io/py/crosstem
   :alt: PyPI version

.. image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.7+

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

Why Crosstem?
-------------

**Crosstem finds true linguistic roots across part-of-speech boundaries,** which is something traditional stemmers and lemmatizers cannot do.

Quick Start
-----------

Installation::

   pip install crosstem

Basic Usage::

   from crosstem import DerivationalStemmer
   
   stemmer = DerivationalStemmer('eng')
   print(stemmer.stem('organization'))  # Output: organize
   print(stemmer.stem('beautiful'))     # Output: beauty

Key Features
------------

* **Cross-POS derivational stemming**: Only library that finds roots across parts of speech
* **Linguistic accuracy**: Uses MorphyNet morphological data, not brittle rules
* **6× faster than Porter**: Hash table lookups instead of regex rules
* **Etymology tracing**: 4.2M relationships across 2,265 languages
* **Word families**: Discover complete derivational networks
* **Pure Python**: Zero runtime dependencies
* **15 languages**: Multilingual morphology support

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   user_guide
   algorithm
   api
   languages
   examples
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
