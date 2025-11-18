User Guide
==========

This guide covers detailed usage of Crosstem's features.

Derivational Stemming
---------------------

Basic Usage
~~~~~~~~~~~

::

   from crosstem import DerivationalStemmer
   
   stemmer = DerivationalStemmer('eng')
   root = stemmer.stem('organization')
   print(root)  # organize

The stemmer finds the morphological root by traversing derivational relationships in the linguistic graph.

Understanding Stems
~~~~~~~~~~~~~~~~~~~

Crosstem returns **linguistic roots**, not just prefix-stripped words:

::

   # Traditional stemmers
   Porter('organization')  → 'organ'      # WRONG (overstemming)
   Lancaster('organization') → 'org'      # WRONG (aggressive)
   
   # Lemmatizers
   WordNet('organization') → 'organization'  # Preserves POS boundary
   
   # Crosstem
   Crosstem('organization') → 'organize'  # TRUE ROOT (crosses POS)

Multi-Hop Derivations
~~~~~~~~~~~~~~~~~~~~~~

Some words require multiple steps to reach their root::

   from crosstem import DerivationalStemmer
   
   stemmer = DerivationalStemmer('eng')
   
   # 2-hop example
   print(stemmer.stem('organizational'))
   # organizational → organization → organize
   
   # 3-hop example  
   print(stemmer.stem('destructiveness'))
   # destructiveness → destructive → destruction → destruct

Batch Processing
~~~~~~~~~~~~~~~~

Process multiple words efficiently::

   words = [
       'organization', 'organizational', 'organize',
       'organizing', 'organizer', 'reorganize'
   ]
   
   stems = [stemmer.stem(word) for word in words]
   print(stems)
   # ['organize', 'organize', 'organize', 
   #  'organize', 'organize', 'organize']

Word Families
-------------

Get All Derivatives
~~~~~~~~~~~~~~~~~~~

Find all words derived from a root::

   stemmer = DerivationalStemmer('eng')
   
   family = stemmer.get_word_family('organize')
   print(f"Found {len(family)} related words")
   print(sorted(family))

Example output::

   Found 43 related words
   ['disorganization', 'disorganize', 'disorganized', 
    'organ', 'organic', 'organism', 'organization',
    'organizational', 'organize', 'organized', 
    'organizer', 'reorganization', 'reorganize', ...]

Use Cases
~~~~~~~~~

Word families are useful for:

* **Information retrieval**: Find all variants of a search term
* **Corpus analysis**: Group related terms together
* **Vocabulary learning**: Discover word relationships
* **Text normalization**: Standardize related forms

Inflectional Analysis
---------------------

Basic Usage
~~~~~~~~~~~

::

   from crosstem import InflectionAnalyzer
   
   analyzer = InflectionAnalyzer('eng')
   
   # Get all inflections of a word
   inflections = analyzer.get_inflections('run')
   print(inflections)
   # {'run', 'runs', 'running', 'ran'}

Difference from Stemming
~~~~~~~~~~~~~~~~~~~~~~~~~

* **Inflections**: Same word, different grammatical form (run/runs/ran)
* **Derivations**: Related words, different meaning (organize/organization)

Crosstem handles both::

   # Inflectional analysis
   analyzer.get_inflections('go')  → {'go', 'goes', 'going', 'went', 'gone'}
   
   # Derivational stemming
   stemmer.stem('going')  → 'go'
   stemmer.stem('organization')  → 'organize'  # different word!

Etymology Tracing
-----------------

Setup
~~~~~

First, download the etymology dataset::

   from crosstem import download_etymology, is_etymology_downloaded
   
   if not is_etymology_downloaded():
       download_etymology()

Basic Usage
~~~~~~~~~~~

::

   from crosstem import EtymologyLinker
   
   linker = EtymologyLinker()
   
   # Trace etymology of a word
   etymology = linker.get_etymology('English', 'organize')
   print(etymology)

Etymology Relationships
~~~~~~~~~~~~~~~~~~~~~~~

The etymology data includes several relationship types:

* **INHERITED_FROM**: Word inherited from ancestor language
* **BORROWED_FROM**: Word borrowed/loaned from another language
* **DERIVED_FROM**: Word derived from another word
* **ETYMOLOGICAL_ORIGIN_OF**: Inverse relationship

Cross-Lingual Queries
~~~~~~~~~~~~~~~~~~~~~

::

   linker = EtymologyLinker()
   
   # Find words borrowed into English from French
   french_loans = linker.get_borrowed_words('English', 'French')
   print(f"Found {len(french_loans)} French loanwords")

Multi-Language Support
----------------------

Supported Languages
~~~~~~~~~~~~~~~~~~~

Crosstem supports 15 languages with full derivational data:

+----------+------------------+---------+
| Code     | Language         | Words   |
+==========+==================+=========+
| cat      | Catalan          | ~50K    |
+----------+------------------+---------+
| ces      | Czech            | ~40K    |
+----------+------------------+---------+
| deu      | German           | ~120K   |
+----------+------------------+---------+
| eng      | English          | ~150K   |
+----------+------------------+---------+
| fin      | Finnish          | ~60K    |
+----------+------------------+---------+
| fra      | French           | ~90K    |
+----------+------------------+---------+
| hbs      | Serbo-Croatian   | ~35K    |
+----------+------------------+---------+
| hun      | Hungarian        | ~45K    |
+----------+------------------+---------+
| ita      | Italian          | ~80K    |
+----------+------------------+---------+
| mon      | Mongolian        | ~25K    |
+----------+------------------+---------+
| pol      | Polish           | ~55K    |
+----------+------------------+---------+
| por      | Portuguese       | ~70K    |
+----------+------------------+---------+
| rus      | Russian          | ~100K   |
+----------+------------------+---------+
| spa      | Spanish          | ~85K    |
+----------+------------------+---------+
| swe      | Swedish          | ~65K    |
+----------+------------------+---------+

Usage Example
~~~~~~~~~~~~~

::

   # German
   de_stemmer = DerivationalStemmer('deu')
   print(de_stemmer.stem('Organisierung'))  # organisieren
   
   # French  
   fr_stemmer = DerivationalStemmer('fra')
   print(fr_stemmer.stem('organisateur'))  # organiser
   
   # Spanish
   es_stemmer = DerivationalStemmer('spa')
   print(es_stemmer.stem('organizador'))  # organizar
   
   # Russian
   ru_stemmer = DerivationalStemmer('rus')
   print(ru_stemmer.stem('организация'))  # организовать

Language-Specific Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each language has calibrated productivity thresholds:

* **English**: High threshold (rich derivational morphology)
* **German**: Moderate (compound-heavy)
* **Russian**: Low threshold (inflection-heavy)

See :doc:`algorithm` for details on language-specific tuning.

Performance Tips
----------------

Memory Usage
~~~~~~~~~~~~

* Base package: ~280 MB (derivational data for 15 languages)
* Etymology data: ~1 GB (optional)
* In-memory graph: Loaded once per language

Speed Optimization
~~~~~~~~~~~~~~~~~~

::

   # ✓ GOOD: Reuse stemmer instance
   stemmer = DerivationalStemmer('eng')
   for word in large_corpus:
       stem = stemmer.stem(word)
   
   # ✗ BAD: Creating new instance each time
   for word in large_corpus:
       stemmer = DerivationalStemmer('eng')  # Reloads graph!
       stem = stemmer.stem(word)

Benchmark: ~547,000 words/second on modern hardware.

Error Handling
--------------

Unknown Words
~~~~~~~~~~~~~

If a word is not in the graph, it's returned unchanged::

   stemmer = DerivationalStemmer('eng')
   
   print(stemmer.stem('neologism123'))  # neologism123
   print(stemmer.stem('known_word'))    # <actual root>

Invalid Language
~~~~~~~~~~~~~~~~

::

   try:
       stemmer = DerivationalStemmer('invalid')
   except ValueError as e:
       print(f"Error: {e}")
       # Error: Language 'invalid' not supported

Missing Etymology Data
~~~~~~~~~~~~~~~~~~~~~~

::

   from crosstem import is_etymology_downloaded, download_etymology
   
   if not is_etymology_downloaded():
       print("Etymology data not found. Downloading...")
       download_etymology()

Best Practices
--------------

1. **Reuse instances**: Don't create new stemmers for each word
2. **Batch processing**: Process lists of words in one go
3. **Check language support**: Verify language code before initialization
4. **Download etymology once**: Check if data exists before downloading
5. **Handle unknown words**: Plan for words not in the corpus

Next Steps
----------

* See :doc:`examples` for real-world use cases
* Read :doc:`algorithm` to understand how it works
* Check :doc:`api` for complete method documentation
* Learn about :doc:`languages` for language-specific details
