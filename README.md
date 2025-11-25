# Audio Effects Generator

A web-based audio effects processor built with Python and Streamlit. Upload a WAV file and apply various digital audio effects in real-time.

## Features

This application provides the following audio effects:

- **Filter** - High-pass and low-pass frequency filtering
- **Overdrive** - Guitar-style distortion with adjustable drive and tone
- **Phaser** - Sweeping all-pass filter effect with configurable stages and feedback
- **Flanger** - Time-varying delay effect with LFO modulation
- **Chorus** - Multiple detuned voices for a rich, layered sound
- **Delay** - Single delayed repetition with feedback control
- **Echo** - Multiple discrete repetitions with exponential decay
- **Reverb** - Convolution-based reverb using impulse response files
- **Reverse** - Reverse playback of audio

## Technology Stack

- **Python** - Core programming language
- **NumPy** - Array operations and signal processing
- **SciPy** - Butterworth filters and convolution algorithms
- **SoundFile** - WAV file reading and writing
- **Streamlit** - Web interface and audio playback

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd audio-effects-generator
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
```

3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run streamlit_app.py
```

2. Open your browser to the URL displayed (typically `http://localhost:8501`)

3. Upload a WAV file using the file uploader

4. Select an effect from the dropdown menu

5. Adjust effect parameters using the sliders

6. Listen to the original and processed audio using the built-in audio players

## Effect Parameters

### Filter
- **Low Pass Frequency** - Removes frequencies above this threshold (20-20000 Hz)
- **High Pass Frequency** - Removes frequencies below this threshold (20-20000 Hz)

### Overdrive
- **Drive** - Amount of gain/distortion applied (1.0-20.0)
- **Tone** - Brightness control, higher values produce brighter sound (0.0-1.0)

### Phaser
- **Rate** - LFO speed in Hz (0.1-2.0)
- **Depth** - Intensity of the phase shifting effect (0.0-1.0)
- **Number of Stages** - Cascaded all-pass filters (2-8)
- **Feedback** - Amount of processed signal fed back (0.0-0.9)
- **Wet/Dry Mix** - Balance between processed and original signal (0.0-1.0)

### Flanger
- **Rate** - LFO speed in Hz (0.1-5.0)
- **Depth** - Maximum delay time in seconds (0.001-0.010)
- **Feedback** - Amount of delayed signal fed back (0.0-0.9)
- **Wet/Dry Mix** - Balance between processed and original signal (0.0-1.0)

### Chorus
- **Number of Voices** - How many detuned copies to create (2-6)
- **Rate** - LFO speed in Hz (0.5-5.0)
- **Depth** - Maximum delay variation in seconds (0.001-0.050)
- **Wet/Dry Mix** - Balance between processed and original signal (0.0-1.0)

### Delay
- **Delay Time** - Time between original and delayed signal (0.01-1.0 seconds)
- **Feedback** - Amount of delayed signal fed back for repetition (0.0-1.0)

### Echo
- **Delay Time** - Time between repetitions (0.01-1.0 seconds)
- **Feedback** - Decay rate of repetitions (0.0-1.0)
- **Repetitions** - Number of discrete echoes (1-10)

### Reverb
- **Room Type** - Select from available impulse response files in the `ir/` folder
- **Wet/Dry Mix** - Balance between reverb and original signal (0.01-1.0)

### Reverse
No parameters - simply reverses the audio playback

## Impulse Response Files

The reverb effect requires impulse response (IR) files:

1. Place `.wav` IR files in the `ir/` folder
2. Files should match the sample rate of your input audio
3. The application will automatically detect and list available IR files

## Project Structure

```
audio-effects-generator/
├── streamlit_app.py    # Main Streamlit application
├── effects.py          # Audio effect implementations
├── normalize.py        # Audio normalization utility
├── settings.py         # Configuration and constants
├── requirements.txt    # Python dependencies
├── ir/                 # Impulse response files directory
└── README.md          # This file
```

## Implementation Details

All effects are implemented using NumPy array operations for performance:

- **Filters** use SciPy's Butterworth filter implementation
- **Phaser** employs cascaded all-pass filters with LFO-modulated frequencies
- **Flanger/Chorus** use fractional delay with linear interpolation
- **Reverb** uses FFT-based convolution for efficiency
- **Overdrive** applies hyperbolic tangent for soft clipping

Audio is automatically normalized after processing to prevent clipping.

## License

This project is freely available for anyone to use, modify, and distribute for any purpose, including commercial applications.

## Author

Developed by Kacper Aleksander ([github.com/kacperfin](https://github.com/kacperfin)) as a course project for Techniki Multimedialne (Multimedia Technology) at Warsaw University of Technology.