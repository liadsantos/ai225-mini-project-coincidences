import nltk   

def replace_links(text):
    """
    Replace 'http' or 'https' in tokenized sentences
    """
    return text.replace('https', '').replace('http://', '')

def pipeline(text, stopwords):
    """
    Define a pipeline to pre-process the text arrived
    """
    words = nltk.word_tokenize(text.lower())                                    # separates in words
    filtered_words = [word.lower() for word in words if word.isalpha()]         # removes characters that are not english
    filtered_words = [word for word in filtered_words if word not in stopwords] # removes too much common words
    filtered_words = [replace_links(word) for word in filtered_words]           # removes links
    return ' '.join(filtered_words)

def set_sentiment(comp_score):
    """
    Define a sentiment according compound.
    The sum of pos, neg, neu intensities give 1. 
    Compound ranges from -1 to 1 and is the metric used to draw the overall sentiment.
    """
    if (comp_score <= -0.5):
        s_analysis = 'neg'
    elif (comp_score > -0.5 and comp_score < 0.5):
        s_analysis = 'neu'
    else:
        s_analysis = 'pos'

    return s_analysis