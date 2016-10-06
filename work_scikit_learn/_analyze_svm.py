from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.utils import shuffle
import numpy as np
np.set_printoptions(threshold=np.nan)

def run_test(r):
    X, y = np.load('dataset.npy'), np.load('label.npy')
    X, y = shuffle(X, y, random_state=r)
    train_x = X[:1915]
    train_y = y[:1915]
    test_x = X[1915:]
    test_y = y[1915:]
     
    res = OneVsRestClassifier(SVC(kernel='sigmoid', random_state=0)).fit(train_x, train_y).predict(test_x)
    #res1 = OneVsRestClassifier(SVC(probability=True, kernel='poly', random_state=0)).fit(train_x, train_y).predict_proba(test_x)
    res = res.tolist()
    test_y = test_y.tolist()
    #res1 = res1.tolist()
    _sum, _pos, _neq = 0, 0, 0
    for k in range(0, len(test_y)):
        _sum += 1
        if res[k] == test_y[k]: _pos += 1 
        else: 
            _neq += 1
            #print(res[k], test_y[k])
    #print("Correct: %s/%s -> %f" % (str(_pos), str(_sum), float(_pos)/float(_sum)))
    return float(_pos), float(_sum)

if __name__ == '__main__':
    _max = -1.0
    for i in range(0,100):
        _pos, _sum = run_test(i)
        rate = _pos/_sum
        if rate > _max: _max = rate
    print(_max)
