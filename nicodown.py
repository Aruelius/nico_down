# -*- coding: utf-8 -*-
import requests
import re
import json
import html
import sys

username = ''
passwd = ''

s = requests.session()
apiurl = 'https://api.dmc.nico/api/sessions?_format=json'
data = {
	'mail_tel': username,
	'password': passwd
}
get_cookie = s.post('https://account.nicovideo.jp/api/v1/login?site=niconico', data = data, allow_redirects=False) # 登录

r = s.get(sys.argv[1])
resp = re.findall(r'<div id="js-initial-watch-data" data-api-data="(.+?)" data-environment="', r.text)[0]
vip = re.findall(r'user.member_status = \'(.+?)\';', r.text)[0] # 找寻会员关键字
txt = html.unescape(resp) # 转码
js1 = json.loads(txt) # 转为json格式

#定义一些需要post的参数
recipe_id = js1['video']['dmcInfo']['session_api']['recipe_id']
content_id = js1['video']['dmcInfo']['session_api']['content_id']
video_src_ids = js1['video']['dmcInfo']['session_api']['videos']
audio_src_ids = js1['video']['dmcInfo']['session_api']['audios']
lifetime = js1['video']['dmcInfo']['session_api']['heartbeat_lifetime']
if vip == 'premium':
	transfer_preset = js1['video']['dmcInfo']['session_api']['transfer_presets'][0]
	player_id = js1['video']['dmcInfo']['storyboard_session_api']['player_id']
	auth_type = js1['video']['dmcInfo']['storyboard_session_api']['auth_types']['storyboard']
elif vip == 'normal':
	transfer_preset = ''
	player_id = js1['video']['dmcInfo']['session_api']['player_id']
	auth_type = 'ht2'
token = js1['video']['dmcInfo']['session_api']['token']
signature = js1['video']['dmcInfo']['session_api']['signature']
content_key_timeout = js1['video']['dmcInfo']['session_api']['content_key_timeout']
service_user_id = js1['video']['dmcInfo']['session_api']['service_user_id']
priority = js1['video']['dmcInfo']['session_api']['priority']


putjson = {"session":{"recipe_id":recipe_id,"content_id":content_id,"content_type":"movie","content_src_id_sets":[{"content_src_ids":[{"src_id_to_mux":{"video_src_ids":video_src_ids,"audio_src_ids":audio_src_ids}}]}],"timing_constraint":"unlimited","keep_method":{"heartbeat":{"lifetime":lifetime}},"protocol":{"name":"http","parameters":{"http_parameters":{"parameters":{"http_output_download_parameters":{"use_well_known_port":"yes","use_ssl":"yes","transfer_preset":transfer_preset}}}}},"content_uri":"","session_operation_auth":{"session_operation_auth_by_signature":{"token":token,"signature":signature}},"content_auth":{"auth_type":auth_type,"content_key_timeout":content_key_timeout,"service_id":"nicovideo","service_user_id":service_user_id},"client_info":{"player_id":player_id},"priority":priority}}
r = s.post(apiurl, json = putjson)
resp = r.json()
if r.status_code == 403:
	print('403错误：token_accept_time_limit')
elif r.status_code == 400:
	print('400错误：session_post_error')
elif r.status_code == 200 or r.status_code == 201:
	print(resp['data']['session']['content_uri'])
else:
	print(r.text)
