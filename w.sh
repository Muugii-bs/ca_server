cd /home/mugi/Analysis/tf_news
source venv/bin/activate 

for i in 1 2 3 4 5
do
  python analyze_keyword.py obama.json
  python create_dataset.py on_obama.tsv
  python run.py >> result_keyword/obama_on_words_20161109 
  python create_dataset.py off_obama.tsv
  python run.py >> result_keyword/obama_off_words_20161109 

  python analyze_keyword.py uber.json
  python create_dataset.py on_uber.tsv
  python run.py >> result_keyword/uber_on_words_20161109 
  python create_dataset.py off_uber.tsv
  python run.py >> result_keyword/uber_off_words_20161109 

  python analyze_keyword.py indiana.json
  python create_dataset.py on_indiana.tsv
  python run.py >> result_keyword/indiana_on_words_20161109 
  python create_dataset.py off_indiana.tsv
  python run.py >> result_keyword/indiana_off_words_20161109 
done
