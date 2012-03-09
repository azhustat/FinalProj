# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/media/76442955442918FF/Berkeley/courses/NLP/weibo/sinatpy2.x-(2011-6-8)/sinatpy2.x')
from weibopy.auth import OAuthHandler
from weibopy.api import API

consumer_key= '1215594774'
consumer_secret ='b7f96f0ff5d7abf5e33a8c6e20109a90'

auth = OAuthHandler(consumer_key, consumer_secret)
auth_url = auth.get_authorization_url()
print 'Please authorize: ' + auth_url
verifier = raw_input('PIN: ').strip()
auth.get_access_token(verifier)
api = API(auth)

status = api.update_status(status='hello world', lat='12.3', long='45.6') 
print status.id
print status.text

angies = api.search_users("Angie Zhu")
angie1 = angies[0]
ch = angie1.screen_name
print ch.encode("utf8")

weibos = api.public_timeline()
for weibo in weibos:
    print weibo.text.encode('utf8')

user = api.get_user('brothercutter')
print user.screen_name
print user.followers_count #打印粉丝数
for friend in user.friends( ):
    print friend.screen_name


def login_check(request):
    """用户成功登录授权后，会回调此方法，获取access_token，完成授权"""
    verifier = request.GET.get('oauth_verifier', None)
    auth_client = _oauth()
    # 设置之前保存在session的request_token
    request_token = request.session['oauth_request_token']
    del request.session['oauth_request_token']
    auth_client.set_request_token(request_token.key, request_token.secret)
    access_token = auth_client.get_access_token(verifier)
    # 保存 access_token，以后访问只需使用access_token即可
    request.session['oauth_access_token'] = access_token
