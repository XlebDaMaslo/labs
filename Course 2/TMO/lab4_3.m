x = -20:0.01:20;
y = -20:0.01:20;

[X, Y] = meshgrid(x, y);

F = 1 ./ (sin(X).^2) + 1 ./ (cos(Y).^2);

figure;
surf(X, Y, F);

title('График функции двух переменных F(x, y)');
xlabel('x');
ylabel('y');
zlabel('Z');

colormap jet; % Цветовая схема
colorbar;

grid on;

shading interp;
