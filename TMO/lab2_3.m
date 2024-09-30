N = 700;
K = 400;
mu = 0;
sigma = 1;

% матрица случайных блужданий с затуханием
xi = zeros(N, K); 
xi(1,:) = randn(1, K) * sigma + mu; % Начальное значение
for n = 2:N
    xi(n,:) = 0.9 * xi(n-1,:) + randn(1, K) * sigma + mu;
end

% графики всех реализаций
figure;
plot(xi);
title('Случайные блуждания с затуханием');
xlabel('n');
ylabel('\xi(n)');

% скаттерограммы
figure;
subplot(1,2,1);
scatter(xi(10,:), xi(9,:));
hold on;
scatter(xi(50,:), xi(49,:));
scatter(xi(100,:), xi(99,:));
scatter(xi(200,:), xi(199,:));
title('Скаттерограммы (\xi(n), \xi(n-1))');
xlabel('\xi(n)');
ylabel('\xi(n-1)');
legend('(10,9)', '(50,49)', '(100,99)', '(200,199)');

subplot(1,2,2);
scatter(xi(50,:), xi(40,:));
hold on;
scatter(xi(100,:), xi(90,:));
scatter(xi(200,:), xi(190,:));
title('Скаттерограммы (\xi(n), \xi(n-10))');
xlabel('\xi(n)');
ylabel('\xi(n-10)');
legend('(50,40)', '(100,90)', '(200,190)');

% выборочная автокорреляции
max_lag = 100;
r_sample = zeros(1, max_lag+1);
for l = 0:max_lag
    for n = l+1:N
        r_sample(l+1) = r_sample(l+1) + xi(n,:) * xi(n-l,:)';
    end
    r_sample(l+1) = r_sample(l+1) / (K * (N-l)); 
end

% теор автокорреляция
r_theory = (sigma^2 / (1 - 0.9^2)) * 0.9.^(0:max_lag);

% графики АКФ
figure;
plot(0:max_lag, r_sample, 'b-', 'LineWidth', 2);
hold on;
plot(0:max_lag, r_theory, 'r--', 'LineWidth', 2);
title('Автокорреляционная функция случайного блуждания с затуханием');
xlabel('Лаг');
ylabel('АКФ');
legend('Выборочная АКФ', 'Теоретическая АКФ');

mean_time = mean(xi, 2); 
mean_ensemble = mean(xi, 1);

fprintf('Среднее по времени для лага 1: %f\n', mean_time(2));
fprintf('Среднее по ансамблю для лага 1: %f\n', mean_ensemble(2));
fprintf('Среднее по времени для лага 2: %f\n', mean_time(3));
fprintf('Среднее по ансамблю для лага 2: %f\n', mean_ensemble(3));

% сравнение с теор значениями
fprintf('Разница между средним по времени и теоретическим значением для лага 1: %f\n', mean_time(2) - r_theory(2));
fprintf('Разница между средним по ансамблю и теоретическим значением для лага 1: %f\n', mean_ensemble(2) - r_theory(2));
fprintf('Разница между средним по времени и теоретическим значением для лага 2: %f\n', mean_time(3) - r_theory(3));
fprintf('Разница между средним по ансамблю и теоретическим значением для лага 2: %f\n\n', mean_ensemble(3) - r_theory(3));
