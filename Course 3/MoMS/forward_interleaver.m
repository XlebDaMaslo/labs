function interleaved_bits = forward_interleaver(bits)
    n = length(bits);
    rng(n);
    
    perm_vector = randperm(n);
    interleaved_bits = bits(perm_vector);
end