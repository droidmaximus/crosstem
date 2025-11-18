Quick Start
===========

This guide will get you started with Crosstem in 5 minutes.

Basic Stemming
--------------

::

   from crosstem import DerivationalStemmer
   
   # Initialize stemmer for English
   stemmer = DerivationalStemmer('eng')
   
   # Stem a single word
   print(stemmer.stem('organization'))  # Output: organize
   print(stemmer.stem('beautiful'))     # Output: beauty
   print(stemmer.stem('happiness'))     # Output: happy

Cross-POS Stemming
------------------

Unlike traditional stemmers, Crosstem finds roots across parts of speech::

   stemmer = DerivationalStemmer('eng')
   
   # Noun → Verb
   print(stemmer.stem('organization'))  # organize
   print(stemmer.stem('destruction'))   # destruct
   
   # Adjective → Noun
   print(stemmer.stem('beautiful'))     # beauty
   print(stemmer.stem('organizational')) # organize

Batch Processing
----------------

::

   words = ['organization', 'organizational', 'organize', 'organizing']
   stems = [stemmer.stem(word) for word in words]
   print(stems)  # ['organize', 'organize', 'organize', 'organize']

Word Families
-------------

Find all words derived from a root::

   stemmer = DerivationalStemmer('eng')
   family = stemmer.get_word_family('organize')
   print(f"Found {len(family)} related words")
   print(family[:10])  # First 10 words

Inflectional Analysis
---------------------

::

   from crosstem import InflectionAnalyzer
   
   analyzer = InflectionAnalyzer('eng')
   
   # Analyze word inflections
   inflections = analyzer.get_inflections('run')
   print(inflections)
   # Output: {'runs', 'running', 'ran'}

Etymology Tracing
-----------------

First, download the etymology data::

   from crosstem import download_etymology
   download_etymology()

Then trace word origins::

   from crosstem import EtymologyLinker
   
   linker = EtymologyLinker()
   
   # Find etymology
   etymology = linker.get_etymology('English', 'organize')
   print(etymology)

Multi-language Support
----------------------

Crosstem supports 15 languages::

   # German
   de_stemmer = DerivationalStemmer('deu')
   print(de_stemmer.stem('Organisation'))  # organisieren
   
   # French
   fr_stemmer = DerivationalStemmer('fra')
   print(fr_stemmer.stem('organisation'))  # organiser
   
   # Spanish
   es_stemmer = DerivationalStemmer('spa')
   print(es_stemmer.stem('organización'))  # organizar

Supported Languages
-------------------

* **cat** - Catalan
* **ces** - Czech
* **deu** - German
* **eng** - English
* **fin** - Finnish
* **fra** - French
* **hbs** - Serbo-Croatian
* **hun** - Hungarian
* **ita** - Italian
* **mon** - Mongolian
* **pol** - Polish
* **por** - Portuguese
* **rus** - Russian
* **spa** - Spanish
* **swe** - Swedish

Next Steps
----------

* Read the :doc:`user_guide` for detailed usage
* Learn about the :doc:`algorithm` behind Crosstem
* Check out :doc:`examples` for real-world use cases
* See the :doc:`api` reference for all available methods
