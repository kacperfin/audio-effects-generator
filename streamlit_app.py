import streamlit as st

from audio_processor import AudioProcessor

if 'audio_processor' not in st.session_state:
    st.session_state.audio_processor = AudioProcessor()
    st.session_state.list_of_effect_names = st.session_state.audio_processor.get_effect_names()

st.title('🎶 Audio effects generator')

with st.form('audio_effects_generator'):

    audio = st.audio_input('Record your voice')

    chosen_effect = st.radio('Choose the effect', st.session_state.list_of_effect_names)
    
    submitted = st.form_submit_button('Generate')


if submitted:
    if audio is None:
        st.write('Please record a voice message first!')
    else:
        processed_audio, sample_rate = st.session_state.audio_processor.apply_effect(audio, chosen_effect) # type: ignore

        if processed_audio is not None:
            st.write(f'Your audio with the {chosen_effect} effect!')
            st.audio(processed_audio, sample_rate=sample_rate)
        else:
            st.write('There was some problem processing your audio.')