% Задаем параметры
lambda = 1; % интенсивность потока заявок (например, 1 заявка в единицу времени)
x_mean = 5; % среднее время обслуживания (например, 5 единиц времени)
mu = 1 / x_mean; % интенсивность обслуживания

rho_vals = linspace(0.01, 0.99, 100); % Коэффициент загрузки (0 < ρ < 1)
C2b_vals = 0:10:100; % Нормированная дисперсия обслуживания для M/G/1

% Подготовка переменных для хранения результатов
Nq_MG1 = zeros(length(C2b_vals), length(rho_vals));
N_MG1 = zeros(length(C2b_vals), length(rho_vals));
W_MG1 = zeros(length(C2b_vals), length(rho_vals));
T_MG1 = zeros(length(C2b_vals), length(rho_vals));

Nq_MD1 = zeros(1, length(rho_vals));
N_MD1 = zeros(1, length(rho_vals));
W_MD1 = zeros(1, length(rho_vals));
T_MD1 = zeros(1, length(rho_vals));

Nq_MM1 = zeros(1, length(rho_vals));
N_MM1 = zeros(1, length(rho_vals));
W_MM1 = zeros(1, length(rho_vals));
T_MM1 = zeros(1, length(rho_vals));

%% 2. Характеристики для M/G/1 (формулы 7.1-7.4)
for i = 1:length(C2b_vals)
    C2b = C2b_vals(i);
    for j = 1:length(rho_vals)
        rho = rho_vals(j);
        
        % Средняя длина очереди (формула 7.1)
        Nq_MG1(i,j) = (rho^2 * (1 + C2b)) / (2 * (1 - rho));
        
        % Среднее число заявок в СМО (формула 7.2)
        N_MG1(i,j) = rho + Nq_MG1(i,j);
        
        % Среднее время ожидания (формула 7.3)
        W_MG1(i,j) = (rho * x_mean * (1 + C2b)) / (2 * (1 - rho));
        
        % Среднее время пребывания заявки в системе (формула 7.4)
        T_MG1(i,j) = x_mean + W_MG1(i,j);
    end
end

%% 3. Характеристики для M/D/1 (формулы 7.5-7.8)
for j = 1:length(rho_vals)
    rho = rho_vals(j);
    
    % Средняя длина очереди (формула 7.5)
    Nq_MD1(j) = rho^2 / (2 * (1 - rho));
    
    % Среднее число заявок в СМО (формула 7.6)
    N_MD1(j) = Nq_MD1(j) + rho;
    
    % Среднее время ожидания (формула 7.7)
    W_MD1(j) = rho * x_mean / (2 * (1 - rho));
    
    % Среднее время пребывания заявки в системе (формула 7.8)
    T_MD1(j) = W_MD1(j) + x_mean;
end

%% 4. Характеристики для M/M/1 (формулы 7.9-7.12)
for j = 1:length(rho_vals)
    rho = rho_vals(j);
    
    % Средняя длина очереди (формула 7.9)
    Nq_MM1(j) = rho^2 / (1 - rho);
    
    % Среднее число заявок в СМО (формула 7.10)
    N_MM1(j) = rho / (1 - rho);
    
    % Среднее время ожидания (формула 7.11)
    W_MM1(j) = rho * x_mean / (1 - rho);
    
    % Среднее время пребывания заявки в системе (формула 7.12)
    T_MM1(j) = W_MM1(j) + x_mean;
end

%% 5. Построение графиков
% M/G/1
figure;
for i = 1:length(C2b_vals)
    subplot(2,2,1);
    plot(rho_vals, Nq_MG1(i,:)); hold on;
    title('N_q для M/G/1');
    xlabel('\rho'); ylabel('N_q');
    
    subplot(2,2,2);
    plot(rho_vals, N_MG1(i,:)); hold on;
    title('N для M/G/1');
    xlabel('\rho'); ylabel('N');
    
    subplot(2,2,3);
    plot(rho_vals, W_MG1(i,:)); hold on;
    title('W для M/G/1');
    xlabel('\rho'); ylabel('W');
    
    subplot(2,2,4);
    plot(rho_vals, T_MG1(i,:)); hold on;
    title('T для M/G/1');
    xlabel('\rho'); ylabel('T');
end

% M/D/1
figure;
subplot(2,2,1);
plot(rho_vals, Nq_MD1);
title('N_q для M/D/1');
xlabel('\rho'); ylabel('N_q');

subplot(2,2,2);
plot(rho_vals, N_MD1);
title('N для M/D/1');
xlabel('\rho'); ylabel('N');

subplot(2,2,3);
plot(rho_vals, W_MD1);
title('W для M/D/1');
xlabel('\rho'); ylabel('W');

subplot(2,2,4);
plot(rho_vals, T_MD1);
title('T для M/D/1');
xlabel('\rho'); ylabel('T');

% M/M/1
figure;
subplot(2,2,1);
plot(rho_vals, Nq_MM1);
title('N_q для M/M/1');
xlabel('\rho'); ylabel('N_q');

subplot(2,2,2);
plot(rho_vals, N_MM1);
title('N для M/M/1');
xlabel('\rho'); ylabel('N');

subplot(2,2,3);
plot(rho_vals, W_MM1);
title('W для M/M/1');
xlabel('\rho'); ylabel('W');

subplot(2,2,4);
plot(rho_vals, T_MM1);
title('T для M/M/1');
xlabel('\rho'); ylabel('T');
