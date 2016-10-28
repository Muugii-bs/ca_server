cd /home/mugi/Analysis/twitter
#### ------ 1_
python analyze.py query_content jpcert 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result/1_all_keyword.txt 
mv senti.txt result/1_all_senti.txt 
mv histogram.txt result/1_all_histogram.txt 
python analyze.py query_content jpcert 2008-08-3000:00:00 2008-10-3000:00:00
mv keywords.txt result/1_core_keyword.txt 
mv senti.txt result/1_core_senti.txt 
mv histogram.txt result/1_core_histogram.txt 
#### ------ 2_
python analyze.py query_content ゲームアーツ 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result/78_all_keyword.txt 
mv senti.txt result/78_all_senti.txt 
mv histogram.txt result/78_all_histogram.txt 
python analyze.py query_content ゲームアーツ 2009-11-0800:00:00 2010-01-0800:00:00
mv keywords.txt result/78_core_keyword.txt 
mv senti.txt result/78_core_senti.txt 
mv histogram.txt result/78_core_histogram.txt 
#### ------ 111_
python analyze.py query_content アッシュ 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result/111_all_keyword.txt 
mv senti.txt result/111_all_senti.txt 
mv histogram.txt result/111_all_histogram.txt 
python analyze.py query_content アッシュ 2009-12-0100:00:00 2010-02-0100:00:00
mv keywords.txt result/111_core_keyword.txt 
mv senti.txt result/111_core_senti.txt 
mv histogram.txt result/111_core_histogram.txt 
#### ------ 121_
python analyze.py query_content トヨタレンタリース 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result/121_all_keyword.txt 
mv senti.txt result/121_all_senti.txt 
mv histogram.txt result/121_all_histogram.txt 
python analyze.py query_content トヨタレンタリース 2009-12-0100:00:00 2010-02-0100:00:00
mv keywords.txt result/121_core_keyword.txt 
mv senti.txt result/121_core_senti.txt 
mv histogram.txt result/121_core_histogram.txt 
#### ------ 124_
python analyze.py query_content mont-bell 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result/124_all_keyword.txt 
mv senti.txt result/124_all_senti.txt 
mv histogram.txt result/124_all_histogram.txt 
python analyze.py query_content mont-bell 2009-11-2500:00:00 2010-01-2500:00:00
mv keywords.txt result/124_core_keyword.txt 
mv senti.txt result/124_core_senti.txt 
mv histogram.txt result/124_core_histogram.txt 
#### ------ 133_
python analyze.py query_content "ebook|イーブック" 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result/133_all_keyword.txt 
mv senti.txt result/133_all_senti.txt 
mv histogram.txt result/133_all_histogram.txt 
python analyze.py query_content "ebook|イーブック" 2010-01-1500:00:00 2010-03-1500:00:00
mv keywords.txt result/133_core_keyword.txt 
mv senti.txt result/133_core_senti.txt 
mv histogram.txt result/133_core_histogram.txt 
#### ------ 142_
python analyze.py query_content "サイバーガジェット" 2008-01-0100:00:00 2019-01-0300:00:00
mv keywords.txt result/142_all_keyword.txt 
mv senti.txt result/142_all_senti.txt 
mv histogram.txt result/142_all_histogram.txt 
python analyze.py query_content "サイバーガジェット" 2010-02-0900:00:00 2010-04-0900:00:00
mv keywords.txt result/142_core_keyword.txt 
mv senti.txt result/142_core_senti.txt 
mv histogram.txt result/142_core_histogram.txt 
