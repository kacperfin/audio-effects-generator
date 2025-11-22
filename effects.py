import numpy as np

def reverse(audio_data: np.ndarray) -> np.ndarray:
    return audio_data[::-1]

def delay(audio_data: np.ndarray, sample_rate: int, delay_time: float = 0.3, feedback: float = 0.3) -> np.ndarray:
    # calculate number of samples to delay by
    delay_samples = int(delay_time * sample_rate)

    # calculate sample length of final audio  
    output_length = len(audio_data) + delay_samples

    # create an output array
    output = np.zeros(output_length)

    # populate the empty output array with current data
    output[:len(audio_data)] = audio_data

    # add delayed audio multiplied by feedback (from 0 to 1)
    output[delay_samples:delay_samples + len(audio_data)] += audio_data * feedback
    
    return output

def echo(audio_data: np.ndarray, sample_rate: int, delay_time: float = 0.3, feedback: float = 0.5, n_of_delays: int = 3) -> np.ndarray:
    single_delay_samples = int(delay_time * sample_rate)

    delay_samples = single_delay_samples * n_of_delays

    output_length = len(audio_data) + delay_samples

    output = np.zeros(output_length)

    output[:len(audio_data)] = audio_data

    for n_of_delay in range(1, n_of_delays + 1):
        output[single_delay_samples * n_of_delay:len(audio_data) + single_delay_samples * n_of_delay] += audio_data * feedback ** n_of_delay

    return output