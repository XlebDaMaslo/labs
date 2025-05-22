function text = decoder(bits)
    chars = [char('A':'Z'), char('a':'z'), char('0':'9'), ' ', '.', '!', '?'];
    error_char = '*';
    
    bits = bits(:)'; 
    if mod(length(bits), 7) ~= 0
        bits = bits(1:end - mod(length(bits), 7));
    end
    
    bit_groups = reshape(bits, 7, [])';
    
    text = repmat(error_char, 1, size(bit_groups, 1));
    for i = 1:size(bit_groups, 1)
        idx = bin2dec( sprintf('%d', bit_groups(i, :)) );
        if idx <= length(chars) - 1
            text(i) = chars(idx + 1);
        end
    end
end