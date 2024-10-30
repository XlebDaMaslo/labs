% 2. Задать значения λ и μ
lambda = 2; % Интенсивность входного потока
mu = 3; % Интенсивность обслуживания

if lambda >= mu
error('Система нестационарна');
end

% 3. Определить аналитические характеристики показательного распределения
E_tau = 1 / lambda;
D_tau = 1 / lambda^2;

% 4. Определить параметры распределения общего вида
% Параметры времени обслуживания (Вейбулловское распределение)
k_weibull = 1.5;
theta_weibull = 1 / mu;

% 5. Определить аналитические характеристики распределения общего вида.
E_nu_weibull = theta_weibull * gamma(1 + 1/k_weibull);
D_nu_weibull = theta_weibull^2 * (gamma(1 + 2/k_weibull) - (gamma(1 + 1/k_weibull))^2);

fprintf('Интенсивность входного потока (λ): %f\n', lambda);
fprintf('Интенсивность обслуживания (μ): %f\n\n', mu);

fprintf('Входной поток (показательное распределение):\n');
fprintf('  Математическое ожидание: %f\n', E_tau);
fprintf('  Дисперсия: %f\n\n', D_tau);

fprintf('Время обслуживания (Вейбулловское распределение):\n');
fprintf('  Математическое ожидание: %f\n', E_nu_weibull);
fprintf('  Дисперсия: %f\n\n', D_nu_weibull);

% 6. Задать длину последовательности N  100.
N = 1000000;  % Размер выборки

% 7. Сформировать управляющие по следовательности для системы M/M/1
tau_n = exprnd(E_tau, 1, N);

% 8. Сформировать управляющие последовательности для потока общего вида
nu_n_weibull = wblrnd(theta_weibull, k_weibull, 1, N);

%9. Рассчитать статистические характеристики для всех полученных выборок
% M/M/1
M_tau = mean(tau_n);
D_tau_sample = var(tau_n);

% G/G/1
M_nu_weibull = mean(nu_n_weibull);
D_nu_weibull_sample = var(nu_n_weibull);

fprintf('\nСтатистические характеристики выборок:\n');
fprintf('-----------------------------------------\n');
fprintf('M/M/1:\n');
fprintf('  tau_n:  Среднее = %f, Дисперсия = %f\n', M_tau, D_tau_sample);

fprintf('\nG/G/1\n');
fprintf('  nu_n:   Среднее = %f, Дисперсия = %f\n', M_nu_weibull, D_nu_weibull_sample);

fprintf('\nСравнение аналитических и статистических характеристик:\n');
fprintf('M/M/1:\n');
fprintf('Аналитическое: E = %.4f, D = %.4f\n', E_tau, D_tau);
fprintf('Статистическое: E = %.4f, D = %.4f\n', M_tau, D_tau_sample);

fprintf('G/G/1:\n');
fprintf('Аналитическое: E = %.4f, D = %.4f\n', E_nu_weibull, D_nu_weibull);
fprintf('Статистическое: E = %.4f, D = %.4f\n', M_nu_weibull, D_nu_weibull_sample);


% M/M/1
figure;
x = linspace(0, max(tau_n), 100);
y = lambda * exp(-lambda * x);
plot(x, y, 'r-', 'LineWidth', 2);
title('M/M/1');
xlabel('Время между поступлениями');
ylabel('Плотность вероятности');

% M/G/1
figure;
x = linspace(0, max(nu_n_weibull), 100);
y = (k_weibull / theta_weibull) * (x / theta_weibull).^(k_weibull - 1) .* exp(-(x / theta_weibull).^k_weibull);
plot(x, y, 'r-', 'LineWidth', 2);
title('M/G/1');
xlabel('Время обслуживания');
ylabel('Плотность вероятности');