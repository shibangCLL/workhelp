from django.shortcuts import render
from .models import Jietu, Doamin, DoaminType, DoaminExpirationDate
from django import views


# Create your views here.
def domaintype_list(request):
    domaintype_list = DoaminType.objects.all()
    return render(request, 'jietu/domaintype_list.html', locals())


def show_domaintype_expiration_date(request, domaintype):
    expiration_dates = DoaminExpirationDate.objects.filter(
        doamin__domaintype__domaintype=domaintype).distinct().order_by('-expiration_date')

    return render(request, 'jietu/show_doamintype_expiration_date.html', locals())


def show_domaintype_expiration_date_pic(request, expiration_date, domaintype):
    jietus = Jietu.objects.filter(domain__domaintype__domaintype=domaintype).filter(
        domain__expiration_date__expiration_date=expiration_date)
    z_count = Doamin.objects.filter(expiration_date__expiration_date=expiration_date).filter(
        domaintype__domaintype=domaintype).count()
    t_count = Doamin.objects.filter(expiration_date__expiration_date=expiration_date).filter(
        domaintype__domaintype=domaintype).filter(status=True).count()
    f_count = Doamin.objects.filter(expiration_date__expiration_date=expiration_date).filter(
        domaintype__domaintype=domaintype).filter(status=False).count()
    return render(request, 'jietu/show_domaintype_expiration_date_pic.html', locals())


def show_domaintype_expiration_date_no_pic(request, expiration_date, domaintype):
    domains = Doamin.objects.filter(expiration_date__expiration_date=expiration_date).filter(
        domaintype__domaintype=domaintype).filter(status=False)
    date_str = DoaminExpirationDate.objects.get(expiration_date=expiration_date).expiration_date.strftime('%Y%m%d')
    return render(request, 'jietu/show_domaintype_expiration_date_no_pic.html', locals())


def jietu_detail(request, domain):
    jietu = Jietu.objects.get(domain__name=domain)
    date_str = jietu.domain.expiration_date.expiration_date.strftime('%Y%m%d')
    return render(request, 'jietu/jietu_detail.html', locals())


class AddDomain(views.View):
    def get(self, request):
        return render(request, "jietu/add_domain.html")

    def post(self, request):
        user = request.user
        domains = request.POST.get('domains')
        domains = domains.split('\n')
        date = request.POST.get('date')
        import datetime
        date = datetime.datetime.strptime(date, '%m/%d/%Y').date()
        exists = DoaminExpirationDate.objects.filter(expiration_date=date)
        if exists:
            date = DoaminExpirationDate.objects.get(expiration_date=date)
        else:
            date = DoaminExpirationDate.objects.create(expiration_date=date)
            date.save()
        domain_list = []
        for domain in domains:
            domain = domain.strip('\r')
            try:
                domaintype = domain.split('.')[-1]
            except Exception as e:
                pass
            exists = DoaminType.objects.filter(domaintype=domaintype).exists()
            if exists:
                domaintype = DoaminType.objects.get(domaintype=domaintype)
            else:
                domaintype = DoaminType.objects.create(domaintype=domaintype)
                domaintype.save()
            domain = Doamin(name=domain, expiration_date=date, domaintype=domaintype)
            domain_list.append(domain)
        try:
            Doamin.objects.bulk_create(domain_list)
        except Exception as e:
            print(e)
            pass

        # for domain in domains:
        #     exists = Doamin.objects.filter(name=domain).exists()
        #     if exists:
        #         domain = Doamin.objects.get(name=domain)
        #         domain.user.add(user)
        #         domain.save()
        #     else:
        #         try:
        #             domaintype = domain.split('.')[-1]
        #         except Exception as e:
        #             print('域名格式不正确，无法获取域名格式')
        #             pass
        #         exists = DoaminType.objects.filter(domaintype=domaintype).exists()
        #         if exists:
        #             domaintype = DoaminType.objects.get(domaintype=domaintype)
        #             domain = Doamin.objects.create(name=domain, expiration_date=date, domaintype=domaintype)
        #             domain.save()
        #             domain.user.add(user)
        #             domain.save()
        #         else:
        #             domaintype = DoaminType.objects.create(domaintype=domaintype)
        #             domaintype.save()
        #             domain = Doamin.objects.create(name=domain, expiration_date=date, domaintype=domaintype)
        #             domain.save()
        #             domain.user.add(user)
        #             domain.save()
        return render(request, "jietu/add_domain.html")
