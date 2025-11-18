"""
Preprocessing script to convert MorphyNet TSV data to JSON format.

This script reads derivational morphology TSV files from MorphyNet and creates
a lightweight JSON graph structure for the package. It supports both MorphyNet's
native format (6 columns) and UniMorph format (4 columns) - both contain the
same MorphyNet data, just in different TSV structures.

Data Source:
    - MorphyNet: Batsuren et al. (2021) - https://github.com/kbatsuren/MorphyNet
      Licensed under CC BY-SA 4.0

Usage:
    # MorphyNet format (6 columns) - DEFAULT
    python -m crosstem.preprocess --input data/morphynet/eng/eng.derivational.v1.tsv --output crosstem/data/eng_derivations.json
    
    # UniMorph format (4 columns) - same data, different structure
    python -m crosstem.preprocess --input data/unimorph/eng.derivations.tsv --output crosstem/data/eng_derivations.json --format unimorph
"""

import argparse
import json
import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict


def detect_format(tsv_file: Path) -> str:
    """
    Auto-detect if the file is MorphyNet (6 columns) or UniMorph (4 columns) format.
    """
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        first_row = next(reader, None)
        
        if first_row:
            num_cols = len(first_row)
            if num_cols == 6:
                return "morphynet"
            elif num_cols == 4:
                return "unimorph"
    
    raise ValueError(f"Could not detect format. Expected 4 or 6 columns, got {num_cols}")


def build_derivation_graph(tsv_file: Path, format: str = "auto") -> Dict:
    """
    Build a bidirectional graph from MorphyNet or UniMorph derivational data.
    
    MorphyNet format (6 columns):
    source_word, target_word, pos_source, pos_target, affix, affix_type
    Example: organize    organizer    V    N    er    suffix
    
    UniMorph format (4 columns):
    source_word, target_word, pos_combined, affix_with_hyphen
    Example: organize    organizer    V:N    -er
    
    Returns:
    {
        "organize": {
            "pos": "V",
            "derives_to": {
                "organizer": {"pos": "N", "affix": "-er"},
                "organization": {"pos": "N", "affix": "-ation"}
            },
            "derived_from": {}
        },
        "organizer": {
            "pos": "N",
            "derives_to": {},
            "derived_from": {
                "organize": {"pos": "V", "affix": "-er"}
            }
        }
    }
    """
    # Auto-detect format if needed
    if format == "auto":
        format = detect_format(tsv_file)
        print(f"Detected format: {format}")
    
    graph = defaultdict(lambda: {
        "pos": None,
        "derives_to": {},
        "derived_from": {}
    })
    
    print(f"Reading {tsv_file}...")
    
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        
        # Process all rows
        for row in reader:
            if format == "morphynet":
                _process_morphynet_row(row, graph)
            elif format == "unimorph":
                _process_unimorph_row(row, graph)
    
    # Convert defaultdict to regular dict
    result = {word: dict(data) for word, data in graph.items()}
    
    print(f"Processed {len(result)} unique words")
    return result


def _process_morphynet_row(row, graph):
    """Process a single MorphyNet TSV row (6 columns)"""
    if len(row) < 6:
        return  # Skip malformed rows
    
    source_word = row[0].strip().lower()
    target_word = row[1].strip().lower()
    pos_source = row[2].strip()
    pos_target = row[3].strip()
    affix = row[4].strip()
    affix_type = row[5].strip()
    
    # Skip empty rows
    if not source_word or not target_word:
        return
    
    # Update source word
    if not graph[source_word]["pos"]:
        graph[source_word]["pos"] = pos_source
    
    graph[source_word]["derives_to"][target_word] = {
        "pos": pos_target,
        "affix": affix,
        "affix_type": affix_type
    }
    
    # Update target word
    if not graph[target_word]["pos"]:
        graph[target_word]["pos"] = pos_target
    
    graph[target_word]["derived_from"][source_word] = {
        "pos": pos_source,
        "affix": affix,
        "affix_type": affix_type
    }


def _process_unimorph_row(row, graph):
    """Process a single UniMorph TSV row (4 columns)"""
    if len(row) < 4:
        return  # Skip malformed rows
    
    source_word = row[0].strip().lower()
    target_word = row[1].strip().lower()
    pos_combined = row[2].strip()  # e.g., "V:N"
    affix = row[3].strip()  # e.g., "-ation"
    
    # Skip empty rows
    if not source_word or not target_word:
        return
    
    # Parse combined POS tag
    if ':' in pos_combined:
        pos_source, pos_target = pos_combined.split(':', 1)
    else:
        pos_source = pos_target = pos_combined
    
    # Determine affix type from the affix string
    affix_type = "prefix" if affix.startswith('-') else "suffix"
    
    # Update source word
    if not graph[source_word]["pos"]:
        graph[source_word]["pos"] = pos_source
    
    graph[source_word]["derives_to"][target_word] = {
        "pos": pos_target,
        "affix": affix,
        "affix_type": affix_type
    }
    
    # Update target word
    if not graph[target_word]["pos"]:
        graph[target_word]["pos"] = pos_target
    
    graph[target_word]["derived_from"][source_word] = {
        "pos": pos_source,
        "affix": affix,
        "affix_type": affix_type
    }


def save_json(data: Dict, output_file: Path):
    """Save the graph to JSON with nice formatting"""
    print(f"Saving to {output_file}...")
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Print file size
    size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"Saved {len(data)} words ({size_mb:.2f} MB)")


def main():
    parser = argparse.ArgumentParser(
        description="Convert MorphyNet or UniMorph TSV to JSON format"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to derivational TSV file (MorphyNet or UniMorph format)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output JSON file path (e.g., crosstem/data/eng_derivations.json)"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["auto", "morphynet", "unimorph"],
        default="auto",
        help="Input format (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1
    
    # Build graph
    graph = build_derivation_graph(args.input, format=args.format)
    
    # Save JSON
    save_json(graph, args.output)
    
    print("Done!")
    return 0


if __name__ == "__main__":
    exit(main())
