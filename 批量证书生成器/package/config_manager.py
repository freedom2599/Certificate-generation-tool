import configparser
import os
import sys
import chardet


def get_base_path():
    """ 获取 .exe 文件所在的目录 """
    if hasattr(sys, '_MEIPASS'):
        # 如果是打包后的 .exe 文件
        base_path = sys._MEIPASS
    else:
        # 如果是在开发环境中运行
        base_path = os.path.abspath(".")
    return base_path

def get_executable_directory():
    """ 获取 .exe 文件所在的目录 """
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 .exe 文件
        executable_dir = os.path.dirname(sys.executable)
    else:
        # 如果是在开发环境中运行
        executable_dir = os.path.dirname(os.path.abspath(__file__))
    return executable_dir

def load_config():
    # 获取 .exe 文件所在的目录
    executable_dir = get_executable_directory()
    config_path = os.path.join(executable_dir, 'config.ini')

    # 检查配置文件是否存在
    if not os.path.exists(config_path):
        # 如果配置文件不存在，则创建一个带有默认值的新配置文件
        config = configparser.ConfigParser()
        config['source'] = {
            'excel_path': '',
            'inputfont': '',
            'img_path': ''
        }
        config['image'] = {
            'fontsize': '12',
            'color': '#000000',
            'header_y': '100',
            'x_offset': '50',
            'out_path': '',
            'img_type': 'png'
        }

        with open(config_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        # 重新读取新创建的配置文件
        with open(config_path, "rb") as fd:
            buf = fd.read()
            result = chardet.detect(buf)
            config.read(config_path, encoding=result["encoding"])
    else:
        # 读取已存在的配置文件
        config = configparser.ConfigParser()
        with open(config_path, "rb") as fd:
            buf = fd.read()
            result = chardet.detect(buf)
            config.read(config_path, encoding=result["encoding"])

    # 获取初始值
    excel_path = config.get('source', 'excel_path', fallback='')
    inputfont = config.get('source', 'inputfont', fallback='')
    img_path = config.get('source', 'img_path', fallback='')
    fontsize = config.getint('image', 'fontsize', fallback=12)
    color = config.get('image', 'color', fallback='black')
    header_y = config.getint('image', 'header_y', fallback=100)
    x_offset = config.getint('image', 'x_offset', fallback=50)
    out_path = config.get('image', 'out_path', fallback='')
    img_type = config.get('image', 'img_type', fallback='png')  # 确保默认值是 png

    # 返回包含所有配置项的字典
    return {
        "excel_path": excel_path,
        "inputfont": inputfont,
        "img_path": img_path,
        "fontsize": fontsize,
        "color": color,
        "header_y": header_y,
        "x_offset": x_offset,
        "out_path": out_path,
        "img_type": img_type
    }


def save_config(config, entry_table, entry_font_style, entry_image, entry_font_size, entry_font_color,
                entry_y_position, entry_x_position, entry_output_folder, var_output_type, status_label, root):
    """保存配置文件"""
    config['excel_path'] = entry_table.get()
    config['inputfont'] = entry_font_style.get()
    config['img_path'] = entry_image.get()
    config['fontsize'] = int(entry_font_size.get())
    config['color'] = entry_font_color.get()
    config['header_y'] = int(entry_y_position.get())
    config['x_offset'] = int(entry_x_position.get())
    config['out_path'] = entry_output_folder.get()
    config['img_type'] = var_output_type.get()

    executable_dir = get_executable_directory()
    config_path = os.path.join(executable_dir, 'config.ini')

    # 将字典内容写入配置文件
    config_parser = configparser.ConfigParser()

    # 添加 [source] 部分
    config_parser.add_section('source')
    config_parser.set('source', 'excel_path', config['excel_path'])
    config_parser.set('source', 'inputfont', config['inputfont'])
    config_parser.set('source', 'img_path', config['img_path'])

    # 添加 [image] 部分
    config_parser.add_section('image')
    config_parser.set('image', 'fontsize', str(config['fontsize']))
    config_parser.set('image', 'color', config['color'])
    config_parser.set('image', 'header_y', str(config['header_y']))
    config_parser.set('image', 'x_offset', str(config['x_offset']))
    config_parser.set('image', 'out_path', config['out_path'])
    config_parser.set('image', 'img_type', config['img_type'])

    with open(config_path, 'w', encoding='utf-8') as configfile:
        config_parser.write(configfile)

    status_label.config(text="已保存", fg="red")
    root.after(2000, lambda: status_label.config(text="", fg="black"))
