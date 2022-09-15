import json
from lxml import etree
import os
import requests

page_count = 41

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
        # "Cookie": "sVoELocvxVW0S=5wHXM0I_xBcTB7BMRAMWPnFBB0Tvmha2jU6rBs8n1M_TEpjLpIC5nUVZXUjT8wHd5uqF7iQ6ZKvdMVBiwzIKTIa; yfx_c_g_u_id_10006654=_ck22050223304813439966761515774; _gscu_2059686908=51505484e9g7y317; yfx_key_10006654=; yfx_mr_10006654=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10006654=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; insert_cookie=97324480; yfx_f_l_v_t_10006654=f_t_1651505448337__r_t_1663067716550__v_t_1663067716550__r_c_4; security_session_verify=f95068184afafa3df29d35be314a8326; sVoELocvxVW0T=53nrbgCWGRXAqqqDkJjlT0qxQHuqbk4ItJX6QxUqA0aoB2GFbZegGkkQEVuSpaJ.O_fplQIa0Nt0kxj0dQSR7.bouJaa7OnkErqH_9gnhjb151EVxy.hVER.HZUw9MTTaIOC59QcgzSwNiwzK4fJD9soMhw_Gt0xgwB_liMJhmRvK2b1NcTSdB7Lqm4DOnIsdQlj9nR3ynF44rXnJr9Xod3ekfzaq9KcOYzrut7OuwI3w_ZsTzmizrw1yjfd5BA7w.XwpgrBExvZIv3qZEFNiok4pp7BplQWFp1NcV3F8_0KcV1FK954BumvUrT7K_q.MdJ0UoQMbfJ_G9HBE2SBXKouPEGK62FruHTNTGHuMD8OA"
        # "Cookie": "sVoELocvxVW0S=5eY6wFXfqRIZvvFkIKOSEJ47m4aW..HI3xRomoGQn1K8JQUvrjrh0lzVGR183ravwK501d2onAANZGIn.GByVuG; yfx_c_g_u_id_10006654=_ck22090721472312170556655717118; sVoELocvxVW0T=53SPflbW3LpEqqqDkDEYwbqxSjdhkgd76RF6vnoMSOLm6HxL_RHVoj6KZYedT4te0D3gipKUt7R.DWb_9EINOFFDV8k3RXZGWWhfx_sZNpl_YgBpw4DUlCmG_Zm2XqXq7SZpZJHy_3VelR3hMuaA.DXpCBHpg0N2.JIpVE0vj2z9ku86gnzqXuiNaeBYIpHT8Pb7FqUWSuNmews2WM74HfC5i7ayp.4mmpyPmNlqiUNeI9E1EHjJcHoRyA6pU4yMjPhP7tIgdH4s4.AZTjz.6614D5Z3DL.aiauCsQII3W9zq; security_session_verify=2a4890eb19dfa8ef19f9c5b70443d79f; insert_cookie=91349450; yfx_f_l_v_t_10006654=f_t_1662558443211__r_t_1663082935491__v_t_1663082935491__r_c_1"
    }
    # 先爬详情页href
    href_list = []
    href_get(url, headers, href_list)
    for page in range(2, page_count+1):
        url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_' + str(page) + '.shtml'
        href_get(url, headers, href_list)
    fp = open('daily.txt', 'w', encoding='utf-8')
    for href in href_list:
        new_url = href
        response_new_text = requests.get(url=new_url, headers=headers).text
        new_tree = etree.HTML(response_new_text)
        data = ''.join(new_tree.xpath(
            '//*[@id="xw_box"]/p[1]//text() | //*[@id="xw_box"]/p[5]//text() | //*[@id="xw_box"]/p[7]//text()'))
        fp.write(data + '\n')
    fp.close()
