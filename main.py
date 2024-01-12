import sys
import requests
import os
import time
from PyQt5.QtGui import QFont, QDoubleValidator, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedLayout, QLabel, \
    QLineEdit, QFormLayout, QGroupBox, QRadioButton, QTextBrowser, QSizePolicy, QButtonGroup, QFileDialog, QCheckBox


class MYSWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_mys_ui()

    def init_mys_ui(self):
        """
        米游社爬虫主界面
        """
        self.resize(1400, 800)  # 设置MyWindow的宽高
        self.setWindowTitle("爬取米游社帖子里的图片")

        font_chinese_SimSun12 = QFont("SimSun", 12)
        font_chinese_SimSun16Bold = QFont("SimSun", 16)
        font_chinese_SimSun16Bold.setBold(True)
        font_english_Times12 = QFont("Times New Roman", 12)
        Input_Width = 800
        Input_Height = 30

        self.Vlayout = QVBoxLayout()
        self.setStyleSheet("background-color:rgba(255, 255, 255, 1);")

        self.Hlayout_Title = QHBoxLayout()

        self.Hlayout_BaseInfo = QHBoxLayout()
        self.layout_mys_Info = QVBoxLayout()
        self.btn_Vlayout = QVBoxLayout()

        self.Hlayout_text = QHBoxLayout()

        self.title = QLabel("米游社帖子爬取")
        self.title.setFont(font_chinese_SimSun16Bold)
        self.title.setStyleSheet("background-color:rgba(102, 204, 255, 0.6);")

        self.label_mysInfo = QLabel("基本信息：")
        self.label_mysInfo.setFont(font_chinese_SimSun16Bold)
        self.label_mysInfo.setStyleSheet("color: red;")
        self.mysInfo_formlayout = QFormLayout()  # 表单容器
        """帖子ID"""
        self.input_ID = QLineEdit()  # ID输入框
        self.input_ID.setPlaceholderText("ID")  # 设置提示语
        self.input_ID.setFont(font_english_Times12)
        self.input_ID.setFixedSize(Input_Width, Input_Height)
        """Cookie和User-Agent"""
        self.input_Cookie = QLineEdit()  # ID输入框
        self.input_Cookie.setPlaceholderText("你的米游社Cookie")  # 设置提示语
        self.input_Cookie.setFont(font_english_Times12)
        self.input_Cookie.setFixedSize(Input_Width, Input_Height)
        self.input_UserAgent = QLineEdit()  # ID输入框
        self.input_UserAgent.setPlaceholderText("代理浏览器型号User-Agent")  # 设置提示语
        self.input_UserAgent.setFont(font_english_Times12)
        self.input_UserAgent.setFixedSize(Input_Width, Input_Height)

        label1 = QLabel("帖子ID:")
        label1.setFont(font_english_Times12)
        label2 = QLabel("Cookie:")
        label2.setFont(font_english_Times12)
        label3 = QLabel("User-Agent:")
        label3.setFont(font_english_Times12)
        self.mysInfo_formlayout.addRow(label1, self.input_ID)
        self.mysInfo_formlayout.addRow(label2, self.input_Cookie)
        self.mysInfo_formlayout.addRow(label3, self.input_UserAgent)
        self.layout_mys_Info.addWidget(self.label_mysInfo)
        self.layout_mys_Info.addLayout(self.mysInfo_formlayout)
        self.layout_mys_Info.addStretch(1)

        """按钮"""
        self.btn_press1 = QPushButton("点击开始")
        self.btn_press1.setFixedSize(100, 40)
        self.btn_press1.setStyleSheet("QPushButton {"
                                      "background-color:rgba(170, 102, 128, 0.7);"  # 设置按钮
                                      "border: none;"  # 移除按钮的边框
                                      "font-weight: bold;"   # 加粗
                                      "color: white;"  # 文本颜色
                                      "padding: 6px 12px;"  # 按钮内边距
                                      "text-align: center;"  # 文本居中对齐
                                      "text-decoration: none;"  # 移除按钮文本的装饰（如下划线）
                                      "display: inline-block;"  # 行内块级元素
                                      "font-size: 16px;"  # 字体大小
                                      "margin: 2px 1px;"  # 外边距
                                      "cursor: pointer;"  # 设置鼠标悬停在按钮上时的光标样式为指针
                                      "border-radius: 8px;"  # 设置按钮边框的圆角半径
                                      "}"
                                      )
        self.btn_press2 = QPushButton("存储Cookie")
        self.btn_press2.setFixedSize(120, 40)
        self.btn_press2.setStyleSheet("QPushButton {"
                                      "background-color:rgba(102, 204, 255, 0.8);"  # 设置按钮颜色
                                      "border: none;"  # 移除按钮的边框
                                      "font-weight: bold;"   # 加粗
                                      "color: white;"  # 文本颜色
                                      "padding: 6px 12px;"  # 按钮内边距
                                      "text-align: center;"  # 文本居中对齐
                                      "text-decoration: none;"  # 移除按钮文本的装饰（如下划线）
                                      "display: inline-block;"  # 行内块级元素
                                      "font-size: 16px;"  # 字体大小
                                      "margin: 2px 1px;"  # 外边距
                                      "cursor: pointer;"  # 设置鼠标悬停在按钮上时的光标样式为指针
                                      "border-radius: 8px;"  # 设置按钮边框的圆角半径
                                      "}"
                                      )
        self.btn_press1.clicked.connect(self.mysArticle)
        self.btn_press2.clicked.connect(self.store_data)
        self.btn_Vlayout.addWidget(self.btn_press1)
        self.btn_Vlayout.addWidget(self.btn_press2)

        """提示框"""
        self.show_ReadData = QTextBrowser()
        self.show_ReadData.setText("初始化Cookie和User-Agent：\n")
        self.show_ReadData.setStyleSheet("color: gray;" "font-size: 18px;")  # 字体大小
        self.show_ReadData.setFixedSize(300, 150)

        self.show_SpiderData = QTextBrowser()
        self.show_SpiderData.setText("这里会展示爬取的进度")
        self.show_SpiderData.setStyleSheet("color: black;" "font-size: 16px;")  # 字体大小
        self.show_SpiderData.setFixedSize(600, 300)

        self.show_Tips = QTextBrowser()
        self.show_Tips.setText("  进入exe立刻读取本地数据，如无本地数据才需要输入Cookie和User-Agent\n"
                               "  点击“点击开始”即可开始爬取\n"
                               "  点击“存储Cookie”可以存储当前界面的Cookie和User-Agent")
        self.show_Tips.setStyleSheet("color: hotpink;" "font-size: 21px;" "font-weight: bold;")  # 字体大小
        self.show_Tips.setFixedSize(320, 210)

        self.Hlayout_text.addWidget(self.show_ReadData)
        self.Hlayout_text.addWidget(self.show_SpiderData)
        self.Hlayout_text.addWidget(self.show_Tips)

        """格式"""
        self.Hlayout_Title.addStretch(1)
        self.Hlayout_Title.addWidget(self.title)
        self.Hlayout_Title.addStretch(1)

        self.Hlayout_BaseInfo.addLayout(self.layout_mys_Info)
        self.Hlayout_BaseInfo.addStretch(1)
        self.Hlayout_BaseInfo.addLayout(self.btn_Vlayout)
        self.Hlayout_BaseInfo.addStretch(2)

        self.Vlayout.addLayout(self.Hlayout_Title)
        self.Vlayout.addLayout(self.Hlayout_BaseInfo)
        self.Vlayout.addLayout(self.Hlayout_text)
        self.Vlayout.addStretch(1)

        self.setLayout(self.Vlayout)
        # self.post_id = "47568922"  # 帖子ID
        self.read_data()

    def mysArticle(self):
        """
        传入post_id来爬取指定帖子
        """
        self.getUI_data()
        headers = {
            "User-Agent": self.UserAgent_str,
            "Cookie": self.Cookie_str,
            "Referer": "https://www.miyoushe.com/"
        }
        r = requests.get(url=self.url, headers=headers)
        print(r.text)
        print(r.json())
        jsonALL = r.json()
        file = "米游社帖子图片" + "\\" + str(self.post_id)
        if not os.path.exists(file):
            os.makedirs(file)

        imagesALL = jsonALL['data']['post']['post']['images']
        authorName = jsonALL['data']['post']['user']['nickname']
        authorIntroduce = jsonALL['data']['post']['user']['introduce']
        authorUID = jsonALL['data']['post']['user']['uid']
        self.show_SpiderData.setText("开始爬取：\n" + "帖子作者名：" + authorName)
        self.show_SpiderData.append("图片总数：" + str(len(imagesALL)))
        with open(file + "\\创作者昵称：" + str(authorName) + ".txt", mode='w') as f:
            f.write("nickname:" + authorName)
            f.write("\nintroduce:" + authorIntroduce)
            f.write("\nUID:" + authorUID)
        for i, imageURL in enumerate(imagesALL):
            imageName = imageURL.split('_')[-1]
            # 请求url，拿到图片内容
            image = requests.get(imageURL).content
            self.show_SpiderData.append("图片已保存:" + str(i) + "/" + str(len(imagesALL)) + "  图片名：" + imageName)
            with open(file + "\\" + imageName, mode='wb') as f:
                f.write(image)
            time.sleep(1)

    def getUI_data(self):
        """获取UI里的data
        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0
        account_mid_v2=0aat9qm2q4_mhy; _MHYUUID=75b7f1f4-d41c-4340-83ef-4c82281e30b6; DEVICEFP_SEED_ID=d2d3d836e7cb5e40; DEVICEFP_SEED_TIME=1669992487487; _ga=GA1.1.206487417.1669992488; ltmid_v2=0aat9qm2q4_mhy; ltuid_v2=332270411; mi18nLang=zh-cn; cookie_token=1kdXmGhHF0XKkyB8QBCVIs2HY7yhrajKNIiMgp8m; account_id=332270411; ltoken=hJDblptMbkcK2gN3CwOQqMzLVdzVl3qQLD8le06f; ltuid=332270411; cookie_token_v2=v2_uPppaaFZihPTEazsqu8QaZNbsiZarVruH83Crai9V_C-fZYbWDLkCVN8bCTbbjPQR7AqOqxIvj1XwCiRc9jbQGHVEa7gXSh5R7nv0quAwDVqPenZGQeteL-47VrQVQTGz5a7; account_id_v2=332270411; ltoken_v2=v2_4A-7ntQCB_q2LajImEmX3ljdt2nM34RkUrN7V4cct59xOElqpYX-4R4epFklBUftLI5FccScRNRZpJjOHmjjz16NY_cG_rRB5NrMDujhorNi8MArknLPVBnw1nE4JNbiHWg=; DEVICEFP=38d7f29418ea8; acw_tc=0a324f9517049820670854516e706f8e5de8d99f6bd5eaf12fd852189dd57a; _ga_KS4J8TXSHQ=GS1.1.1704982086.504.1.1704982110.0.0.0
        """
        self.post_id = int(self.input_ID.text())
        self.UserAgent_str = self.input_UserAgent.text()
        self.Cookie_str = self.input_Cookie.text()
        self.url = f"https://bbs-api.miyoushe.com/post/wapi/getPostFull?gids=2&post_id={self.post_id}&read=1"

    def store_data(self):
        """存储Cookie和User-Agent"""
        self.getUI_data()
        with open("UserAgent.txt", mode='w') as f:
            f.write(self.UserAgent_str)
        with open("Cookie.txt", mode='w') as f:
            f.write(self.Cookie_str)

    def read_data(self):
        """读取Cookie和User-Agent"""
        user_agent_file = "UserAgent.txt"
        cookie_file = "Cookie.txt"
        # 读取 UserAgent
        try:
            with open(user_agent_file, mode='r') as f:
                self.UserAgent_str = f.read().strip()
                self.input_UserAgent.setText(str(self.UserAgent_str))
        except FileNotFoundError:
            self.show_ReadData.append(f"File '{user_agent_file}' not found.")
        except Exception as e:
            self.show_ReadData.append(f"Error reading '{user_agent_file}': {str(e)}")
        # 读取 Cookie
        try:
            with open(cookie_file, mode='r') as f:
                self.Cookie_str = f.read().strip()
                self.input_Cookie.setText(str(self.Cookie_str))
        except FileNotFoundError:
            self.show_ReadData.append(f"File '{cookie_file}' not found.")
        except Exception as e:
            self.show_ReadData.append(f"Error reading '{cookie_file}': {str(e)}")
        # 验证文件是否为空
        if not self.UserAgent_str or not self.Cookie_str:
            self.show_ReadData.append("UserAgent or Cookie data is missing or empty.")
        else:
            self.show_ReadData.append("成功读取本地Cookie文件")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MYSWindow()
    win.show()
    app.exec()
