n = 8;
b = randn(10, 1);
x = [];
num = [];
count = 10;

while n <= 4096
    t_time = 0;
    for k = 1:count
        tic;
        a = randn(n, 1);
        [c, lags] = xcorr(a, b);
        [~, idx] = max(c);
        mn = lags(idx);
        t = toc;
        t_time = t_time + t;
    end
    avg_time = t_time / count;
    num(end + 1) = n;
    x(end + 1) = avg_time;
    n = n + 4;
end

plot(num, x);
xlabel('Размер последовательности');
ylabel('Время выполнения');