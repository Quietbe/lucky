# -*- coding:utf-8 -*-
import json
import os
import re
from multiprocessing import Manager, Pool
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
            # 删除图片img标签  忽略换行符
            pattern = re.compile(r'<img.*?>', re.S)
            description = re.sub(pattern, '', description)
            # 删除 video标签
            pattern = re.compile(r'<video.*?</video>', re.S)
            description = re.sub(pattern, '', description)
            # 删除iframe标签
            pattern = re.compile(r'<iframe.*?</iframe>')
            description = re.sub(pattern, '', description)
            # 删除手机号   xxx-xxx-xxxx
            pattern = re.compile(r'\d*-\d*-\d*')
            description = re.sub(pattern, '', description)
            # 删除手机号   xxx-xxx
            pattern = re.compile(r'\d*-\d*')
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
            pattern = re.compile(r'\b[a-zA-Z].*?\.com')
            description = re.sub(pattern, '', description)
            # 删除 字母开头 .com结尾的所有链接
            pattern = re.compile(r'\b[a-zA-Z].*?\.html')
            description = re.sub(pattern, '', description)
            # 替换svg标签 为span
            pattern = re.compile(r'<svg.*?</svg>')
            description = re.sub(pattern, '', description)
            # 删除div标签
            pattern = re.compile(r'<div.*?>')
            description = re.sub(pattern, '', description)
            pattern = re.compile(r'</div>')
            description = re.sub(pattern, '', description)
            description = description.strip()
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


# error_text = {}  # {'文件名': '[错误信息，错误信息]'}


def jc(file_name, error_text):
    # global error_text
    error_text_ = {}
    file_read = pd.read_excel(file_name, sheet_name=0)
    # 循环每一条数据 对数据进行 处理
    print('当前文件数据量为：', len(file_read))
    columns_between = file_read.columns[file_read.columns.get_loc('gallery') + 1:file_read.columns.get_loc('sku')]
    error_text_[file_name] = {"Pageurl": [], "title": [], "category": [], "price": [], "image": [], "gallery": [],
                             "description": []}
    for col in columns_between:
        error_text_[file_name][col] = []

    for i in range(len(file_read)):
        # 读取每一条数据
        data = file_read.iloc[i]
        Pageurl = data['PageUrl']
        if pd.isnull(Pageurl):
            print('第{}条数据的Pageurl为空'.format(i + 2))
            # error_text[file_name].append('第{}条数据的Pageurl为空'.format(i + 2))
            error_text_[file_name]['Pageurl'].append('第{}条数据的Pageurl为空'.format(i + 2))
        title = str(data['title'])
        if pd.isnull(title):
            print('第{}条数据的title为空'.format(i + 2))
        else:
            title1 = title.strip()
            if title != title1:
                print('第{}条数据的title有空格'.format(i + 2))
                # error_text[file_name].append('第{}条数据的title有空格'.format(i + 2))
                error_text_[file_name]['title'].append('第{}条数据的 title 前后有空格'.format(i + 2))
        # brand = data['brand']
        category = data['category']
        if pd.isnull(category):
            print('第{}条数据的category为空'.format(i + 2))
            # error_text[file_name].append('第{}条数据的category为空'.format(i + 2))
            error_text_[file_name]['category'].append('第{}条数据的category为空'.format(i + 2))
        else:
            if "||" not in category:
                print('第{}条数据的category只有一个面包屑'.format(i + 2))
            else:
                category_list = category.split('||')
                for cate in category_list:
                    cate1 = cate.strip()
                    if cate != cate1:
                        print('第{}条数据的category有空格'.format(i + 2))
                        # error_text[file_name].append('第{}条数据的category有空格'.format(i + 2))
                        error_text_[file_name]['category'].append('第{}条数据的 category 前后有空格'.format(i + 2))
                        break
        # 拿到price
        price = data['price']
        if pd.isnull(price):
            print('第{}条数据的price为空'.format(i + 2))
            # error_text[file_name].append('第{}条数据的price为空'.format(i + 2))
            error_text_[file_name]['price'].append('第{}条数据的price为空'.format(i + 2))
        else:
            for fh in ['-', '£', '$', '€', ',']:
                if fh in str(price):
                    print('第{}条数据的price有问题'.format(i + 2))
                    # error_text[file_name].append('第{}条数据的price格式不正确'.format(i + 2))
                    error_text_[file_name]['price'].append('第{}条数据的price格式不正确'.format(i + 2))
                    break
        image = data['image']
        if pd.isnull(image):
            print('第{}条数据的 主图 为空'.format(i + 2))
            # error_text[file_name].append('第{}条数据的 主图 为空'.format(i + 2))
            error_text_[file_name]['image'].append('第{}条数据的 主图 为空'.format(i + 2))
        else:
            gallery = data['gallery']
            if not pd.isnull(gallery):
                gallery = gallery.split(';')
                if image in gallery:
                    print('第{}条数据的 主图 与 图库 重复'.format(i + 2))
                    # error_text[file_name].append('第{}条数据的 主图 与 图库 重复'.format(i + 2))
                    error_text_[file_name]['image'].append('第{}条数据的 主图 与 图库 重复'.format(i + 2))
        description = data['description']
        if pd.isnull(description):
            print('第{}条数据的description为空'.format(i + 2))
            # error_text[file_name].append('第{}条数据的description为空'.format(i + 2))
            # error_text[file_name]['description'].append('第{}条数据的description为空'.format(i + 2))
        else:
            re_list = r'<div *>|</div>|<a *>|</a>|<img *>|</img>|<iframe *>|</iframe>|<video *>|</video>'
            num = len(re.findall(re_list, description))
            if num > 0:
                print('第{}条数据的description有{}个标签'.format(i + 2, num))
                # error_text[file_name].append('第{}条数据的description有{}个标签'.format(i + 2, num))
                error_text_[file_name]['description'].append('第{}条数据的description有{}个标签'.format(i + 2, num))
        # 判断选项
        for column in columns_between:
            if pd.isnull(data[column]):
                continue
            select_list = str(data[column]).split(',')
            if len(select_list) != len(set(select_list)):
                print('第{}条数据的{}有重复'.format(i + 2, column))
                # error_text[file_name].append('第{}条数据的{}有重复'.format(i + 2, column))
                error_text_[file_name][column].append('第{}条数据的{}有重复'.format(i + 2, column))
            for select in select_list:
                select1 = select.strip()
                if select != select1:
                    print('第{}条数据的 {} 前后有空格'.format(i + 2, column))
                    # error_text[file_name].append('第{}条数据的{}有空格'.format(i + 2, column))
                    error_text_[file_name][column].append('第{}条数据的 {} 前后有空格'.format(i + 2, column))
                    break
            if '' in select_list:
                print('第{}条数据的{}有空元素'.format(i + 2, column))
                # error_text[file_name].append('第{}条数据的{}有空元素'.format(i + 2, column))
                error_text_[file_name][column].append('第{}条数据的{}有空元素'.format(i + 2, column))
    # queue.put(error_text)
    error_text[file_name] = json.dumps(error_text_[file_name])

def xlsx_format_cope():
    """
    对xlsx文件进行基础格式检查
    """
    # 获取当前路径下的所有文件和文件夹
    files = os.listdir(os.getcwd())
    # 仅保留.xlsx文件
    xlsx_files = [file for file in files if file.endswith('.xlsx')]

    manager = Manager()
    error_text = manager.dict()
    pool = Pool(processes=4)
    for file_name in xlsx_files:
        if '单独' in file_name:
            print('处理的文件名为：', file_name)
            pool.apply_async(jc, (file_name, error_text))
    pool.close()
    pool.join()
    # error_text = dict(error_text)
    # print('error_text:', error_text)

    for key, value in error_text.items():
        print(' 文件：' + key)
        value = json.loads(value)
        print('value:', value)
        for k, v in value.items():
            if len(v) > 0:
                print(k, f'({len(v)}): ', v if len(v) < 10 else v[:10])
        print('错误信息数量：', sum([len(v) for v in value.values()]), '\n')
    input("按任意键退出")


if __name__ == '__main__':
    input('只支持英文表格，中文表格请先转换为英文表格，按任意键继续')
    xlsx_format_cope()

# 2023-6-20 更新
# 1.优化了对image和gallery重复的判断
# 2.现在是多进程处理，速度更快
