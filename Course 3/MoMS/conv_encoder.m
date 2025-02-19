function encoded_bits = conv_encoder(input_bits)
    trellis = poly2trellis(7, [133, 171]);
    
    encoded_bits = convenc(input_bits, trellis);
end