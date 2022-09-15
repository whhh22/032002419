import xlrd
import xlwt
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

# 从excel读取数据准备可视化
date_list = []
newConfirm_list = []
newInfection_list = []
workBook = xlrd.open_workbook(r'每日疫情情况.xlsx')
SheetNames = workBook.sheet_names()
for SheetName in SheetNames:
    date_list.append(SheetName)
    sheet_content = workBook.sheet_by_name(SheetName)
    ls1 = []
    ls2 = []
    for row in range(1, 35):
        ls1.append((sheet_content.cell(row, 0).value, int(sheet_content.cell(row, 1).value)))
        ls2.append((sheet_content.cell(row, 0).value, int(sheet_content.cell(row, 2).value)))
    newConfirm_list.append(ls1)
    newInfection_list.append(ls2)

# 可视化
def map(date_list, data_list, name):
    tl = Timeline()
    for i, j in zip(date_list, data_list):
        c = Map(init_opts=opts.InitOpts(bg_color="white"))  # 设置地图颜色

        c.add(series_name="{}".format(name), data_pair=j, maptype="china")  # 地图名称

        c.set_global_opts(
            title_opts=opts.TitleOpts(title="疫情地图"),
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
        tl.add(c, "{}".format(i))
    tl.render("疫情地图_{}.html".format(name))

map(date_list, newConfirm_list, '新增确诊')
map(date_list, newInfection_list, '新增无症状')


