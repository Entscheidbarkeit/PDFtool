import tkinter as tk
from tkinter import filedialog, messagebox
import merger

# 全局变量
file_list = []
index = 0
output_path = ""
current_language = "English"

# 定义不同语言的界面文本
texts = {
    "English": {
        "select_pdf": "Please select your PDFs:",
        "select_file": "Select file",
        "select_output_path": "Please select your output path:",
        "select_path": "Select path",
        "selected_path": "Selected path: ",
        "delete_selected": "Delete selected file",
        "merge": "Merge!",
        "warning_title": "Warning",
        "warning_pdf_count": "The selected PDFs must be more than 1!",
        "warning_output_path": "You have to set an output path first!",
        "success_title": "Success!",
        "success_message": "The PDFs are merged at your output position.",
        "language": "语言"
    },
    "中文": {
        "select_pdf": "请选择要合并的PDF文件：",
        "select_file": "选择文件",
        "select_output_path": "请选择输出路径：",
        "select_path": "选择路径",
        "selected_path": "已选择路径: ",
        "delete_selected": "删除选中文件",
        "merge": "合并！",
        "warning_title": "警告",
        "warning_pdf_count": "选择的PDF文件必须多于1个！",
        "warning_output_path": "请先设置输出路径！",
        "success_title": "成功！",
        "success_message": "PDF文件已在输出位置合并完成",
        "language": "Language"
    }
}

# 切换语言的函数
def switch_language(*args):
    global current_language
    current_language = language_var.get()
    update_ui_language()

def update_ui_language():
    """更新界面文本以匹配当前语言。"""
    lang_texts = texts[current_language]
    select_file_label.config(text=lang_texts["select_pdf"])
    select_file_button.config(text=lang_texts["select_file"])
    select_path_label.config(text=lang_texts["select_output_path"])
    select_path_button.config(text=lang_texts["select_path"])
    delete_button.config(text=lang_texts["delete_selected"])
    merge_button.config(text=lang_texts["merge"])
    language_label.config(text=lang_texts["language"])
    if output_path:
        select_path_label.config(text=f"{lang_texts['selected_path']}{output_path}")

# 选择文件函数
def select_file():
    global index
    file_path = filedialog.askopenfilename(title=texts[current_language]["select_file"])
    if file_path:
        file_list.append(file_path)
        index += 1
        add_item()

# 选择路径函数
def select_path():
    global output_path
    file_path = filedialog.askdirectory(title=texts[current_language]["select_path"])
    if file_path:
        output_path = file_path
        select_path_label.config(text=f"{texts[current_language]['selected_path']}{output_path}")

# 添加文件到列表
def add_item():
    item = file_list[index - 1]
    listbox.insert(tk.END, item)

# 删除选中的文件
def delete_item():
    global index
    selected_items = listbox.curselection()
    for idx in selected_items[::-1]:    
        listbox.delete(idx)
        file_list.pop(idx)
    index = len(file_list)

# 合并 PDF 文件
def merge():
    if len(file_list) < 2:
        messagebox.showwarning(title=texts[current_language]["warning_title"],
                               message=texts[current_language]["warning_pdf_count"])
        return
    if not output_path:
        messagebox.showwarning(title=texts[current_language]["warning_title"],
                               message=texts[current_language]["warning_output_path"])
        return
    merger.merge_pdfs(file_list, output_path + "/merged.pdf")
    messagebox.showinfo(title=texts[current_language]["success_title"],
                        message=texts[current_language]["success_message"])

# 创建主窗口
root = tk.Tk()
root.title("PDF Merger")
root.geometry("500x600")

# 语言选择下拉菜单
language_label = tk.Label(root, text=texts["English"]["language"], font=("Arial", 12))
language_label.pack(pady=5)
language_var = tk.StringVar(value="English")
language_menu = tk.OptionMenu(root, language_var, "English", "中文")
language_menu.config(font=("Arial", 12))
language_menu.pack(pady=5)

# 绑定语言切换事件
language_var.trace_add("write", switch_language)

# 文件选择标签和按钮
select_file_label = tk.Label(root, text=texts["English"]["select_pdf"], font=("Arial", 12))
select_file_label.pack(pady=10)
select_file_button = tk.Button(root, text=texts["English"]["select_file"], command=select_file, font=("Arial", 12))
select_file_button.pack(pady=10)

# 输出路径选择标签和按钮
select_path_label = tk.Label(root, text=texts["English"]["select_output_path"], font=("Arial", 12))
select_path_label.pack(pady=10)
select_path_button = tk.Button(root, text=texts["English"]["select_path"], command=select_path, font=("Arial", 12))
select_path_button.pack(pady=10)

# 显示文件列表的 Listbox
listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
listbox.pack(pady=10)

# 删除选中文件按钮
delete_button = tk.Button(root, text=texts["English"]["delete_selected"], command=delete_item, font=("Arial", 12))
delete_button.pack(pady=5)

# 合并按钮
merge_button = tk.Button(root, text=texts["English"]["merge"], command=merge, font=("Arial", 12))
merge_button.pack(pady=5)

# 运行主循环
root.mainloop()
