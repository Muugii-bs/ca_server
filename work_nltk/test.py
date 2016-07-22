import nltk
import sys

text = """IBM Leads 7.x, 8.1.0 before 8.1.0.14, 8.2, 8.5.0 before 8.5.0.7.3, 8.6.0 
        before 8.6.0.8.1, 9.0.0 through 9.0.0.4, 9.1.0 before 9.1.0.6.1, and 9.1.1 
        before 9.1.1.0.2 does not properly restrict the addition of links, which 
        makes it easier for remote authenticated users to conduct cross-site request 
        forgery (CSRF) attacks via unspecified vectors."""

def get_sturucture(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    print(sentences)

get_sturucture(text)
