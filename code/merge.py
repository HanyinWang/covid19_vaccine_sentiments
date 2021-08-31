import os
import pandas as pd
import sys

sentiment_path = '../data/sentiment'
cleaned_path = '../data/cleaned'
race_path = '../data/race'
age_gender_path = '../data/age_gender'
pregnancy_path = '../data/pregnant_vaccine_text_wo_distribution'
quote_path = '../data/quote_status'
merged_path = '../data/merged'

part = sys.argv[1]

# sentiment
sentiment_user_id = []
sentiment_tweet_id = []
sentiment = []
with open(os.path.join(sentiment_path, 'sentiment_part%s.csv' % (part)), 'r') as sentiment_file:
    for lines in sentiment_file:
        try:
            lst = lines.split('|$|')
            sentiment_user_id.append(lst[1])
            sentiment_tweet_id.append(lst[2])
            sentiment.append(lst[3])
        except:
            pass
sentiment_df = pd.DataFrame({'user_id': sentiment_user_id,
                             'tweet_id': sentiment_tweet_id,
                             'sentiment': sentiment})
# time and place
meta_user_id = []
meta_tweet_id = []
created_at = []
user_location = []
coordinates = []
place = []
with open(os.path.join(cleaned_path, 'tweets_en_part%s.csv' % (part)), 'r') as meta_file:
    for lines in meta_file:
        try:
            lst = lines.split('|$|')
            if len(lst) == 14:
                meta_user_id.append(lst[0].replace('\n', ''))
                meta_tweet_id.append(lst[1])
                created_at.append(lst[9])
                user_location.append(lst[10])
                coordinates.append(lst[11])
                place.append(lst[12].replace('\n', ''))
        except:
            pass
meta_df = pd.DataFrame({'user_id': meta_user_id,
                        'tweet_id': meta_tweet_id,
                        'created_at': created_at,
                        'user_location': user_location,
                        'coordinates': coordinates,
                        'place': place})

merged1 = pd.merge(sentiment_df, meta_df,
                   how='left',
                   on=['tweet_id', 'user_id'])

del sentiment_df
del meta_df

# race
race_user_id = []
race_tweet_id = []
race = []
with open(os.path.join(race_path, 'census2010_race_part%s.csv' % (part)), 'r') as race_file:
    for lines in race_file:
        try:
            lst = lines.split('|$|')
            if (len(lst) == 9) & (lst[2] != ''):
                race_user_id.append(lst[0])
                race_tweet_id.append(lst[1])
                race.append(lst[3])
        except:
            pass
race_df = pd.DataFrame({'user_id': race_user_id,
                        'tweet_id': race_tweet_id,
                        'race': race})

merged2 = pd.merge(merged1, race_df,
                   how='left',
                   on=['tweet_id', 'user_id'])

del merged1
del race_df

# age and gender
age_gender_user_id = []
age = []
gender = []
with open(os.path.join(age_gender_path, 'age_gender_part%s.csv' % (part)), 'r') as age_gender_file:
    for lines in age_gender_file:
        lst = lines.split('|$|')
        if len(lst) == 3:
            age_gender_user_id.append(lst[0].split('.')[0].split('_')[-1])
            age.append(lst[1][1:-1])
            prob_M = float(lst[2].replace('[', '').replace(']', '').replace('\n', '').split()[0])
            prob_F = float(lst[2].replace('[', '').replace(']', '').replace('\n', '').split()[1])
            if prob_M > prob_F:
                gender.append('Male')
            elif prob_M < prob_F:
                gender.append('Female')
            else:
                gender.append('Undefined')
age_gender_df = pd.DataFrame({'user_id': age_gender_user_id,
                              'age': age,
                              'gender': gender})
merged3 = pd.merge(merged2, age_gender_df,
                  how='left',
                  on='user_id')

# pregnancy
read_text = []
clean_text = []
read_user_id_pregnancy = []
read_tweet_id_pregnancy = []
with open(os.path.join(pregnancy_path, 'pregnant_vaccine_text_wo_distribution_part%s.csv'%(part)), 'r') as pregnancy_file:
    for lines in pregnancy_file:
        lst = lines.split('|$|')
        read_text.append(lst[0])
        clean_text.append(lst[1])
        read_user_id_pregnancy.append(lst[2])
        read_tweet_id_pregnancy.append(lst[3].replace('\n',''))
    pregnancy_df = pd.DataFrame({'user_id':read_user_id_pregnancy,
                                 'tweet_id': read_tweet_id_pregnancy,
                                 'pregnancy_text': read_text

                                 })
merged4 = pd.merge(merged3, pregnancy_df,
                   how='left',
                   on=['user_id', 'tweet_id'])

del merged3
del pregnancy_df
merged4['pregnancy_related'] = merged4['pregnancy_text'].isna()==0

# quote
created_at = []
read_user_id = []
read_tweet_id =[]
quoted_status_id = []
quoted_status_created_at = []
quoted_status_full_text = []
quoted_status_user_id = []
quoted_status_user_name = []
quoted_status_user_location = []
quoted_status_user_description = []
with open(os.path.join(quote_path, 'quote_en_df_part%s.csv'%(part)), 'r') as quote_file:
    for lines in quote_file:
        lst = lines.split('|$|')
        created_at.append(lst[0])
        read_user_id.append(lst[1])
        read_tweet_id.append(lst[2])
        quoted_status_id.append(lst[3])
        quoted_status_created_at.append(lst[4])
        quoted_status_full_text.append(lst[5])
        quoted_status_user_id.append(lst[6])
        quoted_status_user_name.append(lst[7])
        quoted_status_user_location.append(lst[8])
        quoted_status_user_description.append(lst[9].replace('\n',''))

quote_df = pd.DataFrame({'user_id': read_user_id,
                         'tweet_id': read_tweet_id,
                         'quoted_status_id': quoted_status_id,
                         'quoted_status_created_at': quoted_status_created_at,
                         'quoted_status_full_text': quoted_status_full_text,
                         'quoted_status_user_id': quoted_status_user_id,
                         'quoted_status_user_name': quoted_status_user_name,
                         'quoted_status_user_location': quoted_status_user_location,
                         'quoted_status_user_description': quoted_status_user_description})

merged = pd.merge(merged4, quote_df,
                  how='left',
                  on=['user_id', 'tweet_id'])
merged = merged.drop_duplicates()
del merged4
del quote_df
merged.to_csv(os.path.join(merged_path, 'merged_part%s.csv' % (part)))