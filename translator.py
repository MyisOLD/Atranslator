import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,scrolledtext

import requests
import yaml

def swap_values(list1,list2):
    # 获取两个下拉框的当前值
    value1 = list1.get()
    value2 = list2.get()

    # 交换两个下拉框的值
    list1.set(value2)
    list2.set(value1)

def getApi():
    # 解析yml文件
    with open('api.yml', 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        apiurl=data['API']['API1']['url']
        apikey=data['API']['API1']['key']
        apiattr=data['API']['API1']['attr']
    return apiurl,apikey,apiattr


def getResult(textarea,list2,url,key,attr,textarea2):
    # 获取文本框中的内容
    text = textarea.get("1.0", tk.END)
    payload = json.dumps({
        "text": text,
        "source_lang": "auto",
        "target_lang": list2.get()
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload,proxies={})
    #设置textarea的值为response.text
    textarea2.delete("1.0", tk.END)
    textarea2.insert("1.0", response.text)
    # textarea2.config(state=tk.DISABLED)




def show_about():
    messagebox.showinfo("关于", "自用简易翻译器\n作者：zyarin\n版本：1.0")
def translate():
    root = tk.Tk()
    root.title("自用简易翻译器")

    # 设置窗口大小
    root.geometry("600x400")

    # 创建菜单栏
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # 添加“关于”菜单
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="关于", command=show_about)
    menubar.add_cascade(label="帮助", menu=help_menu)

    # 上半部分，占据20%
    frame_top = tk.Frame(root, bg="white", height=60)
    frame_top.pack(fill="both", expand=False)

    # 下半部分，占据80%
    frame_bottom = tk.Frame(root, bg="lightgray", height=240)
    frame_bottom.pack(fill="both", expand=True)

    # 上半部分的两个下拉框
    options = ["EN", "ZH", "JP"]
    dropdown1 = ttk.Combobox(frame_top, values=options)
    dropdown2 = ttk.Combobox(frame_top, values=options)
    dropdown1.current(0)
    dropdown2.current(1)
    # 设置下拉框的布局
    dropdown1.pack(side="left", expand=True, padx=10, pady=10)
    dropdown2.pack(side="right", expand=True, padx=10, pady=10)

    # 添加交换按钮
    swap_button = tk.Button(frame_top, text="⇄", command=lambda:swap_values(dropdown1,dropdown2))
    swap_button.pack(side="left", padx=5, pady=5)


    # 下半部分的两个滚动文本框
    text1 = scrolledtext.ScrolledText(frame_bottom, wrap=tk.WORD, xscrollcommand=True, yscrollcommand=True)
    text2 = scrolledtext.ScrolledText(frame_bottom, wrap=tk.WORD, xscrollcommand=True, yscrollcommand=True)
    url,key,attr=getApi()
    translateButton = tk.Button(frame_bottom, text="GO", command=lambda:getResult(text1,dropdown2,url,key,attr,text2),height=1, width=3)

    # 使用 grid 布局管理器
    frame_bottom.grid_rowconfigure(0, weight=1)

    frame_bottom.grid_columnconfigure(0, weight=1)
    frame_bottom.grid_columnconfigure(1, weight=0)
    frame_bottom.grid_columnconfigure(2, weight=1)

    # 设置文本框的布局
    translateButton.grid(row=0, column=1, sticky="ns", padx=1, pady=1)
    text1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    text2.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    translate()
