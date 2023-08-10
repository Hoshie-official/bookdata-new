import tkinter as tk
import pandas as pd
from tkinter import messagebox
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import datetime
from tkinter import Tk, messagebox
from tkinter.ttk import Combobox

def save_data():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "请输入一个网址")
        return

    
    # 发送 HTTP 请求获取网页内容
    response = urlopen(url)

    # 获取网页的 HTML 内容
    html_content = response.read().decode('utf-8')
        


    # 创建 BeautifulSoup 对象
    soup = BeautifulSoup(html_content, 'html.parser')

    # 获取第五个span元素，这个元素的内容是小说的名字
    span_element4 = soup.select('span.text')[4]
    span_text4 = span_element4.text
        
    # 检查'name.xlsx'里面有没有相应的网址

        
    df = pd.read_excel('./Excel/name.xlsx')

        

    if url in df['URL'].values:
        messagebox.showinfo("警告", "网址已存在")
            
    else:
            
        # 把网址和获取的书名保存到Excel表格里
        df_new = pd.DataFrame({'URL':[url], 'Span Text':[span_text4]})
     
      
            
        df = pd.concat([df, df_new], ignore_index=True)
        #df = df.append(df_new, ignore_index=True)
            
       
        df.to_excel('./Excel/name.xlsx', index=False)

        
        # 新建一个以 span_text4为名字的Excel
        if not pd.isnull(span_text4):
            df_span = pd.DataFrame({'Data':[], 'Time': [], 'Difference': []})
            df_span.to_excel(f"./Excel/{span_text4}.xlsx", index=False)
                
            
        
        # 更新下拉菜单
        span_text_list = df['Span Text'].dropna().tolist()
        dropdown_menu.set(span_text_list[0])
        
        # 清空下拉菜单中的选项，然后再重新写入，用这种方法来实现实时更新
        menu = dropdown["menu"]
        menu.delete(0, 'end')

        # 添加新选项
        for span_text in span_text_list:
            menu.add_command(label=span_text, command=lambda text=span_text: dropdown_menu.set(text))
            
        messagebox.showinfo("提示", "数据保存成功")
            
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

def get_data():
    
        
        selected_value = dropdown_menu.get()
        
        if not selected_value:
            messagebox.showerror("Error", "请选取一个值。")
            return
        
        df = pd.read_excel('./Excel/name.xlsx')
        
        
        # 检索选定的span_text4对应的URL
        url = df.loc[df['Span Text'] == selected_value, 'URL'].values[0]
        
        
        # 发送HTTP请求以检索网页内容
        response = urlopen(url)
        
        
        # 获取网页的 HTML 内容
        html_content = response.read().decode('utf-8')
        
        # 创建 BeautifulSoup 对象
        soup = BeautifulSoup(html_content, 'html.parser')
        
        
        # 获取第七个span元素，提取其文本内容，并使用正则表达式查找数字。
        span_element = soup.select('span.text')[7]
        span_text = span_element.text

        number = convert_to_int(span_text)
        
        
        df_span = pd.read_excel(f"./Excel/{selected_value}.xlsx")

        
        
        if df_span.empty:
            # 如果Excel文件为空，则保存当前数据并更新列。
            difference = 0
            df_span = pd.DataFrame({'Data':number, 'Time':[datetime.now()], 'Difference':[0]})
            df_span.to_excel(f"./Excel/{selected_value}.xlsx", index=False)
        else:
            # 比较当前数据与之前的数据

            previous_data = df_span['Data'].values[-1]
            
            if int(number) == int(previous_data):
                difference = 0
            else:
                difference = int(number) - int(previous_data)

            
            if difference != 0:
                # 创建要添加的数据
                new_data = {'Data': number, 'Time': datetime.now(), 'Difference': difference}
                # 使用concat方法将数据合并到DataFrame中
                df_span = pd.concat([df_span, pd.DataFrame(new_data, index=[0])], ignore_index=True)
            else:
                pass
                # 如果差值为零则不进行任何操作，也就是说后续写入Excel表中的df_span仍然是原本的内容

            
            df_span.to_excel(f"./Excel/{selected_value}.xlsx", index=False)
        
        messagebox.showinfo("信息", f"点击新增：{difference}")
        
    
        

# 主窗口创建
root = tk.Tk()
root.title("点击数量获取器")
root.geometry("400x200")

# 标签和输入框
url_label = tk.Label(root, text="输入网址:")
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()

# 保存按钮
save_button = tk.Button(root, text="保存", command=save_data)
save_button.pack()


# 创建下拉菜单
dropdown_menu = tk.StringVar(root)
dropdown = tk.OptionMenu(root, dropdown_menu, "")
dropdown.pack()


# 读取Excel文件，并将非空的数据加载到下拉菜单中
df = pd.read_excel('./Excel/name.xlsx')
span_text_list = df['Span Text'].dropna().tolist()
dropdown_menu.set(span_text_list[0])

# 清空下拉菜单中的选项
menu = dropdown["menu"]
menu.delete(0, 'end')

# 添加新选项
for span_text in span_text_list:
    menu.add_command(label=span_text, command=lambda text=span_text: dropdown_menu.set(text))



# 获取按钮
get_button = tk.Button(root, text="获取", command=get_data)
get_button.pack()

# Run event loop
root.mainloop()
