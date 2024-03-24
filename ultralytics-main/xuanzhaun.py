# 定义旋转函数
import math
# def rotate_coordinate(x, y, angle):
# # 将角度转换为弧度
#     radian = math.radians(angle)
#
# # 计算旋转后的坐标
#     new_x = x * math.cos(radian) - y * math.sin(radian)
#     new_y = x * math.sin(radian) + y * math.cos(radian)
#
#     return new_x, new_y
#
# # 输入原坐标和旋转角度
# x = float(input("请输入原坐标的x值："))
# y = float(input("请输入原坐标的y值："))
# angle = float(input("请输入旋转角度："))
#
# # 调用旋转函数计算新坐标
# new_x, new_y = rotate_coordinate(x, y, angle)
#
# # 输出结果
# print("旋转后的坐标为：({:.2f}, {:.2f})".format(new_x, new_y))

import cv2
def rotate_image(image, angle):
    # 获取图像的宽度和高度
    height, width = image.shape[:2]

    # 计算图像中心点坐标
    center = (width // 2, height // 2)

    # 定义旋转矩阵
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # 计算旋转后的图像
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

    return rotated_image


# 读取图像
rotated_image = cv2.imread('fff.jpg')

# 旋转图像
angle = 45
# rotated_image = rotate_image(image, math.atan2(2620, 80))
row,col=rotated_image.shape[:2]
cv2.line(rotated_image, (int(col/2), 0), (int(col/2), int(row)), (0, 0, 255), 1)
cv2.line(rotated_image, (0, int(row/2)), (int(col), int(row/2)), (0, 0, 255), 1)
# 显示旋转后的图像
cv2.imshow('Rotated Image', rotated_image)
cv2.imwrite('ppp.jpg',rotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()