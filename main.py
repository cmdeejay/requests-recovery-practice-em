import requests
import sqlite3
import pandas as pd

session = requests.session()


body = session.get('https://quote.eastmoney.com/center/api/sidemenu.json')

body = body.json()

df = pd.DataFrame(body)
# df = df.drop(columns='next')
# df.to_csv('sidemenu.csv', index=False)
with sqlite3.connect('./em.sqlite') as conn:
    i = 0
    j = 0
    for value in df['next']:
        if type(value) == list:
            i += 1
            df_next = pd.DataFrame(value)
            # print(df_next)
            print(i)
            df_next.to_csv(f'files/sidemenu_next_{i}.csv', index=False)
            if 'next' in df_next.columns:
                for val in df_next['next']:
                    if type(val) == list:
                        j += 1
                        df_next2 = pd.DataFrame(val)
                        print(df_next2)
                        print(j)
                        df_next2.to_csv(f'files/2_sidemenu_next2_{j}.csv', index=False)
                        df_next2.to_sql(name=f'2_sidemenu_next2_{j}', con=conn, index=False, if_exists='replace')
                df_next = df_next.drop(columns='next')
            df_next.to_sql(name=f'sidemenu_next_{i}', con=conn, index=False, if_exists='replace')
    # df.to_sql(name='sidemenu', con=conn, index=False, if_exists='replace')
    # conn.commit()

# print(df)
