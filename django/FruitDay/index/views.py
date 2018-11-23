from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
import json

from .forms import *
# Create your views here.
def index_views(request):
    return render(request,'index.html')

def login_views(request):
    if request.method == 'GET':
        #获取 请求 中的源地址，如果没有的话则获取 '/'
        url = request.META.get('HTTP_REFERER','/')

        print('GET中的请求源地址：'+url)
        #判断session中是否有 uid和uphone
        if 'uid' in request.session and 'uphone' in request.session:
            return  redirect('url')

        else:
            #判断 cookie 中是否有 uid和uphone
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                # 如果有的话则取出来并保存进session,再回首页
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid'] = uid
                request.session['uphone'] = uphone
                return redirect('/')
            else:
                form = LoginForm()

                # 构建响应对象，并将cookie保存进响应对象中
                resp = render(request,'login.html',locals())
                resp.set_cookie('url', url)
                return resp

            #如果有的话则取出来保存进session，再回首页

        return render(request,'login.html',locals())
    else:
        #post请求
        #获取请求源地址
        url = request.META.get('HTTP_REFERER','/')
        print('POST中的请求源地址：'+url)
        #接收手机号uphone 和 upwd 判断是否登录成功
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']

        users = Users.objects.filter(uphone=uphone,upwd=upwd)
        # 如果成功继续向下执行,否则回到登录页
        if users:
            #登录成功，将 id 和 uphone 保存进 session
            id = users[0].id
            request.session['uid']=id
            request.session['uphone']=uphone
            #如果有记住密码则将数据保存进 cookies
            #先从 cookies 中将 url 的值获取出来
            url = request.COOKIES.get('url','/')

            resp = redirect('/')
            #如果 url 存在于cookies中的话，则将 url 从 cookies 中删除
            if 'url' in request.COOKIES:
                resp.delete_cookie('url')
            if "isSave" in request.POST:
                expires = 60*60*24*365
                resp.set_cookie('uid',id,expires)
                resp.set_cookie('uphone',uphone,expires)
            return resp
        else:
            return redirect('/login/')
        #如果成功继续向下执行，否则回到登录也


def register_views(request):
    return render(request,'register.html')

# def login_views(request):#实验保存 cookies
#     if request.method == 'GET':
#         #判断 uphone 是否登录过
#         if 'uphone' in request.COOKIES:
#             return HttpResponse('您已经登录过')
#         else:
#             form = LoginForm()
#             return render(request,'login.html',locals())
#     else:
#         uphone = request.POST['uphone']
#         upwd = request.POST['upwd']
#
#         users = Users.objects.filter(uphone=uphone,upwd=upwd)
#         if users:
#             #登录成功
#             resp = HttpResponse('登录成功')
#             #如果记住密码。则保存进cookie
#             if 'isSave' in request.POST:
#                 resp.set_cookie('uphone',uphone,60*60*24*365)
#             return  resp
#
#         else:
#             return HttpResponse('登录失败')

def check_login_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        #有登陆信息
        uid = request.session.get('uid')
        uname = Users.objects.get(id = uid).uname
        dic = {
            'loginStatus':1,
            'uname':uname,
        }
    elif 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
        # cookies 中是有登录信息的，那么从 cookies中取出数据
        uid=request.COOKIES('uid')
        uphone=request.COOKIES('uphone')
        request.session['uid'] = uid
        request.session['uphone'] = uphone
        #根据 uid 对应的值，获取对应的 uname，并构建成字典再响应给客户端
        uname = Users.objects.get(id=uid).uname
        dic = {
            'loginStatus':1,
            'uname':uname,
        }
    else:
        #没有登录信息
        dic = {
            'loginStatus':0,
        }

    return HttpResponse(json.dumps(dic))

def logout_views(request):
    #判断 session 是否有
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
        #获取原地址，构建响应对象
        url = request.META.get('HTTP_REFERER','/')
        resp = redirect(url)
        #判断 cookies 有则清除
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            resp.delete_cookie('uid')
            resp.delete_cookie('uphone')
        return resp
    return redirect('/')

def check_uphone_views(request):
    uphone = request.GET['uphone']
    users = Users.objects.filter(uphone=uphone)
    if users:
        dic = {
            'status':1,
            'msg':'手机号码已存在'
        }
    else:
        dic = {
            'status':0,
            'msg':'通过',
        }
    return HttpResponse(json.dumps(dic))


def load_type_goods(request):
    all_list = []
    #读取GoodsType下的所有内容
    types = GoodsType.objects.all()
    for type in types:
        #将类型转换为 json 字符串
        type_json = json.dumps(type.to_dict())
        #通过 type 获取对应的商品
        goods = type.goods_set.all()[0:10]
        #讲 goods 转换为 json 字符串
        goods_json = serializers.serialize('json',goods)
        print(type.title+"的商品为:")
        print(goods)
        dic = {
            'type':type_json,
            'goods':goods_json,
        }
        #将dic追加进 all_list 列表中
        all_list.append(dic)
    return HttpResponse(json.dumps(all_list))