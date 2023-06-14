import nltk   
import re         

def replace_break_line(text):
    return text.replace('\n', ' ')

def replace_links(text):
    return re.sub('http://\S+|https://\S+', '', text)

def pipeline(text, stopwords):
    words = nltk.word_tokenize(text.lower())                                    # separates in words
    filtered_words = [word for word in words if word not in stopwords]          # removes too much common words
    filtered_words = [replace_break_line(word) for word in filtered_words]      # removes break lines 
    filtered_words = [replace_links(word) for word in filtered_words]            # removes links
    return ' '.join(filtered_words)