function main
    number_st = 10; % Номер по списку
    number_st2 = number_st + 7;

    % x^5 + x^4 + 1 первый регистр по схеме
    polynomial1_bin = '00011';

    % x^5 + x^2 + 1 второй регистр по схеме
    polynomial2_bin = '01001';

    sequence1 = gen_gold_seq(number_st, number_st2, polynomial1_bin, polynomial2_bin);
    disp(sequence1);
    fprintf('Count of 1s: %d, Count of 0s: %d\n', sum(sequence1), length(sequence1) - sum(sequence1));
    autocorr(sequence1);

    sequence2 = gen_gold_seq(number_st + 1, (number_st + 7) - 5, polynomial1_bin, polynomial2_bin);
    corr_print(sequence1, sequence2);
end

function isAutocorrelated = autocorr_check(seq)
    n = length(seq);
    first_correlation = [];

    for shift = 1:n-1
        compare = zeros(1, n);
        for j = 1:n
            shifted_index = mod(j - 1 + shift, n) + 1; % MATLAB indexing starts from 1
            if seq(j) == seq(shifted_index)
                compare(j) = 1;
            else
                compare(j) = 0;
            end
        end
        count1 = sum(compare);
        count0 = n - count1;
        correlation = (1/n) * (count1 - count0);

        if isempty(first_correlation)
            first_correlation = correlation;
        elseif correlation ~= first_correlation
            isAutocorrelated = false;
            return;
        end
    end
    isAutocorrelated = true;
end

function sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin)
    n = length(polynomial1_bin);
    init_poly1 = polynomial1_bin;
    init_poly2 = polynomial2_bin;

    x = dec2bin(initial_state1, n) - '0'; % Convert to binary array
    y = dec2bin(initial_state2, n) - '0'; % Convert to binary array

    polynomial1 = find(polynomial1_bin == '1') - 1; % Find indices (0-based)
    polynomial2 = find(polynomial2_bin == '1') - 1; % Find indices (0-based)

    sequence = zeros(1, (2^n) - 1);

    for i = 1:(2^n - 1)
        out = mod(x(end) + y(end), 2); % XOR operation

        new_x = 0;
        for tap = polynomial1
            new_x = mod(new_x + x(tap + 1), 2); % MATLAB index adjustment
        end
        x = [new_x, x(1:end-1)];

        new_y = 0;
        for tap = polynomial2
            new_y = mod(new_y + y(tap + 1), 2); % MATLAB index adjustment
        end
        y = [new_y, y(1:end-1)];

        sequence(i) = out;
    end

    if ~autocorr_check(sequence)
        if strcmp(polynomial1_bin, '11111')
            polynomial1_bin = init_poly1;
            polynomial2_bin = dec2bin(bin2dec(polynomial2_bin) + 1, length(polynomial2_bin));
            sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin);
        elseif strcmp(polynomial2_bin, '11111')
            polynomial2_bin = init_poly2;
            polynomial1_bin = dec2bin(bin2dec(polynomial1_bin) + 1, length(polynomial1_bin));
            sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin);
        else
            polynomial1_bin = dec2bin(bin2dec(polynomial1_bin) + 1, length(polynomial1_bin));
            sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin);
        end
    end
end

function autocorr(seq)
    fprintf('%-8s %s | %-15s\n', 'Сдвиг', sprintf('%d | ', 1:length(seq)), 'Автокорреляция');
    new_seq = seq;

    for i = 0:length(seq)
        compare = seq == new_seq;
        count1 = sum(compare);
        count0 = length(seq) - count1;
        correlation = (1 / (2^(log2(length(seq) + 1) - 1))) * (count1 - count0);
        bits = sprintf('%d | ', compare);
        fprintf('%-8d %s | %-15f\n', i, bits, correlation);
        new_seq = [new_seq(end), new_seq(1:end-1)];
    end
end

function result = correlation(a, b)
    result = sum(a .* b);
end

function n_corr = normalized_correlation(a, b)
    if isempty(a) || isempty(b) || length(a) ~= length(b)
        n_corr = 0; % Return 0 or some indication of error
        return;
    end
    
    sum_a = sum(a.^2);
    sum_b = sum(b.^2);
    result = correlation(a, b);
    
    if sum_a == 0 || sum_b == 0
        n_corr = 0; % Prevent division by zero
    else
        n_corr = result / sqrt(sum_a * sum_b);
    end
end

function corr_print(seq1, seq2)
    fprintf('%-8s %s | %-12s | %-15s\n', 'Сдвиг', sprintf('%d | ', 1:length(seq1)), 'Корреляция', 'Норм. корреляция');
    
    for i = 0:length(seq1)
        compare = seq1 == seq2;
        corr = correlation(seq1, seq2);
        n_corr = normalized_correlation(seq1, seq2);
        bits = sprintf('%d | ', compare);
        fprintf('%-8d %s | %-12d | %-15f\n', i, bits, corr, n_corr);
        seq2 = [seq2(end), seq2(1:end-1)];
    end
end
