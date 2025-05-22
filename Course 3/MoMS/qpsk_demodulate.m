function bits = qpsk_demodulate(symbols)
    bits = zeros(1, 2 * length(symbols));

    modulation_table = [0.707 + 0.707i;  % 00
                        0.707 - 0.707i;  % 01
                       -0.707 + 0.707i;  % 10
                       -0.707 - 0.707i]; % 11

    if isempty(symbols)
        bits = [];
        return;
    end

    for k = 1:length(symbols)
        [~, index] = min(abs(symbols(k) - modulation_table));
        bit_pair = de2bi(index-1, 2, 'left-msb');
        bits(2*k-1:2*k) = bit_pair;
    end
end