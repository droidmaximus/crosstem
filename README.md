# Crosstem

[![PyPI version](https://badge.fury.io/py/crosstem.svg)](https://badge.fury.io/py/crosstem)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python package for morphological analysis combining derivational stemming, inflectional analysis, and cross-lingual etymology.

## Why Crosstem?

**Crosstem finds true linguistic roots across part-of-speech boundaries,** which is something traditional stemmers and lemmatizers cannot do.

### What Makes It Different

```python
# Traditional stemmers (Porter, Lancaster) - Rule-based, prone to errors
Porter: "organization" → "organ"        # Overstemming loses meaning

# Lemmatizers (WordNet, spaCy) - Only handle inflections, not derivations  
WordNet: "organization" → "organization"  # Can't cross POS boundaries
WordNet: "beautiful" → "beautiful"        # Stuck at adjective form

# Crosstem - Linguistically accurate, crosses POS boundaries
Crosstem: "organization" → "organize"   # Noun → Verb (true root)
Crosstem: "beautiful" → "beauty"        # Adjective → Noun (semantic base)
```

### Key Advantages

- **Cross-POS derivational stemming**: Only library that finds roots across parts of speech
- **Linguistic accuracy**: Uses MorphyNet morphological data, not brittle rules
- **Etymology tracing**: 4.2M relationships across 2,265 languages (unique feature)
- **Word families**: Discover complete derivational networks (e.g., organize → 43 related words)
- **Pure Python**: Zero dependencies, works anywhere (no heavy ML models required)
- **15 languages**: Multilingual morphology support out of the box

## Performance Benchmark vs Porter

We compared Crosstem against the widely-used Porter stemmer on 44 English words with 1,000 iterations each.

### Speed Results

```
Crosstem:     ~0.080s (~547,000 words/sec)
Porter:       ~0.490s (~90,000 words/sec)

⚡ Crosstem is ~6× FASTER than Porter
```

**Why?** Crosstem uses **O(1) hash lookups** in JSON dictionaries, while Porter applies sequential pattern-matching rules.

*Note: Results averaged over multiple runs; ±3% variance is normal due to system load.*

### Accuracy Comparison

| Word            | Crosstem  | Porter    | Winner                                         |
| --------------- | --------- | --------- | ---------------------------------------------- |
| organization    | organize  | organ     | ✅ Crosstem (finds true root)                  |
| organizational  | organize  | organiz   | ✅ Crosstem (multi-hop)                        |
| beautiful       | beauty    | beauti    | ✅ Crosstem (crosses POS)                      |
| destruction     | destruct  | destruct  | ⚖️ Tie                                       |
| democracy       | democracy | democraci | ✅ Crosstem (avoids error)                     |
| computerization | compute   | computer  | ✅ Crosstem (deeper root)                      |
| happiness       | happy     | happi     | ✅ Crosstem (productivity filter avoids "hap") |
| redness         | red       | red       | ⚖️ Tie                                       |

**Key Findings:**

1. **Cross-POS stemming**: Crosstem finds roots across parts of speech (`organization` → `organize`, verb), Porter cannot
2. **Overstemming prevention**: Porter creates non-words (`beauti`, `organiz`), Crosstem always produces real words
3. **Data quality**: Crosstem filters bad roots (`democrat`), Porter has no quality control
4. **Multi-hop**: Crosstem traverses multiple derivations (`organizational` → `organization` → `organize`), Porter only strips one suffix

### When to Use Each

**Choose Crosstem when:**

- ✅ Need linguistically accurate roots
- ✅ Working with derivational families (organize/organizer/organization)
- ✅ Building semantic search, clustering, or word embeddings
- ✅ Quality matters more than simplicity
- ✅ Multilingual support needed (15 languages)

**Choose Porter when:**

- ✅ Legacy system compatibility required
- ✅ Working with noisy/misspelled text (rule-based is robust)
- ✅ Only need basic suffix normalization
- ✅ Want the absolute simplest possible solution

**Note**: Crosstem is now faster than Porter while being more accurate, making it the better choice for most modern NLP applications.

## Features

- **Derivational Stemming**: Find roots across part-of-speech boundaries (organization → organize)
- **Inflectional Analysis**: Lemmatization and grammatical forms (running → run)
- **Cross-Lingual Etymology**: Trace word origins across 2,265 languages
- **Word Family Analysis**: Discover complete derivational networks

## Installation

```bash
pip install crosstem
```

### Optional: Etymology Data

Etymology features require additional data (~1 GB) that's downloaded separately:

```python
from crosstem import download_etymology

# One-time download (saves to package data directory)
download_etymology()
```

Or from command line:

```bash
python -m crosstem.download
```

## Quick Start

### Basic Morphological Analysis

```python
from crosstem import MorphologyAnalyzer

# Works immediately - no etymology needed
analyzer = MorphologyAnalyzer('eng', load_etymology=False)
result = analyzer.analyze('organizations')

print(result['derivational_stem'])    # 'organize'
print(result['inflectional_lemma'])   # 'organization'
```

### With Etymology Features

```python
from crosstem import MorphologyAnalyzer, download_etymology

# Download etymology data first (one-time)
if not MorphologyAnalyzer.is_etymology_available():
    download_etymology()

# Now etymology features work
analyzer = MorphologyAnalyzer('eng', load_etymology=True)
result = analyzer.analyze('portmanteau')
print(result['etymology'])  # Shows Middle French origin
```

## Usage

### Derivational Stemming

```python
from crosstem import DerivationalStemmer

stemmer = DerivationalStemmer('eng')
stemmer.stem('organization')  # 'organize'
stemmer.stem('beautiful')     # 'beauty'

family = stemmer.get_word_family('organize')
# ['organize', 'organizer', 'organization', ...]
```

### Inflectional Analysis

```python
from crosstem import InflectionAnalyzer

inflector = InflectionAnalyzer('eng')
inflector.get_lemma('running')  # 'run'

forms = inflector.get_inflections('run')
# [{'form': 'runs', 'pos': 'V', ...}, ...]
```

### Etymology (Requires Download)

```python
from crosstem import EtymologyLinker, download_etymology

# Download etymology data first (one-time, ~1 GB)
download_etymology()

linker = EtymologyLinker()
chain = linker.trace_origin_chain('portmanteau', 'English')
# [{'term': 'portmanteau', 'lang': 'English'},
#  {'term': 'portemanteau', 'lang': 'Middle French', ...}]
```

## Supported Languages

15 languages with derivational morphology:

- English (eng), Russian (rus), French (fra), German (deu), Spanish (spa)
- Portuguese (por), Italian (ita), Polish (pol), Czech (ces)
- Serbo-Croatian (hbs), Hungarian (hun), Finnish (fin)
- Swedish (swe), Mongolian (mon), Catalan (cat)

Plus 2,265 languages with etymology data.

## How It Works

### Theoretical Framework

Crosstem is built on three pillars of morphological linguistics:

#### 1. Derivational Morphology (Word Formation)

Unlike inflection (which modifies words grammatically), **derivation creates new words** by adding affixes or converting between parts of speech:

- `organize` + `-ation` → `organization` (verb → noun)
- `beauty` + `-ful` → `beautiful` (noun → adjective)
- `organize` + `-er` → `organizer` (agent noun)

Crosstem models this as a **directed graph** where:

- **Nodes** = word forms with POS tags
- **Edges** = derivational relationships (affixes, conversions)
- **Stemming** = graph traversal to find the root (preferring verbs and shorter forms)

```
         ┌─────────────┐
         │  organize   │ ← ROOT (verb, shortest)
         │     (V)     │
         └──────┬──────┘
           ┌────┴────┬───────┬──────────┐
           ▼         ▼       ▼          ▼
      organizer  organization  organized  reorganize
         (N)        (N)         (ADJ)      (V)
                     │
                     ▼
             organizational
                  (ADJ)
```

This graph-based approach ensures **linguistically accurate** roots, avoiding the overstemming problem of rule-based stemmers.

#### 2. Inflectional Morphology (Grammatical Forms)

Inflection expresses grammatical categories **without changing core meaning**:

- Number: `cat` → `cats`
- Tense: `run` → `ran`, `running`
- Comparison: `good` → `better`, `best`

Crosstem stores inflectional paradigms as **lemma → forms mappings**:

```python
{
  "run": {
    "pos": "V",
    "forms": {
      "runs": [{"pos": "V", "features": "PRS;3;SG"}],
      "running": [{"pos": "V", "features": "V.PTCP;PRS"}],
      "ran": [{"pos": "V", "features": "PST"}]
    }
  }
}
```

This enables both **lemmatization** (running → run) and **paradigm generation** (run → all forms).

#### 3. Cross-Lingual Etymology (Historical Linguistics)

Etymology traces how words **evolve and transfer across languages**:

- **Borrowing**: English `portmanteau` ← Middle French `portemanteau`
- **Cognates**: Dutch `woordenboek` ↔ German `Wörterbuch` (shared Germanic ancestor)
- **Inheritance**: Latin `mater` → French `mère`, Italian `madre`, Spanish `madre`

Crosstem represents this as a **multilingual graph** with typed edges:

```
English: "portmanteau" ──borrowed_from──→ Middle French: "portemanteau"
                                               │
                                        has_root: "porter" (to carry)
                                               │
                                        has_root: "manteau" (coat)
```

### Implementation

All three frameworks are implemented as **fast JSON lookups** with graph traversal algorithms:

1. **Preprocessing**: TSV/CSV data → optimized JSON dictionaries
2. **Indexing**: Multi-level indices (word → derivations, lemma → inflections, term+lang → etymology)
3. **Traversal**: BFS for word families, chain-following for etymology
4. **Filtering**: POS preference (verbs), length minimization, cycle detection

**Result**: 0.01-0.05ms lookups with zero dependencies, purely in Python.

## Stemming Algorithm Details

### Multi-Hop BFS Traversal

Crosstem uses a sophisticated **breadth-first search** algorithm to find the optimal root:

```python
# Example: organizational → organization → organize
organizational  (14 chars, ADJ)
    ↓ (depth 1)
organization    (12 chars, N, productivity=16) ← candidate
    ↓ (depth 2)  
organize        (8 chars, V, productivity=13)  ← BEST (verb, shortest)
```

**Algorithm steps:**

1. **Start** from input word, add to queue
2. **Expand** all DERIVED_FROM relationships (parents in morphology graph)
3. **Score** each candidate:
   - Length (shorter is better)
   - POS (verbs score -10, nouns -5)
   - Depth (penalize by +2 per hop)
4. **Filter** by productivity threshold (language-specific):
   - English: Verbs ≥5, Others ≥9
   - French/Italian: Verbs ≥4, Others ≥5
   - German: Verbs ≥4, Others ≥3 (compound-heavy)
   - Spanish/Portuguese: Verbs ≥3, Others ≥4
   - Russian/Slavic: Verbs ≥3, Others ≥2-3 (lower productivity)
5. **Continue** traversal through low-productivity nodes (enables multi-hop)
6. **Return** lowest-scoring candidate that's shorter than input or a verb

### Productivity-Based Filtering

**Problem**: MorphyNet contains archaic roots (e.g., `hap`) and data errors (e.g., `democracy` → `democrat`)

**Solution**: Use productivity as a quality signal. Words with many derivations are more likely to be modern, correct roots.

**Examples (English thresholds: V≥5, N≥9):**

| Word         | Productivity   | POS | Threshold | Result                         |
| ------------ | -------------- | --- | --------- | ------------------------------ |
| `red`      | 18 derivations | N   | ≥9       | ✅ PASS (productive noun)      |
| `run`      | 33 derivations | V   | ≥5       | ✅ PASS (very productive verb) |
| `destruct` | 6 derivations  | V   | ≥5       | ✅ PASS (verb threshold)       |
| `hap`      | 8 derivations  | N   | ≥9       | ❌ FILTERED (archaic)          |
| `democrat` | 7 derivations  | N   | ≥9       | ❌ FILTERED (data error)       |

This **data-driven approach** avoids hard-coded rules while maintaining quality.

**Language-Specific Calibration**: Thresholds are adjusted for each language based on morphological richness. Languages with lower overall productivity (Russian, Spanish) use lower thresholds to avoid over-filtering, while English uses higher thresholds due to rich derivational data.

### Why This Works

Traditional stemmers fail because they use **brittle suffix rules**:

```python
# Porter stemmer rule: -ation → (remove suffix)
"organization" → "organ"  # Lost the "ize" (overstemming)

# Lancaster stemmer: even more aggressive
"organization" → "org"    # Completely loses meaning
```

Crosstem succeeds because it uses **linguistic knowledge**:

```python
# Graph data knows: organization DERIVED_FROM organize
"organization" → "organize"  # Preserves semantic relationship
```

## Data Sources

- **MorphyNet v1.0**: Derivational and inflectional morphology (CC BY-SA 4.0)
- **Wiktionary**: Cross-lingual etymology data (CC BY-SA 3.0)

## Citation

If you use this library in your research, please cite:

```bibtex
@software{crosstem2025,
  title={Crosstem: Comprehensive Morphological Analysis for Python},
  author={Avinash Bhojanapalli},
  year={2025},
  url={https://github.com/droidmaximus/crosstem},
  note={A Python package for derivational stemming, inflectional analysis, and cross-lingual etymology}
}

@inproceedings{batsuren2021morphynet,
  title={MorphyNet: a Large Multilingual Database of Derivational and Inflectional Morphology},
  author={Batsuren, Khuyagbaatar and Bella, Gábor and Giunchiglia, Fausto},
  booktitle={Proceedings of the 18th SIGMORPHON Workshop on Computational Research in Phonetics, Phonology, and Morphology},
  pages={39--48},
  year={2021}
}

@misc{wiktionary2025,
  title={Wiktionary, The Free Dictionary},
  author={{Wiktionary contributors}},
  year={2025},
  url={https://en.wiktionary.org/},
  note={Etymology data extracted from Wiktionary dumps}
}
```

## License

- Code: MIT License
- Data: CC BY-SA 4.0 (MorphyNet), CC BY-SA 3.0 (Wiktionary)
