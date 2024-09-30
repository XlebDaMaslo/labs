N = 700;    % количество временных отсчетов
K = 400;    % количество реализаций
mu = 0;     % среднее значение шума
sigma = 1;  % стандартное отклонение шума

w = sigma * randn(N, K) + mu; % белый гауссовский шум

xi = zeros(N, K); %  матрица случайных блужданий

% вычисление случайных блужданий
for k = 1:K
    for n = 2:N
        xi(n, k) = xi(n-1, k) + w(n, k);
    end
end

% график всех реализаций
figure;
plot(xi);
title('Случайные блуждания');
xlabel('N');
ylabel('Значение случайного блуждания');

% пары для скаттерограмм
pairs1 = [10 9; 50 49; 100 99; 200 199];
pairs2 = [50 40; 100 90; 200 190];

% построение скаттерограмм
figure;

% первая группа пар
subplot(1, 2, 1);
hold on;
for i = 1:size(pairs1, 1)
    n1 = pairs1(i, 1);
    n2 = pairs1(i, 2);
    scatter(xi(n1, :), xi(n2, :), '.');
end
title('Скаттерограммы (группа 1)');
xlabel('\xi(n1)');
ylabel('\xi(n2)');
legend(cellstr(num2str(pairs1)))

% вторая группа пар
subplot(1, 2, 2);
hold on;
for i = 1:size(pairs2, 1)
    n1 = pairs2(i, 1);
    n2 = pairs2(i, 2);
    scatter(xi(n1, :), xi(n2, :), '.');
end
title('Скаттерограммы (группа 2)');
xlabel('\xi(n1)');
ylabel('\xi(n2)');
legend(cellstr(num2str(pairs2)))

hold off;

% расчет выборочной автокорреляции по ансамблю
autocorr = zeros(N-1, 1);  % массив для автокорреляции
for n = 2:N
    autocorr(n-1) = mean(xi(n, :) .* xi(n-1, :));
end

autocorr_theor = sigma^2 * (1:N-1);  % теоретическое значение автокорреляции для случайного блуждания

% построение графика
figure;
plot(1:N-1, autocorr, 'r');
hold on;
plot(1:N-1, autocorr_theor, 'b');
title('Автокорреляция случайного блуждания');
xlabel('N');
ylabel('Автокорреляция');
legend('Выборочная автокорреляция', 'Теоретическая автокорреляция');
grid on;
hold off;
