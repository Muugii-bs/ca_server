#!/bin/bash
source ~/ca_prediction/venv/bin/activate
for (( c=$1; c<50000; c=c+50 ))
do
   cd /home/muugii/vulnerability/html  
   d=$(expr 50 + $c)
   python download_exploit_fix1.py $c $d
   mv *.txt storage
   cd /home/muugii/vulnerability/html/storage 
   python fetch_exploit_content.py
   echo "execution No: $c, $d"
done
