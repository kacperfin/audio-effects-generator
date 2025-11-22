import streamlit as st
import soundfile as sf
import numpy as np

from effects import reverse, delay, echo

LIST_OF_EFFECTS = ['Reverse', 'Delay', 'Echo']

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
    n_of_delays = st.slider('Number of delays', 1, 10, 3, 1)

if uploaded_file is not None:
    if effect in LIST_OF_EFFECTS:
        st.success(f'Success! {effect} effect has been applied.')
    else:
        st.warning(f'There is no such effect: {effect}')

    st.divider()

    # stereo -> mono
    audio_data = np.mean(audio_data, axis=1)

    st.header('Original audio')
    st.audio(audio_data, sample_rate=sample_rate)

    # show info about the input audio
    st.code(f'Sample rate: {sample_rate}\nNumber of samples: {len(audio_data)}')

    st.divider()
    st.header('Post-processed audio')

    if effect in LIST_OF_EFFECTS:
        if effect == 'Reverse':
            processed_audio = reverse(audio_data)
        elif effect == 'Delay':
            processed_audio = delay(audio_data, sample_rate, delay_time, feedback)
        elif effect == 'Echo':
            processed_audio = echo(audio_data, sample_rate, delay_time, feedback, n_of_delays)
        
        st.audio(processed_audio, sample_rate=sample_rate)
    else:
        st.warning('No valid effect has been selected.')