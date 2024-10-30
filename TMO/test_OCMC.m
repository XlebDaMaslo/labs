function sequence = gen_gold_seq(num1, num2)
    x = dec2bin(num1) - '0';
    while length(x) < 5
        x = [0 x];
    end
    
    y = dec2bin(num2) - '0';
    while length(y) < 5
        y = [0 y];
    end
    
    sequence = [];

    if mod(num1, 2) == 0
        for i = 1:(2^length(x) - 1)
            out = xor(x(5), y(5));
            x = [xor(x(3), x(5)) x(1:end-1)];
            y = [xor(y(3), y(5)) y(1:end-1)];
            sequence = [sequence out];
        end
    else
        for i = 1:(2^length(x) - 1)
            out = xor(x(5), y(5));
            x = [xor(x(4), x(5)) x(1:end-1)];
            y = [xor(y(2), y(5)) y(1:end-1)];
            sequence = [sequence out];
        end
    end
end

function autocorr(seq)
    n = length(seq);
    fprintf('%s', 'Сдвиг');
    for i = 1:n
        fprintf(' | %d', i);
    end
    fprintf(' | Автокорреляция\n');

    new_seq = seq;
    lags = 0:n;
    correlations = zeros(1, n + 1);

    for i = lags
        compare = seq == new_seq;
        count1 = sum(compare);
        count0 = n - count1;
        correlation = (1 / (2^5 - 1)) * (count1 - count0);
        correlations(i + 1) = correlation;

        fprintf('%d       ', i);
        fprintf(' | %d', compare);
        fprintf(' | %.6f\n', correlation);

        new_seq = [new_seq(end) new_seq(1:end-1)];
    end

    figure;
    plot(lags, correlations);
    title('Автокорреляция последовательности Голда');
    xlabel('Задержка (lag)');
    ylabel('Автокорреляция');
    grid on;
end

function corr_print(seq1, seq2)
    n = length(seq1);
    
    fprintf('%s', '\nСдвиг');
    for i = 1:n
        fprintf(' | %d', i);
    end
    fprintf(' | Корреляция | Норм. корреляция\n');
    
    for i = 0:n
        compare = seq1 == seq2;
        corr = dot(seq1, seq2);
        n_corr = dot(seq1, seq2) / (norm(seq1) * norm(seq2));
        
        fprintf('%d       ', i);
        fprintf(' | %d', compare);
        fprintf(' | %8.6f | %8.6f\n', corr, n_corr);
        
        seq2 = [seq2(end) seq2(1:end-1)];
    end
end

number_st = 10;
sequence1 = gen_gold_seq(number_st, number_st + 7);
disp(sequence1);

count1 = sum(sequence1 == 1);
count0 = sum(sequence1 == 0);
disp([count0, count1]);

autocorr(sequence1);

sequence2 = gen_gold_seq(number_st + 1, (number_st + 7) - 5);
corr_print(sequence1, sequence2);
