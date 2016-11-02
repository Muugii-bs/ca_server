import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import datetime as dt
import matplotlib
import sys

class Grapher:

    def __init__(self):
        font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 8
        }
        matplotlib.rc('font', **font)
        plt.xlabel('date')

    def handle(self, index):
        with open('result_content/' + index + '_histogram.txt', 'r') as fp:
            h1, v1 = [], []
            for line in fp:
                line = line.rstrip().split('\t')
                h1.append(dt.datetime.strptime(line[0][:10], '%Y-%m-%d'))
                v1.append(int(line[1]))
        with open('result_content/' + index + '_senti.txt', 'r') as fp:
            h2, v2 = [], []
            for line in fp:
                line = line.rstrip().split('\t')
                h2.append(dt.datetime.strptime(line[0][:10], '%Y-%m-%d'))
                v2.append(float(line[1]))
        step = len(h1)/6
        self.plot(h1[:step], v1[:step], h1[step:2*step], v1[step:2*step], index + '_1.png')
        self.plot(h1[2*step:3*step], v1[2*step:3*step], h1[3*step:4*step], v1[3*step:4*step], index + '_2.png')
        self.plot(h1[4*step:5*step], v1[4*step:5*step], h1[5*step:], v1[5*step:], index + '_3.png')

    def plot(self, l1, y1, l2, y2, file_name):
        print l1, y1, l2, y2
        x1 = plt.subplot(2, 1, 1)
        x1.plot(l1, y1, 'r.-')
        x2 = plt.subplot(2, 1, 2)
        x2.plot(l2, y2, 'r.-')
        #x1.xaxis.set_major_locator(mticker.MaxNLocator(len(l1)))
        #x1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        #x2.xaxis.set_major_locator(mticker.MaxNLocator(len(l2)))
        #x2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        for label in x1.xaxis.get_ticklabels():
            label.set_rotation(90)
        for label in x2.xaxis.get_ticklabels():
            label.set_rotation(90)
        plt.tight_layout()
        plt.savefig('images/' + file_name)
        #plt.show()

if __name__ == '__main__':
    g = Grapher()
    g.handle('111_all')
