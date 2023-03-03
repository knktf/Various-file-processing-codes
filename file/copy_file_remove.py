import os
import shutil
import string
import random

# 定义源文件夹和目标文件夹
src_folder = r"F:\001工作\03素材\土工膜素材\视频素材"
dst_folder = r"F:\004视频处理结果\02视频素材"

# 遍历源文件夹中的所有文件
for root, dirs, files in os.walk(src_folder):
    for file in files:
        # 判断文件是否为视频文件
        if file.endswith(('.mp4', '.mov', '.avi', '.wmv', '.mkv')):
            # 判断文件名是否包含易乱码的字符
            if not all(c in string.printable for c in file):
                # 构建源文件路径和目标文件路径
                src_file = os.path.join(root, file)
                # 生成新的文件名，使用数字和字母组合
                new_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8)) + '.mp4'
                dst_file = os.path.join(dst_folder, new_name)
                # 复制文件到目标文件夹并重命名
                shutil.copy2(src_file, dst_file)
            else:
                # 构建源文件路径和目标文件路径
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_folder, file)
                # 复制文件到目标文件夹
                shutil.copy2(src_file, dst_file)
