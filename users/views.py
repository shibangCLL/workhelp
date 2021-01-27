from django import views
from django.contrib import auth
from django.shortcuts import (
    render, redirect, HttpResponse
)
from users.utils import auth_code
from .forms import RegForm, LoginForm
from .models import UserInfo


# 注册视图类
class Register(views.View):
    def get(self, request):
        return render(request, "users/register.html")

    def post(self, request):
        # post请求提交注册数据
        data = request.POST
        print(data)
        form_obj = RegForm(data)  # 数据交给form实例化
        print(form_obj)
        if form_obj.is_valid():  # 验证提交数据的合法性
            valid_data = form_obj.cleaned_data
            print(valid_data)
            del valid_data["r_password"]
            UserInfo.objects.create_user(**valid_data)  # 创建普通用户
            return redirect("/users/login")
        else:
            return render(request, "users/register.html", {"form_obj": form_obj})


class Login(views.View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        data = request.POST
        form_obj = LoginForm(request, data)  # 数据交给form实例化
        if form_obj.is_valid():
            username = form_obj.cleaned_data['username']
            password = form_obj.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                # 登录成功为止1
                request.session['user_id'] = user.id
                request.session.set_expiry(60 * 60 * 24 * 14)
                auth.login(request, user)  # 将用户信息添加到session中
                return redirect('/')
            form_obj.add_error('username', '用户名或密码错误')
        return render(request, 'users/login.html', {'form_obj': form_obj})


class LoginOut(views.View):
    def get(self, request):
        request.session.flush()
        return render(request, "users/login.html")


# 验证码视图类
class GetAuthImg(views.View):
    """获取验证码视图类"""

    def get(self, request):
        data = auth_code.get_authcode_img(request)
        return HttpResponse(data)


class Home(views.View):
    def get(self, request):
        return render(request, "index.html")
