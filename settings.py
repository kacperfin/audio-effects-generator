import os
from pathlib import Path

LIST_OF_EFFECTS = ['Filter', 'Overdrive', 'Phaser', 'Flanger', 'Chorus', 'Delay', 'Echo', 'Reverb', 'Reverse']
IR_DIR_PATH = Path('ir')

if IR_DIR_PATH.exists():
    list_of_ir_file_names = sorted([f[:-4] for f in os.listdir(IR_DIR_PATH) if f.endswith('.wav')])
else:
    list_of_ir_file_names = []