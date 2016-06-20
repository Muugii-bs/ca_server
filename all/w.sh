source /home/muugii/ca_prediction/venv/bin/activate 
cd /home/muugii/ca_prediction/all 
python _news_collector_ext.py $1
mv all_* new
cd /home/muugii/ca_prediction/all/new/ 
find . -name "all_*" -size -2b -delete
deactivate
