function X = discrete_random_var(n)
    X = zeros(n, 1);
    for i = 1:n
        z = rand();
        S = z;
        k = 0;
        while S >= 2^(-k-1)
            S = S - 2^(-k-1);
            k = k + 1;
        end
        X(i) = k - 1;
    end
end

N_list = [50, 200, 1000];
alpha_list = [0.1, 0.05, 0.01];

results_disc = table();

for i = 1:length(N_list)
    N = N_list(i);
    X = discrete_random_var(N);
    
    mean_X = mean(X);
    variance_X = var(X);
    stddev_X = std(X);
    
    for j = 1:length(alpha_list)
        alpha = alpha_list(j);
        
        z = norminv(1 - alpha / 2);
        error = z * (stddev_X / sqrt(N));
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
                                           'CI_Mean_L', 'CI_Mean_R', ...
                                           'CI_Var_L', 'CI_Var_R'});
        results_disc = [results_disc; new_row];
    end
end

filename = 'results2.xlsx';
writetable(results_disc, filename);

x_range_disc = 0:30; %первые 30 значений

figure;

for i = 1:length(N_list)
    N = N_list(i);
    X = discrete_random_var(N);
    
    k = ceil(1 + 3.2 * log(N));

    subplot(3, 1, i);
    h = histogram(X, k, 'Normalization', 'probability');
    hold on;
    
    theoretical_probs = 2 .^ (-x_range_disc - 1);
    bar(x_range_disc, theoretical_probs, 'r', 'LineWidth', 2);

    ylim([0 0.6]);
    uistack(h, 'top');
    
    title(['Гистограмма и теоретическое распределение для N = ', num2str(N)]);
    xlabel('Значение');
    ylabel('Вероятность');
    legend('Эмпирическое распределение', 'Теоретическое распределение');
    hold off;
end

theoretical_fpd_disc = cumsum(2 .^ (-x_range_disc - 1));
theoretical_pd_disc = 2 .^ (-x_range_disc - 1);

figure;
plot(x_range_disc, theoretical_pd_disc, 'LineWidth', 2);
hold on;
plot(x_range_disc, theoretical_fpd_disc, 'LineWidth', 2);
hold off;

title('Теоретическая функция распределения и плотность вероятности');
xlabel('Значение');
ylabel('Вероятность');
legend('Функция распределения F(x)', 'Плотность вероятности f(x)');
grid on;
