"""
Benchmark comparison: Crosstem vs Porter Stemmer

Compares:
- Execution time
- Accuracy (finding true linguistic roots)
- Cross-POS capability
"""

import time
from crosstem import DerivationalStemmer

# Try to import Porter stemmer
try:
    from nltk.stem import PorterStemmer
    HAVE_PORTER = True
except ImportError:
    HAVE_PORTER = False
    print("⚠️  NLTK not installed. Install with: pip install nltk")
    print("    Continuing with Crosstem-only benchmarks...\n")


# Test words covering different scenarios
TEST_WORDS = [
    # Simple cases
    "organization", "organizations", "organizational", "organize", "organizer",
    "beautiful", "beauty", "beautify", "beautification",
    "happiness", "happy", "unhappy", "happily",
    
    # Complex derivations
    "microtoming", "microtome", "microtomy",
    "computerization", "computerize", "computer",
    "democratization", "democratize", "democracy", "democratic",
    
    # Cross-POS challenges (where Porter fails)
    "destruction", "destroy", "destructive", "destroyer",
    "collection", "collect", "collective", "collector",
    "revolution", "revolve", "revolutionary", "revolver",
    
    # Edge cases
    "running", "run", "runner",
    "better", "good", "best",
    "went", "go", "going",
]


def benchmark_crosstem(words, iterations=1000):
    """Benchmark Crosstem stemmer."""
    stemmer = DerivationalStemmer('eng')
    
    # Warmup
    for word in words[:5]:
        stemmer.stem(word)
    
    # Benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        for word in words:
            stemmer.stem(word)
    end = time.perf_counter()
    
    total_time = end - start
    avg_time = (total_time / (iterations * len(words))) * 1000  # ms
    
    return total_time, avg_time


def benchmark_porter(words, iterations=1000):
    """Benchmark Porter stemmer."""
    if not HAVE_PORTER:
        return None, None
    
    stemmer = PorterStemmer()
    
    # Warmup
    for word in words[:5]:
        stemmer.stem(word)
    
    # Benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        for word in words:
            stemmer.stem(word)
    end = time.perf_counter()
    
    total_time = end - start
    avg_time = (total_time / (iterations * len(words))) * 1000  # ms
    
    return total_time, avg_time


def compare_accuracy(words):
    """Compare stemming accuracy."""
    crosstem = DerivationalStemmer('eng')
    
    results = []
    
    for word in words:
        cross_result = crosstem.stem(word)
        
        row = {'word': word, 'crosstem': cross_result}
        
        if HAVE_PORTER:
            porter = PorterStemmer()
            porter_result = porter.stem(word)
            row['porter'] = porter_result
        
        results.append(row)
    
    return results


def print_results():
    """Print benchmark results."""
    print("=" * 80)
    print("CROSSTEM vs PORTER STEMMER BENCHMARK")
    print("=" * 80)
    
    # Performance benchmark
    print("\n📊 PERFORMANCE BENCHMARK")
    print("-" * 80)
    
    iterations = 1000
    print(f"Running {iterations:,} iterations on {len(TEST_WORDS)} words...")
    
    cross_total, cross_avg = benchmark_crosstem(TEST_WORDS, iterations)
    print(f"\n✓ Crosstem:")
    print(f"  Total time: {cross_total:.3f}s")
    print(f"  Average per word: {cross_avg:.4f}ms")
    print(f"  Throughput: {1000/cross_avg:.0f} words/second")
    
    if HAVE_PORTER:
        porter_total, porter_avg = benchmark_porter(TEST_WORDS, iterations)
        print(f"\n✓ Porter Stemmer:")
        print(f"  Total time: {porter_total:.3f}s")
        print(f"  Average per word: {porter_avg:.4f}ms")
        print(f"  Throughput: {1000/porter_avg:.0f} words/second")
        
        speedup = porter_avg / cross_avg
        if speedup > 1:
            print(f"\n⚡ Crosstem is {speedup:.2f}x FASTER than Porter")
        else:
            print(f"\n⚠️  Porter is {1/speedup:.2f}x faster than Crosstem")
    
    # Accuracy comparison
    print("\n" + "=" * 80)
    print("📋 ACCURACY COMPARISON")
    print("=" * 80)
    
    # Show specific test cases
    test_cases = [
        "organization", "organizational", "organizer",
        "beautiful", "beauty", "beautification",
        "destruction", "destroy", "destructive",
        "computerization", "computerize", "computer",
        "democratization", "democracy", "democratic"
    ]
    
    results = compare_accuracy(test_cases)
    
    print(f"\n{'Word':<20} {'Crosstem':<20} {'Porter':<20}")
    print("-" * 60)
    
    for row in results:
        word = row['word']
        cross = row['crosstem']
        porter = row.get('porter', 'N/A')
        
        # Highlight differences
        if HAVE_PORTER and cross != porter:
            print(f"{word:<20} {cross:<20} {porter:<20} ⚠️")
        else:
            print(f"{word:<20} {cross:<20} {porter:<20}")
    
    # Analysis
    print("\n" + "=" * 80)
    print("🎯 KEY DIFFERENCES")
    print("=" * 80)
    
    print("\n1️⃣  Cross-POS Stemming (Finding True Roots):")
    print("-" * 60)
    
    crosstem = DerivationalStemmer('eng')
    
    examples = [
        ("organization", "organize (verb)", "organ (overstemming)"),
        ("beautiful", "beauty (noun)", "beauti (meaningless)"),
        ("destruction", "destroy (verb)", "destruct (not a word)"),
    ]
    
    if HAVE_PORTER:
        porter = PorterStemmer()
        print(f"{'Word':<20} {'Crosstem → Root':<25} {'Porter → Root':<25}")
        print("-" * 70)
        for word, cross_expected, porter_expected in examples:
            cross_result = crosstem.stem(word)
            porter_result = porter.stem(word)
            print(f"{word:<20} {cross_result:<25} {porter_result:<25}")
    else:
        print("Porter stemmer not available for comparison.")
    
    print("\n2️⃣  Linguistic Accuracy:")
    print("-" * 60)
    print("✓ Crosstem: Uses MorphyNet linguistic database")
    print("  - Knows actual derivational relationships")
    print("  - Can cross part-of-speech boundaries")
    print("  - Finds semantically meaningful roots")
    print()
    if HAVE_PORTER:
        print("✗ Porter: Rule-based suffix stripping")
        print("  - No linguistic knowledge")
        print("  - Cannot cross POS boundaries")
        print("  - May create non-words (overstemming)")
    
    print("\n3️⃣  Use Cases:")
    print("-" * 60)
    print("🎯 Choose Crosstem when:")
    print("  • You need linguistically accurate stems")
    print("  • Working with related words across POS (organize/organization)")
    print("  • Building word family networks")
    print("  • Semantic search or clustering")
    print()
    if HAVE_PORTER:
        print("🎯 Choose Porter when:")
        print("  • Speed is critical (very simple suffix rules)")
        print("  • Basic inflectional normalization is enough")
        print("  • Working with noisy/misspelled text")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print_results()
