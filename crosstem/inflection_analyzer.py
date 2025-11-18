"""
Inflectional morphology analyzer for Crosstem.

Handles inflectional forms (plurals, verb conjugations, etc.) using MorphyNet data.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path

from .exceptions import LanguageNotSupportedError, DataNotFoundError


class InflectionAnalyzer:
    """
    Analyzes inflectional morphology - variations of words that express grammatical
    distinctions (number, tense, person, etc.) without changing the core meaning.
    
    Examples:
        - run → runs, running, ran (verb inflections)
        - cat → cats (plural noun)
        - good → better, best (adjective comparison)
    """
    
    SUPPORTED_LANGUAGES = {
        'cat': 'Catalan',
        'ces': 'Czech', 
        'deu': 'German',
        'eng': 'English',
        'fin': 'Finnish',
        'fra': 'French',
        'hbs': 'Serbo-Croatian',
        'hun': 'Hungarian',
        'ita': 'Italian',
        'mon': 'Mongolian',
        'pol': 'Polish',
        'por': 'Portuguese',
        'rus': 'Russian',
        'spa': 'Spanish',
        'swe': 'Swedish'
    }
    
    def __init__(self, language: str = 'eng'):
        """
        Initialize inflection analyzer for a specific language.
        
        Args:
            language: ISO 639-3 language code (e.g., 'eng', 'fra', 'deu')
            
        Raises:
            LanguageNotSupportedError: If language is not supported
            DataNotFoundError: If inflection data file not found
        """
        if language not in self.SUPPORTED_LANGUAGES:
            raise LanguageNotSupportedError(
                f"Language '{language}' not supported. "
                f"Supported languages: {', '.join(self.SUPPORTED_LANGUAGES.keys())}"
            )
        
        self.language = language
        self._inflections = self._load_inflections()
    
    def _load_inflections(self) -> Dict[str, Dict]:
        """Load inflection data from JSON file."""
        data_dir = Path(__file__).parent / 'data'
        inflection_file = data_dir / f'{self.language}_inflections.json'
        
        if not inflection_file.exists():
            raise DataNotFoundError(
                f"Inflection data not found for {self.language} at {inflection_file}. "
                f"Run preprocessing first."
            )
        
        with open(inflection_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_lemma(self, word: str) -> Optional[str]:
        """
        Find the base form (lemma) of an inflected word.
        
        Args:
            word: The inflected word form
            
        Returns:
            The lemma (base form), or None if not found
            
        Example:
            >>> analyzer = InflectionAnalyzer('eng')
            >>> analyzer.get_lemma('running')
            'run'
            >>> analyzer.get_lemma('cats')
            'cat'
        """
        word_lower = word.lower()
        
        # Check if already a lemma
        if word_lower in self._inflections:
            return word_lower
        
        # Search through all lemmas for this inflected form
        for lemma, data in self._inflections.items():
            if word_lower in data.get('forms', {}):
                return lemma
        
        return None
    
    def get_inflections(self, word: str) -> List[Dict[str, str]]:
        """
        Get all inflected forms of a word.
        
        Args:
            word: The base word or any inflected form
            
        Returns:
            List of dicts with 'form', 'pos', and 'features' keys
            
        Example:
            >>> analyzer = InflectionAnalyzer('eng')
            >>> analyzer.get_inflections('run')
            [
                {'form': 'runs', 'pos': 'V', 'features': 'PRS;3;SG'},
                {'form': 'running', 'pos': 'V', 'features': 'V.PTCP;PRS'},
                {'form': 'ran', 'pos': 'V', 'features': 'PST'},
                ...
            ]
        """
        lemma = self.get_lemma(word)
        if not lemma:
            return []
        
        lemma_data = self._inflections.get(lemma, {})
        forms = lemma_data.get('forms', {})
        
        result = []
        for form, variants in forms.items():
            if form == lemma:  # Skip the lemma itself
                continue
            for variant in variants:
                result.append({
                    'form': form,
                    'pos': variant.get('pos', ''),
                    'features': variant.get('features', '')
                })
        
        return result
    
    def get_pos(self, word: str) -> Optional[str]:
        """
        Get the part-of-speech tag for a word.
        
        Args:
            word: The word to analyze
            
        Returns:
            POS tag (N, V, ADJ, etc.) or None if not found
        """
        lemma = self.get_lemma(word)
        if not lemma:
            return None
        
        lemma_data = self._inflections.get(lemma, {})
        return lemma_data.get('pos')
    
    def analyze(self, word: str) -> Optional[Dict]:
        """
        Comprehensive inflectional analysis of a word.
        
        Args:
            word: The word to analyze
            
        Returns:
            Dict with 'word', 'lemma', 'pos', 'features', and 'all_forms' keys
            
        Example:
            >>> analyzer = InflectionAnalyzer('eng')
            >>> analyzer.analyze('running')
            {
                'word': 'running',
                'lemma': 'run',
                'pos': 'V',
                'features': 'V.PTCP;PRS',
                'all_forms': ['runs', 'running', 'ran', ...]
            }
        """
        lemma = self.get_lemma(word)
        if not lemma:
            return None
        
        word_lower = word.lower()
        lemma_data = self._inflections.get(lemma, {})
        
        # Find features for this specific form
        features = ''
        if word_lower != lemma:
            forms = lemma_data.get('forms', {})
            if word_lower in forms:
                variants = forms[word_lower]
                if variants:
                    features = variants[0].get('features', '')
        
        # Get all forms
        all_forms = []
        for form, variants in lemma_data.get('forms', {}).items():
            if form != lemma:
                all_forms.append(form)
        
        return {
            'word': word,
            'lemma': lemma,
            'pos': lemma_data.get('pos', ''),
            'features': features,
            'all_forms': sorted(all_forms)
        }
    
    def are_inflections(self, word1: str, word2: str) -> bool:
        """
        Check if two words are inflectional variants of the same lemma.
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            True if both words share the same lemma
            
        Example:
            >>> analyzer = InflectionAnalyzer('eng')
            >>> analyzer.are_inflections('running', 'ran')
            True
            >>> analyzer.are_inflections('running', 'walking')
            False
        """
        lemma1 = self.get_lemma(word1)
        lemma2 = self.get_lemma(word2)
        
        return lemma1 is not None and lemma1 == lemma2
    
    @classmethod
    def supported_languages(cls) -> Dict[str, str]:
        """
        Get all supported languages.
        
        Returns:
            Dict mapping language codes to language names
        """
        return cls.SUPPORTED_LANGUAGES.copy()
