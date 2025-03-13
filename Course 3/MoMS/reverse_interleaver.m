function original_bits = reverse_interleaver(permuted_bits)
    n = length(permuted_bits);
    rng(n);
    permutation = randperm(n);
    
    inverse_permutation = zeros(1, n);
    for i = 1:n
        inverse_permutation(permutation(i)) = i;
    end
    
    original_bits = permuted_bits(inverse_permutation);
end
