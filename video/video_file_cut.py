"""


# 输入文件夹和输出文件夹路径
input_folder = r"F:\001工作\test\input_test"
output_folder = r"F:\001工作\test\output_test\a"


我的需求是
1.写一个可以把本地视频，当检测到视频中的画面发生大范围变化时，剪切一次视频，将剪切成多个子视频并保存的代码。场景变化指的是镜头切换，就像电影中切换镜头一样，而不是每一帧变化后都算做场景切换。可以参考davinci resolve中的探测场景切点功能。
2.重点实现将视频按照场景变化（画面中的场景变化一次视为一次变化）将视频分段切割的功能
3.遍历读取输入文件路径中的所有视频文件
4.依次裁剪每个视频文件，将它们按照场景变化来分割视频，将每个视频切片成多个素材，并将所有都分别保存到本地
5.在对每个视频文件进行操作时，有提示符来提示系统进程
6.尽可能的考虑到系统过程中可能出现的错误，并进行提示。

"""

import os
import cv2.cv2 as cv2
from moviepy.video.io.VideoFileClip import VideoFileClip

import numpy as np


# 定义用于检测场景变化的函数
def detect_scene_changes(video_path, threshold=40000000):
    # 加载视频文件
    try:
        video = cv2.VideoCapture(video_path)
    except:
        raise Exception(f"Failed to load video {video_path}")

    # 获取第一帧的图像
    success, image = video.read()
    if not success:
        raise Exception(f"Failed to read video {video_path}")

    # 初始化参数
    prev_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    scene_changes = []
    frame_count = 0

    # 遍历视频的每一帧
    while success:
        try:
            # 转换为灰度图像
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 计算当前帧和上一帧的差异
            difference = cv2.absdiff(image, prev_image)
            diff_sum = difference.sum()

            # 如果差异超过阈值，则认为是场景变化
            if diff_sum > threshold:
                scene_changes.append(frame_count)

            # 更新参数
            prev_image = image
            success, image = video.read()
            frame_count += 1
        except Exception as e:
            print(e)
            success = False

    # 释放资源
    video.release()

    # 返回场景变化的帧数
    return scene_changes

# 定义用于裁剪视频的函数
def cut_video(video_path, scene_changes):
    # 加载视频文件
    try:
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    except:
        raise Exception(f"Failed to load video {video_path}")

    # 定义输出视频的编解码格式
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # 按照场景变化来裁剪视频
    clips = []
    start_frame = 0
    for end_frame in scene_changes:
        # 创建输出视频文件的名称
        filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_{start_frame}_{end_frame}.mp4"
        output_path = os.path.join(output_dir, filename)

        # 创建输出视频对象
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # 裁剪视频
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)  # 设置视频的起始帧
        while video.get(cv2.CAP_PROP_POS_FRAMES) < end_frame:
            success, image = video.read()
            if not success:
                break
            writer.write(image)

        writer.release()
        clips.append(VideoFileClip(output_path))
        start_frame = end_frame

    # 释放资源
    video.release()

    # 返回裁剪后的视频片段
    return clips


# 遍历读取输入文件路径中的所有视频文件
input_dir = r"F:\001工作\03素材\土工膜素材\视频素材"
output_dir = r"F:\001工作\test\output_test\40000000"

# 遍历读取输入文件路径中的所有视频文件
for root, dirs, files in os.walk(input_dir):
    for filename in files:
        # 检查文件类型是否为视频
        if not filename.lower().endswith(('.mp4', '.avi', '.mov', '.wmv')):
            continue

        # 裁剪视频并保存到本地
        input_path = os.path.join(root, filename)
        scene_changes = detect_scene_changes(input_path)
        clips = cut_video(input_path, scene_changes)
        for i, clip in enumerate(clips):
            output_path = os.path.join(output_dir, f"{filename}_{i}.mp4")
            clip.write_videofile(output_path)
            print(f"已保存文件 {output_path}")

print("完成")



