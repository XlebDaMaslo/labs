a = randn(1, 10);
b = randn(1, 10);

[autocorr1, lags1] = xcorr(a, 'normalized');
[autocorr2, lags2] = xcorr(b, 'normalized');

figure;

plot(lags1, autocorr1);
xlabel('Сдвиг');
ylabel('Автокорреляция');
grid on;
hold on;

plot(lags2, autocorr2);
title('Автокорреляция массива');
xlabel('Сдвиг');
ylabel('Автокорреляция');
grid on;