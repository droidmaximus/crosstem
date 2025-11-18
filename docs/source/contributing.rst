Contributing
============

We welcome contributions to Crosstem! This guide explains how to contribute.

Ways to Contribute
-------------------

* **Bug reports**: Found an issue? Report it on GitHub
* **Feature requests**: Suggest new features or improvements
* **Code contributions**: Submit pull requests with fixes or enhancements
* **Documentation**: Improve docs, add examples, fix typos
* **Language data**: Add support for new languages
* **Testing**: Write tests, report edge cases

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

1. Fork the repository on GitHub
2. Clone your fork locally::

      git clone https://github.com/YOUR_USERNAME/crossstem.git
      cd crossstem

3. Create a virtual environment::

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install in development mode::

      pip install -e .

5. Install development dependencies::

      pip install pytest black flake8 mypy

Running Tests
~~~~~~~~~~~~~

::

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=crossstem

   # Run specific test file
   pytest tests/test_stemmer.py

Code Style
~~~~~~~~~~

We use Black for formatting and flake8 for linting::

   # Format code
   black crossstem/

   # Check linting
   flake8 crossstem/

   # Type checking
   mypy crossstem/

Reporting Bugs
--------------

Before reporting a bug:

1. Check if it's already reported in GitHub Issues
2. Make sure you're using the latest version
3. Test with a minimal reproducible example

Bug Report Template
~~~~~~~~~~~~~~~~~~~

::

   **Describe the bug**
   A clear description of what the bug is.

   **To Reproduce**
   Steps to reproduce the behavior:
   1. Import Crossstem
   2. Call stemmer.stem('word')
   3. See error

   **Expected behavior**
   What you expected to happen.

   **Actual behavior**
   What actually happened.

   **Environment**
   - OS: [e.g., Windows 10, Ubuntu 22.04]
   - Python version: [e.g., 3.9.7]
   - Crossstem version: [e.g., 0.2.0]

   **Minimal example**
   ```python
   from crossstem import DerivationalStemmer
   stemmer = DerivationalStemmer('eng')
   print(stemmer.stem('problematic_word'))
   ```

Feature Requests
----------------

We're open to new features! Please describe:

1. **Use case**: Why is this feature needed?
2. **Proposal**: How should it work?
3. **Examples**: Show example usage
4. **Alternatives**: What alternatives exist?

Pull Requests
-------------

PR Checklist
~~~~~~~~~~~~

Before submitting a PR:

- [ ] Code follows the project style (Black + flake8)
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages are clear

PR Process
~~~~~~~~~~

1. Create a feature branch::

      git checkout -b feature/amazing-feature

2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Commit with clear messages::

      git commit -m "Add amazing feature"

6. Push to your fork::

      git push origin feature/amazing-feature

7. Open a Pull Request on GitHub

Adding Languages
----------------

To add support for a new language:

Data Requirements
~~~~~~~~~~~~~~~~~

1. **Derivational data**: MorphyNet-compatible JSON format
2. **Inflectional data**: UniMorph-compatible TSV format  
3. **Minimum coverage**: At least 20,000 words
4. **License**: Must be open license (CC BY-SA or similar)

Format Example
~~~~~~~~~~~~~~

Derivational data (``<lang>_derivations.json``)::

   {
       "word1": {
           "derives_from": ["parent1", "parent2"],
           "derives_to": ["child1", "child2"],
           "pos": "V"
       },
       "word2": {
           "derives_from": [],
           "derives_to": ["child3"],
           "pos": "N"
       }
   }

Calibrating Thresholds
~~~~~~~~~~~~~~~~~~~~~~~

1. Analyze productivity distribution::

      python scripts/analyze_productivity.py <lang>

2. Set thresholds in ``crossstem/stemmer.py``::

      PRODUCTIVITY_THRESHOLDS = {
          'new': {'V': 3, 'N': 4},  # Your language
          # ... existing languages
      }

3. Test stemming quality::

      python scripts/test_language.py <lang>

4. Adjust thresholds based on results

Adding Tests
~~~~~~~~~~~~

Create ``tests/test_<lang>.py``::

   def test_<lang>_stemming():
       stemmer = DerivationalStemmer('<lang>')
       
       # Test cases
       assert stemmer.stem('word1') == 'expected_root1'
       assert stemmer.stem('word2') == 'expected_root2'
       
       # Multi-hop cases
       assert stemmer.stem('derived_word') == 'root'

Documentation Updates
~~~~~~~~~~~~~~~~~~~~~

1. Add language to ``docs/source/languages.rst``
2. Update README.md with new language count
3. Add examples in ``docs/source/examples.rst``

Improving Algorithm
-------------------

If you have ideas for improving the BFS algorithm:

1. Open an issue to discuss the approach
2. Provide benchmark results showing improvement
3. Include examples of edge cases it handles better
4. Ensure it doesn't regress existing behavior

Testing Strategy
~~~~~~~~~~~~~~~~

* Benchmark against Porter on common word lists
* Test accuracy on hand-labeled examples
* Measure speed with large corpora
* Verify behavior across all 15 languages

Code Organization
-----------------

Project Structure
~~~~~~~~~~~~~~~~~

::

   crossstem/
   ├── __init__.py          # Package exports
   ├── stemmer.py           # DerivationalStemmer class
   ├── analyzer.py          # InflectionAnalyzer class
   ├── etymology_linker.py  # EtymologyLinker class
   ├── download.py          # Etymology download utilities
   ├── exceptions.py        # Custom exceptions
   └── data/                # Language data files

Testing Structure
~~~~~~~~~~~~~~~~~

::

   tests/
   ├── test_stemmer.py      # Stemming tests
   ├── test_analyzer.py     # Inflection tests
   ├── test_etymology.py    # Etymology tests
   └── test_<lang>.py       # Language-specific tests

Adding Documentation
--------------------

Documentation is built with Sphinx and hosted on Read the Docs.

Local Build
~~~~~~~~~~~

::

   cd docs/
   pip install -r requirements.txt
   make html

View at ``docs/build/html/index.html``

Adding Pages
~~~~~~~~~~~~

1. Create ``docs/source/<page>.rst``
2. Add to ``index.rst`` table of contents
3. Build and verify locally
4. Submit PR

Docstring Style
~~~~~~~~~~~~~~~

Use Google-style docstrings::

   def stem(self, word: str) -> str:
       """Find the morphological root of a word.
       
       Args:
           word: The word to stem
           
       Returns:
           The morphological root
           
       Example:
           >>> stemmer = DerivationalStemmer('eng')
           >>> stemmer.stem('organization')
           'organize'
       """

Code Review Process
-------------------

All PRs are reviewed by maintainers. We look for:

* **Correctness**: Does it work as intended?
* **Tests**: Is it well-tested?
* **Documentation**: Is it documented?
* **Style**: Does it follow conventions?
* **Performance**: Does it maintain speed?

Feedback may include:

* Requests for changes
* Suggestions for improvements
* Questions about design decisions

Please be patient and constructive in discussions.

Release Process
---------------

Versioning
~~~~~~~~~~

We follow Semantic Versioning (semver):

* **MAJOR**: Incompatible API changes
* **MINOR**: New features, backwards-compatible
* **PATCH**: Bug fixes, backwards-compatible

Maintainer Responsibilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Review and merge PRs
2. Update CHANGELOG.md
3. Create GitHub releases
4. Publish to PyPI
5. Update documentation

Community Guidelines
--------------------

* Be respectful and constructive
* Focus on the issue, not the person
* Assume good intentions
* Ask questions when unclear
* Give credit to contributors

License
-------

By contributing, you agree that your contributions will be licensed under the MIT License.

Questions?
----------

* Open an issue on GitHub
* Tag maintainers: @droidmaximus

Thank you for contributing to Crossstem!
