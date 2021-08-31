import pandas as pd
import os
import sys
from ethnicolr import pred_census_ln

part = sys.argv[1]

if not os.path.exists("../data/race"):
    os.makedirs("../data/race")

f = open('../data/cleaned/tweets_en_part%s.csv'%(part),'r')
out = open('../data/race/census2010_race_part%s.csv'%(part), 'w+')
s = '|$|'
for lines in f.readlines():
    try:
        lst = lines.split('|$|')
        read_user_id = lst[0].replace('\n', '')
        read_tweet_id = lst[1].replace('\n', '')
        last_name = lst[3].replace('\n', '')
        names = pd.DataFrame([{'last_name': last_name}])
        rdf = pred_census_ln(names, 'last_name', 2010)
        out_str = s.join([read_user_id, read_tweet_id,
                          rdf['last_name'].iloc[0],
                          rdf['race'].iloc[0],
                          str(rdf['api'].iloc[0]),
                          str(rdf['black'].iloc[0]),
                          str(rdf['hispanic'].iloc[0]),
                          str(rdf['white'].iloc[0]), '\n'])

        out.write(out_str)
    except:
        pass
out.close()
f.close()