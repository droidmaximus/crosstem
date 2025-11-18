"""
Preprocessing script to convert etymology CSV to JSON format.

Processes etymology.csv into optimized JSON for fast lookup.
"""

import json
import csv
import argparse
from pathlib import Path

def build_etymology_data(input_file: Path, output_file: Path):
    """
    Convert etymology CSV to JSON format.
    
    CSV format (10 columns):
        term_id, lang, term, reltype, related_term_id, related_lang, 
        related_term, position, group_tag, parent_tag, parent_position
    
    Relation types:
        - borrowed_from
        - inherited_from
        - cognate_of
        - etymologically_related_to
        - has_root
        - has_affix
    
    Output format:
        [
            {
                "term_id": "...",
                "lang": "eng",
                "term": "portmanteau",
                "reltype": "borrowed_from",
                "related_term_id": "...",
                "related_lang": "frm",
                "related_term": "portemanteau",
                "position": "...",
                "group_tag": "...",
                "parent_tag": "...",
                "parent_position": "..."
            },
            ...
        ]
    """
    print(f"Processing {input_file.name}...")
    
    etymology_data = []
    line_count = 0
    error_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        # Skip header
        next(f)
        
        reader = csv.reader(f)
        for line_num, row in enumerate(reader, 2):  # Start at 2 (after header)
            if len(row) != 11:
                error_count += 1
                if error_count <= 5:
                    print(f"  Warning: Line {line_num} has {len(row)} columns (expected 11)")
                continue
            
            term_id, lang, term, reltype, related_term_id, related_lang, \
                related_term, position, group_tag, parent_tag, parent_position = row
            
            record = {
                'term_id': term_id,
                'lang': lang,
                'term': term,
                'reltype': reltype,
                'related_term_id': related_term_id,
                'related_lang': related_lang,
                'related_term': related_term,
                'position': position,
                'group_tag': group_tag,
                'parent_tag': parent_tag,
                'parent_position': parent_position
            }
            
            etymology_data.append(record)
            line_count += 1
            
            if line_count % 500000 == 0:
                print(f"  Processed {line_count:,} lines...")
    
    print(f"  Total lines processed: {line_count:,}")
    if error_count > 0:
        print(f"  Errors: {error_count}")
    
    # Write to JSON
    print(f"Writing to {output_file.name}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(etymology_data, f, ensure_ascii=False, separators=(',', ':'))
    
    # Print statistics
    file_size_mb = output_file.stat().st_size / (1024 * 1024)
    
    # Count by language
    lang_counts = {}
    for record in etymology_data:
        lang = record['lang']
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
    
    print(f"✓ Created {output_file.name}")
    print(f"  Size: {file_size_mb:.2f} MB")
    print(f"  Total relationships: {len(etymology_data):,}")
    print(f"  Languages: {len(lang_counts)}")
    print(f"  Top languages: {sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:5]}")
    
    return len(etymology_data)


def main():
    parser = argparse.ArgumentParser(
        description='Convert etymology CSV to JSON'
    )
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Input CSV file (e.g., etymology.csv)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        required=True,
        help='Output JSON file (e.g., etymology.json)'
    )
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1
    
    # Create output directory if needed
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    build_etymology_data(args.input, args.output)
    return 0


if __name__ == '__main__':
    exit(main())
