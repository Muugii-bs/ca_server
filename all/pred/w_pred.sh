source /home/muugii/ca_prediction/venv/bin/activate 
cd /home/muugii/ca_prediction/all/pred
python _pred_news_collector_ext.py 0
cd /home/muugii/ca_prediction/all/pred/new_pred
find . -name "pred_all_*" -size -2b -delete
python _pred_contentParser.py
mv pred_all_*  /home/muugii/ca_prediction/all/pred/old_pred/ 
cd  /home/muugii/ca_prediction/all/pred/ 
python _pred_dateCollector.py 
deactivate
