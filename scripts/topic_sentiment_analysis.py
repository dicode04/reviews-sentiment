# -*- coding: utf-8 -*-

### Import libraries ###
import nltk
import gensim
nltk.download('wordnet')
import matplotlib.pyplot as plt

from topic_sentiment_data_preparation import bag_of_words, create_dictionary, tf_idf, preprocessing_reviews, preprocessing_reviews_top_products

### Functions ###
def evaluate_topic(corpus, num_topics, dictionary, texts):
    coherence = []
    for n in range(1, num_topics):
        model = gensim.models.LdaMulticore(corpus=corpus, 
                                           num_topics=n, 
                                           random_state=42, 
                                           id2word=dictionary, 
                                           passes=2, 
                                           workers=2,
                                           alpha=0.01,
                                           eta=0.0001,
                                           per_word_topics=True)
        cm = gensim.models.ldamodel.CoherenceModel(model=model, dictionary=dictionary, coherence='c_v', texts=texts)
        coherence.append(cm.get_coherence())
        print('\nNumber of topic:', n)
        for idx, topic in model.print_topics(-1):
            print('\nTopic: {} \nWords: {}'.format(idx, topic))    
    return coherence
        

def plot_coherence(num_topics, coherence):
    x_axis = range(1, num_topics)
    plt.plot(x_axis, coherence)
    plt.xlabel("Number of topics")
    plt.ylabel("Coherence score")
    plt.show()
    
    
def run(df):
    #preprocessed_reviews = preprocessing_reviews(df)
    # Da stella: the main assumption underlying LDA is that document exhibit multiple topics
    # Usare più prodotti (top 20?), Stella fa l'esempio considerando un corpus di articoli di giornale per trovare i vari topic
    top_products = 20
    preprocessed_reviews = preprocessing_reviews_top_products(df, top_products)
    #preprocessing
    dictionary = create_dictionary(df, preprocessed_reviews)
    num_topics = 10
    
    # LDA using Bag of Words
    bow_corpus = bag_of_words(df, preprocessed_reviews)
    coherence_bow = evaluate_topic(corpus=bow_corpus, num_topics=num_topics, dictionary=dictionary, texts=preprocessed_reviews)
    plot_coherence(num_topics=num_topics, coherence=coherence_bow)
       
    # LDA using Tf-Idf
    corpus_tfidf = tf_idf(df, bow_corpus)
    coherence_tfidf = evaluate_topic(corpus=corpus_tfidf, num_topics=num_topics, dictionary=dictionary, texts=preprocessed_reviews)
    plot_coherence(num_topics=num_topics, coherence=coherence_tfidf)
'''
#%% FERRI E BASSO
def topic_based_tokenization(reviews):
    tokenizedReviews = {}
    key = 1
    #stopwords = nltk.corpus.stopwords.words("english")
    regexp = re.compile(r'\?')
    for review in reviews:
        for sentence in nltk.sent_tokenize(review):
            #logic to remove questions and errors
            if regexp.search(sentence):
                print("removed")
            else:
                sentence=re.sub(r'\(.*?\)','',sentence)
                tokenizedReviews[key]=sentence
                key += 1

    for key,value in tokenizedReviews.items():
        print(key,' ',value)
        tokenizedReviews[key]=value
    return tokenizedReviews

#%%
reviews_values = df_product.reviewText.values
reviews = [reviews_values[i] for i in range(len(reviews_values))]

#%%
reviews_filtered = removing_stop_words(reviews)
reviews_tokenized = topic_based_tokenization(reviews_filtered)
'''