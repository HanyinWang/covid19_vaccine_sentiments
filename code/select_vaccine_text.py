import sys
import re

part = sys.argv[1]

vaccine_regex = re.compile(r'\b(vaccine|comirnaty|pfizer\-biontech|moderna|covishield|sputnik|coronavac|bbibp\-corv|epivaccorona|convidicea|covaxin|covivac|john\&johnson|janssen|covax)\b')
f = open('../data/full_text/full_text_en_part%s.csv'%(part),'r')
out = open('../data/vaccine_text/vaccine_text_part%s.csv'%(part), 'w+')
s = '|$|'
for lines in f.readlines():
    try:
        lst = lines.split('|$|')
        read_text = lst[0]
        clean_text = lst[1]
        read_user_id = lst[2]
        read_tweet_id = lst[3]
        if vaccine_regex.search(clean_text):
            out_str = s.join([read_text, clean_text, read_user_id, read_tweet_id])
            out.writelines(out_str)
    except:
        pass
out.close()
f.close()
