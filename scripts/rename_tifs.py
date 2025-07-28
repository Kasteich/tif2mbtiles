import os
import re
from transliterate import translit

def renaming_filenames(filename):
    # Переименование из ру символов
    filename = translit(filename, 'ru', reversed=True)
    # Замена пробелов и символов
    filename = re.sub(r'[^\w.]', '_', filename)
    return filename



folder = "tif_files"

for filename in os.listdir(folder):
    if filename.lower().endswith('.tif'):
        # Замена пробелов
        new_name = renaming_filenames(filename)
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Переименовано: {filename} в {new_name}")