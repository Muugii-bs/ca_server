from pprint import pprint
import os

for i in os.listdir(os.getcwd()):
	if i.startswith("all_"): 
		with open(i, 'r') as fp:
			print i
			content = fp.read()
				
