"""
Cross-lingual etymology analyzer for Crosstem.

Traces word origins across languages using borrowed_from, cognate_of,
and etymologically_related_to relationships.
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from collections import defaultdict

from .exceptions import DataNotFoundError
from .download import is_etymology_downloaded, get_download_instructions


class EtymologyLinker:
    """
    Analyzes cross-lingual etymological relationships between words.
    
    Relationship types:
        - borrowed_from: Word was borrowed from another language
        - cognate_of: Words share common ancestor (cognates)
        - etymologically_related_to: Other etymological relationships
        - has_root: Links to etymological root
        - has_affix: Links to affix
    
    Examples:
        - English "portmanteau" ← Middle French "portemanteau" (borrowed_from)
        - Dutch "woordenboek" ↔ German Low German "Woordenbook" (cognate_of)
    """
    
    def __init__(self):
        """
        Initialize etymology linker.
        
        Raises:
            DataNotFoundError: If etymology data file not found
        """
        self._etymology = self._load_etymology()
        self._by_term = self._index_by_term()
    
    def _load_etymology(self) -> List[Dict]:
        """Load etymology data from JSON file."""
        data_dir = Path(__file__).parent / 'data'
        etymology_file = data_dir / 'etymology.json'
        
        if not etymology_file.exists():
            raise DataNotFoundError(
                f"Etymology data not found.\n\n"
                f"{get_download_instructions()}\n"
            )
        
        with open(etymology_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _index_by_term(self) -> Dict[Tuple[str, str], List[Dict]]:
        """Create index: (term, lang) -> list of etymology records."""
        index = defaultdict(list)
        for record in self._etymology:
            key = (record['term'].lower(), record['lang'])
            index[key].append(record)
        return dict(index)
    
    def get_etymology(self, term: str, language: str) -> List[Dict]:
        """
        Get all etymological relationships for a term.
        
        Args:
            term: The word to look up
            language: Language code (e.g., 'eng', 'fra', 'deu')
            
        Returns:
            List of dicts with etymology information
            
        Example:
            >>> linker = EtymologyLinker()
            >>> linker.get_etymology('portmanteau', 'eng')
            [
                {
                    'term': 'portmanteau',
                    'lang': 'eng',
                    'reltype': 'borrowed_from',
                    'related_term': 'portemanteau',
                    'related_lang': 'frm',  # Middle French
                    ...
                }
            ]
        """
        key = (term.lower(), language)
        return self._by_term.get(key, [])
    
    def get_origin(self, term: str, language: str) -> Optional[Dict]:
        """
        Get the direct origin (source) of a word.
        
        Args:
            term: The word to trace
            language: Language code
            
        Returns:
            Dict with 'term', 'lang', and 'reltype' if found, else None
            
        Example:
            >>> linker.get_origin('portmanteau', 'eng')
            {
                'term': 'portemanteau',
                'lang': 'frm',
                'reltype': 'borrowed_from'
            }
        """
        records = self.get_etymology(term, language)
        
        # Priority: borrowed_from > etymologically_related_to
        for reltype in ['borrowed_from', 'inherited_from', 'etymologically_related_to']:
            for record in records:
                if record['reltype'] == reltype:
                    return {
                        'term': record['related_term'],
                        'lang': record['related_lang'],
                        'reltype': reltype
                    }
        
        return None
    
    def get_cognates(self, term: str, language: str) -> List[Dict]:
        """
        Get cognates (words with common ancestor) across languages.
        
        Args:
            term: The word to find cognates for
            language: Language code
            
        Returns:
            List of dicts with 'term' and 'lang' keys
            
        Example:
            >>> linker.get_cognates('woordenboek', 'nld')
            [
                {'term': 'wurdboek', 'lang': 'fry'},
                {'term': 'Woordenbook', 'lang': 'nds-de'},
                ...
            ]
        """
        records = self.get_etymology(term, language)
        cognates = []
        
        for record in records:
            if record['reltype'] == 'cognate_of':
                cognates.append({
                    'term': record['related_term'],
                    'lang': record['related_lang']
                })
        
        return cognates
    
    def trace_origin_chain(self, term: str, language: str, max_depth: int = 5) -> List[Dict]:
        """
        Trace the etymological chain back through history.
        
        Args:
            term: The word to trace
            language: Language code
            max_depth: Maximum number of steps to trace back
            
        Returns:
            List of dicts showing the etymology chain, newest to oldest
            
        Example:
            >>> linker.trace_origin_chain('portmanteau', 'eng')
            [
                {'term': 'portmanteau', 'lang': 'eng'},
                {'term': 'portemanteau', 'lang': 'frm', 'reltype': 'borrowed_from'},
                {'term': 'porte', 'lang': 'fro', 'reltype': 'has_root'},
                ...
            ]
        """
        chain = [{'term': term, 'lang': language}]
        current_term = term
        current_lang = language
        visited = {(term.lower(), language)}
        
        for _ in range(max_depth):
            origin = self.get_origin(current_term, current_lang)
            if not origin:
                break
            
            # Avoid cycles
            key = (origin['term'].lower(), origin['lang'])
            if key in visited:
                break
            visited.add(key)
            
            chain.append(origin)
            current_term = origin['term']
            current_lang = origin['lang']
        
        return chain
    
    def find_related_across_languages(self, term: str, language: str) -> Dict[str, List[str]]:
        """
        Find all related terms across different languages.
        
        Args:
            term: The word to search for
            language: Source language code
            
        Returns:
            Dict mapping relationship types to lists of (term, lang) tuples
            
        Example:
            >>> linker.find_related_across_languages('portmanteau', 'eng')
            {
                'borrowed_from': [('portemanteau', 'frm')],
                'cognates': [],
                'related': []
            }
        """
        records = self.get_etymology(term, language)
        
        result = {
            'borrowed_from': [],
            'inherited_from': [],
            'cognates': [],
            'related': [],
            'roots': [],
            'affixes': []
        }
        
        for record in records:
            reltype = record['reltype']
            related = (record['related_term'], record['related_lang'])
            
            if reltype == 'borrowed_from':
                result['borrowed_from'].append(related)
            elif reltype == 'inherited_from':
                result['inherited_from'].append(related)
            elif reltype == 'cognate_of':
                result['cognates'].append(related)
            elif reltype == 'etymologically_related_to':
                result['related'].append(related)
            elif reltype == 'has_root':
                result['roots'].append(related)
            elif reltype == 'has_affix':
                result['affixes'].append(related)
        
        return result
    
    def get_language_statistics(self) -> Dict[str, int]:
        """
        Get statistics about available etymology data.
        
        Returns:
            Dict mapping language codes to term counts
        """
        stats = defaultdict(int)
        for key in self._by_term.keys():
            _, lang = key
            stats[lang] += 1
        return dict(stats)
