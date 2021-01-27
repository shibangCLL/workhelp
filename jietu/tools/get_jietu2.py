import os
import django
import re
import datetime
from workhelp import settings
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workhelp.settings")
django.setup()


def replaceCharEntity(htmlstr):
    """
    替换常用HTML字符
    :param htmlstr: 要替换的字符
    :return:
    """
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }
    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def filter_tags(htmlstr):
    """
    过滤HTML中的标签
    :param htmlstr: 要过滤的内容
    :return:
    """
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub(' ', s)
    s = replaceCharEntity(s)  # 替换实体
    return s


from jietu.models import Jietu, Doamin, DoaminType

while True:
    domainlist = Doamin.objects.filter(status=False)
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--log-level=3')
    browser = webdriver.Firefox(firefox_options=firefox_options)
    for domain in domainlist:
        print(domain)
        dete_str = domain.expiration_date.expiration_date.strftime('%Y%m%d')
        url = 'https://web.archive.org/web/' + dete_str + '/' + domain.name

        pic_path = os.path.join(settings.MEDIA_ROOT, 'images', 'jietu', str(domain.expiration_date))
        if not os.path.exists(pic_path):
            os.makedirs(pic_path)
        else:
            pass
        try:
            browser.set_page_load_timeout(60)  # 设置网页加载超时时间为20秒
            browser.get(url)
            html = browser.page_source
            s = filter_tags(html)
            pic_name = domain.name + '.png'
            browser.get_screenshot_as_file(os.path.join(pic_path, pic_name))
        except Exception as e:
            with open('error.txt', 'a', encoding='utf-8') as f:
                f.write(str(e) + '\n')
            pass
        else:
            pic_path = os.path.join('images', 'jietu', str(domain.expiration_date), pic_name)
            jietu = Jietu(domain=domain, image=pic_path, content=s)
            jietu.save()
            domain.status = True
            domain.save()
    browser.quit()
