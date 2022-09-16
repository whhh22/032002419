import re
import pandas as pd
import openpyxl


# 字典date_dic初始化
def data_dic_reset(data_dic: dict):
    data_dic = {
        'Province': ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南',
                     '四川', '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津', '上海', '重庆', '香港',
                     '澳门', '台湾'],
        'newConfirm': [],
        'newInfection': []
    }
    return data_dic


# 将字符串数值转化成整型
def get_value(str, province: str):
    value = 0
    index = str.find(province)
    if index != -1:
        flag = 1
        for i in range(index, len(str)):
            try:
                value = value * 10 + int(str[i])
                flag = 0
            except TypeError:
                if flag == 0:
                    break
                else:
                    continue
    return value


# 从匹配列表match_list中提取值，为字典data_dic赋值
def get_data_dic_values(match: tuple, data_dic: dict, g_a_t_cal_confirm_new: list):
    province_list = data_dic['Province']
    for province in province_list[0: 31]:
        str = match[1]
        value = get_value(str, province)
        data_dic['newConfirm'].append(value)
    for province in province_list:
        str = match[2]
        value = get_value(str, province)
        data_dic['newInfection'].append(value)
    for province in province_list[31:]:
        str = match[3]
        value = get_value(str, province)
        g_a_t_cal_confirm_new.append(value)
    return data_dic, g_a_t_cal_confirm_new


if __name__ == "__main__":

    # 正则匹配
    line_list = []
    with open("daily.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line_list.append(line.strip('\n'))  # 去掉列表中每一个元素的换行符
    rule = '(.*)0—24时，31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例.*本土.*例（(.*)），.*31个省（自治区、直辖市）和新疆生产建设兵团报告新增无症状感染者.*本土.*例（(.*)）。.*港澳台地区通报确诊病例.*(香港.*)。'
    rule_compile = re.compile(rule)
    match = []
    for line in line_list:
        match.append(rule_compile.findall(line))
    match_list = []
    for ls in match:
        try:
            match_list.append(ls[0])
        except IndexError:
            continue

    # 用字典来提取值
    data_dic = {}
    g_a_t_calConfirm = [308594, 82, 28040]  # 记录港澳台上一次累计新增病例
    match_list.reverse()
    for match in match_list:
        data_dic = data_dic_reset(data_dic)
        g_a_t_calConfirm_new = []  # 记录这一次的港澳台累计新增病例
        data_dic, g_a_t_calConfirm_new = get_data_dic_values(match, data_dic, g_a_t_calConfirm_new)
        for i in range(3):
            data_dic['newConfirm'].append(g_a_t_calConfirm_new[i] - g_a_t_calConfirm[i])
        g_a_t_calConfirm = g_a_t_calConfirm_new  # 更新港澳台累计新增病例

        # 数据导入Excel
        df = pd.DataFrame(data_dic)  # 转换pandas格式
        date = match[0]  # 以日期作为Excel中sheet的名字
        workbook = openpyxl.load_workbook(r'每日疫情情况.xlsx')
        sheet_names = workbook.sheetnames
        sheet_name = '{}'.format(date)
        if sheet_name not in sheet_names:
            writer = pd.ExcelWriter(r'每日疫情情况.xlsx', mode='a', engine='openpyxl')
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()
