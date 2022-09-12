import math

content = [
    {"name": "aa", "age": 17},
    {"name": "aa2", "age": 17},
    {"name": "aa3", "age": 19},
    {"name": "aa4", "age": 16},
    {"name": "aa5", "age": 11},
    {"name": "aa6", "age": 12},
    {"name": "aa7", "age": 13},
    {"name": "aa8", "age": 14}
]


class Pagination(object):

    def __init__(self, data_list, page_index, page_size):
        """
        初始化分页数据
        :param data_list: 数据列表
        :param page_index: 当前要查看的列表页
        :param page_size: 每页默认显式几条数据
        """
        self.data_list = data_list
        self.page_index = page_index
        self.page_size = page_size

    @property
    def start(self):
        return (self.page_index - 1) * self.page_size

    @property
    def end(self):
        return self.page_index * self.page_size

    @property
    def page_num(self):
        return math.ceil(len(self.data_list) / self.page_size)

    def show(self):
        """ 切片展示数据 """
        result = self.data_list[self.start:self.end]
        if result and self.page_index <= self.page_num:  # 正常分页
            return result, self.page_index
        else:
            self.page_index = 1
            result = self.data_list[self.start:self.end]
            return result


if __name__ == '__main__':
    p = Pagination(content, page_index=2, page_size=4)
    content, page_index = p.show()
    print(content)
    print(page_index)