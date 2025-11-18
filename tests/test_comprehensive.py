"""Test script for comprehensive Crosstem features."""

from crosstem import MorphologyAnalyzer

# Initialize analyzer
print("Initializing analyzer (loading ~1GB etymology data)...")
analyzer = MorphologyAnalyzer('eng', load_etymology=True)
print("✓ Ready\n")

# Test 1: Inflectional analysis
print("=" * 60)
print("TEST 1: Inflectional Analysis")
print("=" * 60)
result = analyzer.analyze('microtoming', depth=1)
print(f"Word: {result['word']}")
print(f"Inflectional lemma: {result['inflectional_lemma']}")
print(f"POS: {result['pos']}")
print(f"Features: {result['grammatical_features']}")
print(f"Other inflections: {[f['form'] for f in result['inflections'][:5]]}")
print()

# Test 2: Etymology tracing
print("=" * 60)
print("TEST 2: Cross-Lingual Etymology")
print("=" * 60)
chain = analyzer.trace_etymology('portmanteau', max_depth=5)
if chain:
    print("Etymology chain:")
    for i, step in enumerate(chain):
        prefix = "  → " if i > 0 else "  "
        print(f"{prefix}{step}")
else:
    print("  No etymology found")
print()

# Test 3: Comprehensive analysis
print("=" * 60)
print("TEST 3: Full Analysis")
print("=" * 60)
word = 'microtome'
result = analyzer.analyze(word, depth=2)
print(f"Word: {word}")
print(f"  Derivational stem: {result['derivational_stem']}")
print(f"  Inflectional lemma: {result['inflectional_lemma']}")
print(f"  POS: {result['pos']}")
print(f"  Word family size: {len(result['word_family'])}")
print(f"  # of inflections: {len(result['inflections'])}")
print(f"  Etymology: {'Found' if result.get('etymology') else 'Not found'}")
print()

# Test 4: Relationship checking
print("=" * 60)
print("TEST 4: Word Relationships")
print("=" * 60)
pairs = [
    ('run', 'running'),
    ('microtome', 'microtoming'),
    ('run', 'walk')
]
for w1, w2 in pairs:
    rel = analyzer.are_related(w1, w2)
    print(f"'{w1}' ↔ '{w2}': {rel['relationship_type'] or 'unrelated'}")
    if rel['related']:
        print(f"    Common root: {rel['common_root']}")
print()

# Test 5: Supported languages
print("=" * 60)
print("TEST 5: Language Support")
print("=" * 60)
languages = analyzer.supported_languages()
print(f"Supported languages: {len(languages)}")
print(f"Examples: {list(languages.items())[:5]}")
print()

print("✓ All tests completed!")
