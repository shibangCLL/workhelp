from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from users.models import UserInfo


# 注册form认证
class RegForm(forms.Form):
    """定义注册帐号的form组件"""
    username = forms.CharField(
        label="用户名",
        max_length=18,
        error_messages={
            "max_length": "用户名最长不超过18位"
        },
    )

    password = forms.CharField(
        min_length=6,
        error_messages={
            "min_length": "密码不能少于6位"
        }
    )

    r_password = forms.CharField(
        min_length=6,
        error_messages={
            "min_length": "密码不能少于6位"
        }
    )

    email = forms.CharField(
        label="邮箱",
        validators=[RegexValidator(r"^\w+@\w+\.com$", "邮箱格式不正确")]
    )

    mobile_phone = forms.CharField(
        label="电话",
        validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ]
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已经存在，请重新输入')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已经存在')
        return email

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        exists = UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已经存在')
        return mobile_phone

    def clean_password(self):
        # 校验密码的合法性，不能为纯数据
        password = self.cleaned_data.get("password")
        if password.isdecimal():
            raise ValidationError("密码不能为纯数字！")
        return password

    def clean_r_password(self):
        password = self.cleaned_data.get("password")
        r_password = self.cleaned_data.get("r_password")
        if password != r_password:
            raise ValidationError('两次密码不一致')
        return r_password


class LoginForm(forms.Form):
    username = forms.CharField(label='邮箱或手机号')
    password = forms.CharField(label='密码')
    authcode = forms.CharField(label='图片验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_authcode(self):
        """ 钩子 图片验证码是否正确？ """
        authcode = self.cleaned_data['authcode']
        # 去session获取自己的验证码
        session_code = self.request.session.get('authcode')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')

        if authcode.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')
        return authcode
