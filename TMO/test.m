f1 = 10;
f2 = f1 + 4;
f3 = f1 * 2 + 1;

t = linspace(0, 1, 1000);
%t = [0:1000-1]/1000;

s1 = cos(2 * pi * f1 * t);
s2 = cos(2 * pi * f2 * t);
s3 = cos(2 * pi * f3 * t);

a_t = 5 * s1 + 4 * s2 + s3;
b_t = 3 * s1 + s3;

corr_ab = sum(a_t .* b_t);
corr_sa = sum(s1 .* a_t);
corr_sb = sum(s1 .* b_t);
norm_corr_ab = corr(a_t', b_t');
norm_corr_sa = corr(s1', a_t');
norm_corr_sb = corr(s1', b_t');

fprintf('Корреляция между a(t) и b(t): %.2f\n', corr_ab);
fprintf('Корреляция между s1(t) и a(t): %.2f\n', corr_sa);
fprintf('Корреляция между s1(t) и b(t): %.2f\n', corr_sb);

fprintf('Нормализованная корреляция между a(t) и b(t): %.2f\n', norm_corr_ab);
fprintf('Нормализованная корреляция между s1(t) и a(t): %.2f\n', norm_corr_sa);
fprintf('Нормализованная корреляция между s1(t) и b(t): %.2f\n', norm_corr_sb);

a = [0.3, 0.2, -0.1, 4.2, -2, 1.5, 0];
b = [0.3, 4, -2.2, 1.6, 0.1, 0.1, 0.2];

figure;

subplot(2, 1, 1);
plot(a, 'o-');
title('Массив a');
xlabel('N');
ylabel('Значение');
grid on;

subplot(2, 1, 2);
plot(b, 'o-');
title(['Массив b']);
xlabel('N');
ylabel('Значение');
grid on;

N = length(a);
correlations = zeros(1, N); 

for shift = 0:N-1
    b_shifted = [b(end-shift+1:end), b(1:end-shift)];
    correlations(shift + 1) = sum(a .* b_shifted);
end

[max_corr, max_index] = max(correlations);

fprintf('Максимальная корреляция: %.2f при сдвиге: %d\n', max_corr, max_index - 1);

figure;

subplot(2, 1, 1);
plot(a, 'o-');
title('Массив a');
xlabel('Индекс');
ylabel('Значение');
grid on;

b_max_shifted = [b(end-max_index+2:end), b(1:end-max_index+1)];
subplot(2, 1, 2);
plot(b_max_shifted, 'o-');
title(['Сдвинутый массив b (сдвиг: ', num2str(max_index - 1), ')']);
xlabel('Индекс');
ylabel('Значение');
grid on;

figure;
plot(0:N-1, correlations, '-o');
title('Взаимная корреляция между a и сдвинутым b');
xlabel('Сдвиг');
ylabel('Корреляция');
grid on;
