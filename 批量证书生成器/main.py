import tkinter as tk
from functools import partial
from tkinter import filedialog, messagebox

from package.config_manager import load_config, save_config
from package.picture import show_preview, batch_generate_images

# 读取配置文件
config = load_config()


# print(f"Loaded configuration: {config.items('image')}")  # 调试信息

def select_file(entry, section, option, filetypes):
    """打开文件选择对话框并更新文本框"""
    filename = filedialog.askopenfilename(filetypes=filetypes)
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)
        config[option] = filename


def select_folder(entry, section, option):
    """打开文件夹选择对话框并更新文本框"""
    foldername = filedialog.askdirectory()
    if foldername:
        foldername += '/'
        entry.delete(0, tk.END)
        entry.insert(0, foldername)
        config[option] = foldername


def preview():
    """执行预览"""
    try:
        save_config(config, entry_table, entry_font_style, entry_image, entry_font_size, entry_font_color,
                    entry_y_position, entry_x_position, entry_output_folder, var_output_type, status_label, root)
        show_preview()
    except Exception as e:
        messagebox.showerror("预览错误", f"无法执行预览：{str(e)}")


def generate_image():
    """生成图片"""
    try:
        batch_generate_images()
    except Exception as e:
        messagebox.showerror("生成图片错误", f"无法生成图片：{str(e)}")


# 创建主窗口
root = tk.Tk()
root.title("批量证书生成器————FREEDOM")

# 表格文件选择
frame_table = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame_table.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E)
btn_table = tk.Button(frame_table, text="选择表格文件", command=lambda: select_file(entry_table, 'source', 'excel_path',
                                                                                    [("Excel files", "*.xlsx;*.xls"),
                                                                                     ("CSV files", "*.csv")]))
btn_table.pack(side=tk.LEFT, padx=10, pady=10)
entry_table = tk.Entry(frame_table, width=50)
entry_table.insert(0, config['excel_path'])
entry_table.pack(side=tk.RIGHT, padx=10, pady=10)

# 图片文件选择
frame_image = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame_image.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W + tk.E)
btn_image = tk.Button(frame_image, text="选择图片文件", command=lambda: select_file(entry_image, 'source', 'img_path', [
    ("Image files", "*.png;*.jpg;*.jpeg;*.gif")]))
btn_image.pack(side=tk.LEFT, padx=10, pady=10)
entry_image = tk.Entry(frame_image, width=50)
entry_image.insert(0, config['img_path'])
entry_image.pack(side=tk.RIGHT, padx=10, pady=10)

# 字符大小和字体颜色输入框
frame_font = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame_font.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W + tk.E)
label_font_size = tk.Label(frame_font, text="字符大小:")
label_font_size.pack(side=tk.LEFT, padx=10, pady=10)
entry_font_size = tk.Entry(frame_font, width=10)
entry_font_size.insert(0, str(config['fontsize']))
entry_font_size.pack(side=tk.LEFT, padx=10, pady=10)
entry_font_color = tk.Entry(frame_font, width=10)
entry_font_color.insert(0, config['color'])
entry_font_color.pack(side=tk.RIGHT, padx=10, pady=10)
label_font_color = tk.Label(frame_font, text="字体颜色:")
label_font_color.pack(side=tk.RIGHT, padx=10, pady=10)

# 字体样式选择
frame_font_style = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame_font_style.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W + tk.E)
btn_font_style = tk.Button(frame_font_style, text="选择字体样式",
                           command=lambda: select_file(entry_font_style, 'source', 'inputfont',
                                                       [("TrueType Font files", "*.ttf")]))
btn_font_style.pack(side=tk.LEFT, padx=10, pady=10)
entry_font_style = tk.Entry(frame_font_style, width=50)
entry_font_style.insert(0, config['inputfont'])
entry_font_style.pack(side=tk.RIGHT, padx=10, pady=10)

# X轴和Y轴位置输入框
frame_axis_position = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame_axis_position.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W + tk.E)
label_x_position = tk.Label(frame_axis_position, text="X轴位置:")
label_x_position.pack(side=tk.LEFT, padx=10, pady=10)
entry_x_position = tk.Entry(frame_axis_position, width=10)
entry_x_position.insert(0, str(config['x_offset']))
entry_x_position.pack(side=tk.LEFT, padx=10, pady=10)
entry_y_position = tk.Entry(frame_axis_position, width=10)
entry_y_position.insert(0, str(config['header_y']))
entry_y_position.pack(side=tk.RIGHT, padx=10, pady=10)
label_y_position = tk.Label(frame_axis_position, text="Y轴位置:")
label_y_position.pack(side=tk.RIGHT, padx=10, pady=10)

# 输出文件夹选择
frame_output_folder = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame_output_folder.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W + tk.E)
btn_output_folder = tk.Button(frame_output_folder, text="选择输出文件夹",
                              command=lambda: select_folder(entry_output_folder, 'image', 'out_path'))
btn_output_folder.pack(side=tk.LEFT, padx=10, pady=10)
entry_output_folder = tk.Entry(frame_output_folder, width=50)
entry_output_folder.insert(0, config['out_path'])
entry_output_folder.pack(side=tk.RIGHT, padx=10, pady=10)

# 输出类型选择
frame_output_type = tk.Frame(root)
frame_output_type.grid(row=7, column=0, padx=10, pady=10, sticky=tk.W + tk.E)

var_output_type = tk.StringVar(value=config['img_type'])  # 默认选中PNG
label_output_type = tk.Label(frame_output_type, text="输出类型:")
label_output_type.pack(side=tk.LEFT, padx=10, pady=10)
radio_jpg = tk.Radiobutton(frame_output_type, text="JPEG", variable=var_output_type, value='jpeg')
radio_jpg.pack(side=tk.LEFT, padx=10, pady=10)
radio_png = tk.Radiobutton(frame_output_type, text="PNG", variable=var_output_type, value='png')
radio_png.pack(side=tk.LEFT, padx=10, pady=10)
radio_pdf = tk.Radiobutton(frame_output_type, text="PDF", variable=var_output_type, value='pdf')
radio_pdf.pack(side=tk.LEFT, padx=10, pady=10)

# 按钮框架
frame_buttons = tk.Frame(root)
frame_buttons.grid(row=8, column=0, padx=10, pady=10, sticky=tk.W + tk.E)

# 设置列权重，使得按钮可以均匀分布
for i in range(3):
    frame_buttons.columnconfigure(i, weight=1)

# 保存状态标签
status_label = tk.Label(frame_buttons, text="", fg="red")
status_label.grid(row=0, column=0, padx=5, pady=(10, 0), sticky=tk.W + tk.E)  # 调整了pady的上边距

# 保存按钮
save_button = tk.Button(frame_buttons, text="保存",
                        command=partial(save_config, config, entry_table, entry_font_style, entry_image,
                                        entry_font_size, entry_font_color, entry_y_position, entry_x_position,
                                        entry_output_folder, var_output_type, status_label, root))
save_button.grid(row=1, column=0, padx=5, sticky=tk.EW)

# 预览按钮
preview_button = tk.Button(frame_buttons, text="预览", command=preview, )
preview_button.grid(row=1, column=1, padx=5, sticky=tk.EW)

# 生成图片按钮
generate_image_button = tk.Button(frame_buttons, text="生成图片", command=generate_image)
generate_image_button.grid(row=1, column=2, padx=5, sticky=tk.EW)

# 运行主循环
root.mainloop()
