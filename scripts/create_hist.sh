cd /home/muugii/ca_prediction/scripts 

rm ./hist_result/all/count/*
rm ./hist_result/all/senti/*

rm ./hist_result/attack_category/count/*
rm ./hist_result/attack_category/senti/*

rm ./hist_result/attack_type/count/*
rm ./hist_result/attack_type/senti/*

rm ./hist_result/target_category/count/*
rm ./hist_result/target_category/senti/*

source ../venv/bin/activate 
python calculate_deviation.py 1> out_error/hist_exec 2> out_error/hist_err 
