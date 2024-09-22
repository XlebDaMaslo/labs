%1
N = 700;
K = 400;
mu = 14;
sigma = 8;

xi = randn(N,K) * sigma + mu;

mean_ensemble = mean(xi,2);

mean_time = mean(xi,1);

figure;
plot(1:N, mean_ensemble, 'b', 'LineWidth', 2);
hold on;
plot(1:K, mean_time, 'r', 'LineWidth', 1);
xlabel('n');
ylabel('\mu[\xi(n)]');
legend('Среднее по ансамблю', 'Среднее по времени');
title('Средние значения белого шума');
grid on;

%2
n1 = [125, 250, 500];
n2 = [75, 150, 300];

figure;
for i = 1:length(n1)
    subplot(1,3,i);
    plot(xi(n1(i),:), xi(n2(i),:), 'o');
    xlabel(['\xi(', num2str(n1(i)), ')']);
    ylabel(['\xi(', num2str(n2(i)), ')']);
    title(['Диаграмма рассеяния для n1=', num2str(n1(i)), ', n2=', num2str(n2(i))]);
end

correlation = corrcoef(xi(n1(1),:), xi(n2(1),:));
disp(['Выборочная корреляция: ', num2str(correlation(1,2))]);

%3
mu_w = 0;  % Математическое ожидание шума (из таблицы 2.2)
sigma_w = 1; % Стандартное отклонение шума (из таблицы 2.2)

ksi_0 = 0;

n_values = [1, 2, 5, 10, 100];

mu_ksi = mu_w * ones(size(n_values)) + ksi_0;

disp('Теоретические значения mu[ksi(n)] для случайного блуждания:')
for i = 1:length(n_values)
    disp(['n = ', num2str(n_values(i)), ': mu[ksi(n)] = ', num2str(mu_ksi(i))]);
end