function bits = qpsk_demodulate(symbols)
    bits = zeros(1, 2 * length(symbols));
    
    %modulation_table = [0.707 + 0.707i; 0.707 - 0.707i; -0.707 + 0.707i; -0.707 - 0.707i];
    modulation_table = zeros(4, 1);
    for i = 0:3
        phase = (2 * pi * i / 4) + pi/4;
        modulation_table(i+1) = cos(phase) + 1i * sin(phase);
    end
    
    for k = 1:length(symbols)
        [~, index] = min(abs(symbols(k) - modulation_table));
        bit_pair = de2bi(index-1, 2, 'left-msb');
        bits(2*k-1:2*k) = bit_pair;
    end

    for k = 1:length(symbols)
        r_p = real(symbols(k));
        i_p = imag(symbols(k));

        if r_p >= 0 && i_p >= 0
            pair = [0 , 0];
        elseif r_p < 0 && i_p >= 0
            pair = [0 , 1];
        elseif r_p < 0 && i_p < 0
            pair = [1 , 1];
        else
            pair = [1 , 0];
        end
        bits(2*k-1:2*k) = pair;
    end
end