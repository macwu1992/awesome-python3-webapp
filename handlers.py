#!/Users/Tong/dev_repo/liaoxuefeng_shizhan/awesome-python3-webapp/py34en
# -*- coding: utf-8 -*-

' url handlers '
import time, hashlib, json, re, logging
import api_errors
from aiohttp import web
from coroweb import get, post
from models import User, Blog, next_id
from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def cookie2user(cookie_str):
    '''
    parse cookie to user
    '''

    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            logging.info('cookie expired')
            return None
        users = yield from User.findAll('id=?', [uid])
        user = users[0]
        if not user:
            logging.info('user not found')
            return None
        s = '%s-%s-%s-%s' % (uid, user['passwd'], expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid password')
            return None
        user['passwd'] = '******'
        return user
    except Exception as e:
        logging.info(e)
        return None

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user['id'], user['passwd'], expires, _COOKIE_KEY)
    L = [user['id'], expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

@get('/')
def index(request):
    # users = yield from User.findAll()
    blogs = [
        Blog(id='001', user_id='1', user_name='tong', name='blog1', summary='sss', content='sdasd', created_at=time.time()-120),
        Blog(id='002', user_id='2', user_name='tong', name='blog2', summary='sss', content='sdasd', created_at=time.time()-220),
        Blog(id='003', user_id='3', user_name='tong', name='blog3', summary='sss', content='sdasd', created_at=time.time()-320)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }

@get('/register')
def register(request):
    return {
        '__template__': 'register.html'
    }

@get('/login')
def login(request):
    return {
        '__template__': 'login.html'
    }

# 用户注册 api
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
@post('/api/users')
def api_register_user(request):
    passwd=request.__data__['passwd']
    email=request.__data__['email']
    name=request.__data__['name']
    if not name or not name.strip():
        raise api_errors.APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise api_errors.APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise api_errors.APIValueError('passwd')
    users = yield from User.findAll('email=?', [email])
    if len(users) > 0:
        raise api_errors.APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, user_name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='asdasd')
    yield from user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

# 用户登陆api
@post('/api/login')
def api_login(request):
    email = request.__data__['email']
    passwd = request.__data__['passwd']
    # 检查用户名是否存在
    users = yield from User.findAll('email=?', [email])
    if len(users) < 1:
        raise api_errors.APIValueError('email', 'email not exits')
    user = users[0]
    # 检查用户名下的密码是否正确
    sha1 = hashlib.sha1()
    sha1.update(user['id'].encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user['passwd'] != sha1.hexdigest():
        raise api_errors.APIValueError('password', 'invalid password')
    # 处理cookies
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user['passwd'] = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/signout')
def api_signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user %s sign out' % request.__user__)
    return r