import json
import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter import messagebox, scrolledtext

import requests
import yaml

apiNow = None
apiNowNo = None


def swap_values(list1, list2):
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
        apis = data['API']
    return apis


def getResult(textarea, listR, textarea2):
    # 获取文本框中的内容
    global apiNow
    global apiNowNo

    if apiNow is None and apiNowNo is None:
        selected_options, selected_no = get_selected_api()
        apiNow = selected_options
        apiNowNo = selected_no
    apis = getApi()
    api = apis[int(apiNowNo)]
    text = textarea.get("1.0", tk.END)
    print(api.values())
    url = list(api.values())[0]['url']
    #deeplx特供
    payload = json.dumps({
        "text": text,
        "source_lang": "auto",
        "target_lang": listR.get()
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, proxies={})
    #设置textarea的值为response.text
    textarea2.delete("1.0", tk.END)
    textarea2.insert("1.0", json.loads(response.text)['data'])
    # textarea2.config(state=tk.DISABLED)


def get_selected_api():
    # 弹出单选列表窗口
    apis = getApi()
    print(apis)
    apilist = [apiname['name'] for apix in apis for apiname in apix.values()]
    selected_options, selected_no = show_option_list(apilist)
    if selected_options:
        messagebox.showinfo("你选择了", f"你选择的接口是: {selected_options}")
    return selected_options, selected_no


def show_option_list(apilist):
    # 创建一个新的窗口用于显示单选列表
    option_window = tk.Toplevel()
    option_window.title("接口")

    # 定义选项列表
    options = apilist
    selected_options = None
    selected_No = None
    # 创建Listbox
    listbox = tk.Listbox(option_window, selectmode=tk.SINGLE, width=30, height=len(options))
    listbox.pack(pady=10)

    # 将选项添加到Listbox
    for option in options:
        listbox.insert(tk.END, option)

    def on_select():
        nonlocal selected_options
        nonlocal selected_No
        # 获取选中的选项
        selected_index = listbox.curselection()
        if selected_index:
            selected_option = listbox.get(selected_index[0])
            option_window.destroy()
            selected_options = selected_option
            selected_No = selected_index[0]
            return selected_option, selected_No
        else:
            messagebox.showwarning("警告", "请选择一个选项")
            return None

    # 创建确定按钮
    confirm_button = tk.Button(option_window, text="确定", command=on_select)
    confirm_button.pack(pady=5)

    # 运行新窗口的主循环
    option_window.grab_set()  # 模态窗口
    option_window.wait_window()  # 等待窗口关闭
    return selected_options, selected_No


def show_about():
    messagebox.showinfo("关于", "自用简易翻译器\n作者：zyarin\n版本：1.0")


def translate():
    root = tk.Tk()
    root.title("自用简易翻译器")

    # 设置窗口大小
    root.geometry("600x200")

    # 创建菜单栏
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # 添加“关于”菜单
    # 创建一个顶级菜单
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="选择接口", command=get_selected_api)
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="关于", command=show_about)
    menubar.add_cascade(label="帮助", menu=help_menu)
    menubar.add_cascade(label="翻译接口", menu=file_menu)

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
    swap_button = tk.Button(frame_top, text="⇄", command=lambda: swap_values(dropdown1, dropdown2))
    swap_button.pack(side="left", padx=5, pady=5)

    # 下半部分的两个滚动文本框
    text1 = scrolledtext.ScrolledText(frame_bottom, wrap=tk.WORD, xscrollcommand=True, yscrollcommand=True)
    text2 = scrolledtext.ScrolledText(frame_bottom, wrap=tk.WORD, xscrollcommand=True, yscrollcommand=True)
    # url, key, attr = getApi()
    translateButton = tk.Button(frame_bottom, text="GO",
                                command=lambda: getResult(text1, dropdown2, text2), height=1, width=3)

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
