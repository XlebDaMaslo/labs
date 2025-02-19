% Корень
f = @(x) 4*x + 6 - sin(x);

x0 = 0;

root = fzero(f, x0);

disp(['Корень уравнения: ', num2str(root)]);

% График
x = -10:0.1:10;

y1 = 4*x + 6;
y2 = sin(x);

figure;
plot(x, y1, 'b', 'LineWidth', 2);
hold on;
plot(x, y2, 'r', 'LineWidth', 2);
grid on;

title('Графическое решение уравнения 4x + 6 = sin(x)');
xlabel('x');
ylabel('y');
legend('y = 4x + 6', 'y = sin(x)');
ylim([-2 2]);
xlim([-4 4]);