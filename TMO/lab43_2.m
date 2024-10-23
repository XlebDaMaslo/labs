function is_stochastic = stochastic(matrix)
    [rows, cols] = size(matrix);
    if rows ~= cols
        error('Матрица не является квадратной');
    end
    
    if any(matrix(:) < 0)
        is_stochastic = false;
        return;
    end
    
    row_sums = sum(matrix, 2);
    if any(abs(row_sums - 1) > 0.001)
        is_stochastic = false;
        return;
    end
    
    is_stochastic = true;
end

function is_ergodic = ergodic(matrix, e)
    [rows, cols] = size(matrix);
    if rows ~= cols
        error('Матрица не является квадратной');
    end

    m = 200;
    initial_dist = [1, zeros(1, rows - 1)];

    for i = 1:rows
        current_dist = initial_dist;
        for j = 1:m
            current_dist = current_dist * matrix;
        end

        if any(current_dist < e)
            is_ergodic = false;
            return;
        end

        initial_dist = circshift(initial_dist, 1);
    end

    is_ergodic = true;
end

e = 0.1;
L = 15;
T = zeros(L);

T(L,L) = 0;

T(1,4) = 0.2;

%T = [0.2 0.8; 0.3 0.7];



%disp(T);
is_stochastic = stochastic(T);
if is_stochastic
    disp('Матрица является стохастической');
else
    disp('Матрица не является стохастической');
end

is_ergodic = ergodic(T, e);
if is_ergodic
    disp('Цепь Маркова является эргодической');
else
    disp('Цепь Маркова не является эргодической');
end

