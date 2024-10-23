import svgpathtools as svg
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq

paths, attributes = svg.svg2paths(r'G:\Pictures\bird.svg')

x_coords = []
y_coords = []

for path in paths:
    for segment in path:
        x_coords.append(segment.start.real)
        y_coords.append(segment.start.imag)
        x_coords.append(segment.end.real)
        y_coords.append(segment.end.imag)

plt.figure(figsize=(12, 6))
ax = plt.subplot(1, 1, 1)
plt.plot(x_coords, y_coords, 'bo-', markersize=2)
plt.title('Контур из SVG координат')
plt.xlabel('X координата')
plt.ylabel('Y координата')
plt.grid(True)
ax.invert_yaxis()
plt.axis('equal')

signal_x = np.array(x_coords)
signal_y = np.array(y_coords)

plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.plot(signal_x, signal_y, 'b-', markersize=2)
plt.title('Оригинальный сигнал')
plt.xlabel('X')
plt.ylabel('Y')
plt.gca().invert_yaxis()

thinning_factor = 10
signal_x_thinned = signal_x[::thinning_factor]
signal_y_thinned = signal_y[::thinning_factor]

plt.subplot(2, 2, 2)
plt.plot(signal_x_thinned, signal_y_thinned, 'b-', markersize=2)
plt.title(f'Прореженный контур ({thinning_factor} раз)')
plt.xlabel('X')
plt.ylabel('Y')
plt.gca().invert_yaxis()

thinning_factor = 25
signal_x_thinned = signal_x[::thinning_factor]
signal_y_thinned = signal_y[::thinning_factor]

plt.subplot(2, 2, 3)
plt.plot(signal_x_thinned, signal_y_thinned, 'b-', markersize=2)
plt.title(f'Прореженный контур ({thinning_factor} раз)')
plt.xlabel('X')
plt.ylabel('Y')
plt.gca().invert_yaxis()

thinning_factor = 50
signal_x_thinned = signal_x[::thinning_factor]
signal_y_thinned = signal_y[::thinning_factor]

plt.subplot(2, 2, 4)
plt.plot(signal_x_thinned, signal_y_thinned, 'b-', markersize=2)
plt.title(f'Прореженный контур ({thinning_factor} раз)')
plt.xlabel('X')
plt.ylabel('Y')
plt.gca().invert_yaxis()

plt.tight_layout()
plt.show()