import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import operator as op
import datetime as dt
import matplotlib
import json
import sys
import os

class Grapher:

    def __init__(self, id_map, font, flag):
        matplotlib.rc('font', **font)
        self.id_map = {}
        self.flag   = flag
        with open(id_map, 'r') as fp:
            if id_map.endswith('.tsv'):
                    for line in fp:
                        line = line.rstrip().split()
                        self.id_map[line[0]] = line[1]
            elif id_map.endswith('.json'):
                self.id_map = json.load(fp)

    def handle(self, index):
        max_count, data = 0.0, {}
        id = index.split('_')[0]
        date = [dt.datetime.strptime(x, '%Y-%m-%d') for x in self.id_map[id]] if self.flag == '_attacker' else dt.datetime.strptime(self.id_map[id], '%Y-%m-%d') 
        _dir = 'result_content_attacker/' if self.flag == '_attacker' else 'result_content/'
        with open(_dir + index + '_histogram.txt', 'r') as fp:
            for line in fp:
                line = line.rstrip().split('\t')
                if not line[0][:10] in data: 
                    data[line[0][:10]] = {
                        'count': int(line[1]), 
                        'senti': 0.0
                    }
                if max_count < float(line[1]): max_count = float(line[1])
        with open(_dir + index + '_senti.txt', 'r') as fp:
            for line in fp:
                line = line.rstrip().split('\t')
                if line[0][:10] in data:
                    data[line[0][:10]]['senti'] = float(line[1])
        step  = len(data)/4
        label = sorted(data.items(), key=op.itemgetter(0))
        count = [float(y[1]['count']) / max_count for y in label]
        senti = [y[1]['senti'] for y in label]
        label = [dt.datetime.strptime(x[0], '%Y-%m-%d') for x in label]
        if self.flag == '_attacker':
            try:
                self.plot(label, count, label, senti, index + '.png', max_count, date)
            except Exception,e:
                print(e)
        else:
            try:
                self.plot(label[:step], count[:step], label[:step], senti[:step], index + '_1.png', max_count, [date,])
                self.plot(label[step:2*step], count[step:2*step], label[step:2*step], senti[step:2*step], index + '_2.png', max_count, [date,])
                self.plot(label[2*step:3*step], count[2*step:3*step], label[2*step:3*step], senti[2*step:3*step], index + '_3.png', max_count, [date,])
                self.plot(label[3*step:], count[3*step:], label[3*step:], senti[3*step:], index + '_4.png', max_count, [date,])
            except Exception,e:
                print(e)


    def plot(self, l1, y1, l2, y2, file_name, max_count, date):
        _, x = plt.subplots()
        plt.xlabel('date')
        plt.ylabel('blue: count (count/max_count), red: sentiment score')
        #plt.annotate('count/max(%s)' % str(max_count), xy=(l1[len(l1)/2], 1), xytext=(l1[len(l1)/2], 0.8))
        x.plot_date(l1, y1, 'b.-')
        x.plot_date(l1, y2, 'r.:')
        x.xaxis.set_major_locator(mticker.MaxNLocator(len(l1) * 2))
        x.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        for label in x.xaxis.get_ticklabels():
            label.set_rotation(90)
        #if date in l1:
        for d in date:
            plt.axvline(x=d, color='g')
        plt.tight_layout()
        plt.savefig('images%s/' % self.flag + file_name)

def plot_all():
    font = {'family' : 'normal',
            'weight' : 'normal',
            'size'   : 12
    }
    #g = Grapher('./result_content/id_map.tsv')
    g = Grapher('./result_content_attacker/date_map.json', font, '_attacker')
    _dir = sys.argv[1]
    for file in os.listdir(_dir):
	#if file.endswith(".txt") and '_all_' in file:
	if file.endswith(".txt"):
            if 'senti' in file:
                print file
                g.handle(file.split('_senti.txt')[0])
            elif 'histogram' in file:
                print file
                g.handle(file.split('_histogram.txt')[0])

if __name__ == '__main__':
    plot_all()
