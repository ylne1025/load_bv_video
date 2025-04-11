import os
import sys
import you_get
from moviepy import VideoFileClip, AudioFileClip


def load_video(url_, float_syn_path_, name):
    """下载视频"""
    sys.argv = ['you-get', '-o', float_syn_path_, '-O', name, url_, "--debug"]
    you_get.main()


def _merge_audio_video(video_path1, audio_path1, output_path1):
    """合并视频"""
    video = VideoFileClip(video_path1)
    audio = AudioFileClip(audio_path1)
    video_ = video.with_audio(audio)
    video_.write_videofile(output_path1)


def load_main(bv: str):
    """通过b站的BV号下载BV号对应的视频"""
    # 下载视频
    _url = f"https://www.bilibili.com/video/{bv}"
    _name = bv
    float_syn_path = "./AAAA_no_syn"
    os.makedirs(float_syn_path, exist_ok=True)
    load_video(_url, float_syn_path, _name)
    # 合并视频
    true_syn_path = "./AAAA_yes_syn"
    os.makedirs(true_syn_path, exist_ok=True)
    _video_path = float_syn_path + "/{name}[00].mp4".format(name=_name)
    _audio_path = float_syn_path + "/{name}[01].mp4".format(name=_name)
    _output_path = true_syn_path + "/{name}.mp4".format(name=_name)
    _merge_audio_video(_video_path, _audio_path, _output_path)


if __name__ == '__main__':
    load_main("BV1Cy9XYwER2")
