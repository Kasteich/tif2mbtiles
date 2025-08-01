import os
from osgeo import gdal
import sys
import logging
from typing import List



# Логирование
logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Ищет путь к папке
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
INPUT_FOLDER = os.path.join(PROJECT_ROOT, "tif_files")

# Спрашивает формат
def ask_format() -> str:
    while True:
        print("\nВыберите формат для конвертации:")
        print("1. JPG")
        print("2. PNG")
        print("3. WEBP")
        choice = input("Ваш выбор (1-3): ").strip()

        if choice == "1":
            return "jpg"
        elif choice == "2":
            return "png"
        elif choice == "3":
            return "webp"
        else:
            print("Ошибка. Выберите 1, 2 или 3")

# Запрос качества
def get_quality(format_type:str) -> str:
    while True:
        try:
            if format_type == "jpg":
                default = 90
                prompt = f"Качество JPG (1-100, по умолчанию {default}): "
                quality = int(input(prompt) or default)
                if 1 <= quality <= 100:
                    return quality
            elif format_type == "webp":
                default = 85
                prompt = f"Качество WEBP (1-100, по умолчанию {default}): "
                quality = int(input(prompt) or default)
                if 1 <= quality <= 100:
                    return quality
            else:
                default = 9
                prompt = f"Сжатие PNG (1-9, по умолчанию {default}): "
                quality = int(input(prompt) or default)
                if 1 <= quality <= 9:
                    return quality
        except ValueError:
            pass
        print("Ошибка. Введите корректное число")

# Возвращает список tif файлов
def get_tif_files(folder: str) -> List[str]:
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".tif", ".tiff"))
    ]

# Конвертирует один файл
def convert_file(input_path: str, output_path: str, format_type: str, quality: int):
    options = {
        'format': 'JPEG' if format_type == 'jpg' else 'PNG' if format_type == 'png' else 'WEBP',
        'creationOptions': []
    }

    if format_type == "jpg":
        options['creationOptions'].extend([f'QUALITY={quality}', 'PROGRESSIVE=YES'])
    elif format_type == "webp":
        options['creationOptions'].extend([f'QUALITY={quality}', 'LOSSLESS=FALSE'])
    else:
        options['creationOptions'].extend([f'ZLEVEL={quality}', 'PREDICTOR=2'])

    gdal.Translate(output_path, input_path, **options)
    logging.info(f"Конвертирован: {os.path.basename(input_path)} - {os.path.basename(output_path)}")

def main():
    print("Конвертер тайлов TIF в JPG/PNG/WEBP")

    print(f"Ищм папку: {INPUT_FOLDER}")

    # Проверка папки
    if not os.path.exists(INPUT_FOLDER):
        logging.error(f"Папка {INPUT_FOLDER} не найдена")
        print("\nВозможные решения:")
        print(f"1. Создайте папке 'tif_files' в: {PROJECT_ROOT}")
        print(f"2. Укажите правильный путь в коде скрипта")
        return

    # Выбор формата
    format_type = ask_format()
    quality = get_quality(format_type)

    tif_files = get_tif_files(INPUT_FOLDER)
    if not tif_files:
        logging.error("Не найдено .tif файлов для конвертации")
        return

    logging.info(f"\nНачинаю конвертацию {len(tif_files)} файлов в {format_type.upper()}")

    for tif_file in tif_files:
        output_file = os.path.splitext(tif_file)[0] + f".{format_type}"
        try:
            convert_file(tif_file, output_file, format_type, quality)
        except Exception as e:
            logging.error(f"Ошибка конвертации {tif_file}: {str(e)}")

    logging.error("\nГотово. Все файлы успешно конвертированы")

if __name__ == "__main__":
    main()


