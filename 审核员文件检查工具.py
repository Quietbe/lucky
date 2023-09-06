import sys
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, \
    QFileDialog, QMessageBox
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
import tkinter as tk
import jinja2


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
    data["产品图片"] = data["产品图片"].split(';')
    print('产品图片', data["产品图片"])
    print(data)
    template = """ 
    <html>
    <body>
        <p> {{ data['产品分类'] }}  </p?>
      <h1>{{data["产品名称"]}}</h1>
        <p>产品链接: </p>
        <a href="{{data['PageUrl']}}" target="_blank">{{data["PageUrl"]}}</a>
        <h2>产品图片</h2>
        <img src="{{data["产品封面"]}}" style='max-width: 200px;'>
        {% for img in data["产品图片"] %}
        <img src="{{ img }}" style='max-width: 200px;'>
        {% endfor %}
        <hr>
        <h3>品牌: {{data["品牌名称"]}}</h3>
        <hr>
        <h3>价格:  {{data["产品价格"]}}  {{data["货币标识"]}}</h3>
        <hr>
        <div>{{data["产品描述"]}}</div>
        <hr>
        {% for key,val in select_data_list.items() %}
            <h3>{{key}}:  {{val}}</h3>
            {% for option in val.split(',') %}
                <button>{{option}}</button>
            {% endfor %}
            <hr>
        {% endfor %}
    </body>
    </html>
    """
    # https://www.revitsport.com/us_en/race-leathers-argon-2-black-white		One Piece Argon 2		Men||Motorcycle Suits	https://www.revitsport.com/media/catalog/product/2/0/20230101-060738_FOL037-One-Piece-Argon-2-Black-White-front-jpg.jpg	https://www.revitsport.com/media/catalog/product/2/0/20230101-060748_FOL037-One-Piece-Argon-2-Black-White-back-jpg.jpg		999.99		USD	The Argon 2 racing suit has a bold, figure-hugging profile constructed from Monaco cowhide, assuring rugged protection from abrasion-resistant leather to keep the luster lasting longer. When you’re setting the pace, PWR|Shell stretch textile liberates your motion, giving you more range to shift riding position as you hold the racing line. And when you’re chasing that lowest lap time, knitted 3D spacer mesh and a perforated outer shell both ventilate and cool you as the track heats up.<br><br>Tailor-made protection<br>With AAA-standard Betac® protection at shoulders, knees, and elbows – this is CE-rated kit designed to take to the track. Protector pockets in this high-safety spec REV'IT! one-piece provides race-ready options of SEESOFT back and split chest protectors. SEESMART hip protection is lightweight and ventilated, and safety seams throughout the suit add inner strength – keeping the outer shell panels tightly fused together.<br><br>Pure race aesthetics<br>Argon 2 is what happens when all-round style meets substance. Feel the part with a look inspired by professional racing leathers – we’re talking outspoken colors, bold graphics, and shoulder armor straight out of MotoGP. Because when you look good, you feel good. And when you feel good, you take to the track with that extra bit of confidence and conviction.						46,48,50,52,54,56	standard

    template = jinja2.Template(template)
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

    def loadFile(self):
        # self.table = QTableWidget()
        path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')

        if path:
            df = pd.read_excel(path)
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

    def checkRow(self, row):
        print('当前点击的行数:', row)
        data = self.df.iloc[row]
        print(data)
        # QMessageBox.information(self, '行数据', str(data))  # 弹窗
        # 将data复制到剪切板
        self.cope_url.clipboard_clear()
        self.cope_url.clipboard_append(data['PageUrl'])
        # self.cope_url.destroy()

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
        # 设置置顶
        self.window.setWindowFlags(self.window.windowFlags() | Qt.WindowStaysOnTopHint)
        self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle('文件检查工具')
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())
