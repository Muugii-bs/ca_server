import nltk 

#{{{
black_list = [',', '.', ';', ':', '-', '~', '_', '?', '!', 'the', 'in', 
              'on', 'at', 'a', 'an', 'does', 'do', 'allows', 'allow', 
              'attackers', 'attacker', 'remote', 'by', 'with', 'through', 
              'or', 'is', 'are', 'to', 'as', 'without', 'via', 'of', 'and',
              'have', 'has', 'had', 'must', 'should', ')', '(', ']', '[',
              '{', '}', "''", "'", '"', '""', "``", '`', 'not', '..', ',,', 
              '.,', ',.', '--', '~~', '::', ';;', '+', '++', 'than', 'other',
              'it', 'its', 'for', 'along', 'be', 'it\'s', 'these', 'this',
              'these', 'those', 'into', "'s"]
#}}}

def get_tokens(text):
    tokens = nltk.word_tokenize(text)
    tokens = [x.lower() for x in tokens]
    tokens = list(set(tokens) - set(black_list))
    return tokens

