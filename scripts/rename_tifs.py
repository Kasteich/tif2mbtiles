import os
import re
from transliterate import translit

def normalize_filenames(filename: str) -> str:
    try:
        name, ext = os.path.splitext(filename)
        name = translit(name, 'ru', reversed=True)
        name = re.sub(r'[^\w\-]','_', name) # Замена спецсимволов
        name = re.sub(r'_+', '_', name) # Удаление дублей _
        return f"{name}{ext}".lower() # Нижний регистр
    except Exception as e:
        print(f"[ERROR] Ошибка обработки имени {filename}: {str(e)}")
        return filename

def rename_files(folder: str = "tif_files") -> None:
    if not os.path.exists(folder):
        print(f"[ERROR] Папка {folder} не найдена!")
        return

    supp_ext = ('.tif', '.tiff', '.jpg', '.jpeg', '.png', '.webp')
    renamed_count = 0

    for filename in os.listdir(folder):
        if filename.lower().endswith(supp_ext):
            new_name = normalize_filenames(filename)

            if new_name != filename:
                old_path = os.path.join(folder, filename)
                new_path = os.path.join(folder, new_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"[INFO] Переименовано: {filename} в {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"[ERROR] Не удалось переименовать {filename} : {str(e)}")

    print(f"Готово. Переименовано файлов: {renamed_count}")

if __name__ == "__main__":
    rename_files()