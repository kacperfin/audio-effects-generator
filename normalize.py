import numpy as np

def normalize(audio_data: np.ndarray) -> np.ndarray:
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        return audio_data / max_val
    return audio_data