__author__ = 'Vincent'
from django import forms
from captcha.fields import CaptchaField



#通过表单提交，方便前端验证，数据库减压
class LoginForm(forms.Form):
    username =forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"}) #可不写error_messages



class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"}) #可不写error_messages


class ModifyPwdForm(forms.Form):
    '''重置密码'''
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)