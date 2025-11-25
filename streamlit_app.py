import streamlit as st
import soundfile as sf
import numpy as np

from effects import filter, overdrive, phaser, flanger, chorus, delay, echo, convolution_reverb, reverse
from normalize import normalize
from settings import LIST_OF_EFFECTS, list_of_ir_file_names

st.set_page_config(page_title='Audio Effects Generator', page_icon='🎧', layout='centered')

st.title('🎧 Audio Effects Generator')
st.write('Upload a `.wav` file and apply different audio effects.')

st.divider()

uploaded_file = st.file_uploader('Upload a WAV file', type=['wav'])

if uploaded_file is not None:
    audio_data, sample_rate = sf.read(uploaded_file)

st.divider()

st.header('Effects')
effect = st.selectbox('Select effect', LIST_OF_EFFECTS)

if effect == 'Filter':
    lowpass_freq = st.slider('Low Pass Frequency (Hz)', 20, 20000, 20000, 10)
    highpass_freq = st.slider('High Pass Frequency (Hz)', 20, 20000, 20, 10)
elif effect == 'Overdrive':
    drive = st.slider('Drive', 1.0, 20.0, 5.0, 0.1)
    tone = st.slider('Tone', 0.0, 1.0, 1.0, 0.01)
elif effect == 'Phaser':
    rate = st.slider('Rate (Hz)', 0.1, 2.0, 0.5, 0.01)
    depth = st.slider('Depth', 0.0, 1.0, 1.0, 0.01)
    num_stages = st.slider('Number of stages', 2, 8, 4, 1)
    feedback = st.slider('Feedback', 0.0, 0.9, 0.5, 0.01)
    wet_dry_mix = st.slider('Wet/Dry mix', 0.0, 1.0, 0.5, 0.01)
elif effect == 'Flanger':
    rate = st.slider('Rate (Hz)', 0.1, 5.0, 0.5, 0.1)
    depth = st.slider('Depth (seconds)', 0.001, 0.010, 0.002, 0.001, format='%.3f')
    feedback = st.slider('Feedback', 0.0, 0.9, 0.5, 0.01)
    wet_dry_mix = st.slider('Wet/Dry mix', 0.0, 1.0, 0.5, 0.01)
elif effect == 'Chorus':
    num_voices = st.slider('Number of voices', 2, 6, 3, 1)
    rate = st.slider('Rate (Hz)', 0.5, 5.0, 1.5, 0.01)
    depth = st.slider('Depth (seconds)', 0.001, 0.050, 0.020, 0.001, format='%.3f')
    wet_dry_mix = st.slider('Wet/Dry mix', 0.0, 1.0, 0.5, 0.01)
elif effect == 'Delay':
    delay_time = st.slider('Delay time', 0.01, 1.0, 0.3, 0.01)
    feedback = st.slider('Feedback', 0.0, 1.0, 0.3, 0.01)
elif effect == 'Echo':
    delay_time = st.slider('Delay time', 0.01, 1.0, 0.3, 0.01)
    feedback = st.slider('Feedback', 0.0, 1.0, 0.5, 0.01)
    repetitions = st.slider('Repetitions', 1, 10, 3, 1)
elif effect == 'Reverb':
    if not list_of_ir_file_names:
        st.warning('No IR files found in the "ir" folder. Please add .wav IR files to use the Reverb effect.')
    ir_file_name = st.selectbox('Room type', list_of_ir_file_names) if list_of_ir_file_names else None
    wet_dry_mix = st.slider('Wet/Dry mix', 0.01, 1.0, 0.3, 0.01) if list_of_ir_file_names else 0.3
elif effect == 'Reverse':
    pass

if uploaded_file is not None:
    st.divider()

    # stereo -> mono
    audio_data = np.mean(audio_data, axis=1)

    st.header('Original audio')
    st.audio(audio_data, sample_rate=sample_rate)

    # show info about the input audio
    st.code(f'Sample rate: {sample_rate}\nNumber of samples: {len(audio_data)}')

    st.divider()
    st.header('Post-processed audio')

    try:
        if effect == 'Filter':
            processed_audio = filter(audio_data, sample_rate, lowpass_freq, highpass_freq)
        elif effect == 'Overdrive':
            processed_audio = overdrive(audio_data, sample_rate, drive, tone)
        elif effect == 'Phaser':
            processed_audio = phaser(audio_data, sample_rate, rate, depth, num_stages, feedback, wet_dry_mix)
        elif effect == 'Flanger':
            processed_audio = flanger(audio_data, sample_rate, rate, depth, feedback, wet_dry_mix)
        elif effect == 'Chorus':
            processed_audio = chorus(audio_data, sample_rate, num_voices, rate, depth, wet_dry_mix)
        elif effect == 'Delay':
            processed_audio = delay(audio_data, sample_rate, delay_time, feedback)
        elif effect == 'Echo':
            processed_audio = echo(audio_data, sample_rate, delay_time, feedback, repetitions)
        elif effect == 'Reverb':
            if ir_file_name is not None:
                processed_audio = convolution_reverb(audio_data, sample_rate, ir_file_name, wet_dry_mix)
            else:
                raise FileNotFoundError('No IR files available. Cannot apply Reverb effect.')
        elif effect == 'Reverse':
            processed_audio = reverse(audio_data)

        # normalize after applying effect
        processed_audio = normalize(processed_audio)
    except Exception as e:
        st.error(e)
    else:
        st.audio(processed_audio, sample_rate=sample_rate)
        st.success(f'Success! {effect} effect has been applied.')
