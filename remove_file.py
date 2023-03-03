import os
import shutil
import cv2.cv2 as cv2

# 定义源文件夹和目标文件夹

#一次切片结果素材文件夹
src_folder = r"F:\004视频处理结果\03视频素材切片结果"
#切片成功视频（视频时长1-60秒的视频）
short_video_folder = r"F:\004视频处理结果\05一次二次视频切片合格素材"
#需要二次切片的文件
long_video_folder = r"F:\004视频处理结果\04一次切片不合格素材"
# 获取src_folder的深度
depth = src_folder.count(os.sep)

#素材时长限度
time=60


# 遍历源文件夹中的所有文件
for root, dirs, files in os.walk(src_folder):
    for file in files:
        # 判断文件是否为视频文件
        if file.endswith(('.mp4', '.mov', '.avi', '.wmv', '.mkv')):
            # 构建源文件路径
            src_file = os.path.join(root, file)
            # 使用OpenCV获取视频时长
            cap = cv2.VideoCapture(src_file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if fps == 0:
                cap.release()
                continue
            duration = frame_count / fps
            cap.release()
            # 判断视频时长并移动到不同的文件夹
            if duration < 1:
                os.remove(src_file)
                continue
            elif duration > 1 and duration < time:
                dst_folder = short_video_folder
            elif duration >= time:
                dst_folder = long_video_folder
            else:
                continue
            # 构建目标文件路径
            dst_file = os.path.join(dst_folder, file)
            # 移动文件到目标文件夹
            shutil.move(src_file, dst_file)
# 遍历完成后删除空文件夹
for root, dirs, files in os.walk(src_folder, topdown=False):
    for dir in dirs:
        folder = os.path.join(root, dir)
        if os.path.isdir(folder) and not os.listdir(folder):
            os.rmdir(folder)
            print(f"Deleted empty folder: {folder}")
