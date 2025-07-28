from osgeo import gdal
import os
import sys
import time

input_folder = "tif_files"
output_file = "map.mbtiles"

# Отображение прогресса
def progress_callback(progress, _, message):
    print(f"\rПрогресс: {progress * 100:.1f}%", end="", flush=True)
    return 1

# Обработка
if __name__ == "__main__":
    # Проверяем память
    if not os.path.isdir(input_folder):
        print(f"Папка '{input_folder}' не найдена")
        sys.exit(1)

    # Ищем TIFF файлы
    tif_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder)
                 if f.lower().endswith('.tif')]

    if not tif_files:
        print("Ошибка. В папке нет файлов tif")
        sys.exit(1)

    start_time = time.time()

    try:
        # Если один файл
        if len(tif_files) == 1:
            print("Обработка файла...")
            src_file = tif_files[0] # исходный файл
        else:
            # Если файлов больше одного
            print(f"Начинаем сшивание {len(tif_files)} файлов...")
            warp_result = gdal.Warp("", tif_files,
                          options=gdal.WarpOptions(
                              format='MEM',
                              callback=progress_callback
                          ))
            src_file = warp_result
            print()

        print("\nСоздаем карту...")
        gdal.Translate(
            output_file,
            src_file,
            format="MBTILES",
            creationOptions=["TILE_FORMAT=PNG"],
            callback=progress_callback
        )
        print()

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        sys.exit(1)

    finally:
        total_time = time.time() - start_time
        print(f"Файл карты {output_file} готов. Время выполнения: {total_time:.1f} секунд")


