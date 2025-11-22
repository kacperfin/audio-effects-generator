import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve
from pathlib import Path

from settings import IR_DIR_PATH

def reverse(audio_data: np.ndarray) -> np.ndarray:
    return audio_data[::-1]

def delay(audio_data: np.ndarray, sample_rate: int, delay_time: float = 0.3, feedback: float = 0.3) -> np.ndarray:
    # calculate number of samples to delay by
    delay_samples = int(delay_time * sample_rate)

    # calculate sample length of final audio  
    output_length = len(audio_data) + delay_samples

    # create an output array
    output = np.zeros(output_length)

    # add original audio to output
    output[:len(audio_data)] = audio_data

    # add delayed audio scaled by feedback
    output[delay_samples:delay_samples + len(audio_data)] += audio_data * feedback
    
    return output

def echo(audio_data: np.ndarray, sample_rate: int, delay_time: float = 0.3, feedback: float = 0.5, repetitions: int = 3) -> np.ndarray:
    # calculate samples per repetition
    single_repetition_samples = int(delay_time * sample_rate)

    # calculate total samples for all repetitions
    total_repetition_samples = single_repetition_samples * repetitions

    # calculate sample length of final audio
    output_length = len(audio_data) + total_repetition_samples

    # create an output array
    output = np.zeros(output_length)

    # add original audio to output
    output[:len(audio_data)] = audio_data

    # add each repetition with exponentially decaying volume
    for n in range(1, repetitions + 1):
        output[single_repetition_samples * n:len(audio_data) + single_repetition_samples * n] += audio_data * feedback ** n

    return output

def convolution_reverb(audio_data: np.ndarray, sample_rate: int, ir_file_name: str, wet_dry_mix: float = 0.3) -> np.ndarray:
    path = IR_DIR_PATH / f'{ir_file_name}.wav'

    # load the impulse response file
    try:
        ir_data, ir_sample_rate = sf.read(path)
    except Exception:
        raise FileNotFoundError(f'Impulse response file not found. Please ensure IR files are placed in the "ir" folder.')

    # check if sample rates match
    if sample_rate != ir_sample_rate:
        raise ValueError(f"Sample rate mismatch: audio = {sample_rate}, IR = {ir_sample_rate}.")

    # convert IR to mono if stereo
    if ir_data.ndim > 1:
        ir_data = np.mean(ir_data, axis=1)

    # perform convolution
    wet_signal = fftconvolve(audio_data, ir_data, mode='full')

    # pad dry signal to match wet signal length
    dry_signal = np.zeros(len(wet_signal))
    dry_signal[:len(audio_data)] = audio_data

    # mix wet and dry signals
    output = dry_signal * (1 - wet_dry_mix) + wet_signal * wet_dry_mix

    return output