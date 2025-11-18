Algorithm
=========

This page explains the graph-based algorithm that powers Crosstem's derivational stemming.

Graph Representation
--------------------

Crosstem treats morphology as a **graph problem** instead of a rules-based problem:

* **Nodes**: Individual words (e.g., "organize", "organization", "organizational")
* **Edges**: Derivational relationships (DERIVED_FROM connections)
* **Graph Structure**: Pre-computed from MorphyNet linguistic data, stored as nested JSON dictionaries

Why Graph-Based?
----------------

Traditional stemmers use suffix-stripping rules::

   # Porter Stemmer approach
   "organizational" → strip "al" → "organization" 
                    → strip "tion" → "organiz"
                    → ERROR: overstemming

Graph-based approach::

   # Crosstem approach
   "organizational" → DERIVED_FROM → "organization"
                    → DERIVED_FROM → "organize"
                    → [STOP: root found]

BFS Traversal
-------------

Crosstem uses **Breadth-First Search (BFS)** to find the morphological root:

1. Start at the input word
2. Explore all words it derives from (direct parents)
3. Score each candidate based on linguistic features
4. Continue traversing until reaching the best root
5. Maximum depth: 3 hops

Multi-Hop Example
~~~~~~~~~~~~~~~~~

::

   "organizational" (adjective)
        ↓ hop 1
   "organization" (noun)
        ↓ hop 2
   "organize" (verb) ← ROOT FOUND

This 2-hop traversal is impossible for single-pass suffix strippers.

Scoring Function
----------------

At each hop, candidates are scored based on three factors:

1. **Word Length** (shorter = better)
   
   * Penalty: +2 points per hop depth
   * Rationale: Roots tend to be shorter than derivatives

2. **Part of Speech** (verbs = roots)
   
   * Verbs: -10 points (strong preference)
   * Nouns: -5 points (moderate preference)
   * Rationale: Many derivations start from verbal roots

3. **Productivity** (high derivatives = real root)
   
   * Must exceed language-specific threshold
   * Filters out archaic/rare words
   * Example: "run" (33 derivatives) vs "hap" (8 derivatives)

Scoring Example
~~~~~~~~~~~~~~~

::

   Candidate: "organize" (verb, 13 derivations)
   - Length penalty: +2 (depth 2)
   - POS bonus: -10 (verb)
   - Productivity: ✓ passes threshold (≥5 for English verbs)
   - Final score: -8 (lower is better)
   
   Candidate: "hap" (noun, 8 derivations)
   - Length penalty: +2 (depth 2)  
   - POS bonus: -5 (noun)
   - Productivity: ✗ fails threshold (≥9 for English nouns)
   - Result: FILTERED OUT

Productivity Thresholds
-----------------------

Different languages have different morphological productivity. Thresholds are calibrated per language:

English (Rich Morphology)
~~~~~~~~~~~~~~~~~~~~~~~~~

* Verbs: ≥5 derivations
* Nouns: ≥9 derivations
* Rationale: English has extensive derivational morphology

French/Italian (Moderate)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Verbs: ≥4 derivations
* Nouns: ≥5 derivations
* Rationale: Romance languages have moderate productivity

Russian/Slavic (Low)
~~~~~~~~~~~~~~~~~~~~

* Verbs: ≥3 derivations
* Nouns: ≥2-3 derivations
* Rationale: Slavic morphology relies more on inflection than derivation

German (Compound-Heavy)
~~~~~~~~~~~~~~~~~~~~~~~

* Verbs: ≥4 derivations
* Nouns: ≥3 derivations
* Rationale: German uses compounding more than derivation

Why Faster Than Porter?
------------------------

Porter Stemmer
~~~~~~~~~~~~~~

* Applies regex rules sequentially on every character
* Multiple conditional branches
* String manipulation at each step
* ~90,000 words/second

Crosstem
~~~~~~~~

* Hash table lookup (O(1) average case)
* Pre-computed graph stored in memory
* No regex, no string manipulation
* Just dictionary access + BFS traversal
* ~547,000 words/second

**Result: 6× faster while being more accurate**

Algorithm Pseudocode
--------------------

::

   function find_root(word, language):
       graph = load_graph(language)
       
       if word not in graph:
           return word  # Unknown word, return as-is
       
       queue = [(word, 0)]  # (word, depth)
       visited = set()
       best_candidate = word
       best_score = infinity
       
       while queue:
           current, depth = queue.pop(0)
           
           if depth > MAX_DEPTH:
               break
           
           for parent in graph[current].derives_from:
               if parent in visited:
                   continue
               
               visited.add(parent)
               
               # Check productivity threshold
               if not meets_productivity(parent, language):
                   continue
               
               # Score candidate
               score = calculate_score(parent, depth)
               
               if score < best_score:
                   best_score = score
                   best_candidate = parent
               
               # Add to queue for further exploration
               queue.append((parent, depth + 1))
       
       return best_candidate

Limitations
-----------

Data Quality
~~~~~~~~~~~~

The algorithm is only as good as the input data:

* Bad edges in MorphyNet → wrong roots
* Example: "democracy" incorrectly derives from "democrat" in the data
* Mitigation: Productivity filtering catches many errors

Arbitrary Thresholds
~~~~~~~~~~~~~~~~~~~~

Productivity thresholds are calibrated empirically:

* Based on percentile analysis of each language
* May not generalize to all domains
* Trade-off between precision and coverage

Finite Corpus
~~~~~~~~~~~~~

The graph only contains words in MorphyNet:

* Domain-specific jargon not included
* Neologisms and slang missing
* Historical/archaic terms may be incomplete

Future Improvements
-------------------

Potential enhancements to the algorithm:

1. **Contextual scoring**: Consider surrounding words in sentences
2. **Frequency weighting**: Prefer common words over rare ones
3. **Semantic similarity**: Use embeddings to validate derivational relationships
4. **Dynamic thresholds**: Learn optimal thresholds per corpus
5. **Error correction**: Detect and fix bad edges in the graph

References
----------

* MorphyNet: https://morphynet.org/
* BFS algorithm: https://en.wikipedia.org/wiki/Breadth-first_search
* Derivational morphology: https://en.wikipedia.org/wiki/Derivation_(linguistics)
