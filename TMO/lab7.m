%% 3. Установить значения входных параметров lambda и mu
lambda = 2;  % Интенсивность входного потока
mu = 3;      % Интенсивность обслуживания

% Параметры Вейбулловского распределения
k_weibull = 1.5;
theta_weibull = 1 / mu;

if lambda >= mu
error('Система нестационарна');
end

N = 1000000; % Количество заявок
t = linspace(0, 100, N);

%% 4. Передать в программу входные параметры, сформированные в лабораторной работе №5
% M/M/1 (экспоненциальные распределения для поступления и обслуживания)
tau_mm1 = exprnd(1/lambda, 1, N); % время между поступлениями
nu_mm1 = exprnd(1/mu, 1, N);      % время обслуживания

% M/G/1 (экспоненциальные поступления, Вейбулловское обслуживание)
tau_mg1 = exprnd(1/lambda, 1, N);
nu_mg1 = wblrnd(theta_weibull, k_weibull, 1, N);

% G/M/1 (Вейбулловские поступления, экспоненциальное обслуживание)
tau_gm1 = wblrnd(1/lambda, k_weibull, 1, N);
nu_gm1 = exprnd(1/mu, 1, N);

% G/G/1 (Вейбулловские поступления и Вейбулловское обслуживание)
tau_gg1 = wblrnd(1/lambda, k_weibull, 1, N);
nu_gg1 = wblrnd(theta_weibull, k_weibull, 1, N);

%% 5. Получить следующие зависимости для четырех типов СМО
% 6. Построить зависимости для каждого типа СМО на отдельном графике и подписать каждый график.
figure;

yl = N / 5;
% M/M/1
subplot(2,2,1);
plot(t, cumsum(tau_mm1) - cumsum(nu_mm1));
title('M/M/1');
xlabel('Время');
ylabel('Число заявок');
ylim([0 yl]);

% M/G/1
subplot(2,2,2);
plot(t, cumsum(tau_mg1) - cumsum(nu_mg1));
title('M/G/1');
xlabel('Время');
ylabel('Число заявок');
ylim([0 yl]);

% G/M/1
subplot(2,2,3);
plot(t, cumsum(tau_gm1) - cumsum(nu_gm1));
title('G/M/1');
xlabel('Время');
ylabel('Число заявок');
ylim([0 yl]);

% G/G/1
subplot(2,2,4);
plot(t, cumsum(tau_gg1) - cumsum(nu_gg1));
title('G/G/1');
xlabel('Время');
ylabel('Число заявок');
ylim([0 yl]);

%% 7. Рассчитать следующие статистические характеристики для каждого типа СМО:
rho_mm1 = lambda / mu;
rho_mg1 = lambda / mu;
rho_gm1 = lambda / mu;
rho_gg1 = lambda / mu;

L_mm1 = rho_mm1 / (1 - rho_mm1); % L = ρ / (1 - ρ)
W_q_mm1 = rho_mm1 / (mu * (1 - rho_mm1)); % W_q = ρ / (μ * (1 - ρ))
W_s_mm1 = 1 / (mu * (1 - rho_mm1)); % Среднее время пребывания в системе

fprintf('M/M/1:\n Коэффициент загрузки: %.4f\n Среднее число заявок в системе: %.4f\n Среднее время в очереди: %.4f\n Среднее время пребывания в системе: %.4f\n\n', rho_mm1, L_mm1, W_q_mm1, W_s_mm1);

L_mg1 = mean(cumsum(tau_mg1) - cumsum(nu_mg1)); % Среднее число заявок в системе M/G/1
L_gm1 = mean(cumsum(tau_gm1) - cumsum(nu_gm1)); % Среднее число заявок в системе G/M/1
L_gg1 = mean(cumsum(tau_gg1) - cumsum(nu_gg1)); % Среднее число заявок в системе G/G/1

W_q_mg1 = L_mg1 / lambda;  % Среднее время в очереди M/G/1
W_q_gm1 = L_gm1 / lambda;  % Среднее время в очереди G/M/1
W_q_gg1 = L_gg1 / lambda;  % Среднее время в очереди G/G/1

fprintf('M/G/1:\n Коэффициент загрузки: %.4f\n Среднее число заявок в системе: %.4f\n Среднее время в очереди: %.4f\n\n', rho_mg1, L_mg1, W_q_mg1);

fprintf('G/M/1:\n Коэффициент загрузки: %.4f\n Среднее число заявок в системе: %.4f\n Среднее время в очереди: %.4f\n\n', rho_gm1, L_gm1, W_q_gm1);

fprintf('G/G/1:\n Коэффициент загрузки: %.4f\n Среднее число заявок в системе: %.4f\n Среднее время в очереди: %.4f\n\n', rho_gg1, L_gg1, W_q_gg1);