function bits = encoder(text)
    chars = [char('A':'Z'), char('a':'z'), char('0':'9'), ' ', '.', '!', '?'];
    text = char(text);
    bits = [];
    for i = 1:length(text)
        idx = find(chars == text(i), 1) - 1;
        binStr = dec2bin(idx, 7);
        binVec = (binStr == '1');
        bits = [bits, binVec];
    end
    bits = double(bits);
end