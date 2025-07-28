from osgeo import gdal
import os
import sys
import time
import logging
from typing import List

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler()
    ]
)
# Основная конфигурация
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
input_folder = os.path.join(project_root, "tif_files")
output_file = os.path.join(project_root, "map.mbtiles")
max_mem_size = 10 * 1024 * 1024 * 1024 # Лимит 10GB для работы в памяти

# Вычисляем общий размр файлов в байтах
def get_total_size(files: List[str]) -> int:
    return sum(os.path.getsize(f) for f in files)

# Отображение прогресса
def progress_callback(progress, _, message):
    logging.info(f"\rПрогресс: {progress * 100:.1f}%", extra={'end': ''})
    return 1

# Возвращаем список поддерживаемых форматов
def get_supp_extensions() -> List[str]:
    return ['.tif', '.tiff', '.jpg', '.jpeg', '.png']

# Находим файл для обработки
def find_input_files() -> List[str]:
    extensions = get_supp_extensions()
    return [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if os.path.splitext(f.lower())[1] in extensions
    ]

# Обрабатываем входные файлы
def process_input_files(files: List[str]):
    if len(files) == 1:
        logging.info(f"Обработка файла {os.path.basename(files[0])}")
        return files[0]

    logging.info(f"Начинаем сшивание {len(files)} файлов...")

    # Выбираем метод в зависимости от размера
    if get_total_size(files) > max_mem_size:
        logging.warning("Большой объем данных - используем временный файл")
        temp_file = "merged.tif"
        gdal.Warp(temp_file, files, callback=progress_callback)
        return temp_file
    else:
        return gdal.Warp("", files, options=gdal.WarpOptions(
            format='MEM',
            callback=progress_callback
        ))

# Удаляем временные файлы
def cleanup_temp_files():
    if os.path.exists("merged.tif"):
        os.remove("merged.tif")
        logging.info("Удалён временный файл merged.tif")

if __name__ == "__main__":
    try:
        start_time = time.time()

        logging.info(f"Ищем файлы в папке: {input_folder}")

        if not os.path.isdir(input_folder):
            raise FileNotFoundError(f"Папка '{input_folder}' не найдена")

        input_files = find_input_files()
        if not input_files:
            raise ValueError("Не найден файлов для обработки")

        # Обработка
        src_file = process_input_files(input_files)

        # Конвертация
        logging.info("Создаём карту mbtiles...")
        gdal.Translate(
            output_file,
            src_file,
            format="MBTILES",
            creationOptions=["TILE_FORMAT=PNG", "QUALITY=90"],
            callback=progress_callback
        )
        logging.info(f"\nФайл карты {output_file} успешно создан")

    except Exception as e:
        logging.error(f"Ошибка: {str(e)}", exc_info=True)
        sys.exit(1)

    finally:
        cleanup_temp_files()
        total_time = time.time() - start_time
        print(f"Файл карты {output_file} готов. Время выполнения: {total_time:.1f} секунд")


