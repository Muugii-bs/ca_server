cd /home/mugi/Analysis/twitter
#### ------ 7_
python analyze.py query_user "JRHokkaidoSap|jrhokkaido_jsb" 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result_user/7_all_keyword.txt 
mv senti.txt result_user/7_all_senti.txt 
mv histogram.txt result_user/7_all_histogram.txt 
python analyze.py query_user "JRHokkaidoSap|jrhokkaido_jsb" 2008-09-1200:00:00 2008-11-1200:00:00
mv keywords.txt result_user/7_core_keyword.txt 
mv senti.txt result_user/7_core_senti.txt 
mv histogram.txt result_user/7_core_histogram.txt 
#### ------ 13_
python analyze.py query_user lac_security 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result_user/13_all_keyword.txt 
mv senti.txt result_user/13_all_senti.txt 
mv histogram.txt result_user/13_all_histogram.txt 
python analyze.py query_user lac_security 2008-10-1500:00:00 2008-12-1500:00:00
mv keywords.txt result_user/13_core_keyword.txt 
mv senti.txt result_user/13_core_senti.txt 
mv histogram.txt result_user/13_core_histogram.txt 
#### ------ 15_
python analyze.py query_user "ExciteJapan|Excite_Bit|excite_music|ExciteAnime|Excite_ism" 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result_user/15_all_keyword.txt 
mv senti.txt result_user/15_all_senti.txt 
mv histogram.txt result_user/15_all_histogram.txt 
python analyze.py query_user "ExciteJapan|Excite_Bit|excite_music|ExciteAnime|Excite_ism" 2008-11-0300:00:00 2009-01-0300:00:00
mv keywords.txt result_user/15_core_keyword.txt 
mv senti.txt result_user/15_core_senti.txt 
mv histogram.txt result_user/15_core_histogram.txt 
#### ------ 23_
python analyze.py query_user puppine 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result_user/23_all_keyword.txt 
mv senti.txt result_user/23_all_senti.txt 
mv histogram.txt result_user/23_all_histogram.txt 
python analyze.py query_user puppine 2009-02-0700:00:00 2009-04-0700:00:00
mv keywords.txt result_user/23_core_keyword.txt 
mv senti.txt result_user/23_core_senti.txt 
mv histogram.txt result_user/23_core_histogram.txt 
