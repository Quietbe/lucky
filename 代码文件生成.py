# -*- coding:utf-8 -*-
import json
import os
import random
import re
import time

import numpy as np
import pandas as pd


class DataFormat:
    """
    数据格式化
    """

    def description_format(self, description):
        """
        描述内容处理
        :param description:   描述内容处理
        :return:           处理后的描述内容
        """
        if pd.isnull(description):
            return description
        if description is not None:
            # 删除所有a标签
            # pattern = re.compile(r'<a.*?/a>')
            # description = re.sub(pattern, '', str(description))
            # 清理字符串中非打印字符
            """等待添加"""
            # 将所有a标签替换为span标签
            pattern = re.compile(r'<a.*?>')
            description = re.sub(pattern, '<span>', str(description))
            pattern = re.compile(r'</a>')
            description = re.sub(pattern, '</span>', description)
            # 删除所有链接  "http开头  " 结尾
            pattern = re.compile(r'"http.*?"')
            description = re.sub(pattern, '""', description)
            # 删除button标签
            pattern = re.compile(r'<button.*?</button>', re.S)
            description = re.sub(pattern, '', description)
            # 删除图片img标签  忽略换行符
            pattern = re.compile(r'<img.*?>', re.S)
            description = re.sub(pattern, '', description)
            # 删除 video标签
            pattern = re.compile(r'<video.*?</video>', re.S)
            description = re.sub(pattern, '', description)
            # 删除iframe标签
            pattern = re.compile(r'<iframe.*?</iframe>')
            description = re.sub(pattern, '', description)
            # 删除input标签
            pattern = re.compile(r'<input.*?>', re.S)
            description = re.sub(pattern, '', description)
            # 删除script标签
            pattern = re.compile(r'<script.*?</script>', re.S)
            description = re.sub(pattern, '', description)
            # 删除div标签
            pattern = re.compile(r'<div.*?>')
            description = re.sub(pattern, '', description)
            pattern = re.compile(r'</div>')
            description = re.sub(pattern, '', description)
            description = description.strip()
            # 删除手机号   xxx-xxx-xxxx
            pattern = re.compile(r'\d+-\d+-\d+')
            description = re.sub(pattern, '', description)
            # 删除手机号   xxx-xxx
            pattern = re.compile(r'\d+-\d+')
            description = re.sub(pattern, '', description)
            # 删除邮箱
            pattern = re.compile(r'\w*@\w*\.\w*')
            description = re.sub(pattern, '', description)
            # 删除 src" 开头 "结尾的
            pattern = re.compile(r'src=".*?"')
            description = re.sub(pattern, '', description)
            # 删除http开头的所有链接
            pattern = re.compile(r'http.*?"')
            description = re.sub(pattern, '"', description)
            # 删除http开头 com结尾的所有链接
            pattern = re.compile(r'http.*?com')
            description = re.sub(pattern, '', description)
            # 删除所有https链接
            pattern = r'\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s\[\]{};:\'".,<>?«»“”‘’]))'
            description = re.sub(pattern, '', description)
            # 删除所有https链接
            pattern = r'\b((?:http?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s\[\]{};:\'".,<>?«»“”‘’]))'
            description = re.sub(pattern, '', description)
            # 删除 字母开头 .com结尾的所有链接
            pattern = re.compile(r'\b[a-zA-Z]+\.com')
            description = re.sub(pattern, '', description)
            # 删除大写字母开头 .COM结尾的所有链接
            pattern = re.compile(r'\b[A-Z]+\.COM')
            description = re.sub(pattern, '', description)
            # 删除 字母开头 .html结尾的所有链接
            pattern = re.compile(r'\b[a-zA-Z].*?\.html')
            description = re.sub(pattern, '', description)
            # 替换svg标签 为span
            pattern = re.compile(r'<svg.*?</svg>')
            description = re.sub(pattern, '', description)
            # 删除中文
            pattern = re.compile(r'[\u4e00-\u9fa5]')
            description = re.sub(pattern, '', description)

        return description

    def price_format(self, price):
        """
        价格处理
        :param price: 价格
        :return: 处理后的价格
        """
        if pd.isnull(price):
            return price
        price = str(price)
        if '-' in price:
            price = price.split('-')[0]
        if '£' in price:  # 去除价格前面的£
            price = price.replace('£', '').strip()
        if price is not None and price != '':
            if '$' in price:  # 去除价格前面的$
                price = price.replace('$', '')
                price = price.strip()
            if '€' in price:
                price = price.replace('€', '')
                price = price.strip()
            if ',' in price:
                price = price.replace(',', '')
                price = price.strip()
        price = price.strip()
        return price

    def image_format(self, image):
        """
        图片处理
        :param image: 图片
        :return: 处理后的图片
        """
        if pd.isnull(image):
            return image
        if image is not None and image != '':
            image1 = image.split('?')[0]
            if image1.endswith('.jpg') or image1.endswith('.png') or image1.endswith('.jpeg') or image1.endswith(
                    '.gif'):
                image = image1
            if ' ' in image:  # 去除图片后面的空格
                image = image.strip()
            if image.startswith('http'):  # 如果图片路径是以http开头的
                image = image
            else:
                image = 'https:' + image
        return image

    def gallery_format(self, gallery):
        """
        图片处理
        :param image: 图片
        :return: 处理后的图片
        """
        if pd.isnull(gallery):
            return gallery
        if gallery is not None and gallery != '':
            gallery_list = gallery.split(';')
            gallery_list.remove('')
            for i in range(len(gallery_list)):
                gallery_list[i] = self.image_format(gallery_list[i])
            gallery_list = list(set(gallery_list))
            gallery = ';'.join(gallery_list)
        return gallery

    def color_format(self, color):
        """
        颜色处理
        :param color: 颜色
        :return: 处理后的颜色
        """
        if pd.isnull(color):
            return color
        if color is not None and color != '':
            color_list = color.split(',')
            color_list = list(set(color_list))
            for i in range(len(color_list)):
                color_list[i] = color_list[i].strip()
            color = ','.join(color_list)
        return color

    def size_format(self, size):
        """
        尺码处理
        :param size: 尺码
        :return: 处理后的尺码
        """
        if pd.isnull(size):
            return size
        if size is not None and size != '':
            size_list = size.split(',')
            size_list = list(set(size_list))
            for i in range(len(size_list)):
                size_list[i] = size_list[i].strip()
            size = ','.join(size_list)
        return size

    def category_format(self, category):
        """
        分类处理
        :param category: 分类
        :return: 处理后的分类
        """
        if pd.isnull(category):
            return category
        if category is not None and category != '':
            category_list = category.split('||')
            for i in range(len(category_list)):
                category_list[i] = category_list[i].strip()
            category_list = [i for i in category_list if i != '']
            category = '||'.join(category_list)
        return category

    def brand_format(self, brand):
        """
        品牌处理
        :param brand: 品牌
        :return: 处理后的品牌
        """
        # 如果brand是 pandas中的 nan数据类型就返回空字符串
        if pd.isnull(brand):
            return brand
        if brand is not None and brand != '':
            brand = brand.strip()
        return brand

    def title_format(self, title):
        """
        标题处理
        :param title: 标题
        :return: 处理后的标题
        """
        if pd.isnull(title):
            return title
        if title is not None and title != '':
            title = title.strip()
            # 删除title中的中文
            pattern = re.compile(r'[\u4e00-\u9fa5]')
            title = re.sub(pattern, '', title)
        return title

    def pageurl_format(self, pageurl):
        """
        页面url处理
        :param pageurl: 页面url
        :return: 处理后的页面url
        """
        if pd.isnull(pageurl):
            return pageurl
        if pageurl.startswith('https'):
            return pageurl
        elif pageurl.startswith('http'):
            pageurl = pageurl.replace('http', 'https')
            return pageurl
        return pageurl


DataFormat = DataFormat()
ym, language, category = '', '', ''


def xlsx_format_cope():
    """
    xlsx文件格式初始化, 文件名格式为：人名-域名-语言-表分类.xlsx
    """
    global ym, language, category
    # 获取当前路径下的所有文件和文件夹
    files = os.listdir(os.getcwd())
    # 仅保留.xlsx文件
    xlsx_files = [file for file in files if file.endswith('.xlsx')]
    file_name = xlsx_files[0]
    print('处理的文件名为：', file_name)

    name, ym, language, category = file_name.split('-')
    category = category.split('.')[0]

    print('ym:', ym, 'language:', language, 'category:', category)
    out_enfile_name = f"{name}-新-{ym}-单独-{language}-{category}"
    out_chfile_name = f"{name}-新-{ym}-站群-{language}-{category}"
    # 读取文件
    file_read = pd.read_excel(file_name, sheet_name=0)
    # 循环每一条数据 对数据进行 处理

    # 查看表有没有 value1,value2,value3,value3 列
    if 'value1' not in file_read.columns:
        file_read['value1'] = ''
    if 'value2' not in file_read.columns:
        file_read['value2'] = ''
    if 'value3' not in file_read.columns:
        file_read['value3'] = ''
    if 'value4' not in file_read.columns:
        file_read['value4'] = ''
    if 'value5' not in file_read.columns:
        file_read['value5'] = ''
    if 'value6' not in file_read.columns:
        file_read['value6'] = ''
    if 'value7' not in file_read.columns:
        file_read['value7'] = ''
    if 'value8' not in file_read.columns:
        file_read['value8'] = ''

    select_list = []

    for i in range(len(file_read)):
        # 读取每一条数据
        data = file_read.iloc[i]
        # print(data)
        # 拿到Pageurl
        Pageurl = data['PageUrl']
        Pageurl = DataFormat.pageurl_format(Pageurl)
        # 拿到title
        title = data['title']
        title = DataFormat.title_format(title)
        # 拿到brand
        brand = data['brand']
        brand = DataFormat.brand_format(brand)
        # 拿到category
        category = data['category']
        category = DataFormat.category_format(category)
        # 拿到price
        price = data['price']
        price = DataFormat.price_format(price)
        # 拿到image
        image = data['image']
        image = DataFormat.image_format(image)
        # 拿到gallery
        gallery = data['gallery']
        gallery = DataFormat.gallery_format(gallery)
        # 去重图片
        if not pd.isnull(gallery):
            gallery = gallery.split(';')
            gallery = list(set(gallery))
            if image in gallery:
                gallery.remove(image)
            gallery = ';'.join(gallery)
        # 拿到description
        description = data['description']
        description = DataFormat.description_format(description)

        """多选项"""
        value1 = data['value1'] if 'value1' in data else ''
        if not pd.isnull(value1) and value1 != '':
            value1 = json.loads(value1)
            for key, value in value1.items():
                value1_key = key.strip()
            if value1_key not in select_list:
                select_list.append(value1_key)

        value2 = data['value2'] if 'value2' in data else ''
        if not pd.isnull(value2) and value2 != '':
            value2 = json.loads(value2)
            for key, value in value2.items():
                value2_key = key.strip()
            if value2_key not in select_list:
                select_list.append(value2_key)

        value3 = data['value3'] if 'value3' in data else ''
        if not pd.isnull(value3) and value3 != '':
            value3 = json.loads(value3)
            for key, value in value3.items():
                value3_key = key.strip()
            if value3_key not in select_list:
                select_list.append(value3_key)

        value4 = data['value4'] if 'value4' in data else ''
        if not pd.isnull(value4) and value4 != '':
            value4 = json.loads(value4)
            for key, value in value4.items():
                value4_key = key.strip()
            if value4_key not in select_list:
                select_list.append(value4_key)

        value5 = data['value5'] if 'value5' in data else ''
        if not pd.isnull(value5) and value5 != '':
            value5 = json.loads(value5)
            for key, value in value5.items():
                value5_key = key.strip()
            if value5_key not in select_list:
                select_list.append(value5_key)

        value6 = data['value6'] if 'value6' in data else ''
        if not pd.isnull(value6) and value6 != '':
            value6 = json.loads(value6)
            for key, value in value6.items():
                value6_key = key.strip()
            if value6_key not in select_list:
                select_list.append(value6_key)

        value7 = data['value7'] if 'value7' in data else ''
        if not pd.isnull(value7) and value7 != '':
            value7 = json.loads(value7)
            for key, value in value7.items():
                value7_key = key.strip()
            if value7_key not in select_list:
                select_list.append(value7_key)

        value8 = data['value8'] if 'value8' in data else ''
        if not pd.isnull(value8) and value8 != '':
            value8 = json.loads(value8)
            for key, value in value8.items():
                value8_key = key.strip()
            if value8_key not in select_list:
                select_list.append(value8_key)

        # 覆盖原数据
        file_read.loc[i, 'PageUrl'] = Pageurl
        file_read.loc[i, 'title'] = title
        file_read.loc[i, 'brand'] = brand
        file_read.loc[i, 'category'] = category
        file_read.loc[i, 'price'] = price
        file_read.loc[i, 'image'] = image
        file_read.loc[i, 'gallery'] = gallery
        file_read.loc[i, 'description'] = description
        file_read.loc[i, 'value1'] = data['value1'] if 'value1' in data else ''
        file_read.loc[i, 'value2'] = data['value2'] if 'value2' in data else ''
        file_read.loc[i, 'value3'] = data['value3'] if 'value3' in data else ''
        file_read.loc[i, 'value4'] = data['value4'] if 'value4' in data else ''
        file_read.loc[i, 'value5'] = data['value5'] if 'value5' in data else ''
        file_read.loc[i, 'value6'] = data['value6'] if 'value6' in data else ''
        file_read.loc[i, 'value7'] = data['value7'] if 'value7' in data else ''
        file_read.loc[i, 'value8'] = data['value8'] if 'value8' in data else ''

        print('第', i, '条数据处理完成')

    # 记录行数
    rows0 = file_read.shape[0]
    rows = file_read.shape[0]

    # PageUrl	ID	产品名称	品牌名称	产品分类	产品封面	产品图片	产品SKU	产品价格	折扣价格	货币标识	产品描述	产品简介	SEO标题	SEO描述	SEO标签	多选项	Size    Color
    # 删除 产品名称为空的行
    file_read.dropna(subset=['title'], inplace=True)
    print('删除产品名称为空的行数：', rows - file_read.shape[0])
    rows = file_read.shape[0]

    # 删除 产品价格为空的行
    file_read.dropna(subset=['price'], inplace=True)
    print('删除产品价格为空的行数：', rows - file_read.shape[0])
    rows = file_read.shape[0]

    # 删除 PageUrl 重复的行
    file_read.drop_duplicates(subset=['PageUrl'], keep='first', inplace=True)
    print('删除Url重复的行数：', rows - file_read.shape[0])
    rows = file_read.shape[0]

    # 将price转换为float类型
    file_read['price'] = file_read['price'].astype(float)
    # 删除 产品价格不在 3-10000 之间的行
    file_read = file_read[(file_read['price'] >= 3) & (file_read['price'] <= 10000)]
    print('删除产品价格不在 3-10000 之间的行数：', rows - file_read.shape[0])
    rows = file_read.shape[0]

    # 删除产品封面为空的行
    file_read.dropna(subset=['image'], inplace=True)
    print('删除产品封面为空的行数：', rows - file_read.shape[0])
    rows = file_read.shape[0]

    # 删除产品封面重复的行
    file_read.drop_duplicates(subset=['image'], keep='first', inplace=True)
    print('删除产品封面重复的行数：', rows - file_read.shape[0])
    rows = file_read.shape[0]

    # 删除描述为空的行
    # file_read.dropna(subset=['description'], inplace=True)
    # print('删除描述为空的行数：', rows - file_read.shape[0])
    # rows = file_read.shape[0]

    # 删除brand为空的行
    # file_read.dropna(subset=['brand'], inplace=True)
    # print('删除brand为空的行数：', rows - file_read.shape[0])
    # rows = file_read.shape[0]

    # 处理后的行数
    rows2 = file_read.shape[0]
    print('总共删除的行数：', rows0 - rows2)
    print('当前剩余数行数：', rows2)

    # 当前的表格形式：PageUrl	ID	title	brand	category	productid	image	gallery	value1	value2	value3	sku	price	sprice	description	money

    index = ['ID', 'title', 'brand', 'category', 'productid', 'image', 'gallery']
    for select in select_list:
        # print(select)
        index.append(select)
    index = index + ['sku', 'price', 'sprice', 'description', 'PageUrl']
    # print("index:", index)
    print(file_read)
    pd2 = pd.DataFrame(columns=index)
    for i in range(len(file_read)):
        data = file_read.iloc[i]
        # print(data)
        # 拿到Pageurl
        Pageurl = data['PageUrl']
        # 拿到title
        title = data['title']
        # 拿到brand
        brand = data['brand']
        # 拿到category
        category = data['category']
        # 拿到price
        price = data['price']
        # 拿到image
        image = data['image']
        # 拿到gallery
        gallery = data['gallery']
        # 拿到description
        description = data['description']
        """构造多选项"""
        select_name = {}
        for ss in select_list:
            select_name[ss] = ''
        value1 = data['value1'] if 'value1' in data else ''
        if not pd.isnull(value1) and value1 != '':
            value1 = json.loads(value1)
            for key, value in value1.items():
                value1_key = key.strip()
                if value1_key in select_list:
                    value = [str(i).strip().replace(',', '.') for i in value if i != '']
                    value = [i for i in value if i != '']
                    value_ = list(set(value))
                    value_.sort(key=value.index)
                    select_name[value1_key] = ','.join(value_)
        value2 = data['value2'] if 'value2' in data else ''
        if not pd.isnull(value2) and value2 != '':
            value2 = json.loads(value2)
            for key, value in value2.items():
                value2_key = key.strip()
                if value2_key in select_list:
                    value = [str(i).strip().replace(',', '.') for i in value if i != '']
                    value = [i for i in value if i != '']
                    value_ = list(set(value))
                    value_.sort(key=value.index)
                    select_name[value2_key] = ','.join(value_)
        value3 = data['value3'] if 'value3' in data else ''
        if not pd.isnull(value3) and value3 != '':
            value3 = json.loads(value3)
            for key, value in value3.items():
                value3_key = key.strip()
                if value3_key in select_list:
                    value = [str(i).strip().replace(',', '.') for i in value if i != '']
                    value = [i for i in value if i != '']
                    value_ = list(set(value))
                    value_.sort(key=value.index)
                    select_name[value3_key] = ','.join(value_)
        value4 = data['value4'] if 'value4' in data else ''
        if not pd.isnull(value4) and value4 != '':
            value4 = json.loads(value4)
            for key, value in value4.items():
                value4_key = key.strip()
                if value4_key in select_list:
                    value = [str(i).strip().replace(',', '.') for i in value if i != '']
                    value = [i for i in value if i != '']
                    value_ = list(set(value))
                    value_.sort(key=value.index)
                    select_name[value4_key] = ','.join(value_)
        value5 = data['value5'] if 'value5' in data else ''
        if not pd.isnull(value5) and value5 != '':
            value5 = json.loads(value5)
            for key, value in value5.items():
                value5_key = key.strip()
                if value5_key in select_list:
                    value = [str(i).strip().replace(',', '.') for i in value if i != '']
                    value = [i for i in value if i != '']
                    value_ = list(set(value))
                    value_.sort(key=value.index)
                    select_name[value5_key] = ','.join(value_)
        value6 = data['value6'] if 'value6' in data else ''
        if not pd.isnull(value6) and value6 != '':
            value6 = json.loads(value6)
            for key, value in value6.items():
                value6_key = key.strip()
                if value6_key in select_list:
                    value = [str(i).strip().replace(',', '.') for i in value if i != '']
                    value = [i for i in value if i != '']
                    value_ = list(set(value))
                    value_.sort(key=value.index)
                    select_name[value6_key] = ','.join(value_)
        value7 = data['value7'] if 'value7' in data else ''
        if not pd.isnull(value7) and value7 != '':
            value7 = json.loads(value7)
            for key, value in value7.items():
                value7_key = key.strip()
                if value7_key in select_list:
                    value = [str(i).strip().replace(',', '.') for i in value if i != '']
                    value = [i for i in value if i != '']
                    value_ = list(set(value))
                    value_.sort(key=value.index)
                    select_name[value7_key] = ','.join(value_)
        value8 = data['value8'] if 'value8' in data else ''
        if not pd.isnull(value8) and value8 != '':
            value8 = json.loads(value8)
            for key, value in value8.items():
                value8_key = key.strip()
                if value8_key in select_list:
                    value = [str(i).strip().replace(',', '.') for i in value if i != '']
                    value = [i for i in value if i != '']
                    value_ = list(set(value))
                    value_.sort(key=value.index)
                    select_name[value8_key] = ','.join(value_)

        data = ['', title, brand, category, '', image, gallery] + list(select_name.values()) + \
               ['', price, '', description, Pageurl]
        # print(f"当前是第{i}个")
        pd2.loc[i] = data

    """保存 英文表格"""
    print('保存 英文表格中....')
    df = pd.DataFrame(np.insert(pd2.values, 0, values=index, axis=0))
    df.to_excel(f'{out_enfile_name}.xlsx', sheet_name='Sheet', index=False, header=False)
    print('保存 英文表格成功....\n 保存中文表格中....')
    """数据复制"""
    data_index = ['PageUrl', 'ID', 'title', 'brand', 'category', 'image', 'gallery', '产品SKU', 'price', '折扣价格',
                  'money', 'description', '产品简介', 'SEO标题', 'SEO描述', 'SEO标签', '多选项'] + select_list
    # PageUrl	ID	产品名称	品牌名称	产品分类	产品封面	产品图片	产品SKU	产品价格	折扣价格	货币标识	产品描述	产品简介	SEO标题	SEO描述	SEO标签	多选项	color	Size
    for index in data_index:
        # 如果index在pd2中
        if index in pd2.columns:
            continue
        else:
            pd2[index] = ''
    # print(pd2.index)
    try:
        money = file_read['money'][0]
    except Exception as e:
        while True:
            print('当前货币标识为空，请输入货币标识,商品链接为：', pd2['PageUrl'][random.randint(0, len(pd2) - 1)])
            money = input('请在money中输入货币标识，例如：USD :')
            if len(money) == 3:
                break
            else:
                print('输入错误，请重新输入--->')
    # print('money:', money)
    df = pd2[data_index]
    df['money'] = money
    # 添加表头
    add_index = ['PageUrl', 'ID', '产品名称', '品牌名称', '产品分类', '产品封面', '产品图片', '产品SKU', '产品价格',
                 '折扣价格', '货币标识', '产品描述',
                 '产品简介', 'SEO标题', 'SEO描述', 'SEO标签', '多选项'] + select_list
    df = pd.DataFrame(np.insert(df.values, 0, values=add_index, axis=0))
    df.to_excel(f'{out_chfile_name}.xlsx', sheet_name='Sheet', index=False, header=False)
    print('保存中文表格成功....\n 程序结束....')


if __name__ == '__main__':
    xlsx_format_cope()

# ******************************************************
# 2023-06-13更新：
# 1.增加了图片去重处理(主图不在附图中，附图不重复)
# 2.修改了4个多选项列的bug
# 3.增加了对价格范围删除的处理 3-10000
# 3.删除了对 描述、品牌 为空的行删除处理的代码
#
# 2023-06-14更新：
# 1.增加了图片切割处理，如果图片链接切割后不是.png或.jpg结尾的，就不切割
#
# 2023-06-20更新：
# 1.增加了多选项的去重排序，保持原有顺序
# 2.增加了货币标识的输入，如果货币标识为空，就输入货币标识
# 3.增加了对多选项内容和选项名的处理，避免格式错误
#
# 2023-06-30更新：
# 1.增加了对 Button按钮的删除处理
# 2.增加了对多选项内容 ，的替换成 . 处理，避免格式错误
# 3.增加了多 category 中空分类的处理
# 2023-07-05更新：
# 1.增加了对大写 AABC.COM 内容的删除
# 2023-07-07更新：
# 1.增加了对input标签的删除
# 2023-07-17更新：
# 1.添加了描述对script标签的删除

