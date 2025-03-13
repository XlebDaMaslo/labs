function symbols = qpsk_modulate(bits)
    if mod(length(bits), 2) ~= 0
        bits = [bits, 0]; % Нулевой бит, если количество нечетное
    end
    
    symbols = zeros(1, length(bits)/2);
    
    modulation_table = [0.707 + 0.707i; 0.707 - 0.707i; -0.707 + 0.707i; -0.707 - 0.707i];
    
    for k = 1:2:length(bits)
        bit_pair = [bits(k), bits(k+1)];
        index = bi2de(bit_pair, 'left-msb') + 1;
        symbols((k+1)/2) = modulation_table(index);
    end
end