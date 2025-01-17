import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
import random
from PIL import Image

def load_image(image_path):
    """Загружает изображение с использованием Pillow и преобразует в массив NumPy для OpenCV."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")  # Преобразуем изображение в RGB
        return np.array(img)  # Возвращаем массив
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

def shuffle_image(image_path, output_image_path):
    # Загружаем изображение
    image = load_image(image_path)
    
    # Проверка на успешность загрузки изображения
    if image is None:
        print(f"Не удалось загрузить изображение: {image_path}")
        return

    # Проверьте количество каналов (должно быть 3 для RGB)
    if len(image.shape) < 3 or image.shape[2] != 3:
        print(f"Неподдерживаемый формат изображения: {image_path}. Изображение должно иметь 3 канала (RGB).")
        return

    height, width, _ = image.shape
    
    # Убедимся, что при делении на 2, мы корректно разбиваем на 4 плитки
    h, w = height // 2, width // 2

    # Переписываем плитки, чтобы гарантировать, что мы имеем 4 плитки
    tiles = [
        image[0:h, 0:w],        # Верхняя левая плитка
        image[0:h, w:width],    # Верхняя правая плитка
        image[h:height, 0:w],   # Нижняя левая плитка
        image[h:height, w:width] # Нижняя правая плитка
    ]

    # Перемешивание плиток
    random.shuffle(tiles)

    # Собираем плитки обратно в одно изображение
    shuffled_image = np.vstack((np.hstack((tiles[0], tiles[1])), np.hstack((tiles[2], tiles[3]))))

    # Сохраняем перемешанное изображение
    cv2.imwrite(output_image_path, shuffled_image)
    print(f"Создано перемешанное изображение: {output_image_path}")

def select_image():
    file_path = filedialog.askopenfilename(title="Выберите изображение файл", 
                                           filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        output_path = os.path.join(os.path.expanduser("~"), "Desktop", "shuffled_image.jpg")
        shuffle_image(file_path, output_path)

# Создание графического интерфейса
root = tk.Tk()
root.title("Перемешиватель изображений")
root.geometry("320x120")  # Установка размера окна

select_image_button = tk.Button(root, text="Выбрать изображение", command=select_image)
select_image_button.pack(pady=10)

# Запустить основной цикл интерфейса
root.mainloop()
