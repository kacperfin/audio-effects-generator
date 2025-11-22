import os
from pathlib import Path

LIST_OF_EFFECTS = ['Reverse', 'Delay', 'Echo', 'Reverb']
IR_DIR_PATH = Path('ir')

if IR_DIR_PATH.exists():
    list_of_ir_file_names = sorted([f[:-4] for f in os.listdir(IR_DIR_PATH) if f.endswith('.wav')])
else:
    list_of_ir_file_names = []