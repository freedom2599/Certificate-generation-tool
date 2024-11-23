
import logging
import os

import time
import tkinter as tk
from tkinter import messagebox

import openpyxl  # 使用 openpyxl 替换 xlrd
from PIL import Image, ImageDraw, ImageFont

from package.config_manager import load_config

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def reconfig():
    # 全局配置
    config = load_config()
    # 确保配置文件中的值类型正确
    config['fontsize'] = int(config['fontsize'])
    config['header_y'] = int(config['header_y'])
    config['x_offset'] = int(config['x_offset'])
    return config


def show_message(title, *messages):
    """显示一个消息对话框，支持多行消息"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    full_message = "\n".join(messages)
    messagebox.showinfo(title, full_message)
    root.destroy()


def read_excel_data():
    config = reconfig()
    """读取 Excel 文件中的数据"""
    try:
        workbook = openpyxl.load_workbook(config['excel_path'])
        sheet = workbook.active
        names = [cell.value for cell in sheet['A'][1:] if cell.value is not None]
        return names
    except Exception as e:
        logging.error(f"读取 Excel 文件时出错: {e}")
        show_message("错误", f"读取 Excel 文件时出错: {e}")
        raise



def generate_single_image(name):
    config = reconfig()
    """基于模板图片和文字生成一张图片，但不保存"""
    try:
        font = ImageFont.truetype(config['inputfont'], config['fontsize'])
        img = Image.open(config['img_path'])
        draw = ImageDraw.Draw(img)

        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_coordinate = (img.size[0] - text_width) // 2 - config['x_offset'], config['header_y']

        draw.text(text_coordinate, name, config['color'], font=font)

        return img
    except Exception as e:
        logging.error(f"生成单张图片时出错: {e}")
        show_message("错误", f"生成单张图片时出错: {e}")
        raise


def show_preview():
    """显示第一个名字的预览图像，不保存图片"""
    names = read_excel_data()
    if names:
        preview_img = generate_single_image(names[0])
        preview_img.show()
    else:
        show_message("提示", "没有可预览的数据")


def batch_generate_images():
    config = reconfig()
    """批量生成图片并保存到指定路径"""
    names = read_excel_data()

    checks_names = messagebox.askyesno("确认",
                                       f"确认是要生成 {', '.join(map(str, names[:5]))} 一共 {len(names)} 个人哦\n"
                                       f"底图为 {config['img_path']} ？\n"
                                       f"生成位置为 {config['out_path']} ？")

    if checks_names:


        # 开始批量生成图片
        names = read_excel_data()
        num_count = 0
        for name in names:
            img = generate_single_image(name)
            filename = "{}.{}".format(name, config['img_type'])
            img.save(os.path.join(config['out_path'], filename), config['img_type'], quality=95)
            logging.info(
                f'保存成功 在 {os.path.join(os.getcwd().replace("\\", "/"), config["out_path"][1:], filename)}')
            num_count += 1
            logging.info(f'已经生成 {num_count} 共计 {len(names)} 还有 {len(names) - num_count} 个')

        messages = [
            f'在 {config["out_path"]} 下生成 {len(names)} 张图\n',
            '可以关掉我了，bye！'
        ]
        show_message("完成", *messages)
        time.sleep(1)
    else:
        show_message("取消", "操作已取消")


if __name__ == "__main__":
    batch_generate_images()
