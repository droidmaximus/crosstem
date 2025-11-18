"""
Unified morphological analyzer combining all Crosstem features.

Provides a single interface for derivational stemming, inflectional analysis,
cross-lingual etymology, and comprehensive morphological analysis.
"""

from typing import Dict, List, Optional
from .stemmer import DerivationalStemmer
from .inflection_analyzer import InflectionAnalyzer
from .etymology_linker import EtymologyLinker
from .exceptions import DataNotFoundError

class MorphologyAnalyzer:
    """
    Comprehensive morphological analyzer combining:
    - Derivational morphology (organize → organization)
    - Inflectional morphology (run → runs, running, ran)
    - Cross-lingual etymology (portmanteau ← portemanteau)
    - Word family analysis
    
    Example:
        >>> analyzer = MorphologyAnalyzer('eng')
        >>> result = analyzer.analyze('organization')
        >>> print(result['derivational_stem'])  # 'organize'
        >>> print(result['inflectional_lemma'])  # 'organization'
        >>> print(result['word_family'])  # ['organize', 'organizer', 'organizational', ...]
    """
    
    def __init__(self, language: str = 'eng', load_etymology: bool = True):
        """
        Initialize the morphology analyzer.
        
        Args:
            language: ISO 639-3 language code (e.g., 'eng', 'fra', 'deu')
            load_etymology: Whether to load cross-lingual etymology data.
                          Set to False if you don't need etymology features.
                          Note: Etymology data must be downloaded separately
                          (see download_etymology() method)
        
        Raises:
            LanguageNotSupportedError: If language is not supported
        """
        self.language = language
        
        # Initialize component analyzers
        self.derivational = DerivationalStemmer(language)
        self.inflectional = InflectionAnalyzer(language)
        
        # Etymology is optional - only load if requested and available
        self.etymology = None
        if load_etymology:
            try:
                self.etymology = EtymologyLinker()
            except DataNotFoundError:
                # Etymology not downloaded - will be None
                pass
    
    def analyze(self, word: str, depth: int = 2) -> Dict:
        """
        Perform comprehensive morphological analysis of a word.
        
        Args:
            word: The word to analyze
            depth: Depth for word family traversal (default: 2)
            
        Returns:
            Dict containing:
                - word: Original word
                - derivational_stem: Derivational root (e.g., organize)
                - inflectional_lemma: Inflectional base form
                - pos: Part of speech
                - word_family: Related words through derivation
                - inflections: Inflected forms
                - derivations: Derivationally related forms
                - etymology: Cross-lingual origin (if load_etymology=True)
                
        Example:
            >>> analyzer = MorphologyAnalyzer('eng')
            >>> analyzer.analyze('organizations')
            {
                'word': 'organizations',
                'derivational_stem': 'organize',
                'inflectional_lemma': 'organization',
                'pos': 'N',
                'word_family': ['organize', 'organizer', 'organization', ...],
                'inflections': [{'form': 'organizations', 'pos': 'N', 'features': 'N|PL'}],
                'derivations': [{'form': 'organize', 'pos': 'V', 'relation': 'HAS_DERIVATION'}, ...],
                'etymology': {...}
            }
        """
        result = {'word': word}
        
        # Derivational analysis
        deriv_stem = self.derivational.stem(word)
        result['derivational_stem'] = deriv_stem
        result['word_family'] = self.derivational.get_word_family(word, max_depth=depth)
        result['derivations'] = self.derivational.get_derivations(word)
        
        # Inflectional analysis
        infl_data = self.inflectional.analyze(word)
        if infl_data:
            result['inflectional_lemma'] = infl_data['lemma']
            result['pos'] = infl_data['pos']
            result['grammatical_features'] = infl_data['features']
            result['inflections'] = self.inflectional.get_inflections(word)
        else:
            result['inflectional_lemma'] = None
            result['pos'] = None
            result['grammatical_features'] = ''
            result['inflections'] = []
        
        # Etymology analysis (if enabled)
        if self.etymology:
            lang_name = self._get_language_name()
            origin = self.etymology.get_origin(word, lang_name)
            if origin:
                result['etymology'] = {
                    'origin': origin,
                    'chain': self.etymology.trace_origin_chain(word, lang_name),
                    'related_languages': self.etymology.find_related_across_languages(word, lang_name)
                }
            else:
                result['etymology'] = None
        
        return result
    
    def get_full_stem(self, word: str) -> str:
        """
        Get the most reduced form by applying both inflectional and derivational stemming.
        
        Args:
            word: The word to stem
            
        Returns:
            The fully stemmed form
            
        Example:
            >>> analyzer = MorphologyAnalyzer('eng')
            >>> analyzer.get_full_stem('organizations')
            'organize'  # organization (inflectional) → organize (derivational)
        """
        # First inflectional lemmatization
        lemma = self.inflectional.get_lemma(word)
        if not lemma:
            lemma = word
        
        # Then derivational stemming
        return self.derivational.stem(lemma)
    
    def are_related(self, word1: str, word2: str, check_inflection: bool = True) -> Dict:
        """
        Check if two words are morphologically related.
        
        Args:
            word1: First word
            word2: Second word
            check_inflection: Also check inflectional relationship
            
        Returns:
            Dict with relationship information:
                - related: Boolean indicating if words are related
                - relationship_type: 'derivational', 'inflectional', 'both', or None
                - common_root: The shared root/lemma
                
        Example:
            >>> analyzer = MorphologyAnalyzer('eng')
            >>> analyzer.are_related('organize', 'organizational')
            {'related': True, 'relationship_type': 'derivational', 'common_root': 'organize'}
            >>> analyzer.are_related('run', 'running')
            {'related': True, 'relationship_type': 'inflectional', 'common_root': 'run'}
        """
        result = {
            'related': False,
            'relationship_type': None,
            'common_root': None
        }
        
        # Check derivational relationship
        deriv_related = self.derivational.are_related(word1, word2)
        
        # Check inflectional relationship
        infl_related = False
        if check_inflection:
            infl_related = self.inflectional.are_inflections(word1, word2)
        
        if deriv_related and infl_related:
            result['related'] = True
            result['relationship_type'] = 'both'
            result['common_root'] = self.get_full_stem(word1)
        elif deriv_related:
            result['related'] = True
            result['relationship_type'] = 'derivational'
            result['common_root'] = self.derivational.stem(word1)
        elif infl_related:
            result['related'] = True
            result['relationship_type'] = 'inflectional'
            result['common_root'] = self.inflectional.get_lemma(word1)
        
        return result
    
    def trace_etymology(self, word: str, max_depth: int = 5) -> Optional[List[Dict]]:
        """
        Trace the etymological history of a word across languages.
        
        Args:
            word: The word to trace
            max_depth: Maximum depth to trace back
            
        Returns:
            List of dicts showing etymology chain, or None if not found
            
        Example:
            >>> analyzer = MorphologyAnalyzer('eng')
            >>> analyzer.trace_etymology('portmanteau')
            [
                {'term': 'portmanteau', 'lang': 'English'},
                {'term': 'portemanteau', 'lang': 'Middle French', 'reltype': 'borrowed_from'}
            ]
        """
        if not self.etymology:
            return None
        
        lang_name = self._get_language_name()
        return self.etymology.trace_origin_chain(word, lang_name, max_depth)
    
    def _get_language_name(self) -> str:
        """Convert language code to full name for etymology lookup."""
        # Map ISO 639-3 codes to full language names used in etymology data
        lang_map = {
            'eng': 'English',
            'fra': 'French',
            'deu': 'German',
            'spa': 'Spanish',
            'ita': 'Italian',
            'por': 'Portuguese',
            'rus': 'Russian',
            'pol': 'Polish',
            'ces': 'Czech',
            'hun': 'Hungarian',
            'fin': 'Finnish',
            'swe': 'Swedish',
            'cat': 'Catalan',
            'hbs': 'Serbo-Croatian',
            'mon': 'Mongolian'
        }
        return lang_map.get(self.language, self.language.title())
    
    @classmethod
    def supported_languages(cls) -> Dict[str, str]:
        """
        Get all supported languages.
        
        Returns:
            Dict mapping language codes to language names
        """
        from .stemmer import SUPPORTED_LANGUAGES
        return SUPPORTED_LANGUAGES.copy()
    
    @staticmethod
    def download_etymology(force: bool = False, verbose: bool = True) -> bool:
        """
        Download etymology data from GitHub Releases.
        
        Etymology data (~1 GB) is not included in the package by default.
        Call this method to download it for etymology features.
        
        Args:
            force: If True, re-download even if file exists
            verbose: If True, print progress messages
            
        Returns:
            bool: True if download successful, False otherwise
            
        Example:
            >>> from crosstem import MorphologyAnalyzer
            >>> MorphologyAnalyzer.download_etymology()
            Downloading etymology data (~1 GB) from GitHub Releases...
            ✓ Etymology data successfully downloaded!
            
            >>> # Now etymology features work
            >>> analyzer = MorphologyAnalyzer('eng', load_etymology=True)
            >>> result = analyzer.trace_etymology('portmanteau')
        """
        from .download import download_etymology as dl_etym
        return dl_etym(force=force, verbose=verbose)
    
    @staticmethod
    def is_etymology_available() -> bool:
        """
        Check if etymology data is downloaded and available.
        
        Returns:
            bool: True if etymology data exists locally
            
        Example:
            >>> from crosstem import MorphologyAnalyzer
            >>> if not MorphologyAnalyzer.is_etymology_available():
            ...     MorphologyAnalyzer.download_etymology()
        """
        from .download import is_etymology_downloaded
        return is_etymology_downloaded()
