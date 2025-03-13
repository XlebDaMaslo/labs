function decoded_bits = viterbi_decoder(encoded_bits)
    trellis = poly2trellis(7, [133, 171]);
    
    traceback_depth = length(encoded_bits) / 2;
    
    decoded_bits = vitdec(encoded_bits, trellis, traceback_depth, 'trunc', 'hard');
end