import spacy
import nltk
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import translators as ts
import translators.server as tss
import pkg_resources

# check if punkt is installed, if not, install it
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
# check if stopwords is installed, if not, install it
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
# check if wordnet is installed, if not, install it
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    
# check if averaged_perceptron_tagger is installed, if not, install it
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
    
# load the synonyms_pt_BR.parquet file to a dataframe using pkg_resources to avoid hardcoding the path
synonyms_df = pd.read_parquet(pkg_resources.resource_filename('data_augmentation_GASPLN', 'data/synonyms_pt_BR.parquet'))

def synonyms_replacement(text, percentage=0.5):
    tokens = nltk.word_tokenize(text)
    nlp = spacy.load('pt_core_news_sm')
    
    number_of_words = int(len(tokens) * percentage)
    indexes = np.random.choice(len(tokens), number_of_words, replace=False)
    
    for index in indexes:
        word = tokens[index]
        
        if len(word) == 1:
            continue
        
        syn_category = None
        for syn in synonyms_df.itertuples():
            if syn.word == word:
                syn_category = nlp(syn.synonyms[0])[0].pos_
                break
        
        if syn_category is None:
            continue
        
        word_category = nlp(word)[0].pos_
        
        if word_category != syn_category:
            continue
        
        synonyms = list(synonyms_df[synonyms_df['word'] == word]['synonyms'].values[0])
        
        if len(synonyms) == 0:
            continue
        
        synonym_index = np.random.randint(0, len(synonyms))
        tokens[index] = synonyms[synonym_index]
        
    return ' '.join(tokens)

def back_translation(sentence, languages=['en', 'es', 'pt'], translator='google'):
        
    # Check if the sentence is a string
    if not isinstance(sentence, str):
        raise ValueError('Sentence must be a string')
    
    # Check if the sentence is not empty
    if sentence == '':
        raise ValueError('Sentence must not be empty')
    
    # For the number of languages, translate the sentence to the next language using the specified translator (if the last language is not pt, add it as the last language)
    for i in range(len(languages) - 1):
        sentence = ts.translate_text(query_text=sentence, to_language=languages[i + 1], translator=translator)
        
    # If the last language is not pt, translate the sentence to pt
    if languages[-1] != 'pt':
        sentence = ts.translate_text(query_text=sentence, to_language='pt', translator=translator)

    return sentence