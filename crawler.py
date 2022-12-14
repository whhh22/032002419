from lxml import etree
import requests

page_count = 41  # 总页数


#  获取详情页链接href
def href_get(url, headers, href_list):
    response_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(response_text)
    li_list = tree.xpath('//ul[@class="zxxx_list"]/li')
    for li in li_list:
        href = 'http://www.nhc.gov.cn' + li.xpath('./a/@href')[0]
        href_list.append(href)
    return href_list


if __name__ == "__main__":

    # 开始爬
    url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 ",
        "Cookie": "yfx_c_g_u_id_10006654=_ck22090716221713320659133618350; "
                  "yfx_f_l_v_t_10006654=f_t_1662538937316__r_t_1662538937316__v_t_1662538937316__r_c_0; "
                  "sVoELocvxVW0S=59vVEUPdYzZViiQJRL3OzuBKuo7wiZfNKBKnd2T"
                  ".QlJkdAV6jykVnmkgDoA1bSxA3FE0yGvjRmm5dn0qMamwfTa; "
                  "sVoELocvxVW0T=53SfVXCW3Yh7qqqDkma"
                  ".Z4aiyHZ9XdIkPzwgpQ17TKqqLAsHlZUM1q1pke_KCzorYBxqnuE6DeVQ_NYxVaGT3o3LRelh7w8sI7Agrzv0C0GCxttt0KtlLRFQQ1 "
                  ".A_1CwHhnko12KXJzcLUdN331hp8qw8kny"
                  ".96LlCWOqOqkAfuIzB2mOAZxUa7B1MoQtboYtJnmCYx6h1mpoXZZJktvjm3wHde_ZNOcK88CQShMnVpuA;"
                  " insert_cookie=91349450;"
                  " JSESSIONID=C21F48AD6B160B83E2C69BEBB37D66C0; "
                  " security_session_verify=c889cc19a59214c681f09377c14b439d "
    }

    # 先爬详情页链接href
    href_list = []
    href_get(url, headers, href_list)
    for page in range(2, page_count + 1):
        url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_' + str(page) + '.shtml'
        href_get(url, headers, href_list)

    # 再爬详情页具体内容，并存储在文件‘daily.txt’中
    fp = open('daily.txt', 'w', encoding='utf-8')
    for href in href_list:
        new_url = href
        response_new_text = requests.get(url=new_url, headers=headers).text
        new_tree = etree.HTML(response_new_text)
        data = ''.join(new_tree.xpath(
            '//*[@id="xw_box"]/p[1]//text() | //*[@id="xw_box"]/p[5]//text() | //*[@id="xw_box"]/p[7]//text()'))
        fp.write(data + '\n')
    fp.close()
