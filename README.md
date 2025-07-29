# Конвертер TIF-тайлов в MBTiles

Скрипт для объединения гео-тайлов (TIF) в единую карту формата MBTiles.


## Установка
1. **Установите зависимости**:
   ```bash
   pip install gdal transliterate
2. Для Windows установите GDAL через OSGeo4W или Conda
3. Для Linux
    ```bash
    sudo apt-get install gdal-bin

## Как использовать

### 1. Подготовка файлов
- Положите ваши .tif файлы в папку tif_files
- Если есть пробелы и кириллица, выполните:
```bash
python scripts/rename_tifs.py
```

### 2. Сшивание и конвертация
```bash
python scripts/tif_mbtiles.py
```

Результат появится в файле ```map.mbtiles``` в корне проекта.