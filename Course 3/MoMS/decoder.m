function text = decoder(bits)
    chars = [char('A':'Z'), char('a':'z'), char('0':'9'), ' ', '.', '!', '?'];
    n = length(bits);
    n_groups = floor(n / 7);
    bits = bits(1 : 7*n_groups);
    if isempty(bits)
        text = '';
        return;
    end
    bitMatrix = reshape(bits, 7, [])';
    text = [];
    for i = 1:n_groups
        binVec = bitMatrix(i, :);
        binStr = char('0' + binVec);
        idx = bin2dec(binStr);
        text(i) = chars(idx + 1);
    end
    text = char(text);
end