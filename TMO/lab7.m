%% 3. Установить значения входных параметров lambda и mu
lambda = 2;  % Интенсивность входного потока
mu = 3;      % Интенсивность обслуживания

% Параметры Вейбулловского распределения
k_weibull = 1.5;
theta_weibull = 1 / mu;

% Проверка стационарности системы для M/M/1
if lambda >= mu
    error('Система M/M/1 нестабильна, λ должно быть меньше μ');
end

N = 1000000; % Количество заявок для полной симуляции
t = linspace(0, 100, N);  % Временная шкала

%% 4. Моделирование поступления и обслуживания для различных систем
% M/M/1 (экспоненциальные распределения для поступления и обслуживания)
tau_mm1 = exprnd(1/lambda, 1, N);  % Время между поступлениями
nu_mm1 = exprnd(1/mu, 1, N);       % Время обслуживания

% M/G/1 (экспоненциальные поступления, Вейбулловское обслуживание)
tau_mg1 = exprnd(1/lambda, 1, N);
nu_mg1 = wblrnd(theta_weibull, k_weibull, 1, N);

% Проверка стационарности системы M/G/1
if lambda >= 1 / mean(nu_mg1)
    error('Система M/G/1 нестабильна, λ должно быть меньше среднего значения обслуживания');
end

% G/M/1 (Вейбулловские поступления, экспоненциальное обслуживание)
tau_gm1 = wblrnd(1/lambda, k_weibull, 1, N);
nu_gm1 = exprnd(1/mu, 1, N);

% Проверка стационарности системы G/M/1
if lambda >= mu
    error('Система G/M/1 нестабильна, λ должно быть меньше μ');
end

% G/G/1 (Вейбулловские поступления и Вейбулловское обслуживание)
tau_gg1 = wblrnd(1/lambda, k_weibull, 1, N);
nu_gg1 = wblrnd(theta_weibull, k_weibull, 1, N);

% Проверка стационарности системы G/G/1
if lambda >= 1 / mean(nu_gg1)
    error('Система G/G/1 нестабильна, λ должно быть меньше среднего значения обслуживания');
end

%% 5. Построение графиков для каждого типа СМО
figure;
sample_rate = 1000;  % Шаг выборки данных для ускорения построения графиков
t_sample = t(1:sample_rate:end);  % Выборка времени для графика

% M/M/1
subplot(2,2,1);
plot(t_sample, cumsum(tau_mm1(1:sample_rate:end)) - cumsum(nu_mm1(1:sample_rate:end)));
title('M/M/1');
xlabel('Время');
ylabel('Число заявок');
ylim([0 N/5]);

% M/G/1
cum_tau_mg1 = cumsum(tau_mg1);
cum_nu_mg1 = cumsum(nu_mg1);
subplot(2,2,2);
plot(t_sample, cum_tau_mg1(1:sample_rate:end) - cum_nu_mg1(1:sample_rate:end));
title('M/G/1');
xlabel('Время');
ylabel('Число заявок');
ylim([0 N/5]);

% G/M/1
cum_tau_gm1 = cumsum(tau_gm1);
cum_nu_gm1 = cumsum(nu_gm1);
subplot(2,2,3);
plot(t_sample, cum_tau_gm1(1:sample_rate:end) - cum_nu_gm1(1:sample_rate:end));
title('G/M/1');
xlabel('Время');
ylabel('Число заявок');
ylim([0 N/5]);

% G/G/1
cum_tau_gg1 = cumsum(tau_gg1);
cum_nu_gg1 = cumsum(nu_gg1);
subplot(2,2,4);
plot(t_sample, cum_tau_gg1(1:sample_rate:end) - cum_nu_gg1(1:sample_rate:end));
title('G/G/1');
xlabel('Время');
ylabel('Число заявок');
ylim([0 N/5]);

%% 7. Рассчитать статистические характеристики для каждого типа СМО
% M/M/1
rho_mm1 = lambda / mu;
L_mm1 = rho_mm1 / (1 - rho_mm1);  % Среднее число заявок в системе L = ρ / (1 - ρ)
W_q_mm1 = rho_mm1 / (mu * (1 - rho_mm1));  % Среднее время ожидания в очереди
W_s_mm1 = 1 / (mu * (1 - rho_mm1));  % Среднее время пребывания в системе

fprintf('M/M/1:\n Коэффициент загрузки: %.4f\n Среднее число заявок в системе: %.4f\n Среднее время в очереди: %.4f\n Среднее время пребывания в системе: %.4f\n\n', ...
    rho_mm1, L_mm1, W_q_mm1, W_s_mm1);

% M/G/1 - формула Поллачека-Кинчина
L_mg1 = mean(cum_tau_mg1 - cum_nu_mg1);  % Среднее число заявок в системе
sigma2_nu_mg1 = var(nu_mg1);  % Дисперсия времени обслуживания
W_q_mg1 = (lambda * sigma2_nu_mg1 + rho_mg1^2) / (2 * (1 - rho_mg1));  % Среднее время в очереди по формуле Поллачека-Кинчина
W_s_mg1 = W_q_mg1 + 1 / mu;  % Среднее время пребывания в системе

fprintf('M/G/1:\n Коэффициент загрузки: %.4f\n Среднее число заявок в системе: %.4f\n Среднее время в очереди: %.4f\n Среднее время пребывания в системе: %.4f\n\n', ...
    rho_mg1, L_mg1, W_q_mg1, W_s_mg1);

% G/M/1
L_gm1 = mean(cum_tau_gm1 - cum_nu_gm1);  % Среднее число заявок в системе
W_q_gm1 = L_gm1 / lambda;  % Среднее время в очереди
W_s_gm1 = W_q_gm1 + 1 / mu;  % Среднее время пребывания в системе

fprintf('G/M/1:\n Коэффициент загрузки: %.4f\n Среднее число заявок в системе: %.4f\n Среднее время в очереди: %.4f\n Среднее время пребывания в системе: %.4f\n\n', ...
    rho_gm1, L_gm1, W_q_gm1, W_s_gm1);

% G/G/1
L_gg1 = mean(cum_tau_gg1 - cum_nu_gg1);  % Среднее число заявок в системе
W_q_gg1 = L_gg1 / lambda;  % Среднее время в очереди
W_s_gg1 = W_q_gg1 + 1 / mean(nu_gg1);  % Среднее время пребывания в системе

fprintf('G/G/1:\n Коэффициент загрузки: %.4f\n Среднее число заявок в системе: %.4f\n Среднее время в очереди: %.4f\n Среднее время пребывания в системе: %.4f\n\n', ...
    rho_gg1, L_gg1, W_q_gg1, W_s_gg1);
