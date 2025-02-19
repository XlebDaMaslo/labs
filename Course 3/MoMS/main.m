%% 1
text = 'Test text!';
bits = encoder(text);
decoded_text = decoder(bits);
disp(decoded_text);

%% 1
input_bits = [0 1 0 1 1 0];

encoded_bits = conv_encoder(input_bits);
%disp(encoded_bits);

decoded_bits = viterbi_decoder(encoded_bits);
disp(decoded_bits);