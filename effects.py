import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, butter, sosfilt

from settings import IR_DIR_PATH

def filter(audio_data: np.ndarray, sample_rate: int, lowpass_freq: float = 20000.0, highpass_freq: float = 20.0) -> np.ndarray:
    # ensure frequencies are within valid range
    nyquist = sample_rate / 2
    lowpass_freq = min(lowpass_freq, nyquist - 1)
    highpass_freq = max(highpass_freq, 1)

    # if highpass is higher than lowpass, return silence (invalid configuration)
    if highpass_freq >= lowpass_freq:
        return np.zeros_like(audio_data)

    output = audio_data.copy()

    # apply highpass filter if frequency is above minimum
    if highpass_freq > 20:
        sos_high = butter(4, highpass_freq, btype='highpass', fs=sample_rate, output='sos')
        output = sosfilt(sos_high, output)

    # apply lowpass filter if frequency is below maximum
    if lowpass_freq < nyquist - 1:
        sos_low = butter(4, lowpass_freq, btype='lowpass', fs=sample_rate, output='sos')
        output = sosfilt(sos_low, output)

    return output

def overdrive(audio_data: np.ndarray, sample_rate: int, drive: float = 5.0, tone: float = 0.5) -> np.ndarray:
    # apply pre-gain to boost signal before clipping
    gained_signal = audio_data * drive

    # apply soft clipping using tanh function for smooth overdrive
    clipped_signal = np.tanh(gained_signal)

    # apply tone control (simple low-pass filter)
    # higher tone = brighter sound, lower tone = darker sound
    if tone < 1.0:
        # calculate cutoff frequency based on tone (500 Hz to 5000 Hz)
        cutoff_freq = 500 + (5000 - 500) * tone
        nyquist = sample_rate / 2
        cutoff_freq = min(cutoff_freq, nyquist - 1)

        # apply low-pass filter for tone control
        sos = butter(2, cutoff_freq, btype='lowpass', fs=sample_rate, output='sos')
        clipped_signal = sosfilt(sos, clipped_signal)

    return clipped_signal

def phaser(audio_data: np.ndarray, sample_rate: int, rate: float = 0.5, depth: float = 1.0, num_stages: int = 4, feedback: float = 0.5, wet_dry_mix: float = 0.5) -> np.ndarray:
    num_samples = len(audio_data)

    # create LFO for sweeping the all-pass filter frequencies
    lfo = np.sin(2 * np.pi * rate * np.arange(num_samples) / sample_rate)

    # map LFO to frequency range (200 Hz to 2000 Hz)
    min_freq = 200
    max_freq = 2000
    sweep_freq = min_freq + (max_freq - min_freq) * (lfo * depth + 1) / 2

    # initialize output
    output = audio_data.copy()

    # apply cascaded all-pass filters
    for stage in range(num_stages):
        stage_output = np.zeros_like(audio_data)

        for i in range(num_samples):
            # calculate all-pass filter coefficient based on frequency
            freq = sweep_freq[i]
            # all-pass filter coefficient
            tan_val = np.tan(np.pi * freq / sample_rate)
            a = (tan_val - 1) / (tan_val + 1)

            # apply all-pass filter with state variable
            if i == 0:
                x_prev = 0
                y_prev = 0
            else:
                x_prev = output[i-1]
                y_prev = stage_output[i-1]

            # all-pass filter difference equation
            stage_output[i] = a * output[i] + x_prev - a * y_prev

        output = stage_output.copy()

    # mix with feedback
    phased_signal = output + audio_data * feedback

    # mix wet and dry signals
    result = audio_data * (1 - wet_dry_mix) + phased_signal * wet_dry_mix

    return result

def flanger(audio_data: np.ndarray, sample_rate: int, rate: float = 0.5, depth: float = 0.002, feedback: float = 0.5, wet_dry_mix: float = 0.5) -> np.ndarray:
    # create output array
    output = np.zeros_like(audio_data)

    # maximum delay in samples
    max_delay_samples = int(depth * sample_rate)

    # create LFO (Low Frequency Oscillator) for varying delay
    num_samples = len(audio_data)
    lfo = np.sin(2 * np.pi * rate * np.arange(num_samples) / sample_rate)

    # map LFO from [-1, 1] to [0, max_delay_samples]
    delay_samples = (lfo + 1) * 0.5 * max_delay_samples

    # initialize feedback buffer
    feedback_buffer = np.zeros(num_samples + max_delay_samples)
    feedback_buffer[:num_samples] = audio_data

    # apply time-varying delay with feedback
    for i in range(num_samples):
        # get the delay for this sample
        delay = delay_samples[i]

        # calculate fractional delay position
        delay_pos = i - delay

        if delay_pos >= 0:
            # linear interpolation for fractional delay
            index = int(delay_pos)
            frac = delay_pos - index

            if index + 1 < len(feedback_buffer):
                delayed_sample = feedback_buffer[index] * (1 - frac) + feedback_buffer[index + 1] * frac
            else:
                delayed_sample = feedback_buffer[index]

            # mix with feedback
            output[i] = delayed_sample
            feedback_buffer[i] += delayed_sample * feedback
        else:
            output[i] = 0

    # mix wet and dry signals
    result = audio_data * (1 - wet_dry_mix) + output * wet_dry_mix

    return result

def chorus(audio_data: np.ndarray, sample_rate: int, num_voices: int = 3, rate: float = 1.5, depth: float = 0.02, wet_dry_mix: float = 0.5) -> np.ndarray:
    # create output array for wet signal
    wet_signal = np.zeros_like(audio_data)

    num_samples = len(audio_data)

    # maximum delay in samples
    max_delay_samples = int(depth * sample_rate)

    # create multiple voices with different LFO phases and rates
    for voice in range(num_voices):
        # slight variation in rate and phase for each voice
        voice_rate = rate * (1 + voice * 0.1)
        phase_offset = voice * (2 * np.pi / num_voices)

        # create LFO with phase offset
        lfo = np.sin(2 * np.pi * voice_rate * np.arange(num_samples) / sample_rate + phase_offset)

        # map LFO from [-1, 1] to [0, max_delay_samples]
        delay_samples = (lfo + 1) * 0.5 * max_delay_samples

        # apply time-varying delay for this voice
        voice_output = np.zeros_like(audio_data)

        for i in range(num_samples):
            # get the delay for this sample
            delay = delay_samples[i]

            # calculate fractional delay position
            delay_pos = i - delay

            if delay_pos >= 0:
                # linear interpolation for fractional delay
                index = int(delay_pos)
                frac = delay_pos - index

                if index + 1 < num_samples:
                    voice_output[i] = audio_data[index] * (1 - frac) + audio_data[index + 1] * frac
                else:
                    voice_output[i] = audio_data[index]
            else:
                voice_output[i] = 0

        # add this voice to the wet signal
        wet_signal += voice_output

    # normalize by number of voices to avoid clipping
    wet_signal = wet_signal / num_voices

    # mix wet and dry signals
    result = audio_data * (1 - wet_dry_mix) + wet_signal * wet_dry_mix

    return result

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

def reverse(audio_data: np.ndarray) -> np.ndarray:
    return audio_data[::-1]