import json
import os
import sys
sys.path.append('./')
from utilities import del_http_user_tokenize, clean_str2
from tqdm import tqdm

part = sys.argv[1]

if not os.path.exists("../data/quote_status"):
    os.makedirs("../data/quote_status")

dist_out = open('../data/vaccine_distribution_text/vaccine_distribution_text_part%s.csv' % (part), 'w+')
wo_dist_out = open('../data/vaccine_text_wo_distribution/vaccine_text_wo_distribution_part%s.csv'%(part), 'w+')

tweet_file = open("../data/extracted/%s_clean_extracted"%(part), 'r')
quote_file = open('../data/quote_status/quote_en_df_part%s.csv' % (part), 'w+')

for line in tqdm(tweet_file):
    dic = json.loads(line)
    try:
        read_user_id = dic['user']['id_str']
        read_tweet_id = dic['id_str']
        lang = dic['lang']
        created_at = dic['created_at']

        if lang == 'en':
            is_quote_status = dic['is_quote_status']

            if is_quote_status:
                quoted_status_id = dic['quoted_status_id_str']
                quoted_status_created_at = dic['quoted_status']['created_at']
                quoted_status_full_text = clean_str2(del_http_user_tokenize(dic['quoted_status']['full_text']))
                quoted_status_user_id = dic['quoted_status']['user']['id_str']
                quoted_status_user_name = dic['quoted_status']['user']['name']
                quoted_status_user_location = clean_str2(del_http_user_tokenize(dic['quoted_status']['user']['location']))
                quoted_status_user_description = clean_str2(del_http_user_tokenize(dic['quoted_status']['user']['description']))

                s = '|$|'
                output_str = s.join([str(created_at), str(read_user_id), str(read_tweet_id),
                                     str(quoted_status_id), str(quoted_status_created_at),
                                     str(quoted_status_full_text), str(quoted_status_user_id),
                                     str(quoted_status_user_name), str(quoted_status_user_location),
                                     str(quoted_status_user_description)])
                quote_file.writelines(output_str)

    except:
        continue

tweet_file.close()
quote_file.close()