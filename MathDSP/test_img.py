import cv2
import numpy as np
import matplotlib.pyplot as plt

# Загрузка изображения
image = cv2.imread(r'G:\Pictures\memes\photo_2024-10-23_16-00-39.jpg', cv2.IMREAD_GRAYSCALE)

# Преобразование Фурье
f = np.fft.fft2(image)
fshift = np.fft.fftshift(f)

# Создание фильтра низких частот (маска)
rows, cols = image.shape
crow, ccol = rows//2, cols//2
radius = 100  # Радиус области низких частот (уменьшить для большего ухудшения)
mask = np.zeros((rows, cols), np.uint8)
cv2.circle(mask, (crow, ccol), radius, 1, -1)

# Применение маски к преобразованию Фурье
fshift_masked = fshift * mask

# Обратное преобразование Фурье
f_ishift = np.fft.ifftshift(fshift_masked)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

# Обеспечение, что значения пикселей находятся в допустимом диапазоне
img_back = np.clip(img_back, 0, 255).astype(np.uint8)

# Отображение изображений
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Оригинальное изображение')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img_back, cmap='gray')
plt.title('Изображение с ухудшенным сигналом')
plt.axis('off')

plt.tight_layout()
plt.show()