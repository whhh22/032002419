import re
import pandas as pd
import datetime
import os
# from pyecharts.charts import Map
from pyecharts.globals import CurrentConfig, NotebookType
# import xlrd
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK
CurrentConfig.ONLINE_HOST = 'https://assets.pyecharts.org/assets/'
from pyecharts import options as opts
from pyecharts.charts import Map, Grid, Bar


def data_dicReset(data_dic:dict):
    data_dic = {
        'Province': ['河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','海南',
                     '四川','贵州','云南','陕西','甘肃','青海','内蒙古','广西','西藏','宁夏','新疆','北京','天津','上海','重庆'],
        'newConfirm': [],
        'newInfection': []
    }
    return data_dic

def getValue(str, province:str):
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

def getData_dicvalues(match:list, data_dic:dict):
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

def time_list():
    today = datetime.datetime.now()
    time_ls = []
    for i in range(1, 15):
        time = today - datetime.timedelta(days=i)
        time = time.timetuple()
        VersionInfo = str(time.tm_mon) + "." + str(time.tm_mday)
        time_ls.append(VersionInfo)
    return time_ls

def writeData_dicIntoExcel(data_dic:dict, date:str, path:str):
    df = pd.DataFrame(data_dic)
    writer = pd.ExcelWriter(path + '\{}新增疫情.xls'.format(date))
    df.to_excel(writer, index=False)
    writer.save()

def bar_combination(df):
    c = (
        Bar()
        .add_xaxis(df['Province'].values.tolist())
        .add_yaxis("新增无症状", df['newInfection'].values.tolist())
        .add_yaxis("新增确诊", df['newConfirm'].values.tolist())

        # .reversal_axis()
        # .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="各地区新增疫情"),
                         xaxis_opts=opts.AxisOpts(
                             name='地区',
                             name_location='middle',
                             name_gap=30,  # 标签与轴线之间的距离，默认为20，最好不要设置20
                             name_textstyle_opts=opts.TextStyleOpts(
                                 font_family='Times New Roman',
                                 font_size=16  # 标签字体大小
                             ),
                             boundary_gap=True,
                             axisline_opts=opts.LabelOpts(interval=0, rotate=40)

                         ),
                         yaxis_opts=opts.AxisOpts(
                             name='人数',
                             name_location='middle',
                             name_gap=30,
                             name_textstyle_opts=opts.TextStyleOpts(
                                 font_family='Times New Roman',
                                 font_size=16
                                 # font_weight='bolder',
                             )
                        ),
                         datazoom_opts=opts.DataZoomOpts(type_="slider"),  #鼠标可以滑动控制
                         # toolbox_opts=opts.ToolboxOpts()  # 工具选项
                         # brush_opts=opts.BrushOpts()       #可以保存选择
                        )
    )

    return c

def bar_newInfection(df):
    c = (
        Bar()
        .add_xaxis(df['Province'].values.tolist())
        .add_yaxis("新增无症状", df['newInfection'].values.tolist())
        # .add_yaxis("新增确诊", df['newConfirm'].values.tolist())

        # .reversal_axis()
        # .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="各地区新增疫情"),
                         xaxis_opts=opts.AxisOpts(
                             name='地区',
                             name_location='middle',
                             name_gap=35,  # 标签与轴线之间的距离，默认为20，最好不要设置20
                             name_textstyle_opts=opts.TextStyleOpts(
                                 font_family='Times New Roman',
                                 font_size=16  # 标签字体大小
                             ),
                             boundary_gap=True,
                             axisline_opts=opts.LabelOpts(interval=0, rotate=40)

                         ),
                         yaxis_opts=opts.AxisOpts(
                             name='人数',
                             name_location='middle',
                             name_gap=30,
                             name_textstyle_opts=opts.TextStyleOpts(
                                 font_family='Times New Roman',
                                 font_size=16
                                 # font_weight='bolder',
                             )
                        ),
                         datazoom_opts=opts.DataZoomOpts(type_="slider")
                         # datazoom_opts=opts.DataZoomOpts(type_=""),  #鼠标可以滑动控制
                         # toolbox_opts=opts.ToolboxOpts()  # 工具选项
                         # brush_opts=opts.BrushOpts()       #可以保存选择
                        )
    )

    return c

def map_newConfirm(df):
    c = (
        Map()
        .add("新增确诊", [list(z) for z in zip(df['Province'].values.tolist(), df['newConfirm'].values.tolist())], "china")
        .set_global_opts(
            title_opts = opts.TitleOpts(title="各地区新增确诊人数"),
            visualmap_opts = opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"min": 50, "label": '>50', "color": "#DC143C"},
                    {"min": 40, "max": 49, "label": '40-49', "color": "#FF3030"},
                    {"min": 30, "max": 39, "label": '30-39', "color": "#FF4500"},
                    {"min": 20, "max": 29, "label": '20-29', "color": "#DB7093"},
                    {"min": 10, "max": 19, "label": '10-19', "color": "#FFC0CB"},
                    {"min": 1, "max": 9, "label": '1-9', "color": "#FFF0F5"},
                    {"min": 0, "max": 0, "label": '0', "color": "#fff"}
                ]
            )
        )
    )
    return c
def map_newInfection(df):
    c = (
        Map()
        .add("新增无症状感染", [list(z) for z in zip(df['Province'].values.tolist(), df['newInfection'].values.tolist())],"china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各地区新增无症状感染人数"),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"min": 50, "label": '>50', "color": "#DC143C"},
                    {"min": 40, "max": 49, "label": '40-49', "color": "#FF3030"},
                    {"min": 30, "max": 39, "label": '30-39', "color": "#FF4500"},
                    {"min": 20, "max": 29, "label": '20-29', "color": "#DB7093"},
                    {"min": 10, "max": 19, "label": '10-19', "color": "#FFC0CB"},
                    {"min": 1, "max": 9, "label": '1-9', "color": "#FFF0F5"},
                    {"min": 0, "max": 0, "label": '0', "color": "#fff"}
                ]
            )
        )
    )
    return c

if __name__ == "__main__":

    line_list = []
    with open("daily.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line_list.append(line.strip('\n'))   # 去掉列表中每一个元素的换行符

    rule = "（.[^（）]+）" #匹配每对括号
    rule_compile = re.compile(rule)
    match_list = []
    for line in line_list:
        match_list.append(rule_compile.findall(line))

    data_dic = {}
    time_list = time_list()
    i = 0
    path = '每日疫情情况'
    if not os.path.exists(path):
        os.mkdir(path)
    for match in match_list:
        data_dic = data_dicReset(data_dic)
        data_dic = getData_dicvalues(match, data_dic)
        # print(data_dic.items())
        # writeData_dicIntoExcel(data_dic, time_list[i], path)
        # visualization(data_dic)
        df = pd.DataFrame(data_dic)
        bar_combination(df).render()
        i = i + 1











