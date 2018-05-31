from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password


from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm
from utils.email_send  import send_register_email


#用户名和邮箱并行验证
# 基础ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except  Exception as e:
            return None


#基于类,具备良好的封装性、拓展性
class LoginView(View):
    def get(self,request):
        return render(request, "login.html")


    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():       #检查form中Error是否为空
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)  # 验证，如果通过返回该对象，如果不通过返回None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, 'login.html', {'msg': '用户为未激活','login_form': login_form})
                # 只有当用户名或密码不存在时，才返回错误信息到前端
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误','login_form':login_form})
        else:
            return render(request, "login.html", {'login_form':login_form})




class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html",{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 检查form中Error是否为空
            user_name = request.POST.get("email", None)
            if UserProfile.objects.get(email=user_name):
                return render(request,"register.html",{"register_form":register_form,"msg":"用户已经存在"})
            pass_word = request.POST.get("password", None)

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False

            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name,'register')
            return render(request, 'login.html')
        else:
            return render(request,"register.html",{"register_form":register_form})



# 激活用户的view
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")


#忘记密码
class ForgetPwdView(View):
    '''找回密码'''
    def get(self,request):
        forget_form = ForgetPwdForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})


    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email  = request.POST.get("email",None)
            send_register_email(email,"forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})



class ResetView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,"password_reset.html",{"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

#提交修改密码
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1',"")
            pwd2 = request.POST.get('password2', "")
            email = request.POST.get("email","")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email,"msg":"密码不一致"})
            user = UserProfile.objects.get(email = email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email,"modify_form":modify_form})


                    # def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get("username","")
#         pass_word = request.POST.get("password","")
#         user = authenticate(username=user_name,password=pass_word)      #验证，如果通过返回该对象，如果不通过返回None
#         if user is not None:
#             login(request,user)
#             return render(request,"index.html")
#         else:
#             return render(request,"login.html",{"msg":"用户名或密码错误!"})
#     elif request.method == 'GET':
#         return render(request,"login.html",{})