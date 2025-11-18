API Reference
=============

This page documents all public classes and methods in Crosstem.

DerivationalStemmer
-------------------

.. py:class:: DerivationalStemmer(language: str)

   Main class for finding morphological roots through derivational relationships.
   
   :param language: ISO 639-3 language code (e.g., 'eng', 'deu', 'fra')
   :type language: str
   :raises ValueError: If language is not supported
   
   **Example**::
   
      from crosstem import DerivationalStemmer
      
      stemmer = DerivationalStemmer('eng')
      root = stemmer.stem('organization')

   .. py:method:: stem(word: str) -> str
   
      Find the morphological root of a word using BFS graph traversal.
      
      :param word: The word to stem
      :type word: str
      :return: The morphological root, or the original word if not in graph
      :rtype: str
      
      **Algorithm**: Uses breadth-first search through derivational relationships,
      scoring candidates based on word length, part of speech, and productivity.
      
      **Example**::
      
         stemmer = DerivationalStemmer('eng')
         
         # Cross-POS stemming
         print(stemmer.stem('organization'))    # organize (noun → verb)
         print(stemmer.stem('beautiful'))       # beauty (adj → noun)
         
         # Multi-hop traversal
         print(stemmer.stem('organizational'))  # organize (2 hops)

   .. py:method:: get_word_family(word: str) -> set
   
      Get all words derived from the given root word.
      
      :param word: The root word
      :type word: str
      :return: Set of all words in the derivational family
      :rtype: set
      
      **Example**::
      
         stemmer = DerivationalStemmer('eng')
         family = stemmer.get_word_family('organize')
         print(len(family))  # 43 related words

InflectionAnalyzer
------------------

.. py:class:: InflectionAnalyzer(language: str)

   Analyzer for inflectional morphology (grammatical variations of the same word).
   
   :param language: ISO 639-3 language code
   :type language: str
   :raises ValueError: If language is not supported
   
   **Example**::
   
      from crosstem import InflectionAnalyzer
      
      analyzer = InflectionAnalyzer('eng')
      inflections = analyzer.get_inflections('run')

   .. py:method:: get_inflections(word: str) -> set
   
      Get all inflectional forms of a word.
      
      :param word: The base word
      :type word: str
      :return: Set of inflected forms
      :rtype: set
      
      **Example**::
      
         analyzer = InflectionAnalyzer('eng')
         
         print(analyzer.get_inflections('run'))
         # {'run', 'runs', 'running', 'ran'}
         
         print(analyzer.get_inflections('go'))
         # {'go', 'goes', 'going', 'went', 'gone'}

EtymologyLinker
---------------

.. py:class:: EtymologyLinker()

   Class for tracing cross-lingual etymology relationships.
   
   .. note::
      Requires etymology data to be downloaded first using :func:`download_etymology`.
   
   **Example**::
   
      from crosstem import EtymologyLinker, download_etymology
      
      download_etymology()  # One-time download
      linker = EtymologyLinker()

   .. py:method:: get_etymology(language: str, word: str) -> dict
   
      Get etymology information for a word.
      
      :param language: Full language name (e.g., 'English', 'French')
      :type language: str
      :param word: The word to look up
      :type word: str
      :return: Dictionary of etymology relationships
      :rtype: dict
      
      **Relationship types**:
      
      * ``INHERITED_FROM``: Inherited from ancestor language
      * ``BORROWED_FROM``: Borrowed/loaned from another language
      * ``DERIVED_FROM``: Derived from another word
      * ``ETYMOLOGICAL_ORIGIN_OF``: Source of another word
      
      **Example**::
      
         linker = EtymologyLinker()
         etymology = linker.get_etymology('English', 'organize')
         print(etymology)

   .. py:method:: get_borrowed_words(target_lang: str, source_lang: str) -> list
   
      Find all words borrowed from one language into another.
      
      :param target_lang: Language that borrowed words
      :type target_lang: str
      :param source_lang: Language that provided words
      :type source_lang: str
      :return: List of borrowed words
      :rtype: list
      
      **Example**::
      
         linker = EtymologyLinker()
         french_loans = linker.get_borrowed_words('English', 'French')
         print(f"Found {len(french_loans)} French loanwords")

Helper Functions
----------------

.. py:function:: download_etymology() -> None

   Download the etymology dataset (~1 GB) from GitHub Releases.
   
   Shows a progress bar during download and validates the file after completion.
   
   **Example**::
   
      from crosstem import download_etymology
      download_etymology()

.. py:function:: is_etymology_downloaded() -> bool

   Check if etymology data is available.
   
   :return: True if etymology.json exists, False otherwise
   :rtype: bool
   
   **Example**::
   
      from crosstem import is_etymology_downloaded
      
      if not is_etymology_downloaded():
          print("Please download etymology data first")

.. py:function:: remove_etymology() -> None

   Remove downloaded etymology data to free disk space.
   
   **Example**::
   
      from crosstem import remove_etymology
      remove_etymology()

Supported Languages
-------------------

.. py:data:: SUPPORTED_LANGUAGES
   :type: list

   List of supported ISO 639-3 language codes::
   
      [
          'cat',  # Catalan
          'ces',  # Czech
          'deu',  # German
          'eng',  # English
          'fin',  # Finnish
          'fra',  # French
          'hbs',  # Serbo-Croatian
          'hun',  # Hungarian
          'ita',  # Italian
          'mon',  # Mongolian
          'pol',  # Polish
          'por',  # Portuguese
          'rus',  # Russian
          'spa',  # Spanish
          'swe',  # Swedish
      ]

Exceptions
----------

.. py:exception:: ValueError

   Raised when an invalid language code is provided::
   
      stemmer = DerivationalStemmer('invalid')
      # ValueError: Language 'invalid' not supported

.. py:exception:: FileNotFoundError

   Raised when attempting to use etymology features without downloading data::
   
      linker = EtymologyLinker()  # Without downloading first
      # FileNotFoundError: Etymology data not found

Constants
---------

.. py:data:: MAX_DEPTH
   :type: int
   :value: 3

   Maximum depth for BFS traversal when finding roots.

.. py:data:: PRODUCTIVITY_THRESHOLDS
   :type: dict

   Language-specific productivity thresholds for filtering candidates::
   
      {
          'eng': {'V': 5, 'N': 9},    # English
          'deu': {'V': 4, 'N': 3},    # German
          'fra': {'V': 4, 'N': 5},    # French
          'rus': {'V': 3, 'N': 2},    # Russian
          # ... other languages
      }

Type Hints
----------

All public methods include type hints for better IDE support::

   from crosstem import DerivationalStemmer
   
   def process_text(text: str, language: str = 'eng') -> list[str]:
       """Process text and return stems."""
       stemmer = DerivationalStemmer(language)
       words = text.split()
       return [stemmer.stem(word) for word in words]
