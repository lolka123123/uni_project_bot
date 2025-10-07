from pydub import AudioSegment, utils
import os
from dotenv import load_dotenv

load_dotenv()


if os.getenv('WITHOUT_DOCKER=False'):
    ffmpeg_path = r"/app/ffmpeg/ffmpeg.exe"
    ffprobe_path = r"/app/ffmpeg/ffprobe.exe"
    AudioSegment.converter = ffmpeg_path
    AudioSegment.ffprobe = ffprobe_path
    utils.get_prober_name = lambda: ffprobe_path
    utils.get_encoder_name = lambda: ffmpeg_path



def cut_audio(audio_url, cut_from, cut_to, output_path):

    audio = AudioSegment.from_file(audio_url)
    cut = audio[cut_from*1000:cut_to*1000]
    cut.export(output_path, format="mp3")

def cut_audio_center(audio_url, cut_from, cut_to, output_path):
    audio = AudioSegment.from_file(audio_url)

    if cut_to > len(audio):
        cut_to = len(audio)

    before = audio[:cut_from]
    after = audio[cut_to:]
    result = before + after

    result.export(output_path, format="mp3")



