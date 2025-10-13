from scipy.io import wavfile
import numpy as np

class AudioProcessor():
    _EFFECT_NAMES = ['no_effect', 'no_sound', 'reverse', 'delay']

    def get_effect_names(self) -> list[str]:
        return self._EFFECT_NAMES

    def apply_effect(self, audio, effect: str):
        # Get a numpy array (wav)
        sample_rate, wav = wavfile.read(audio)

        if hasattr(self, effect):
            func = getattr(self, effect)

            # Process the numpy array
            processed_wav = func(wav, sample_rate)

            final_wav = np.clip(processed_wav, -32768, 32767).astype(np.int16)

            return final_wav, sample_rate
        else:
            print(f'No effect "{effect}" found.')
        return None
    
    def no_effect(self, wav: np.ndarray, sample_rate: int) -> np.ndarray:
        return wav
    
    def no_sound(self, wav: np.ndarray, sample_rate: int) -> np.ndarray:
        return wav * 0
    
    def reverse(self, wav: np.ndarray, sample_rate: int) -> np.ndarray:
        return wav[::-1]
    
    def delay(self, wav: np.ndarray, sample_rate: int, delay_time_ms: float = 500, num_repeats: int = 3, feedback: float = 0.5) -> np.ndarray:
        delay_samples = int(sample_rate * delay_time_ms / 1000)

        # Work in int32 to prevent overflow
        output = wav.astype(np.int32)

        # Add each delayed repetition with decreasing volume
        for i in range(1, num_repeats + 1):
            delay_offset = i * delay_samples
            gain = feedback ** i

            if delay_offset < len(output):
                output[delay_offset:] += (wav[:len(output) - delay_offset] * gain).astype(np.int32)

        return output