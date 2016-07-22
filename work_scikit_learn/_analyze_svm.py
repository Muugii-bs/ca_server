from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import numpy as np
np.set_printoptions(threshold=np.nan)

def main():
    X, y = np.load('dataset.npy'), np.load('label.npy')
    #res = OneVsRestClassifier(LinearSVC(random_state=0)).fit(X, y).predict(X)
    res = OneVsRestClassifier(SVC(random_state=0)).fit(X, y).predict(X)
    res1 = OneVsRestClassifier(SVC(probability=True, random_state=0)).fit(X, y).predict_proba(X)
    res = res.tolist()
    y = y.tolist()
    _sum, _pos, _neq = 0, 0, 0
    for k in range(0, len(y)):
        _sum += 1
        if res[k] == y[k]: _pos += 1 
        else: 
            _neq += 1
            print(res1[k], res[k], y[k])
    print("Correct: %s/%s -> %f" % (str(_pos), str(_sum), float(_pos)/float(_sum)))

if __name__ == '__main__':
    main()
