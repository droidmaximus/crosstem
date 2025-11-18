"""
Preprocessing script to convert MorphyNet inflectional TSV data to JSON format.

Processes files like eng.inflectional.v1.tsv into optimized JSON files for fast lookup.
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict

def build_inflection_graph(input_file: Path, output_file: Path):
    """
    Convert MorphyNet inflectional TSV to JSON format.
    
    MorphyNet inflectional format (4 columns):
        lemma    inflected_form    features    segmentation
        
    Example:
        microtome    microtomes    N|PL    microtome|s
        microtome    microtoming   V|V.PTCP;PRS    microtome|ing
    
    Output format:
        {
            "lemma": {
                "pos": "primary_pos",
                "forms": {
                    "inflected_form": [
                        {"pos": "V", "features": "V.PTCP;PRS", "segmentation": "micro|tom|e|ing"},
                        ...
                    ]
                }
            }
        }
    """
    print(f"Processing {input_file.name}...")
    
    # Build graph structure
    inflection_graph = defaultdict(lambda: {'forms': defaultdict(list)})
    line_count = 0
    error_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) != 4:
                error_count += 1
                if error_count <= 5:
                    print(f"  Warning: Line {line_num} has {len(parts)} columns (expected 4): {line[:100]}")
                continue
            
            lemma, inflected_form, features, segmentation = parts
            lemma = lemma.lower()
            inflected_form = inflected_form.lower()
            
            # Extract POS from features (before first | or ;)
            pos = features.split('|')[0].split(';')[0] if features else ''
            
            # Store inflected form data
            form_data = {
                'pos': pos,
                'features': features,
                'segmentation': segmentation
            }
            
            inflection_graph[lemma]['forms'][inflected_form].append(form_data)
            
            # Set primary POS for lemma (first occurrence)
            if 'pos' not in inflection_graph[lemma]:
                inflection_graph[lemma]['pos'] = pos
            
            line_count += 1
            
            if line_count % 100000 == 0:
                print(f"  Processed {line_count:,} lines...")
    
    print(f"  Total lines processed: {line_count:,}")
    print(f"  Unique lemmas: {len(inflection_graph):,}")
    if error_count > 0:
        print(f"  Errors: {error_count}")
    
    # Convert defaultdict to regular dict for JSON serialization
    output_data = {}
    for lemma, data in inflection_graph.items():
        output_data[lemma] = {
            'pos': data.get('pos', ''),
            'forms': dict(data['forms'])
        }
    
    # Write to JSON
    print(f"Writing to {output_file.name}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, separators=(',', ':'))
    
    # Print statistics
    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"✓ Created {output_file.name}")
    print(f"  Size: {file_size_mb:.2f} MB")
    print(f"  Lemmas: {len(output_data):,}")
    
    return len(output_data)


def main():
    parser = argparse.ArgumentParser(
        description='Convert MorphyNet inflectional TSV to JSON'
    )
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Input TSV file (e.g., eng.inflectional.v1.tsv)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        required=True,
        help='Output JSON file (e.g., eng_inflections.json)'
    )
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1
    
    # Create output directory if needed
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    build_inflection_graph(args.input, args.output)
    return 0


if __name__ == '__main__':
    exit(main())
