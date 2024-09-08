import numpy as np
from ffmpeg import FFmpeg

def convert_to_mono_audio_from_stdin_to_stdout(raw_data: bytes, sample_rate: int) -> np.ndarray:
    out = convert_to_mono_audio_from_stdin_to_buffer(raw_data, sample_rate)
    out = np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
    return out

def convert_to_mono_audio_from_stdin_to_buffer(raw_data: bytes, sample_rate: int) -> bytes:
    ffmpeg = (
            FFmpeg()
            .option("y")
            .input("pipe:0")
            .output(
                "pipe:1",
                {"codec:a": "pcm_s16le"},
                f="s16le",
                ac=1,
                ar=sample_rate,
           )
        )
    out = ffmpeg.execute(raw_data)
    return out
