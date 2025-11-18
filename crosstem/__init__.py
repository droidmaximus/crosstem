"""
Crosstem: Comprehensive Morphological Analysis for Python

A powerful morphological analysis toolkit combining:
- **Derivational stemming**: Cross-POS relationships (organize ↔ organization)
- **Inflectional analysis**: Grammatical forms (run → runs, running, ran)
- **Cross-lingual etymology**: Word origins across 2,265 languages
- **Word family analysis**: Complete derivational networks

Examples:
    >>> from crosstem import MorphologyAnalyzer
    >>> analyzer = MorphologyAnalyzer('eng')
    >>> result = analyzer.analyze('organizations')
    >>> result['derivational_stem']
    'organize'
    >>> result['inflections']
    [{'form': 'organizations', 'pos': 'N', 'features': 'N|PL'}]
    >>> result['etymology']['origin']
    {...}

For simple derivational stemming only:
    >>> from crosstem import DerivationalStemmer
    >>> stemmer = DerivationalStemmer()
    >>> stemmer.stem("organization")
    'organize'

Data Sources:
    - MorphyNet v1.0: https://github.com/kbatsuren/MorphyNet (CC BY-SA 4.0)
      Batsuren et al. (2021) - SIGMORPHON Workshop
    - Wiktionary Etymology: Cross-lingual word origins
"""

from .stemmer import DerivationalStemmer, SUPPORTED_LANGUAGES
from .inflection_analyzer import InflectionAnalyzer
from .etymology_linker import EtymologyLinker
from .analyzer import MorphologyAnalyzer
from .exceptions import CrosstemError, DataNotFoundError, LanguageNotSupportedError
from .download import download_etymology, is_etymology_downloaded

__version__ = "0.2.0"
__author__ = "Avinash Bhojanapalli"
__all__ = [
    # Main unified interface
    "MorphologyAnalyzer",
    
    # Component analyzers
    "DerivationalStemmer",
    "InflectionAnalyzer",
    "EtymologyLinker",
    
    # Utilities
    "download_etymology",
    "is_etymology_downloaded",
    
    # Constants
    "SUPPORTED_LANGUAGES",
    
    # Exceptions
    "CrosstemError",
    "DataNotFoundError",
    "LanguageNotSupportedError",
]
