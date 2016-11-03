import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import operator as op
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

    def handle(self, index):
        max_count, data = 0.0, {}
        with open('result_content/' + index + '_histogram.txt', 'r') as fp:
            for line in fp:
                line = line.rstrip().split('\t')
                if not line[0][:10] in data: 
                    data[line[0][:10]] = {
                        'count': int(line[1]), 
                        'senti': 0.0
                    }
                if max_count < float(line[1]): max_count = float(line[1])
        with open('result_content/' + index + '_senti.txt', 'r') as fp:
            for line in fp:
                line = line.rstrip().split('\t')
                if line[0][:10] in data:
                    data[line[0][:10]]['senti'] = float(line[1])
        step  = len(data)/4
        label = sorted(data.items(), key=op.itemgetter(0))
        count = [float(y[1]['count']) / max_count for y in label]
        senti = [y[1]['senti'] for y in label]
        label = [dt.datetime.strptime(x[0], '%Y-%m-%d') for x in label]
        self.plot(label[:step], count[:step], label[:step], senti[:step], index + '_1.png', max_count)
        self.plot(label[step:2*step], count[step:2*step], label[step:2*step], senti[step:2*step], index + '_2.png', max_count)
        self.plot(label[2*step:3*step], count[2*step:3*step], label[2*step:3*step], senti[2*step:3*step], index + '_3.png', max_count)
        self.plot(label[3*step:], count[3*step:], label[3*step:], senti[3*step:], index + '_4.png', max_count)

    def plot(self, l1, y1, l2, y2, file_name, max_count):
        _, x = plt.subplots()
        plt.xlabel('date')
        plt.ylabel('blue: count (count/max_count), red: sentiment score')
        #plt.annotate('count/max(%s)' % str(max_count), xy=(l1[len(l1)/2], 1), xytext=(l1[len(l1)/2], 0.8))
        x.plot_date(l1, y1, 'b.-')
        x.plot_date(l1, y2, 'r.:')
        x.xaxis.set_major_locator(mticker.MaxNLocator(len(l1)/2))
        x.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        for label in x.xaxis.get_ticklabels():
            label.set_rotation(90)
        """
        x1 = plt.subplot(2, 1, 1)
        x1.plot(l1, y1, 'r.-')
        x2 = plt.subplot(2, 1, 2)
        x2.plot(l2, y2, 'r.-')
        x1.xaxis.set_major_locator(mticker.MaxNLocator(len(l1)/2))
        x1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        x2.xaxis.set_major_locator(mticker.MaxNLocator(len(l2)/2))
        x2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        for label in x1.xaxis.get_ticklabels():
            label.set_rotation(90)
        for label in x2.xaxis.get_ticklabels():
            label.set_rotation(90)
        plt.tight_layout()
        """
        plt.tight_layout()
        plt.savefig('images/' + file_name)

if __name__ == '__main__':
    g = Grapher()
    g.handle('111_all')
