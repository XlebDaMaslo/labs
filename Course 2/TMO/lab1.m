N_list = [50, 200, 1000];
alpha_list = [0.1, 0.05, 0.01];

results = table(); %для сохранения данных в таблицу

for i = 1:length(N_list)
    N = N_list(i);
    z = rand(N, 1);
    X = sqrt(1 ./ (1 - z));
    
    mean_X = mean(X);
    variance_X = var(X);
    stddev_X = std(X);
    
    for j = 1:length(alpha_list)
        alpha = alpha_list(j);
        
        t = norminv(1 - alpha / 2);
        error = t * (stddev_X / sqrt(N));
        interval_mean_l = mean_X - error;
        interval_mean_r = mean_X + error;
        
        chi2_l = chi2inv(alpha / 2, N - 1);
        chi2_r = chi2inv(1 - alpha / 2, N - 1);
        interval_var_l = (N - 1) * variance_X / chi2_r;
        interval_var_r = (N - 1) * variance_X / chi2_l;
        
        new_row = table(N, alpha, mean_X, variance_X, stddev_X, ...
                        interval_mean_l, interval_mean_r, ...
                        interval_var_l, interval_var_r, ...
                        'VariableNames', {'N', 'Alpha', 'Mean', 'Variance', 'SKO', ...
                                           'Int_Mean_L', 'Int_Mean_R', ...
                                           'Int_Var_L', 'Int_Var_R'});
        results = [results; new_row];
    end
end

filename = 'results1.xlsx';
writetable(results, filename);

x_range = linspace(1, 10, 1000); %диапазон x для теоретической плотности

figure;

for i = 1:length(N_list)
    N = N_list(i);
    z = rand(N, 1);
    X = sqrt(1 ./ (1 - z));
    
    k = ceil(1 + 3.2 * log(N));
    
    subplot(3, 1, i);
    h = histogram(X, k, 'Normalization', 'pdf');
    hold on;
    
    theoretical_pd = 2 ./ (x_range.^3);
    plot(x_range, theoretical_pd, 'r', 'LineWidth', 2);
    
    ylim([0 2]);
    xlim([0 10]);
    title(['Гистограмма и теоретическая плотность для N = ', num2str(N)]);
    xlabel('Значение');
    ylabel('Плотность вероятности');
    legend('Гистограмма', 'Теоретическая плотность');
    hold off;
end

theoretical_pd = 2 ./ (x_range.^3);

theoretical_fpd = 1 - 1 ./ (x_range.^2);

figure;
plot(x_range, theoretical_pd, 'r', 'LineWidth', 2);
hold on;
plot(x_range, theoretical_fpd, 'b', 'LineWidth', 2);
hold off;

title('Теоретическая плотность и функция распределения вероятности');
xlabel('Значение');
ylabel('Плотность / Функция распределения');
legend('Плотность вероятности f(x)', 'Функция распределения F(x)');

X = normrnd(0, 1, [1000, 1]);

skewness_X = skewness(X);
kurtosis_X = kurtosis(X);

fprintf('Коэффициент асимметрии: %.4f\n', skewness_X);
fprintf('Коэффициент эксцесса: %.4f\n\n', kurtosis_X);

fprintf('По критерию Колмогорова-Смирнова:\n');
for i = 1:length(alpha_list)
    [h, p] = kstest(X, 'CDF', makedist('Normal', 'mu', 0, 'sigma', 1), 'Alpha', 0.1);
    fprintf('Для уровня значимости %.2f: h = %d, p-value = %.8f\n',1 - alpha_list(i), h, p);
end