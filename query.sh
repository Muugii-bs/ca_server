# user?content id keyword start end
cd /home/mugi/Analysis/twitter
all_keyword='_all_keyword.txt'
all_senti='_all_senti.txt'
all_histogram='_all_histogram.txt'
core_keyword='_core_keyword.txt'
core_senti='_core_senti.txt'
core_histogram='_core_histogram.txt'
query='query_'
dir='result_'
python analyze.py $query$1 "$3" 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt $dir$1/$2$all_keyword 
mv senti.txt $dir$1/$2$all_senti
mv histogram.txt $dir$1/$2$all_histogram 
python analyze.py $query$1 "$3" $4 $5
mv keywords.txt $dir$1/$2$core_keyword
mv senti.txt $dir$1/$2$core_senti 
mv histogram.txt $dir$1/$2$core_histogram
find ./$dir$1 -size 0c -delete
