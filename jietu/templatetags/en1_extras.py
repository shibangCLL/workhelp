from django import template

from jietu.models import Jietu, Doamin, DoaminExpirationDate, DoaminType

register = template.Library()


@register.inclusion_tag('jietu/inclusions/status.html', takes_context=True)
def show_product_category_list(context,expiration_date, domaintype):
    return {
        'z_count': Doamin.objects.filter(domaintype=domaintype).filter(
            expiration_date__expiration_date=expiration_date).count(),

        't_count': Doamin.objects.filter(domaintype=domaintype).filter(
            expiration_date__expiration_date=expiration_date).folter(status=True).count(),
        'f_count': Doamin.objects.filter(domaintype=domaintype).filter(
            expiration_date__expiration_date=expiration_date).folter(status=False).count(),
    }


#
#
# @register.inclusion_tag('inclusions/tag_list.html', takes_context=True)
# def show_tags(context):
#     return {
#         'tag_list': Tag.objects.all(),
#     }
#
#
# @register.inclusion_tag('inclusions/banner_product_category_list.html', takes_context=True)
# def show_product_categories_banner(context):
#     return {
#         'parent_category_list': ProductCategory.objects.filter(parent_category__name='Product'),
#     }
#
# @register.inclusion_tag('inclusions/banner_project_category_list.html', takes_context=True)
# def show_project_categories_banner(context):
#     return {
#         'parent_category_list': ProjectCategory.objects.filter(parent_category__name='Project'),
#     }
#
# @register.inclusion_tag('inclusions/banner_news_category_list.html', takes_context=True)
# def show_news_categories_banner(context):
#     return {
#         'parent_category_list': Category.objects.filter(parent_category__name='News'),
#     }
