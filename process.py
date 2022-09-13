import re
import pandas as pd
import datetime
import os
from pyecharts import options as opts
from pyecharts.charts import Bar

def data_dicReset(data_dic: dict):
    data_dic = {
        'Province': ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南',
                     '四川', '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津', '上海', '重庆'],
        'newConfirm': [],
        'newInfection': []
    }
    return data_dic

def getValue(str, province: str):
    value = 0
    index = str.find(province)
    if index != -1:
        flag = 1
        for i in range(index, len(str)):
            try:
                value = value * 10 + int(str[i])
                flag = 0
            except:
                if flag == 0:
                    break
                else:
                    continue
    return value

def getData_dicvalues(match: list, data_dic: dict):
    province_list = list(data_dic['Province'])
    for province in province_list:
        str = match[3]
        value = getValue(str, province)
        data_dic['newConfirm'].append(value)
    for province in province_list:
        str = match[6]
        value = getValue(str, province)
        data_dic['newInfection'].append(value)
    return data_dic


def date_list():
    today = datetime.datetime.now()
    date_list = []
    for i in range(1, 15):
        time = today - datetime.timedelta(days=i)
        time = time.timetuple()
        VersionInfo = str(time.tm_mon) + "." + str(time.tm_mday)
        date_list.append(VersionInfo)
    return date_list

def writeData_dicIntoExcel(df, date: str, path: str):
    writer = pd.ExcelWriter(path + '\{}新增疫情.xls'.format(date))
    df.to_excel(writer, index=False)
    writer.save()

def bar_combination(df, date):
    c = (
        Bar()
            .add_xaxis(df['Province'].values.tolist())
            .add_yaxis("新增无症状", df['newInfection'].values.tolist())
            .add_yaxis("新增确诊", df['newConfirm'].values.tolist())
            .set_global_opts(
            title_opts=opts.TitleOpts(title="{}新增疫情".format(date)),
            xaxis_opts=opts.AxisOpts(
                name='地区',
                name_location='middle',
                name_gap=30,
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Times New Roman',
                    font_size=16
                ),
                boundary_gap=True,
                axislabel_opts=opts.LabelOpts(interval=0) #!!!

            ),
            yaxis_opts=opts.AxisOpts(
                name='人数',
                name_location='middle',
                name_gap=30,
                name_textstyle_opts=opts.TextStyleOpts(
                    font_family='Times New Roman',
                    font_size=16
                )
            ),
            datazoom_opts=opts.DataZoomOpts(type_="slider"),
        )
    )
    return c

if __name__ == "__main__":

    line_list = []
    with open("daily.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line_list.append(line.strip('\n'))  # 去掉列表中每一个元素的换行符

    rule = "（.[^（）]+）"  # 匹配每对括号
    rule_compile = re.compile(rule)
    match_list = []
    for line in line_list:
        match_list.append(rule_compile.findall(line))

    data_dic = {}
    date_list = date_list()
    i = 0
    path = '每日疫情情况'
    if not os.path.exists(path):
        os.mkdir(path)
    for match in match_list:
        data_dic = data_dicReset(data_dic)
        data_dic = getData_dicvalues(match, data_dic)
        df = pd.DataFrame(data_dic)

        writeData_dicIntoExcel(df, date_list[i], path)

        bar_combination(df, date_list[i]).render(r"./每日疫情情况/{}新增疫情.html".format(date_list[i]))

        i = i + 1
