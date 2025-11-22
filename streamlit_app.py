import streamlit as st
import soundfile as sf
import numpy as np

from effects import reverse, delay, echo, convolution_reverb
from normalize import normalize
from settings import LIST_OF_EFFECTS, list_of_ir_file_names

st.set_page_config(page_title='Audio Effects Generator', page_icon='🎧', layout='centered')

st.title('🎧 Audio Effects Generator')
st.write('Upload a `.wav` file and apply different audio effects.')

st.divider()

uploaded_file = st.file_uploader('Upload a WAV file', type=['wav'])

if uploaded_file is not None:
    audio_data, sample_rate = sf.read(uploaded_file) # audio_data is an numpy.ndarray

st.divider()

st.header('Effects')
effect = st.selectbox('Select effect', LIST_OF_EFFECTS)

if effect == 'Reverse':
    pass
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
        if effect == 'Reverse':
            processed_audio = reverse(audio_data)
        elif effect == 'Delay':
            processed_audio = delay(audio_data, sample_rate, delay_time, feedback)
        elif effect == 'Echo':
            processed_audio = echo(audio_data, sample_rate, delay_time, feedback, repetitions)
        elif effect == 'Reverb':
            if ir_file_name is not None:
                processed_audio = convolution_reverb(audio_data, sample_rate, ir_file_name, wet_dry_mix)
            else:
                raise FileNotFoundError('No IR files available. Cannot apply Reverb effect.')

        # normalize after applying effect
        processed_audio = normalize(processed_audio)
    except Exception as e:
        st.error(e)
    else:
        st.audio(processed_audio, sample_rate=sample_rate)
        st.success(f'Success! {effect} effect has been applied.')