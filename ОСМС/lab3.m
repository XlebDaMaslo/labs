f1 = 10;
f2 = f1 + 4;
f3 = f1 * 2 + 1;

t = linspace(0, 1, 1000);
%t = [0:1000-1]/1000;

s1 = cos(2 * pi * f1 * t);
s2 = cos(2 * pi * f2 * t);
s3 = cos(2 * pi * f3 * t);

a_t = 5 * s1 + 4 * s2 + s3;
b_t = 3 * s1 + s3;

corr_ab = sum(a_t .* b_t);
corr_sa = sum(s1 .* a_t);
corr_sb = sum(s1 .* b_t);
norm_corr_ab = corr(a_t', b_t');
norm_corr_sa = corr(s1', a_t');
norm_corr_sb = corr(s1', b_t');

fprintf('Корреляция между a(t) и b(t): %.2f\n', corr_ab);
fprintf('Корреляция между s1(t) и a(t): %.2f\n', corr_sa);
fprintf('Корреляция между s1(t) и b(t): %.2f\n', corr_sb);

fprintf('Нормализованная корреляция между a(t) и b(t): %.2f\n', norm_corr_ab);
fprintf('Нормализованная корреляция между s1(t) и a(t): %.2f\n', norm_corr_sa);
fprintf('Нормализованная корреляция между s1(t) и b(t): %.2f\n', norm_corr_sb);