res = {'status': 'SUCCESS',
       'code': 200,
       'data': {
           'study_url': 'http://study.test.classba.cn/api/login?jupiter_token=eyJjb3Vyc2VfaWQiOjEwMDAxOTk3LCJjb3Vyc2Vfc2VjdGlvbl9pZCI6MTAwMDE5OTcsImNoYXB0ZXJfaWQiOjEwMDAyNTA0LCJjaGFwdGVyX3R5cGUiOiIxMSIsInN1YmplY3RfaWQiOiI0IiwidXNlcl9pZCI6IjY4NjkzNjExODYyNDAxMjUiLCJhcHBfdHlwZSI6MiwibGVhcm5fd2F5IjoyMiwiYm9va192ZXJzaW9uIjoiNDMiLCJzdGFnZSI6IjQwIiwidHlwZSI6MSwic3ViX3R5cGUiOiIxIiwibGVhcm5fY291bnQiOiIxIiwiYWxsX3VubG9jayI6MH0O0O0O&authKey=M3hedYHycYUd2AEesidB16djCveySAUuqj0auwl2pd4ETw4iXeGwzw7iJ2G8rnDCWesF08mqD1',
           'token': 'eyJjb3Vyc2VfaWQiOjEwMDAxOTk3LCJjb3Vyc2Vfc2VjdGlvbl9pZCI6MTAwMDE5OTcsImNoYXB0ZXJfaWQiOjEwMDAyNTA0LCJjaGFwdGVyX3R5cGUiOiIxMSIsInN1YmplY3RfaWQiOiI0IiwidXNlcl9pZCI6IjY4NjkzNjExODYyNDAxMjUiLCJhcHBfdHlwZSI6MiwibGVhcm5fd2F5IjoyMiwiYm9va192ZXJzaW9uIjoiNDMiLCJzdGFnZSI6IjQwIiwidHlwZSI6MSwic3ViX3R5cGUiOiIxIiwibGVhcm5fY291bnQiOiIxIiwiYWxsX3VubG9jayI6MH0O0O0O'
           },
       'remain_refresh_token_time': 0,
       'message': 'ok',
       'date': '2020-11-04 16:21:23'
       }


params = res['data']['study_url'].split('?')
obj = {}
for i in params[1].split('&'):
    temp = i.split('=')
    obj[temp[0]] = temp[1]


print(obj)



# print(studyUrl[1])