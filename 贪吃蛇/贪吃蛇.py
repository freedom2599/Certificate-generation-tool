"""
项目名称： 贪吃蛇
作者： freedom
"""
import pygame
import random

# 贪吃蛇
snake_list = [[150, 50], [150, 60]]

# 食物 点 随机
food_point = [random.randint(5, 495), random.randint(5, 495)]


"""初始化游戏"""
pygame.init()
# 刷新
clock = pygame.time.Clock()
# 设置屏幕大小
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("贪吃蛇")

"""进入游戏"""
running = True
while running:
    # 绘制屏幕为白色
    screen.fill((255, 255, 255))
    # 绘制食物
    food_rect = pygame.draw.circle(screen, [255, 0, 0], food_point, 5, 0)
    # 绘制蛇 snark_rect：蛇的身子
    snark_rect = []
    for snake_point in snake_list:
        snark_rect_point = pygame.draw.circle(screen, [255, 0, 0], snake_point, 5, 0)
        snark_rect.append(snark_rect_point)


    # 将绘制的内容显示出来
    pygame.display.update()
