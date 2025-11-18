"""
Core derivational stemmer using MorphyNet data

Data Source:
    - MorphyNet: Batsuren et al. (2021) - https://github.com/kbatsuren/MorphyNet
      Licensed under CC BY-SA 4.0
    
Note: The preprocessing script also supports UniMorph format, which contains
      the same MorphyNet derivational data in a different TSV structure.
"""

import json
from typing import List, Dict
from pathlib import Path

from .exceptions import DataNotFoundError, LanguageNotSupportedError

# Supported languages
SUPPORTED_LANGUAGES = {
    "cat": "Catalan",
    "ces": "Czech",
    "deu": "German",
    "eng": "English",
    "fin": "Finnish",
    "fra": "French",
    "hbs": "Serbo-Croatian",
    "hun": "Hungarian",
    "ita": "Italian",
    "mon": "Mongolian",
    "pol": "Polish",
    "por": "Portuguese",
    "rus": "Russian",
    "spa": "Spanish",
    "swe": "Swedish"
}

# Language-specific productivity thresholds
# Based on empirical analysis of MorphyNet data distributions
# Format: (min_verb_productivity, min_other_productivity)
PRODUCTIVITY_THRESHOLDS = {
    "eng": (5, 9),   # English: Rich derivational data, higher thresholds
    "fra": (4, 5),   # French: Moderate productivity
    "deu": (4, 3),   # German: Compound-heavy, lower threshold for non-verbs
    "ita": (4, 5),   # Italian: Similar to French
    "spa": (3, 4),   # Spanish: Lower overall productivity
    "por": (3, 4),   # Portuguese: Similar to Spanish
    "rus": (3, 2),   # Russian: Very low non-verb productivity
    "pol": (3, 3),   # Polish: Slavic like Russian but slightly higher
    "ces": (3, 3),   # Czech: Similar to Polish
    "hbs": (3, 3),   # Serbo-Croatian: Slavic family
    "hun": (3, 3),   # Hungarian: Lower productivity
    "fin": (3, 3),   # Finnish: Agglutinative, different pattern
    "swe": (3, 4),   # Swedish: Germanic like German
    "cat": (3, 4),   # Catalan: Romance like Spanish
    "mon": (3, 3),   # Mongolian: Limited data
}

# Default threshold for unsupported languages
DEFAULT_THRESHOLDS = (3, 5)


class DerivationalStemmer:
    """
    Derivational stemmer that finds root forms by traversing morphological relationships.
    
    Unlike traditional stemmers (Porter, Lancaster) or lemmatizers (WordNet), this stemmer
    uses derivational morphology to cross part-of-speech boundaries:
    - organization (N) → organize (V)
    - beautiful (ADJ) → beauty (N)
    - observation (N) → observe (V)
    
    Based on MorphyNet derivational data.
    """
    
    def __init__(self, language: str = "eng"):
        """
        Initialize the stemmer for a specific language.
        
        Args:
            language: ISO 639-3 language code. Supported languages:
                     cat, ces, deu, eng, fin, fra, hbs, hun, ita,
                     mon, pol, por, rus, spa, swe
        
        Raises:
            LanguageNotSupportedError: If language data is not available
            DataNotFoundError: If data files cannot be loaded
        """
        if language not in SUPPORTED_LANGUAGES:
            available = ", ".join(sorted(SUPPORTED_LANGUAGES.keys()))
            raise LanguageNotSupportedError(
                f"Language '{language}' not supported. "
                f"Available languages: {available}"
            )
        
        self.language = language
        self.data = None
        self._load_data()
    
    def _load_data(self):
        """Load the preprocessed morphology data for the language"""
        # Try to find the data file
        package_dir = Path(__file__).parent
        data_file = package_dir / "data" / f"{self.language}_derivations.json"
        
        if not data_file.exists():
            raise DataNotFoundError(
                f"Data file not found for language '{self.language}'. "
                f"Expected: {data_file}"
            )
        
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            raise DataNotFoundError(f"Failed to load data file: {e}")
    
    def get_derivations(self, word: str) -> List[Dict[str, str]]:
        """
        Get all derivationally related words.
        
        Args:
            word: The word to analyze
        
        Returns:
            List of dictionaries with keys: 'form', 'pos', 'relation'
        """
        if not self.data:
            return []
        
        word_lower = word.lower()
        
        # Check if word exists in our graph
        if word_lower not in self.data:
            return []
        
        derivations = []
        word_data = self.data[word_lower]
        
        # Add derivations (words derived FROM this word)
        for derived_word, info in word_data.get("derives_to", {}).items():
            derivations.append({
                "form": derived_word,
                "pos": info.get("pos", ""),
                "relation": "DERIVES_TO"
            })
        
        # Add sources (words this word is derived FROM)
        for source_word, info in word_data.get("derived_from", {}).items():
            derivations.append({
                "form": source_word,
                "pos": info.get("pos", ""),
                "relation": "DERIVED_FROM"
            })
        
        return derivations
    
    def stem(self, word: str, use_derivations: bool = True) -> str:
        """
        Find the root form of a word.
        
        Strategy:
        1. If use_derivations=False, returns the word as-is (conservative mode)
        2. If use_derivations=True, traverses derivational links to find the simplest root
        3. Prefers verbs (V) as roots when multiple candidates exist
        4. Prefers shorter forms (closer to the etymological root)
        5. Uses BFS to traverse multiple hops (e.g., organizational → organization → organize)
        
        Args:
            word: The word to stem
            use_derivations: Whether to use derivational analysis (default: True)
        
        Returns:
            The root form of the word
        
        Examples:
            >>> stemmer = DerivationalStemmer("eng")
            >>> stemmer.stem("organization")
            'organize'
            >>> stemmer.stem("beautiful")
            'beauty'
            >>> stemmer.stem("observation")
            'observe'
        """
        if not use_derivations or not self.data:
            return word
        
        word_lower = word.lower()
        
        # If word not in data, return as-is
        if word_lower not in self.data:
            return word
        
        # BFS traversal to find the best root
        from collections import deque
        
        visited = {word_lower}
        queue = deque([(word_lower, 0)])  # (word, depth)
        root_candidates = []
        max_depth = 3  # Limit traversal depth
        
        while queue:
            current_word, depth = queue.popleft()
            
            # Don't traverse too deep
            if depth >= max_depth:
                continue
            
            # Get DERIVED_FROM relationships for current word
            if current_word in self.data:
                word_data = self.data[current_word]
                derived_from = word_data.get("derived_from", {})
                
                for parent_word, info in derived_from.items():
                    if parent_word in visited:
                        continue
                    
                    visited.add(parent_word)
                    
                    # Check productivity to decide if this is a good root candidate
                    if parent_word in self.data:
                        productivity = len(self.data[parent_word].get("derives_to", {}))
                        parent_pos = info.get("pos", "")
                        
                        # Use language-specific productivity thresholds
                        # Different languages have different morphological richness
                        verb_threshold, other_threshold = PRODUCTIVITY_THRESHOLDS.get(
                            self.language, DEFAULT_THRESHOLDS
                        )
                        min_productivity = verb_threshold if parent_pos == "V" else other_threshold
                        
                        # Only add productive roots as candidates
                        if productivity >= min_productivity:
                            # This is a valid candidate root
                            # Score: shorter = better, verbs = better, shallower = better
                            score = len(parent_word) + (depth * 2)  # Penalize depth slightly
                            if parent_pos == "V":  # Verbs are often roots
                                score -= 10
                            elif parent_pos == "N" and len(parent_word) < len(word_lower):
                                score -= 5
                            
                            root_candidates.append((score, parent_word, parent_pos))
                        
                        # Continue traversing from this parent (even if low productivity)
                        # This allows multi-hop traversal through intermediate forms
                        queue.append((parent_word, depth + 1))
        
        if root_candidates:
            # Sort by score (lower = better), return the best root
            root_candidates.sort(key=lambda x: x[0])
            best_root = root_candidates[0][1]
            best_pos = root_candidates[0][2]
            
            # Only use the root if it's actually simpler (shorter or verb form)
            if len(best_root) <= len(word_lower) or best_pos == "V":
                return best_root
        
        return word
    
    def get_word_family(self, word: str, max_depth: int = 2) -> List[str]:
        """
        Get all related words in the morphological family.
        
        Args:
            word: The word to analyze
            max_depth: Maximum depth to traverse (default: 2)
        
        Returns:
            List of all related words (including the input word)
        
        Examples:
            >>> stemmer = DerivationalStemmer("eng")
            >>> stemmer.get_word_family("organize")
            ['organize', 'organizer', 'organization', 'organizational', ...]
        """
        if not self.data:
            return [word]
        
        word_lower = word.lower()
        
        if word_lower not in self.data:
            return [word]
        
        # BFS to find all related words
        visited = set()
        to_visit = [(word_lower, 0)]
        word_family = []
        
        while to_visit:
            current_word, depth = to_visit.pop(0)
            
            if current_word in visited or depth > max_depth:
                continue
            
            visited.add(current_word)
            word_family.append(current_word)
            
            # Add derivations if within depth limit
            if depth < max_depth:
                derivations = self.get_derivations(current_word)
                for der in derivations:
                    der_form = der.get("form")
                    if der_form and der_form not in visited:
                        to_visit.append((der_form, depth + 1))
        
        return sorted(word_family)
    
    def are_related(self, word1: str, word2: str) -> bool:
        """
        Check if two words are derivationally related.
        
        Args:
            word1: First word
            word2: Second word
        
        Returns:
            True if the words share a common root or are directly related
        
        Examples:
            >>> stemmer = DerivationalStemmer("eng")
            >>> stemmer.are_related("organize", "organization")
            True
            >>> stemmer.are_related("organize", "orange")
            False
        """
        # Try direct stemming comparison
        stem1 = self.stem(word1)
        stem2 = self.stem(word2)
        
        if stem1.lower() == stem2.lower():
            return True
        
        # Try word family membership
        family1 = set(self.get_word_family(word1, max_depth=1))
        family2 = set(self.get_word_family(word2, max_depth=1))
        
        return bool(family1 & family2)  # True if intersection is non-empty
    
    @staticmethod
    def supported_languages():
        """
        Get a dictionary of all supported languages.
        
        Returns:
            Dict mapping language codes to language names
        
        Examples:
            >>> DerivationalStemmer.supported_languages()
            {'cat': 'Catalan', 'ces': 'Czech', 'deu': 'German', ...}
        """
        return SUPPORTED_LANGUAGES.copy()
