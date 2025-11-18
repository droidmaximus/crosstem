Languages
=========

Language-specific details and coverage information.

Supported Languages
-------------------

Crosstem currently supports 15 languages with full derivational morphology data.

European Languages
~~~~~~~~~~~~~~~~~~

English (eng)
^^^^^^^^^^^^^

* **Coverage**: ~150,000 words
* **Productivity**: High (rich derivational morphology)
* **Thresholds**: Verbs ≥5, Nouns ≥9
* **Notes**: Best coverage, most extensively tested

German (deu)
^^^^^^^^^^^^

* **Coverage**: ~120,000 words
* **Productivity**: Moderate (compound-heavy)
* **Thresholds**: Verbs ≥4, Nouns ≥3
* **Notes**: Handles compound words well

French (fra)
^^^^^^^^^^^^

* **Coverage**: ~90,000 words
* **Productivity**: Moderate
* **Thresholds**: Verbs ≥4, Nouns ≥5
* **Notes**: Romance language patterns

Italian (ita)
^^^^^^^^^^^^^

* **Coverage**: ~80,000 words
* **Productivity**: Moderate
* **Thresholds**: Verbs ≥4, Nouns ≥5
* **Notes**: Similar to French

Spanish (spa)
^^^^^^^^^^^^^

* **Coverage**: ~85,000 words
* **Productivity**: Moderate-Low
* **Thresholds**: Verbs ≥3, Nouns ≥4
* **Notes**: Romance language, extensive verbal system

Portuguese (por)
^^^^^^^^^^^^^^^^

* **Coverage**: ~70,000 words
* **Productivity**: Moderate-Low
* **Thresholds**: Verbs ≥3, Nouns ≥4
* **Notes**: Similar to Spanish

Catalan (cat)
^^^^^^^^^^^^^

* **Coverage**: ~50,000 words
* **Productivity**: Moderate
* **Thresholds**: Verbs ≥3, Nouns ≥4
* **Notes**: Romance language spoken in Catalonia

Swedish (swe)
^^^^^^^^^^^^^

* **Coverage**: ~65,000 words
* **Productivity**: Moderate
* **Thresholds**: Verbs ≥3, Nouns ≥4
* **Notes**: North Germanic language

Slavic Languages
~~~~~~~~~~~~~~~~

Russian (rus)
^^^^^^^^^^^^^

* **Coverage**: ~100,000 words
* **Productivity**: Low (inflection-heavy)
* **Thresholds**: Verbs ≥3, Nouns ≥2
* **Notes**: Rich inflectional system, less derivation

Polish (pol)
^^^^^^^^^^^^

* **Coverage**: ~55,000 words
* **Productivity**: Low
* **Thresholds**: Verbs ≥3, Nouns ≥3
* **Notes**: Complex inflectional morphology

Czech (ces)
^^^^^^^^^^^

* **Coverage**: ~40,000 words
* **Productivity**: Low
* **Thresholds**: Verbs ≥3, Nouns ≥3
* **Notes**: West Slavic language

Serbo-Croatian (hbs)
^^^^^^^^^^^^^^^^^^^^

* **Coverage**: ~35,000 words
* **Productivity**: Low
* **Thresholds**: Verbs ≥2, Nouns ≥2
* **Notes**: South Slavic language

Other Languages
~~~~~~~~~~~~~~~

Finnish (fin)
^^^^^^^^^^^^^

* **Coverage**: ~60,000 words
* **Productivity**: Moderate
* **Thresholds**: Verbs ≥3, Nouns ≥4
* **Notes**: Finno-Ugric language, agglutinative

Hungarian (hun)
^^^^^^^^^^^^^^^

* **Coverage**: ~45,000 words
* **Productivity**: Moderate
* **Thresholds**: Verbs ≥3, Nouns ≥3
* **Notes**: Finno-Ugric language, agglutinative

Mongolian (mon)
^^^^^^^^^^^^^^^

* **Coverage**: ~25,000 words
* **Productivity**: Moderate-Low
* **Thresholds**: Verbs ≥2, Nouns ≥2
* **Notes**: Mongolic language

Language Codes
--------------

Crossstem uses ISO 639-3 language codes:

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Code
     - Language
     - Example Usage
   * - cat
     - Catalan
     - ``DerivationalStemmer('cat')``
   * - ces
     - Czech
     - ``DerivationalStemmer('ces')``
   * - deu
     - German
     - ``DerivationalStemmer('deu')``
   * - eng
     - English
     - ``DerivationalStemmer('eng')``
   * - fin
     - Finnish
     - ``DerivationalStemmer('fin')``
   * - fra
     - French
     - ``DerivationalStemmer('fra')``
   * - hbs
     - Serbo-Croatian
     - ``DerivationalStemmer('hbs')``
   * - hun
     - Hungarian
     - ``DerivationalStemmer('hun')``
   * - ita
     - Italian
     - ``DerivationalStemmer('ita')``
   * - mon
     - Mongolian
     - ``DerivationalStemmer('mon')``
   * - pol
     - Polish
     - ``DerivationalStemmer('pol')``
   * - por
     - Portuguese
     - ``DerivationalStemmer('por')``
   * - rus
     - Russian
     - ``DerivationalStemmer('rus')``
   * - spa
     - Spanish
     - ``DerivationalStemmer('spa')``
   * - swe
     - Swedish
     - ``DerivationalStemmer('swe')``

Productivity Thresholds
-----------------------

Each language has calibrated thresholds for filtering candidates:

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Language
     - Verbs
     - Nouns
     - Rationale
   * - English
     - ≥5
     - ≥9
     - Rich derivational morphology
   * - German
     - ≥4
     - ≥3
     - Compound-heavy language
   * - French
     - ≥4
     - ≥5
     - Romance language patterns
   * - Italian
     - ≥4
     - ≥5
     - Similar to French
   * - Spanish
     - ≥3
     - ≥4
     - Lower productivity
   * - Portuguese
     - ≥3
     - ≥4
     - Similar to Spanish
   * - Russian
     - ≥3
     - ≥2
     - Inflection-heavy
   * - Polish
     - ≥3
     - ≥3
     - Slavic patterns
   * - Czech
     - ≥3
     - ≥3
     - Similar to Polish
   * - Finnish
     - ≥3
     - ≥4
     - Agglutinative morphology
   * - Hungarian
     - ≥3
     - ≥3
     - Agglutinative morphology
   * - Others
     - ≥2-3
     - ≥2-4
     - Conservative thresholds

Language-Specific Examples
---------------------------

English
~~~~~~~

::

   from crosstem import DerivationalStemmer
   
   stemmer = DerivationalStemmer('eng')
   
   # Noun → Verb
   print(stemmer.stem('organization'))    # organize
   print(stemmer.stem('destruction'))     # destruct
   
   # Adjective → Noun
   print(stemmer.stem('beautiful'))       # beauty
   print(stemmer.stem('happiness'))       # happy

German
~~~~~~

::

   stemmer = DerivationalStemmer('deu')
   
   print(stemmer.stem('Organisation'))    # organisieren
   print(stemmer.stem('Organisierung'))   # organisieren
   print(stemmer.stem('Schönheit'))       # schön

French
~~~~~~

::

   stemmer = DerivationalStemmer('fra')
   
   print(stemmer.stem('organisation'))    # organiser
   print(stemmer.stem('organisateur'))    # organiser
   print(stemmer.stem('beauté'))          # beau

Spanish
~~~~~~~

::

   stemmer = DerivationalStemmer('spa')
   
   print(stemmer.stem('organización'))    # organizar
   print(stemmer.stem('organizador'))     # organizar
   print(stemmer.stem('belleza'))         # bello

Russian
~~~~~~~

::

   stemmer = DerivationalStemmer('rus')
   
   print(stemmer.stem('организация'))     # организовать
   print(stemmer.stem('красота'))         # красивый

Data Sources
------------

Language data comes from:

1. **MorphyNet v1.0**: Derivational morphology
   
   * Source: https://morphynet.org/
   * License: CC BY-SA 4.0
   * Coverage: 15 languages

2. **UniMorph**: Inflectional morphology
   
   * Source: https://unimorph.github.io/
   * License: CC BY-SA 3.0
   * Coverage: Subset of supported languages

3. **Wiktionary**: Etymology relationships
   
   * Source: Wiktionary dumps
   * License: CC BY-SA 3.0
   * Coverage: 2,265 languages

Future Languages
----------------

Potential additions (dependent on data availability):

* Arabic
* Chinese (Mandarin)
* Japanese
* Korean
* Hindi
* Turkish
* Dutch
* Norwegian
* Danish

To request language support, please open an issue on GitHub.

Language Limitations
--------------------

Coverage Gaps
~~~~~~~~~~~~~

* **Domain jargon**: Technical/medical terms may be missing
* **Neologisms**: New words not in training data
* **Slang**: Informal language not well-represented
* **Archaic terms**: Historical words may have incomplete data

Morphological Patterns
~~~~~~~~~~~~~~~~~~~~~~

* **Compounds**: Some compound words may not decompose correctly
* **Irregular forms**: Irregular derivations may be missing
* **Borrowed words**: Recently borrowed words may lack derivational data
* **Regional variants**: Dialect-specific forms may not be included

Performance Variations
~~~~~~~~~~~~~~~~~~~~~~

* **English**: Best tested, highest quality
* **Major European**: Well-tested, good quality
* **Slavic**: Good coverage, lower productivity requires tuning
* **Other**: Adequate coverage, less extensively tested

Contributing Languages
----------------------

To add a new language:

1. Obtain derivational morphology data
2. Format as MorphyNet-compatible JSON
3. Calibrate productivity thresholds
4. Add test cases
5. Submit pull request

See :doc:`contributing` for detailed guidelines.
