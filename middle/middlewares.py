from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse
from users.models import UserInfo


class AuthMD(MiddlewareMixin):
    # white_list = ['/users/login/', '/users/get_auth_img/']  # 白名单
    # balck_list = ['', ]  # 黑名单
    #
    # def process_request(self, request):
    #     next_url = request.path_info
    #     print(request.path)
    #     print(next_url)
    #     print(request.session.get("user_id"))
    #     if next_url in self.white_list or request.session.get("user_id"):
    #         print('1')
    #         return
    #     elif next_url in self.balck_list:
    #         return HttpResponse('This is an illegal URL')
    #     else:
    #         print('2')
    #         return redirect("/users/login/?next={}".format(next_url))
    def process_request(self, request):
        white_list = ['/users/login/', '/users/register/', '/users/get_auth_img/', '/admin/']  # 白名单
        if request.path in white_list:
            return
        ticket = request.session.get("user_id")
        if not ticket:
            return redirect("/users/login/?next={}".format(request.path))
        user = UserInfo.objects.filter(id=ticket)
        if not user:
            return redirect("/users/login/?next={}".format(request.path))
        request.user = user[0]
