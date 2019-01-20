#!/usr/bin/env python

import os
import sys
import re
import xlrd
from collections import defaultdict
 
dir = "/online/home/chenff/X170001-p212-testing"
exon_excel = os.path.join(dir,"X170001外显子统计.xlsx")
 
exon_data = xlrd.open_workbook(exon_excel)
exon_table = exon_data.sheets()[1]
SEQID_col= exon_table.col_values(1)
nrows_exon = exon_table.nrows
newproject_col = exon_table.col_values(0)
 
dict = {}
for np in range(1,nrows_exon):
    newproject = newproject_col[np]
    newCHGid = SEQID_col[np]
    dict[newCHGid] = newproject
#print (dict['CHG033826']);sys.exit()


#tools dir
java = "/online/software/jdk1.8.0_111/bin/java"
gatk = "/online/software/GenomeAnalysisTK-3.7/GenomeAnalysisTK.jar"
dir = "/online/home/chenff/X170001-p212-testing"


#data dir 
genome_fasta = "/online/databases/Homo_sapiens/hg38/hg38bundle/Homo_sapiens_assembly38.fasta"
exon_bed = "/online/home/wanghn/data/SureSelect/hg38/v6/hg38_Agilent_V6_100bp_stand.bed"

mem_aln = "20G"
prefix = sys.argv[1]
project = sys.argv[2]
user = sys.argv[3]
out_dir = os.path.join(prefix,project)
pbs_dir = "/online/home/chenff/X170001-p212-testing/pbs_varscan"

list = os.path.join(dir,'sample_seq_pair_20180807.txt')

info_dict = {}
qsub_mutect = os.path.join(out_dir,'qub_varscan.sh')
qsub = open(qsub_mutect,'w')
qsub.write('#!/bin/bash\n')


with open (list) as f_bam:
    for line in f_bam:
        infos = re.split('\t',line.strip())
        for info in infos:
            if re.search('_new$',info):
                for info_2 in infos:
                    if (':'.join([info,info_2]) not in info_dict and ':'.join([info_2,info]) not in info_dict) \
                        and info_2 != info and re.search('CHG',info_2):
                        info_dict[':'.join([info,info_2])] = 1
                        info_dict[':'.join([info_2,info])] = 1
for info in info_dict.keys():
    infos = info.split(':')
    normal_bam_id = infos[0]
    tumor_bam_id = infos[1]
    if re.search('_new$',normal_bam_id):
        normal_bam_id = normal_bam_id.strip('_new')
        normal_bam = os.path.join(out_dir,normal_bam_id,normal_bam_id+'.ready.bam')
        if re.search('_new$',tumor_bam_id):
            tumor_bam_id = tumor_bam_id.strip('_new')
            tumor_bam = os.path.join(out_dir,tumor_bam_id,tumor_bam_id+'.ready.bam')
            tumor_dir = os.path.join(out_dir,tumor_bam_id)
        else:
            tumor_bam = os.path.join(prefix,dict[tumor_bam_id],tumor_bam_id,'out',tumor_bam_id+'.ready.bam')
            tumor_dir = os.path.join(prefix,dict[tumor_bam_id],tumor_bam_id,'out')
    if re.search('_new$',tumor_bam_id):
        tumor_bam_id = tumor_bam_id.strip('_new')
        tumor_bam = os.path.join(out_dir,tumor_bam_id,tumor_bam_id+'.ready.bam')
        tumor_dir = os.path.join(out_dir,tumor_bam_id)
        if re.search('_new$',normal_bam_id):
            normal_bam_id = normal_bam_id.strip('_new')
            normal_bam = os.path.join(out_dir,normal_bam_id,normal_bam_id+'.ready.bam')
        else:
            normal_bam = normal_bam = os.path.join(prefix,dict[normal_bam_id],normal_bam_id,'out',normal_bam_id+'.ready.bam')
        
    pbs_file = os.path.join(pbs_dir, '%s_%s_varscan.pbs' % (normal_bam_id,tumor_bam_id))
    pbs = open(pbs_file, 'w')
    #print (pbs_file);sys.exit()
    PBS_N = '#PBS -N %s_%s\n' % (normal_bam_id,tumor_bam_id)
    PBS_o = '#PBS -o %s/%s_%s_varscan.out\n' % (out_dir,normal_bam_id,tumor_bam_id)
    PBS_e = '#PBS -e %s/%s_%s_varscan.err\n' % (out_dir,normal_bam_id,tumor_bam_id)
    PBS_l = '#PBS -l nodes=1:ppn=10\n'
    PBS_r = '#PBS -r y\n'
    PBS_u = '#PBS -u %s\n' % user
    PBS_q = '#PBS -q high\n'
    
   # print (pbs_file);sys.exit()
    pbs.write( ' '.join([
        PBS_N,PBS_o,PBS_e,PBS_l,PBS_r,PBS_u,PBS_q,
        '/online/software/Python-3.5.1/python', dir+'/X170001-P212_varscan.py',normal_bam_id,tumor_bam_id,normal_bam,tumor_bam,tumor_dir
    ]) )
    

    pbs.close()
    qsub.write('qsub %s\n' % pbs_file)
qsub.close()


