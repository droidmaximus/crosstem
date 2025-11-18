"""
Batch preprocessing script to convert all available MorphyNet languages to JSON.

This script processes all derivational TSV files in the data/morphynet directory
and creates JSON files for each language in the package data directory.

Usage:
    python scripts/build_all_languages.py
"""

from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from preprocess import build_derivation_graph, save_json


# Language code mapping
LANGUAGES = {
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


def process_all_languages(morphynet_dir: Path, output_dir: Path):
    """Process all available MorphyNet languages"""
    
    print(f"Processing {len(LANGUAGES)} languages from {morphynet_dir}")
    print("=" * 70)
    
    success_count = 0
    failed_languages = []
    
    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n📚 Processing {lang_name} ({lang_code})...")
        
        # Find the derivational TSV file
        lang_dir = morphynet_dir / lang_code
        tsv_file = lang_dir / f"{lang_code}.derivational.v1.tsv"
        
        if not tsv_file.exists():
            print(f"   ⚠️  Skipping - file not found: {tsv_file}")
            failed_languages.append((lang_code, "File not found"))
            continue
        
        try:
            # Build graph
            graph = build_derivation_graph(tsv_file, format="morphynet")
            
            # Save JSON
            output_file = output_dir / f"{lang_code}_derivations.json"
            save_json(graph, output_file)
            
            print(f"   ✅ Success - {len(graph)} words processed")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Failed - {e}")
            failed_languages.append((lang_code, str(e)))
    
    # Summary
    print("\n" + "=" * 70)
    print(f"SUMMARY: {success_count}/{len(LANGUAGES)} languages processed successfully")
    
    if failed_languages:
        print(f"\n❌ Failed languages:")
        for lang_code, reason in failed_languages:
            print(f"   - {lang_code}: {reason}")
    
    return success_count == len(LANGUAGES)


def main():
    # Paths - crosstem is inside the finalproject directory
    script_dir = Path(__file__).parent
    crosstem_root = script_dir.parent  # crosstem/
    project_root = crosstem_root.parent  # finalproject/
    
    morphynet_dir = project_root / "data" / "morphynet"
    output_dir = crosstem_root / "crosstem" / "data"
    
    if not morphynet_dir.exists():
        print(f"Error: MorphyNet directory not found: {morphynet_dir}")
        return 1
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all languages
    success = process_all_languages(morphynet_dir, output_dir)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
