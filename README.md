# awesome-python3-webapp
updated on 2016-3-6  

创建数据表
---
table 'users':
id pk string
email string
passwd string
name string
image string
created_at float  

table 'blogs'
id pk string
user_id string
user_name string
user_image string
name string
summary string
content text
created_at float

table 'comments'

id pk StringField
blog_id StringField
user_id StringField
user_name StringField
user_image StringField
content TextField
created_at FloatField