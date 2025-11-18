Examples
========

Real-world examples of using Crosstem.

Text Preprocessing
------------------

Normalize documents for analysis::

   from crosstem import DerivationalStemmer
   
   def preprocess_document(text, language='eng'):
       """Normalize document by stemming to linguistic roots."""
       stemmer = DerivationalStemmer(language)
       
       words = text.lower().split()
       stems = [stemmer.stem(word) for word in words]
       
       return ' '.join(stems)
   
   # Example
   text = "The organization is organizing a conference for organizers"
   normalized = preprocess_document(text)
   print(normalized)
   # Output: "the organize is organize a conference for organize"

Information Retrieval
---------------------

Expand search queries with word families::

   from crossstem import DerivationalStemmer
   
   def expand_query(query, language='eng'):
       """Expand search query with all derivational forms."""
       stemmer = DerivationalStemmer(language)
       
       # Stem the query to find root
       root = stemmer.stem(query)
       
       # Get all words in the family
       family = stemmer.get_word_family(root)
       
       return sorted(family)
   
   # Example
   variants = expand_query('organize')
   print(f"Searching for: {', '.join(variants[:10])}...")
   # Searching for: disorganization, disorganize, organ, 
   # organic, organism, organization, organizational, ...

Document Similarity
-------------------

Compare documents using morphological roots::

   from crosstem import DerivationalStemmer
   from collections import Counter
   
   def document_similarity(doc1, doc2, language='eng'):
       """Calculate similarity based on shared roots."""
       stemmer = DerivationalStemmer(language)
       
       # Stem both documents
       roots1 = [stemmer.stem(w.lower()) for w in doc1.split()]
       roots2 = [stemmer.stem(w.lower()) for w in doc2.split()]
       
       # Count roots
       counter1 = Counter(roots1)
       counter2 = Counter(roots2)
       
       # Calculate overlap
       shared = set(counter1.keys()) & set(counter2.keys())
       total = len(set(counter1.keys()) | set(counter2.keys()))
       
       return len(shared) / total if total > 0 else 0
   
   # Example
   doc1 = "The organization organized an organizational meeting"
   doc2 = "We need to organize and create an organization"
   similarity = document_similarity(doc1, doc2)
   print(f"Similarity: {similarity:.2%}")  # ~71%

Topic Modeling Preprocessing
-----------------------------

Prepare text for topic modeling::

   from crosstem import DerivationalStemmer
   
   class MorphologicalTokenizer:
       def __init__(self, language='eng', min_length=3):
           self.stemmer = DerivationalStemmer(language)
           self.min_length = min_length
       
       def tokenize(self, text):
           """Tokenize and stem to roots."""
           words = text.lower().split()
           stems = []
           
           for word in words:
               # Remove punctuation
               word = ''.join(c for c in word if c.isalnum())
               
               if len(word) >= self.min_length:
                   stem = self.stemmer.stem(word)
                   stems.append(stem)
           
           return stems
   
   # Example with sklearn
   from sklearn.feature_extraction.text import CountVectorizer
   
   tokenizer = MorphologicalTokenizer()
   vectorizer = CountVectorizer(tokenizer=tokenizer.tokenize)
   
   documents = [
       "The organization organized a meeting",
       "Organizers are organizing the event",
       "She works for an organizational consultancy"
   ]
   
   X = vectorizer.fit_transform(documents)
   print(vectorizer.get_feature_names_out())
   # ['consultancy', 'event', 'meet', 'organize', 'she', 'work']

Historical Linguistics
----------------------

Track word evolution across languages::

   from crosstem import EtymologyLinker, download_etymology
   
   # Download etymology data (one-time)
   if not is_etymology_downloaded():
       download_etymology()
   
   def trace_word_origin(word, start_lang='English', max_depth=5):
       """Trace etymology back through ancestor languages."""
       linker = EtymologyLinker()
       
       chain = [(start_lang, word)]
       current_lang = start_lang
       current_word = word
       
       for _ in range(max_depth):
           etymology = linker.get_etymology(current_lang, current_word)
           
           if not etymology or 'INHERITED_FROM' not in etymology:
               break
           
           # Follow inheritance chain
           inherited = etymology['INHERITED_FROM'][0]
           chain.append((inherited['language'], inherited['word']))
           current_lang = inherited['language']
           current_word = inherited['word']
       
       return chain
   
   # Example
   origin_chain = trace_word_origin('organize')
   for lang, word in origin_chain:
       print(f"{lang}: {word}")
   # English: organize
   # Middle English: organisen
   # Old French: organiser
   # Late Latin: organizare
   # ...

Corpus Analysis
---------------

Analyze word relationships in a corpus::

   from crosstem import DerivationalStemmer
   from collections import defaultdict
   
   def analyze_word_families(corpus, language='eng', top_n=10):
       """Find most productive word families in corpus."""
       stemmer = DerivationalStemmer(language)
       
       # Group words by root
       families = defaultdict(set)
       
       for word in corpus:
           root = stemmer.stem(word.lower())
           families[root].add(word.lower())
       
       # Sort by family size
       sorted_families = sorted(
           families.items(),
           key=lambda x: len(x[1]),
           reverse=True
       )
       
       # Return top N
       return sorted_families[:top_n]
   
   # Example
   corpus = [
       'organize', 'organization', 'organizational', 'organizer',
       'organizing', 'reorganize', 'disorganize', 'beauty',
       'beautiful', 'beautifully', 'beautify', 'run', 'running',
       'runner', 'ran', 'rerun'
   ]
   
   top_families = analyze_word_families(corpus, top_n=3)
   for root, members in top_families:
       print(f"{root}: {len(members)} variants - {sorted(members)}")
   # organize: 7 variants - [disorganize, organization, ...]
   # beauty: 4 variants - [beautify, beautiful, ...]
   # run: 5 variants - [ran, rerun, run, runner, running]

Multilingual Processing
-----------------------

Process documents in multiple languages::

   from crossstem import DerivationalStemmer
   
   class MultilingualStemmer:
       def __init__(self, languages):
           self.stemmers = {
               lang: DerivationalStemmer(lang)
               for lang in languages
           }
       
       def stem(self, word, language):
           """Stem word in specified language."""
           if language not in self.stemmers:
               raise ValueError(f"Unsupported language: {language}")
           return self.stemmers[language].stem(word)
       
       def stem_document(self, document, language):
           """Stem entire document."""
           words = document.split()
           return [self.stem(word, language) for word in words]
   
   # Example
   stemmer = MultilingualStemmer(['eng', 'fra', 'deu'])
   
   # English
   print(stemmer.stem('organization', 'eng'))  # organize
   
   # French
   print(stemmer.stem('organisation', 'fra'))  # organiser
   
   # German
   print(stemmer.stem('Organisation', 'deu'))  # organisieren

Named Entity Recognition
-------------------------

Normalize entity variations::

   from crosstem import DerivationalStemmer
   
   def normalize_entities(entities, language='eng'):
       """Normalize entity mentions to canonical forms."""
       stemmer = DerivationalStemmer(language)
       
       normalized = {}
       for entity in entities:
           words = entity.split()
           roots = [stemmer.stem(w.lower()) for w in words]
           canonical = ' '.join(roots)
           
           if canonical not in normalized:
               normalized[canonical] = []
           normalized[canonical].append(entity)
       
       return normalized
   
   # Example
   entities = [
       "United Nations Organization",
       "UN Organization",
       "Organizational Structure",
       "Organizing Committee"
   ]
   
   grouped = normalize_entities(entities)
   for canonical, variants in grouped.items():
       print(f"{canonical}: {variants}")

Question Answering
------------------

Improve QA by matching word roots::

   from crosstem import DerivationalStemmer
   
   def find_relevant_passages(question, passages, language='eng'):
       """Find passages relevant to question using root matching."""
       stemmer = DerivationalStemmer(language)
       
       # Stem question
       q_roots = set(stemmer.stem(w.lower()) for w in question.split())
       
       # Score passages
       scored = []
       for passage in passages:
           p_roots = set(stemmer.stem(w.lower()) for w in passage.split())
           overlap = len(q_roots & p_roots)
           scored.append((overlap, passage))
       
       # Return sorted by relevance
       scored.sort(reverse=True, key=lambda x: x[0])
       return [passage for _, passage in scored]
   
   # Example
   question = "How do organizations organize their structure?"
   
   passages = [
       "Companies use organizational charts to show structure.",
       "The meeting was well organized by the committee.",
       "Trees provide shade in the summer."
   ]
   
   relevant = find_relevant_passages(question, passages)
   print("Most relevant:", relevant[0])
   # "Companies use organizational charts to show structure."

Text Classification Features
-----------------------------

Generate morphological features::

   from crossstem import DerivationalStemmer
   from sklearn.feature_extraction.text import CountVectorizer
   
   class MorphologicalVectorizer:
       def __init__(self, language='eng'):
           self.stemmer = DerivationalStemmer(language)
           self.vectorizer = CountVectorizer()
       
       def fit_transform(self, documents):
           # Stem all documents
           stemmed_docs = [
               ' '.join(self.stemmer.stem(w) for w in doc.split())
               for doc in documents
           ]
           return self.vectorizer.fit_transform(stemmed_docs)
       
       def transform(self, documents):
           stemmed_docs = [
               ' '.join(self.stemmer.stem(w) for w in doc.split())
               for doc in documents
           ]
           return self.vectorizer.transform(stemmed_docs)
   
   # Example with classification
   from sklearn.naive_bayes import MultinomialNB
   
   vectorizer = MorphologicalVectorizer()
   classifier = MultinomialNB()
   
   X_train = vectorizer.fit_transform(train_documents)
   classifier.fit(X_train, train_labels)
   
   X_test = vectorizer.transform(test_documents)
   predictions = classifier.predict(X_test)
