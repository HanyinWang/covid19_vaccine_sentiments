import re
import os
import sys

part = sys.argv[1]

pregnant_regex = re.compile(r'\b(pregnant|pregnancy)\b')
in_path = '../data/vaccine_text_wo_distribution/'
out_path = '../data/pregnant_vaccine_text_wo_distribution/'
f = open(os.path.join(in_path, 'vaccine_text_wo_distribution_part%s.csv'%(part)), 'r')
out = open(os.path.join(out_path, 'pregnant_vaccine_text_wo_distribution_part%s.csv'%(part)), 'w+')
s = '|$|'
for lines in f.readlines():
    try:
        lst = lines.split('|$|')
        read_text = lst[0]
        clean_text = lst[1]
        read_user_id = lst[2]
        read_tweet_id = lst[3]
        if pregnant_regex.search(clean_text):
            out_str = s.join([read_text, clean_text, read_user_id, read_tweet_id])
            out.writelines(out_str)
    except:
        pass
out.close()
f.close()


