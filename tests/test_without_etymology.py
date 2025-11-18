"""
Test that Crosstem works without etymology data.
"""

print("Testing Crosstem without etymology...")
print("=" * 60)

# Test 1: DerivationalStemmer (should work)
print("\n1. Testing DerivationalStemmer...")
try:
    from crosstem import DerivationalStemmer
    stemmer = DerivationalStemmer('eng')
    result = stemmer.stem('organization')
    print(f"   ✓ organization → {result}")
    assert result == 'organize', f"Expected 'organize', got '{result}'"
    print("   ✓ DerivationalStemmer works!")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 2: InflectionAnalyzer (should work)
print("\n2. Testing InflectionAnalyzer...")
try:
    from crosstem import InflectionAnalyzer
    inflector = InflectionAnalyzer('eng')
    result = inflector.get_lemma('microtoming')
    print(f"   ✓ microtoming → {result}")
    assert result == 'microtome', f"Expected 'microtome', got '{result}'"
    print("   ✓ InflectionAnalyzer works!")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 3: MorphologyAnalyzer without etymology (should work)
print("\n3. Testing MorphologyAnalyzer (load_etymology=False)...")
try:
    from crosstem import MorphologyAnalyzer
    analyzer = MorphologyAnalyzer('eng', load_etymology=False)
    result = analyzer.analyze('organizations')
    print(f"   ✓ Derivational stem: {result['derivational_stem']}")
    print(f"   ✓ Inflectional lemma: {result['inflectional_lemma']}")
    print(f"   ✓ Etymology: {result.get('etymology', 'Not loaded')}")
    assert analyzer.etymology is None, "Etymology should be None"
    print("   ✓ MorphologyAnalyzer works without etymology!")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 4: Check etymology availability
print("\n4. Testing etymology availability check...")
try:
    is_available = MorphologyAnalyzer.is_etymology_available()
    print(f"   Etymology available: {is_available}")
    print("   ✓ Availability check works!")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 5: MorphologyAnalyzer with etymology (should handle gracefully)
print("\n5. Testing MorphologyAnalyzer (load_etymology=True)...")
try:
    analyzer = MorphologyAnalyzer('eng', load_etymology=True)
    if analyzer.etymology is None:
        print("   ℹ Etymology not loaded (data not available)")
        print("   ✓ Gracefully handled missing etymology!")
    else:
        print("   ✓ Etymology loaded successfully!")
        result = analyzer.trace_etymology('portmanteau')
        if result:
            print(f"   ✓ Etymology trace: {len(result)} entries")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 6: Download functions available
print("\n6. Testing download functions...")
try:
    from crosstem import download_etymology, is_etymology_downloaded
    print("   ✓ download_etymology imported")
    print("   ✓ is_etymology_downloaded imported")
    downloaded = is_etymology_downloaded()
    print(f"   Etymology downloaded: {downloaded}")
    print("   ✓ Download utilities work!")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✓ All tests passed! Package works without etymology data.")
print("=" * 60)
