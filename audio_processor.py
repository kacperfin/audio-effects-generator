from scipy.io import wavfile
import numpy as np

class AudioProcessor():
    _EFFECT_NAMES = ['no_effect', 'no_sound', 'reverse']

    def get_effect_names(self) -> list[str]:
        return self._EFFECT_NAMES

    def apply_effect(self, audio, effect: str):
        # Get a numpy array (wav)
        sample_rate, wav = wavfile.read(audio)

        if hasattr(self, effect):
            func = getattr(self, effect)

            # Process the numpy array
            processed_wav = func(wav)

            return processed_wav, sample_rate
        else:
            print(f'No effect "{effect}" found.')
        return None
    
    def no_effect(self, wav: np.ndarray) -> np.ndarray:
        return wav
    
    def no_sound(self, wav: np.ndarray) -> np.ndarray:
        return wav * 0
    
    def reverse(self, wav: np.ndarray) -> np.ndarray:
        return wav[::-1]