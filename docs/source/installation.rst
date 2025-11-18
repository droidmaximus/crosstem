Installation
============

Requirements
------------

* Python 3.7 or higher
* No runtime dependencies

PyPI Installation
-----------------

The easiest way to install Crosstem is via pip::

   pip install crosstem

This installs the base package (~280 MB) with derivational and inflectional data for 15 languages.

Etymology Data (Optional)
--------------------------

The etymology dataset is ~1 GB and hosted separately on GitHub Releases. To download it::

   from crosstem import download_etymology
   download_etymology()

Or from the command line::

   python -m crosstem.download

This downloads etymology.json to the crosstem/data directory with a progress bar.

Check if Etymology is Installed
--------------------------------

::

   from crosstem import is_etymology_downloaded
   
   if is_etymology_downloaded():
       print("Etymology data is available")
   else:
       print("Etymology data not found")

Remove Etymology Data
---------------------

To free up disk space::

   from crosstem import remove_etymology
   remove_etymology()

Development Installation
------------------------

To install from source for development::

   git clone https://github.com/droidmaximus/crosstem.git
   cd crosstem
   pip install -e .

Verifying Installation
----------------------

Test your installation::

   python -c "from crosstem import DerivationalStemmer; print(DerivationalStemmer('eng').stem('organization'))"

Expected output: ``organize``
