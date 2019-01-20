#!/usr/bin/env python
#encoding=utf-8
import os
import sys
import re
import xlrd
from collections import defaultdict




dir = "/online/home/chenff/X170001-p212-testing"
re_excel = os.path.join(dir,"复发临床资料_2018_0529.xlsx")
exon_excel = os.path.join(dir,"X170001外显子统计.xlsx")
sample_add = os.path.join(dir,"sample_add")

dict1 = {}
dict2 = {}
dict3 = {}
dict4 = {}
Recurrence_data = xlrd.open_workbook(re_excel)
Recurrence_table = Recurrence_data.sheets()[0]
nrows = Recurrence_table.nrows
Patient_col = Recurrence_table.col_values(1)
Pathology_col = Recurrence_table.col_values(12)
SEQnumber_col = Recurrence_table.col_values(27)

exon_data = xlrd.open_workbook(exon_excel)
exon_table = exon_data.sheets()[1]
SEQnumber_col_exon = exon_table.col_values(3)
SEQID_col= exon_table.col_values(1)
nrows_exon = exon_table.nrows
newproject_col = exon_table.col_values(0)


#print Recurrence_table.cell(1,0).ctype
#print Recurrence_table.cell(1,0).value.encode('utf-8')
#dict[Patient_col[4].encode('utf-8').decode('utf-8')] = 1
#print(dict)


for row in range(2,nrows):
	Patient_name = Patient_col[row].encode('utf-8').decode('utf-8')
	Pathologyid = Pathology_col[row].encode('utf-8').decode('utf-8')
	SEQnumber = str(int(SEQnumber_col[row])) if len(str(SEQnumber_col[row])) != 0 else 'NA'
	#print(SEQnumber);sys.exit()
	if ':'.join([Patient_name,Pathologyid]) in dict1:
		continue
	if len(Patient_name) == 0:
		continue
	if len(str(SEQnumber)) == 0:
		SEQnumber = "NA"
	dict2.setdefault(Patient_name,[]).append([Pathologyid,SEQnumber])
	dict1[ ':'.join([Patient_name,Pathologyid]) ] = 1
#print(dict2)


for row_exon in range(1,nrows_exon):
	SEQnumber_exon = SEQnumber_col_exon[row_exon]
	if isinstance(SEQnumber_exon,str):
		pass
	else:
		SEQnumber_exon = str(int(SEQnumber_exon)) 
	SEQID = SEQID_col[row_exon]
	#print(SEQID);sys.exit()
	dict3[SEQnumber_exon] = SEQID
with open (sample_add) as f_new:
	for infos_new in f_new:
		infos_new_split = infos_new.strip().split('\t')
		ch_id = str(infos_new_split[1])
		#print (ch_id);sys.exit()
		add_CHG_id = '_'.join([infos_new_split[2],'new'])
		if ch_id in dict3:
			dict3[ch_id] = add_CHG_id
		else:
			continue
print(dict3)

output_file = os.path.join(dir,'Name_Pathology_Seq.list')
output_h = open(output_file,'w')
for p_id in dict2.keys():
	output_h.write(p_id)
	for v in dict2[p_id]:
		#print(v);sys.exit()
		v_pathology = v[0]
		v_seqid = v[1]
		#output_h.write('\t'+'\t'.join(list(map(lambda x:str(x),v_pathology))))
		output_h.write('\t%s' %v_pathology)
		output_h.write('\t%s' %v_seqid)
		#print (dict3.keys())
		if v_seqid in dict3.keys():
			output_h.write('\t%s' % dict3[v_seqid])
		else:
			output_h.write('\tNA')
	output_h.write('\n')




