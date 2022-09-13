from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Pie, Tab
from pyecharts.faker import Faker
from pyecharts.globals import CurrentConfig, NotebookType

# 配置对应的环境类型
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK
CurrentConfig.ONLINE_HOST = 'https://assets.pyecharts.org/assets/'


def line_markpoint():
    c = (
        Line()
            .add_xaxis(Faker.choose())
            .add_yaxis(
            "商家A",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min")]),
        )
            .add_yaxis(
            "商家B",
            Faker.values(),
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-MarkPoint"))
    )
    return c


grid = (
    Grid(init_opts=opts.InitOpts(
        width="900px",
        height="300px",
        bg_color="skyblue"
    ))

        .add(line_markpoint(), grid_opts=opts.GridOpts(pos_bottom="60%", pos_right="10%"))
        .add(line_markpoint(), grid_opts=opts.GridOpts(pos_top="60%", pos_left="10%"))
)

grid.render()
