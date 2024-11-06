% 1. Проверка параметров
lambda = 2; % Интенсивность входного потока
mu = 3; % Интенсивность обслуживания

if lambda <= 0 || mu <= 0
    error('Интенсивность потока (λ) и обслуживания (μ) должны быть положительными.');
end

if lambda >= mu
    error('Система нестационарна, λ должно быть меньше μ.');
end

% 2. Аналитические характеристики показательного распределения
E_tau = 1 / lambda;
D_tau = 1 / lambda^2;

% 3. Параметры распределения Вейбулла
k_weibull = 1.5;
theta_weibull = 1 / mu;

if k_weibull <= 0
    error('Параметр формы Вейбулловского распределения (k_weibull) должен быть положительным.');
end

% 4. Аналитические характеристики распределения Вейбулла
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

% 5. Задать длину последовательности N >= 100.
N = 1000000;  % Размер выборки
if N < 100
    error('Размер выборки N должен быть не меньше 100.');
end

% 6. Сформировать выборки для системы M/M/1 и M/G/1
tau_n = exprnd(1/lambda, 1, N);
nu_n_weibull = wblrnd(theta_weibull, k_weibull, 1, N);

% 7. Статистические характеристики выборок
% M/M/1
M_tau = mean(tau_n);
D_tau_sample = var(tau_n);

% M/G/1
M_nu_weibull = mean(nu_n_weibull);
D_nu_weibull_sample = var(nu_n_weibull);

% 8. Вывод статистических характеристик
fprintf('\nСтатистические характеристики выборок:\n');
fprintf('-----------------------------------------\n');
fprintf('M/M/1:\n');
fprintf('  tau_n:  Среднее = %f, Дисперсия = %f\n', M_tau, D_tau_sample);

fprintf('\nM/G/1\n');
fprintf('  nu_n:   Среднее = %f, Дисперсия = %f\n', M_nu_weibull, D_nu_weibull_sample);

% 9. Сравнение аналитических и статистических характеристик
compare_stats(E_tau, D_tau, M_tau, D_tau_sample, 'M/M/1');
compare_stats(E_nu_weibull, D_nu_weibull, M_nu_weibull, D_nu_weibull_sample, 'M/G/1');

% 10. Визуализация результатов
x_mm1 = linspace(0, max(tau_n), 100);
y_mm1 = pdf('Exponential', x_mm1, 1/lambda);
plot_density(tau_n, x_mm1, y_mm1, 'M/M/1: Плотность вероятности и гистограмма выборки', 'Время между поступлениями', 'Плотность вероятности');

x_mg1 = linspace(0, max(nu_n_weibull), 100);
y_mg1 = pdf('Weibull', x_mg1, k_weibull, theta_weibull);
plot_density(nu_n_weibull, x_mg1, y_mg1, 'M/G/1: Плотность вероятности и гистограмма выборки', 'Время обслуживания', 'Плотность вероятности');

% --- Вспомогательные функции ---

% Функция для сравнения аналитических и статистических характеристик
function compare_stats(analytical_E, analytical_D, sample_E, sample_D, system_name)
    fprintf('\n%s:\n', system_name);
    fprintf('Аналитическое: E = %.4f, D = %.4f\n', analytical_E, analytical_D);
    fprintf('Статистическое: E = %.4f, D = %.4f\n', sample_E, sample_D);
    if abs(analytical_E - sample_E) > 0.01
        fprintf('ВНИМАНИЕ: Средние значения существенно различаются!\n');
    end
    if abs(analytical_D - sample_D) > 0.01
        fprintf('ВНИМАНИЕ: Дисперсии существенно различаются!\n');
    end
end

% Функция для построения графиков плотности вероятности и гистограммы
function plot_density(sample, x, y, title_text, xlabel_text, ylabel_text)
    figure;
    plot(x, y, 'r-', 'LineWidth', 2); % Плотность вероятности
    hold on;
    histogram(sample, 'Normalization', 'pdf', 'FaceAlpha', 0.3); % Гистограмма выборки
    grid on;
    title(title_text);
    xlabel(xlabel_text);
    ylabel(ylabel_text);
    legend('Аналитическая плотность', 'Гистограмма выборки');
end
