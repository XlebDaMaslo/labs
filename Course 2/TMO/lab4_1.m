x = -10:0.001:10;
f = (sin(x)).^2 ./ exp((sin(x)).^2);

dx = x(2) - x(1);
f_pr = diff(f) / dx;
x_pr = x(1:end-1);

f_integral = cumtrapz(x, f);

figure;

subplot(3,1,1)
plot(x, f, 'b', 'LineWidth', 2);
grid on;
title('График функции f(x) = (sin(x))^2 / e^{(sin(x))^2}');
xlabel('x');
ylabel('f(x)');

subplot(3,1,2);
plot(x_pr, f_pr, 'r', 'LineWidth', 2);
grid on;
title('График производной f''(x)');
xlabel('x');
ylabel('f''(x)');

subplot(3,1,3);
plot(x, f_integral, 'g', 'LineWidth', 2);
grid on;
title('График интеграла F(x) (определённого от -10)');
xlabel('x');
ylabel('F(x)');
