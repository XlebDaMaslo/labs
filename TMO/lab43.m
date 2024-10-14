L = 15;
T = zeros(L);

for i = 1:L
    j = randperm(L, 3);
    T(i, j) = 1;
    T(j, i) = 1;

end

G = graph(T);

plot(G)