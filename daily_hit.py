import xlrd

hit_num = 50  # 参照值


def hit_display(ls, str):
    for k in range(len(ls)):
        if k == 0:
            fp.write('  ')  # 首行缩进，下同
        fp.write('{}'.format(ls[k]))
        if k != len(ls) - 1:
            fp.write('，')  # 分隔多个地区，下同
        else:
            fp.write('{}\n'.format(str))


if __name__ == "__main__":

    # 从excel读出数据并处理
    workBook = xlrd.open_workbook(r'每日疫情情况.xlsx')
    SheetNames = workBook.sheet_names()
    fp = open('daily_hit.txt', 'w', encoding='utf-8')
    date_list = []  # 日期列表
    data_list = []  # 数据列表
    for SheetName in SheetNames:  # 以表单名为索引遍历文件
        sheet_content = workBook.sheet_by_name(SheetName)
        date = SheetName
        date_list.append(date)
        ls = []  #
        for row in range(1, 35):  # 按行遍历取值
            province = sheet_content.cell(row, 0).value
            new_confirm = int(sheet_content.cell(row, 1).value)
            new_infection = int(sheet_content.cell(row, 2).value)
            ls.append((province, new_confirm, new_infection))
        data_list.append(ls)

    for i in range(len(data_list)):
        date = date_list[i]
        new_confirm_up_list = []  # 记录新增确诊人数攀升的地区
        new_confirm_hit_list = []  # 记录新增确诊人数众多的地区
        new_infection_hit_list = []  # 记录新增无症状人数众多的地区
        for j in range(34):
            province = data_list[i][j][0]
            new_confirm = data_list[i][j][1]
            new_infection = data_list[i][j][2]
            if new_confirm >= hit_num:
                new_confirm_hit_list.append(province)
            if new_infection >= hit_num:
                new_infection_hit_list.append(province)
            if i != 0:
                dt = new_confirm - data_list[i - 1][j][1]
                if dt > 0:
                    new_confirm_up_list.append(province)
        # 输出热点
        fp.write('{}热点：\n'.format(date))
        if len(new_confirm_hit_list) == 0 and len(new_infection_hit_list) == 0 and len(new_confirm_up_list) == 0:
            fp.write('  无。')
        else:
            hit_display(new_confirm_hit_list, '各地区疫情爆发，出现多例新增确诊病例！')
            hit_display(new_infection_hit_list, '各地区出现多例新增无症状感染病例！')
            hit_display(new_confirm_up_list, '各地区疫情仍在扩散！')
    fp.close()
