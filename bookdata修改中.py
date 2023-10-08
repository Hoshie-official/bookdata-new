import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import messagebox
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import datetime
from tkinter import Tk, NoDefaultRoot,messagebox
from tkinter.ttk import Combobox
from ttkbootstrap import Style



def save_data():
    url1 = url_entry.get()
    # 将网址替换成类似移动端的页面，这里有更精确的点击数
    url = url1.replace('book', 'm').replace('Novel', 'b')
    if not url:
        messagebox.showerror("Error", "请输入一个网址")
        return
    #input('0')
    
    # 发送 HTTP 请求获取网页内容
    response = urlopen(url)

    # 获取网页的 HTML 内容
    html_content = response.read().decode('utf-8')
        
    #input('01')

    # 创建 BeautifulSoup 对象
    soup = BeautifulSoup(html_content, 'html.parser')

    # 获取第五个span元素，这个元素的内容是小说的名字
    # 这里我修改了，因为前面替换了网址内容。现在是另外一个html网页
    span_element4 = soup.select('.book_newtitle')[0]
    span_text4 = span_element4.text
        
    # 检查'name.xlsx'里面有没有相应的网址
    #input('02')
        
    df = pd.read_excel('name.xlsx')
    #print(df)
        
    input('001')
    if url1 in df['URL'].values:
        messagebox.showinfo("警告", "网址已存在")
            
    else:
            
        # 把网址和获取的书名保存到Excel表格里
        df_new = pd.DataFrame({'URL':[url1], 'Span Text':[span_text4]})
        #print(df_new.dtypes)
        #print(df.dtypes)
      
            
        df = pd.concat([df, df_new], ignore_index=True)
        #df = df.append(df_new, ignore_index=True)
            
       
        df.to_excel('name.xlsx', index=False)
        #input('2')
        
        # Create new Excel file with name as span_text4
        if not pd.isnull(span_text4):
            df_span = pd.DataFrame({'Data':[], 'Time': [], 'Difference': []})
            df_span.to_excel(f"{span_text4}.xlsx", index=False)
                
            
        
        # 这里是把列表更新
        df = pd.read_excel('./name.xlsx')

        options = df['Span Text'].dropna().tolist()
        dropdown['values'] = []
        dropdown['values'] = options
        #update_values()
        #update_options()
        
        
        
        

        
            
        #input('4')
            
        messagebox.showinfo("提示", "数据保存成功")
'''            
def convert_to_int(string):
    parts = re.findall(r'\d+', string)
    if "万" in string:
        
        if len(parts) == 2:
            num = float(parts[0]) * 10000 + float(parts[1]) * 1000
            return int(num)
        else:
            num = float(parts[0]) * 10000
            return int(num)
    else:
        num = int(parts[0])
        return int(num)
    return int(string)
'''
def get_data():
    
        
        selected_value = dropdown.get()
        
        if not selected_value:
            messagebox.showerror("Error", "请选取一个值。")
            return
        
        df = pd.read_excel('name.xlsx')
        
        
        # 检索选定的span_text4对应的URL
        url1 = df.loc[df['Span Text'] == selected_value, 'URL'].values[0]
        url = url1.replace('book', 'm').replace('Novel', 'b')
        
        
        # 发送HTTP请求以检索网页内容
        response = urlopen(url)
        
        
        # 获取网页的 HTML 内容
        html_content = response.read().decode('utf-8')
        
        # 创建 BeautifulSoup 对象
        soup = BeautifulSoup(html_content, 'html.parser')
        
        
        # 获取第七个span元素，提取其文本内容，并使用正则表达式查找数字。
        span_element = soup.select('.book_info3')[0]
        s = span_element.text
        span_text = s[s.index("/", s.index("/") + 1) + 2: s.index(" ", s.index("/", s.index("/") + 1) + 2)]
        # numbers = re.findall(r'\d+', span_text)
        # number = convert_to_int(span_text)
        number = int(span_text)
        
        
        df_span = pd.read_excel(f"{selected_value}.xlsx")
        print(df_span)
        
        
        if df_span.empty:
            # 如果Excel文件为空，则保存当前数据并更新列。
            difference = 0
            df_span = pd.DataFrame({'Data':number, 'Time':[datetime.now()], 'Difference':[0]})
            df_span.to_excel(f"{selected_value}.xlsx", index=False)
        else:
            # 比较当前数据与之前的数据
            #input('1')
            previous_data = df_span['Data'].values[-1]
            
            if int(number) == int(previous_data):
                difference = 0
            else:
                difference = int(number) - int(previous_data)
            #input('3')
            
            if difference != 0:
                # 创建要添加的数据
                new_data = {'Data': number, 'Time': datetime.now(), 'Difference': difference}
                # 使用concat方法将数据合并到DataFrame中
                df_span = pd.concat([df_span, pd.DataFrame(new_data, index=[0])], ignore_index=True)
            else:
                pass
                # 如果差值为零则不进行任何操作，也就是说后续写入Excel表中的df_span仍然是原本的内容
            
            
            # 创建要添加的数据
            #new_data = {'Data': numbers, 'Time': datetime.now(), 'Difference': difference}
            # 使用concat方法将数据合并到DataFrame中
            #df_span = pd.concat([df_span, pd.DataFrame(new_data, index=[0])], ignore_index=True)
            
            #df_span = df_span.append({'Data':numbers, 'Time':datetime.now(), 'Difference':difference}, ignore_index=True)
            
            
            
            df_span.to_excel(f"{selected_value}.xlsx", index=False)
        
        messagebox.showinfo("信息", f"点击新增：{difference}")
        

'''
def update_values(event):
    # 根据需要更新values的值
    df = pd.read_excel('./name.xlsx')
    print(df)
    options = df['Span Text'].dropna().tolist()
    
    values.set(options)
    print(values.get())
'''
    
'''
def update_options(event):
    global options
    # 在这里更新 options 列表的内容
    dropdown_menu['values'] = options
'''
# 用来让占位的第一行不会被误点
def set_button_state(event):
    selected_item = dropdown.get()
    # 检测下拉列表dropdown_menu是哪一项
    # 如果是第一项，也就是我设立的占位内容的话：
    if selected_item == dropdown['values'][0]:
        get_button['state'] = tk.DISABLED
    else:
        get_button['state'] = tk.NORMAL


# 以下是UI部分

style = Style(theme = 'darkly')
root = style.master
root.title("点击数量获取器")
root.geometry("300x500")
root.resizable(False, False)
        






# 标签和输入框
url_label = ttk.Label(root, text="输入网址:")
url_label.grid(row=0, column=0, padx=10, pady=10)
#url_label.pack(expand=True, pady=5)
url_entry = ttk.Entry(root)
url_entry.grid(row=0, column=1, padx=15, ipadx=20, pady=10)
#url_entry.pack(expand=True, pady=5)

values = tk.StringVar(root, value='')


# 保存按钮
save_button = ttk.Button(root, text="保存", command=save_data)
save_button.grid(row=1, column=1,sticky="w", padx=55, pady=10)
#save_button.pack(expand=True, pady=5)


# 创建下拉菜单
dropdown = ttk.Combobox(root, values=values.get(), style='Custom.TCombobox', state='readonly')
dropdown.grid(row=2, column=0, columnspan=2, ipadx=50, padx=(10,10), pady=10)
#dropdown.pack(expand=True, pady=5)





# 读取Excel文件，并将非空的数据加载到下拉菜单中
df = pd.read_excel('./name.xlsx')
options = df['Span Text'].dropna().tolist()
values.set(options[0])
#update_options()


# 清空下拉菜单中的选项

dropdown['values'] = []
dropdown['values'] = options


# 获取按钮
get_button = ttk.Button(root, text="Get", command=get_data, state=tk.DISABLED)
get_button.grid(row=3, column=1,sticky="w", padx=55, pady=10)
#get_button.pack(expand=True, pady=5)

# 绑定事件
dropdown.bind('<<ComboboxSelected>>', set_button_state)

#save_button.bind("<Button-1>", save_data) 
#save_button.bind("<Button-1>", update_values, add="+")

# Run event loop
root.mainloop()
