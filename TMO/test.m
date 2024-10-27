mu = 3;
rho_values = 0:0.01:0.99;
Cb_squared_values = [0, 1, 10, 20, 30:10:100]; % Значения нормированной дисперсии

%% 3
function Nq = Nq_MG1(rho, Cb_squared) % 7.1
    Nq = rho^2 * (1 + Cb_squared) / (2 * (1 - rho));
end

function N = N_MG1(rho, Cb_squared) % 7.2
    N = Nq_MG1(rho, Cb_squared) + rho;
end

function Wq = Wq_MG1(rho, Cb_squared, mu) % 7.3
    x_mean = 1 / mu;
    Wq = rho * x_mean * (1 + Cb_squared) / (2 * (1 - rho));
end

function W = W_MG1(rho, Cb_squared, mu) % 7.4
    x_mean = 1 / mu;
    W = Wq_MG1(rho, Cb_squared, mu) + x_mean;
end

%% 4
function Nq = Nq_MD1(rho) % 7.5
    Nq = rho^2 / (2 * (1 - rho));
end

function Wq = Wq_MD1(rho, mu) % 7.7
    x_mean = 1 / mu;
    Wq = (rho * x_mean) / (2 * (1 - rho));
end

function N = N_MD1(rho) % 7.6
    N = Nq_MD1(rho) + rho;
end

function W = W_MD1(rho, mu) % 7.8
    x_mean = 1 / mu;
    W = (x_mean * (2 - rho)) / (2 * (1 - rho));
end

%% 5
function Nq = Nq_MM1(rho) % 7.9
    Nq = rho^2 / (1 - rho);
end

function Wq = Wq_MM1(rho, mu) % 7.11
    x_mean = 1 / mu;
    Wq = (rho * x_mean) / (1 - rho);
end

function N = N_MM1(rho) % 7.10
    N = rho / (1 - rho);
end

function W = W_MM1(rho, mu) % 7.12
    x_mean = 1 / mu;
    W = x_mean / (1 - rho);
end

%% 2
for i = 1:length(rho_values)
    rho = rho_values(i); % Коэффициент использования системы
    for j = 1:length(Cb_squared_values)
        Cb_squared = Cb_squared_values(j);
        
        Nq_MG1_values(i, j) = Nq_MG1(rho, Cb_squared);
        Wq_MG1_values(i, j) = Wq_MG1(rho, Cb_squared, mu);
        N_MG1_values(i, j) = N_MG1(rho, Cb_squared);
        W_MG1_values(i, j) = W_MG1(rho, Cb_squared, mu);
        
        Nq_MD1_values(i) = Nq_MD1(rho);
        Wq_MD1_values(i) = Wq_MD1(rho, mu);
        N_MD1_values(i) = N_MD1(rho);
        W_MD1_values(i) = W_MD1(rho, mu);
        
        Nq_MM1_values(i) = Nq_MM1(rho);
        Wq_MM1_values(i) = Wq_MM1(rho, mu);
        N_MM1_values(i) = N_MM1(rho);
        W_MM1_values(i) = W_MM1(rho, mu);
    end
end

%% 6
% M/G/1
figure;
sgtitle('M/G/1');

subplot(2, 2, 1);
plot(rho_values, Nq_MG1_values);
xlabel('Коэффициент загрузки');
ylabel('Средняя длина очереди');
title('Средняя длина очереди');
legend(string(Cb_squared_values), 'Location', 'northwest');
xlim([0.7 1]);

subplot(2, 2, 2);
plot(rho_values, Wq_MG1_values);
xlabel('Коэффициент загрузки');
ylabel('Среднее время ожидания в очереди');
title('Среднее время ожидания в очереди');
legend(string(Cb_squared_values), 'Location', 'northwest');
xlim([0.7 1]);

subplot(2, 2, 3);
plot(rho_values, N_MG1_values);
xlabel('Коэффициент загрузки');
ylabel('Среднее число заявок в системе');
title('Среднее число заявок в системе');
legend(string(Cb_squared_values), 'Location', 'northwest');
xlim([0.7 1]);

subplot(2, 2, 4);
plot(rho_values, W_MG1_values);
xlabel('Коэффициент загрузки');
ylabel('Среднее время пребывания заявки в системе');
title('Среднее время пребывания заявки в системе');
legend(string(Cb_squared_values), 'Location', 'northwest');
xlim([0.7 1]);


% M/D/1
figure;
sgtitle('M/D/1');

subplot(2, 2, 1);
plot(rho_values, Nq_MD1_values, '-');
xlabel('Коэффициент загрузки');
ylabel('Средняя длина очереди');
title('Средняя длина очереди');
xlim([0.7 1]);

subplot(2, 2, 2);
plot(rho_values, Wq_MD1_values, '-');
xlabel('Коэффициент загрузки');
ylabel('Среднее время ожидания в очереди');
title('Среднее время ожидания в очереди');
xlim([0.7 1]);

subplot(2, 2, 3);
plot(rho_values, N_MD1_values, '-');
xlabel('Коэффициент загрузки');
ylabel('Среднее число заявок в системе');
title('Среднее число заявок в системе');
xlim([0.7 1]);

subplot(2, 2, 4);
plot(rho_values, W_MD1_values, '-');
xlabel('Коэффициент загрузки');
ylabel('Среднее время пребывания заявки в системе');
title('Среднее время пребывания заявки в системе');
xlim([0.7 1]);


% M/M/1
figure;
sgtitle('M/M/1');

subplot(2, 2, 1);
plot(rho_values, Nq_MM1_values, '-');
xlabel('Коэффициент загрузки');
ylabel('Средняя длина очереди');
title('Средняя длина очереди');
xlim([0.7 1]);

subplot(2, 2, 2);
plot(rho_values, Wq_MM1_values, '-');
xlabel('Коэффициент загрузки');
ylabel('Среднее время ожидания в очереди');
title('Среднее время ожидания в очереди');
xlim([0.7 1]);

subplot(2, 2, 3);
plot(rho_values, N_MM1_values, '-');
xlabel('Коэффициент загрузки');
ylabel('Среднее число заявок в системе');
title('Среднее число заявок в системе');
xlim([0.7 1]);

subplot(2, 2, 4);
plot(rho_values, W_MM1_values, '-');
xlabel('Коэффициент загрузки');
ylabel('Среднее время пребывания заявки в системе');
title('Среднее время пребывания заявки в системе');
xlim([0.7 1]);