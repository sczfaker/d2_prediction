import pandas as pd
import sys,io
import os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
file_to_fix_list=os.listdir("./data_recent_mmr/")
print (file_to_fix_list)
file_to_fix_list=["pmatches_list_ranking_0731_500.csv"]
for file_format_fix in file_to_fix_list:
	with open("./data_recent_mmr/"+file_format_fix,encoding="utf-8") as f:
		x=f.readlines()
		len_str=str(len(x)-1)
	print(len_str)
	row_title=x[0]
	row_title=["match_id","time","radiant_team","dire_team","radiant_win"]

	new_list=[]
	print (row_title)
	for line in x[1:]:
		one_line_list=line.split(" ")		
		new_oneline_list=[one_line_list[0][:-1],one_line_list[5][:-1]],,one_line_list[3][:-1],one_line_list[4][:-1]," ".join([one_line_list[1],one_line_list[2][:-1]])
		new_list.append(new_oneline_list)
	df=pd.DataFrame(new_list,columns=row_title)
	date_of_set=file_format_fix.split("_")[-2]
	df.to_csv("./data_recent_mmr/"+"exp_"+len_str+"_"+date_of_set+".csv",index=False)

"['5496024009,', '2020-07-02', '22:29:16,', '54,2,14,106,87,', '67,18,22,112,25,', 'False\n']"
