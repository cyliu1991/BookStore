import hashlib

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from user.models import User


def login_view(request):
    if request.method == 'GET':
        if 'username' in request.session:
            return HttpResponseRedirect('index/allbook')
        if 'username' in request.COOKIES:
            request.session['username'] = request.COOKISE['username']
            return HttpResponseRedirect('index/allbook')
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        if not username or not password:
            error = '你输入的用户名或者密码错误！'
            return render(request, 'user/login.html', locals())
        users = User.objects.filter(username=username, password=password)
        if not users:
            error = '用户不存在或用户密码输入错误!!'
            return render(request, 'user/login.html', locals())
            # 返回值是个数组，并且用户名具备唯一索引，当前用户是该数组中第一个元素
        users = users[0]
        request.session['username'] = username
        response = HttpResponseRedirect('/index/allbook')
        # 检查post 提交的所有键中是否存在 isSaved 键
        if 'isSaved' in request.POST.keys():
            # 若存在则说明用户选择了记住用户名功能，执行以下语句设置cookie的过期时间
            response.set_cookie('username', username, 60 * 60 * 24 * 7)
        return response


def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    resp = HttpResponseRedirect('/user/index')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    return resp

def reg_view(request):
    if request.method == "GET":
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            username_error = "请输入正确的用户名"
            return render(request, 'user/register.html', locals())
        password_1 = request.POST.get('password_1')
        m = hashlib.md5()
        m.update(password_1.encode())
        password_m1 = m.hexdigest()
        print(password_m1)

        password_2 = request.POST.get('password_2')
        m = hashlib.md5()
        m.update(password_2.encode())
        password_m2 = m.hexdigest()
        print(password_m2)

        if not password_m1 or not password_m2:
            password_1_error = '请输入正确的密码'
            return render(request, 'user/register.html', locals())

        if password_m2 != password_m2:
            password_2_error = '两次密码不一致'
            return render(request, 'user/register.html', locals())

        try:
            old_user = User.objects.get(username=username)
            username_error = '用户已被注册！'
            return render(request, 'user/register.html', locals())
        except Exception as e:
            print('%s是可用用户名——%s' % (username, e))
            try:
                user = User.objects.create(username=username, password=password_m1)
                html = """
                注册成功 点击<a href='/index/'>进入首页</a>
                """
                request.session['username'] = username
                return HttpResponse(html)
            except Exception as e:
                print(e)
                username_error = '该用户名已被占用'
                return render(request, 'user/register.html', locals())