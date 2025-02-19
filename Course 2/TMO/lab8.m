%% Основные параметры
lambda = 1; % интенсивность потока заявок (например, 1 заявка в единицу времени)
x_mean = 5; % среднее время обслуживания (например, 5 единиц времени)
mu = 1 / x_mean; % интенсивность обслуживания
rho_vals = linspace(0.01, 0.99, 100); % коэффициент загрузки (0 < ρ < 1)
C2b_vals = 0:10:100; % нормированная дисперсия обслуживания для M/G/1

%% Общая функция для проверки значений rho
function check_rho(rho)
    if rho >= 1
        warning('Значение \rho слишком близко к 1. Пропускаем расчет.');
    end
end

%% Функция для расчета характеристик для M/G/1
function [Nq, N, W, T] = MG1_calculations(rho_vals, x_mean, C2b_vals)
    Nq = zeros(length(C2b_vals), length(rho_vals));
    N = zeros(length(C2b_vals), length(rho_vals));
    W = zeros(length(C2b_vals), length(rho_vals));
    T = zeros(length(C2b_vals), length(rho_vals));

    for i = 1:length(C2b_vals)
        C2b = C2b_vals(i);
        for j = 1:length(rho_vals)
            rho = rho_vals(j);
            check_rho(rho);  % Проверка rho
            % Вычисления для M/G/1
            Nq(i,j) = (rho^2 * (1 + C2b)) / (2 * (1 - rho));
            N(i,j) = rho + Nq(i,j);
            W(i,j) = (rho * x_mean * (1 + C2b)) / (2 * (1 - rho));
            T(i,j) = x_mean + W(i,j);
        end
    end
end

%% Функция для расчета характеристик для M/D/1
function [Nq, N, W, T] = MD1_calculations(rho_vals, x_mean)
    Nq = zeros(1, length(rho_vals));
    N = zeros(1, length(rho_vals));
    W = zeros(1, length(rho_vals));
    T = zeros(1, length(rho_vals));
    
    for j = 1:length(rho_vals)
        rho = rho_vals(j);
        check_rho(rho);  % Проверка rho
        % Вычисления для M/D/1
        Nq(j) = rho^2 / (2 * (1 - rho));
        N(j) = Nq(j) + rho;
        W(j) = rho * x_mean / (2 * (1 - rho));
        T(j) = W(j) + x_mean;
    end
end

%% Функция для расчета характеристик для M/M/1
function [Nq, N, W, T] = MM1_calculations(rho_vals, x_mean)
    Nq = zeros(1, length(rho_vals));
    N = zeros(1, length(rho_vals));
    W = zeros(1, length(rho_vals));
    T = zeros(1, length(rho_vals));
    
    for j = 1:length(rho_vals)
        rho = rho_vals(j);
        check_rho(rho);  % Проверка rho
        % Вычисления для M/M/1
        Nq(j) = rho^2 / (1 - rho);
        N(j) = rho / (1 - rho);
        W(j) = rho * x_mean / (1 - rho);
        T(j) = W(j) + x_mean;
    end
end

%% Функция для построения графиков для M/G/1
function plot_results_MG1(rho_vals, Nq, N, W, T, C2b_vals)
    figure;
    subplot(2,2,1);
    for i = 1:length(C2b_vals)
        plot(rho_vals, Nq(i,:)); hold on;
    end
    title('N_q для M/G/1');
    xlabel('\rho'); ylabel('N_q');
    legend(arrayfun(@(x) ['C2b = ', num2str(x)], C2b_vals, 'UniformOutput', false));
    
    subplot(2,2,2);
    for i = 1:length(C2b_vals)
        plot(rho_vals, N(i,:)); hold on;
    end
    title('N для M/G/1');
    xlabel('\rho'); ylabel('N');
    legend(arrayfun(@(x) ['C2b = ', num2str(x)], C2b_vals, 'UniformOutput', false));
    
    subplot(2,2,3);
    for i = 1:length(C2b_vals)
        plot(rho_vals, W(i,:)); hold on;
    end
    title('W для M/G/1');
    xlabel('\rho'); ylabel('W');
    legend(arrayfun(@(x) ['C2b = ', num2str(x)], C2b_vals, 'UniformOutput', false));
    
    subplot(2,2,4);
    for i = 1:length(C2b_vals)
        plot(rho_vals, T(i,:)); hold on;
    end
    title('T для M/G/1');
    xlabel('\rho'); ylabel('T');
    legend(arrayfun(@(x) ['C2b = ', num2str(x)], C2b_vals, 'UniformOutput', false));
end

%% Функция для построения графиков для других систем
function plot_results(rho_vals, Nq, N, W, T, system_name)
    figure;
    subplot(2,2,1);
    plot(rho_vals, Nq);
    title(['N_q для ', system_name]);
    xlabel('\rho'); ylabel('N_q');
    
    subplot(2,2,2);
    plot(rho_vals, N);
    title(['N для ', system_name]);
    xlabel('\rho'); ylabel('N');
    
    subplot(2,2,3);
    plot(rho_vals, W);
    title(['W для ', system_name]);
    xlabel('\rho'); ylabel('W');
    
    subplot(2,2,4);
    plot(rho_vals, T);
    title(['T для ', system_name]);
    xlabel('\rho'); ylabel('T');
end

%% Основная программа
% Расчеты для M/G/1
[Nq_MG1, N_MG1, W_MG1, T_MG1] = MG1_calculations(rho_vals, x_mean, C2b_vals);
% Расчеты для M/D/1
[Nq_MD1, N_MD1, W_MD1, T_MD1] = MD1_calculations(rho_vals, x_mean);
% Расчеты для M/M/1
[Nq_MM1, N_MM1, W_MM1, T_MM1] = MM1_calculations(rho_vals, x_mean);

%% Построение графиков
% Графики для M/G/1 с разными C2b на одном наборе графиков
plot_results_MG1(rho_vals, Nq_MG1, N_MG1, W_MG1, T_MG1, C2b_vals);

% Графики для M/D/1
plot_results(rho_vals, Nq_MD1, N_MD1, W_MD1, T_MD1, 'M/D/1');

% Графики для M/M/1
plot_results(rho_vals, Nq_MM1, N_MM1, W_MM1, T_MM1, 'M/M/1');
