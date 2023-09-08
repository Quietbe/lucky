import sys
from functools import partial
from os import startfile
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, \
    QFileDialog, QStatusBar
from pandas import read_excel
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
import tkinter as tk
# import jinja2
from jinja2 import Template


def render_html(data):
    data = data.fillna('')
    # 拿到 产品选项以后的列
    select_data_list = data[9:].to_dict()
    del_keys = []
    for key, val in select_data_list.items():
        if not val:
            del_keys.append(key)
    for key in del_keys:
        del select_data_list[key]
    print('删除完成')
    print("select_data_list", select_data_list)
    # data = data.to_dict(na_action='null')
    data["产品图片"] = data["产品图片"].split(';')  # if data['产品图片'] != '' else []
    print('产品图片', data["产品图片"])
    print(data)
    template = """ 
    <html>
    <body>
        <p>产品链接: </p>
        <a href="{{data['PageUrl']}}" target="_blank">{{data["PageUrl"]}}</a>
        <hr>
        <p> {{ data['产品分类'] }}  </p?>
        <hr>
        <h1>{{data["产品名称"]}}</h1>
        <hr>
        <h3>品牌: {{data["品牌名称"]}}</h3>
        <hr>
        <h3>价格:  {{data["产品价格"]}}  {{data["货币标识"]}}</h3>
        <hr>
        {% for key,val in select_data_list.items() %}
            <h3>{{key}}:  {{val}}</h3>
            {% for option in val.split(',') %}
                <button>{{option}}</button>
            {% endfor %}
            <hr>
        {% endfor %}
        <hr>
        <div>{{data["产品描述"]}}</div>
        <hr>
        <h2>产品图片</h2>
        <img class="myImage" src="{{data["产品封面"]}}" alt='123' style="max-width: 200px;">
        <p class="imageSize"></p>
        <div style="display: flex;flex-wrap: wrap;">
        {% for img in data["产品图片"] %}
            <div>
            <img class="myImage" src="{{ img }}" style="max-width: 200px;">
            <p class="imageSize"></p>
            </div>
        {% endfor %}
        </div>    
        <script>
        // 使用 window.onload 事件确保页面和资源加载完成后执行
        window.onload = function () {
            // 获取所有带有 "myImage" 类的图像元素
            var images = document.getElementsByClassName('myImage');

            // 遍历所有图像元素
            for (var i = 0; i < images.length; i++) {
                // 创建一个新的Image对象以获取图像的尺寸
                var imgSize = new Image();
                imgSize.src = images[i].src;
                // 获取与当前图像关联的 p 标签
                var pElement = document.getElementsByClassName('imageSize')[i];
                var imageWidth = imgSize.width;
                var imageHeight = imgSize.height;
                // 更新 p 标签的文本以显示图像的大小
                // pElement.textContent = 'Width: ' + imageWidth + 'px, Height: ' + imageHeight + 'px';
                pElement.textContent = 'Size: ' + imageWidth + 'x' + imageHeight;
            }
        };
        </script>
    </body>
    </html>
    """

    # template = jinja2.Template(template)
    template = Template(template)
    return template.render(data=data, select_data_list=select_data_list)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 read xlsx")
        self.resize(500, 300)
        layout = QVBoxLayout()

        self.btn = QPushButton('选择文件')
        self.btn.clicked.connect(self.loadFile)

        # 表格初始化
        self.table = QTableWidget()
        layout.addWidget(self.btn)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # 原表数据初始化
        self.df = None

        # 初始化剪切板
        self.cope_url = tk.Tk()
        self.cope_url.withdraw()

        # # 窗口URl展示
        # self.statusBar = QStatusBar()
        # self.setStatusBar(self.statusBar)
        # self.browser2.urlChanged.connect(self.update_urlbar)
        # central_widget = QWidget()
        # self.setCentralWidget(central_widget)
        # central_widget.setLayout(QVBoxLayout())
        # central_widget.layout().addWidget(self.browser2)


    def loadFile(self):
        # self.table = QTableWidget()
        path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')

        if path:
            df = read_excel(path)
            # 删除 id 列
            df = df.drop(['ID', '产品SKU', '折扣价格', '产品简介', 'SEO标题', 'SEO描述', 'SEO标签', '多选项'], axis=1)
            self.df = df
            # 增加一列用于放按钮
            self.table.setColumnCount(df.shape[1] + 1)
            self.table.setRowCount(df.shape[0])
            # for i in range(df.shape[0]):
            #     print("i:", i)
            #     # 添加按钮
            #     btn = QPushButton('检查')
            #     self.table.setCellWidget(i, df.shape[1], btn)
            #     btn.clicked.connect(partial(self.checkRow, i))
            #     # 添加数据
            #     for j in range(df.shape[1]):
            #         self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
            # self.table.setHorizontalHeaderLabels(df.columns)
            # 重置table
            self.table.clear()

            for i in range(df.shape[0]):
                # 添加按钮
                btn = QPushButton('检查')
                # 改为设置在第一列
                self.table.setCellWidget(i, 0, btn)
                btn.clicked.connect(partial(self.checkRow, i))
                # 添加数据
                for j in range(df.shape[1]):
                    self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
            self.table.setHorizontalHeaderLabels(df.columns)

    def update_urlbar(self, url):
        self.statusBar.showMessage(url.toString())


    def checkRow(self, row):
        print('当前点击的行数:', row)
        data = self.df.iloc[row]
        print(data)
        # QMessageBox.information(self, '行数据', str(data))  # 弹窗
        # 将data复制到剪切板
        self.cope_url.clipboard_clear()
        self.cope_url.clipboard_append(data['PageUrl'])
        # self.cope_url.destroy()

        """渲染Web"""
        html = render_html(data)  # 使用data渲染模板
        self.window = QWidget()
        self.window.setWindowTitle('商品详情')
        self.browser = QWebEngineView()
        self.browser.setHtml(html)
        self.window.setLayout(QVBoxLayout())
        self.window.layout().addWidget(self.browser)
        # 设置窗口位置
        # self.window.setGeometry(1, 40, 800, 600)
        # 设置窗口放在左上角
        self.window.move(1, 1)
        # 设置窗口的透明度为0.5
        self.window.setWindowOpacity(0.95)
        # 设置置顶
        self.window.setWindowFlags(self.window.windowFlags() | Qt.WindowStaysOnTopHint)
        self.window.show()

        """展示原来网页"""
        # self.window2 = QWidget()
        # self.window2.setWindowTitle('商品详情')
        # self.browser2 = QWebEngineView()
        # self.browser2.load(QUrl(data['PageUrl']))
        # self.window2.setLayout(QVBoxLayout())
        # self.window2.layout().addWidget(self.browser2)
        # # 设置窗口位置
        # # self.window2.setGeometry(1, 1, 800, 1200)
        # # 设置窗口放在左上角
        # # self.window2.move(800, 1)
        # # 设置置顶
        # # self.window2.setWindowFlags(self.window2.windowFlags() | Qt.WindowStaysOnTopHint)
        # # 全屏
        # desktop = QApplication.desktop()
        # screenRect = desktop.screenGeometry()
        # height = screenRect.height()
        # width = screenRect.width()
        # self.window2.resize(width, height)
        # self.window2.show()
        """浏览器唤醒"""
        # from os import startfile
        startfile(data['PageUrl'])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle('文件检查工具')
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())
