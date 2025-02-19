% 2
function trajectory = MarkovTrajectory(P, N, s)
    trajectory = zeros(1, N);
    trajectory(1) = s;
    
    for i = 2:N
        next_state = randsample(size(P, 1), 1, true, P(trajectory(i-1), :));
        trajectory(i) = next_state;
    end
end

%P = [0.6 0.2 0.2; 0.3 0.5 0.2; 0.1 0.3 0.6];
L = 10;
T = zeros(L);

for i = 1:L
    j = randperm(L, 3);
    T(i, j) = rand();
    T(j, i) = rand();

end

P = T;
P = P ./ sum(P, 2);

s = 1;

% 3
e = 0.01;

% 4
P_m_ij = zeros(size(P, 1), size(P, 2), 100);
f_m_ij = zeros(size(P, 1), size(P, 2), 100);
M_ij = zeros(size(P));
M_M = zeros(size(P));
D_M = zeros(size(P));

for i = 1:size(P, 1)
    for j = 1:size(P, 2)
        m = 1;
        while true
            P_m_ij(i, j, m) = P(i, j)^m;
            f_m_ij(i, j, m) = P_m_ij(i, j, m) * (1 - P(i, i))^(m-1);

            if f_m_ij(i, j, m) <= e
                M_ij(i, j) = m;
                break;
            end

            M_M(i, j) = M_M(i, j) + m * f_m_ij(i, j, m);
            D_M(i, j) = D_M(i, j) + ((m - M_M(i, j))^2 * f_m_ij(i, j, m));
            m = m + 1;
        end
    end
end

disp('Вероятности пребывания пакета в узле j после m коммутаций:')
disp(P_m_ij)
disp('Вероятности первого перехода пакета в узел j из узла i после m коммутаций:')
disp(f_m_ij)
disp('Длина кратчайшего пути перехода пакета в узел j из узла i:')
disp(M_ij)
disp('Математическое ожидание длины пути перехода пакета в узел j из узла i:')
disp(M_M)
disp('Дисперсия длины пути перехода пакета в узел j из узла i:')
disp(D_M)

% 5
figure;

subplot(2, 1, 1);
plot(1:L, P_m_ij(:, :, m));
xlabel('Номер узла');
ylabel('Вероятность пребывания');
title('Вероятности пребывания пакета в узлах');
grid on;

subplot(2, 1, 2);
plot(1:L, f_m_ij(:, :, m));
xlabel('Номер узла');
ylabel('Вероятность пребывания');
title('Вероятности первого перехода');
grid on;

figure;
imagesc(M_ij);
xlabel('Номер узла j');
ylabel('Номер узла i');
title('Длина кратчайшего пути');
colorbar;

figure;

subplot(2, 1, 1);
plot(1:L, M_M(:, :));
xlabel('Номер узла');
ylabel('Математическое ожидание');
title('Математическое ожидание длины пути');
grid on;

subplot(2, 1, 2);
plot(1:L, D_M(:, :));
xlabel('Номер узла');
ylabel('Дисперсия');
title('Дисперсия длины пути');
grid on;
