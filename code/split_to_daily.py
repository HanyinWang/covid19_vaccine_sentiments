import os
import pandas as pd
from tqdm import tqdm
from datetime import datetime

vaccine_wo_dist_path = '../data/vaccine_text_wo_distribution'
merged_foler = '../data/merged'
vaccine_wo_dist_real_date_path = '../data/vaccine_text_wo_distribution_real_date'

separater = '|$|'

for file in tqdm(os.listdir(vaccine_wo_dist_path)):
    # text file
    text = []
    user_id = []
    tweet_id = []
    with open(os.path.join(vaccine_wo_dist_path, file)) as vaccine_wo_dist_file:

        for lines in vaccine_wo_dist_file:
            try:
                lst = lines.split(separater)
                text.append(lst[0])
                user_id.append(lst[2])
                tweet_id.append(lst[3].replace('\n',''))
            except:
                pass

    vaccine_wo_dist_df = pd.DataFrame({'text': text,
                                       'user_id': user_id,
                                       'tweet_id': tweet_id})
    vaccine_wo_dist_df = vaccine_wo_dist_df.drop_duplicates()

    # merged file with date available
    merged_df = pd.read_csv(os.path.join(merged_foler, 'merged_part%s'%(file.split('part')[-1])),
                            usecols = [2,3,4], dtype={'created_at': str,
                                                      'sentiment':str,
                                                      'tweet_id': str})
    merged_df = merged_df.drop_duplicates()

    vaccine_wo_dist_df_dt = pd.merge(vaccine_wo_dist_df, merged_df,
                                     how = 'inner',
                                     on = 'tweet_id')
    # remove missing date
    vaccine_wo_dist_df_dt = vaccine_wo_dist_df_dt[vaccine_wo_dist_df_dt['created_at'].isna()==0]
    # parse date
    vaccine_wo_dist_df_dt['dttm'] = [datetime.strptime(ca,'%a %b %d %H:%M:%S +%f %Y') for ca in vaccine_wo_dist_df_dt['created_at']]
    vaccine_wo_dist_df_dt['date'] = [ca.date() for ca in
                                     vaccine_wo_dist_df_dt['dttm']]
    for real_date in list(set(vaccine_wo_dist_df_dt['date'])):
        df = vaccine_wo_dist_df_dt[vaccine_wo_dist_df_dt['date'] == real_date]
        df = df.astype(str)
        df.to_csv(os.path.join(vaccine_wo_dist_real_date_path,
                               'vaccine_text_wo_distribution_real_date_part%s.csv'%(str(real_date))),
                  mode = 'a') # caution!! appending!!! delete all files when running again!!!!


