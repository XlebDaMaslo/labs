%% 1
text = 'Test text!';
bits = encoder(text);
decoded_text = decoder(bits);
disp(decoded_text);

%% 2
input_bits = [0 1 0 1 1 0];

encoded_bits = conv_encoder(input_bits);
%disp(encoded_bits);

decoded_bits = viterbi_decoder(encoded_bits);
%disp(decoded_bits);

%% 3
disp('Исходные биты:');
disp(input_bits);

permuted_bits = forward_interleaver(input_bits);
disp('Перемешанные биты:');
disp(permuted_bits);

original_bits = reverse_interleaver(permuted_bits);
disp('Восстановленные биты:');
disp(original_bits);

if isequal(input_bits, original_bits)
    disp('Восстановление выполнено успешно!');
else
    disp('Ошибка при восстановлении битов.');
end

%% 4
symbols = qpsk_modulate(input_bits);
disp('Модулированные символы:');
disp(symbols);

received_bits = qpsk_demodulate(symbols);
disp('Демодулированные биты:');
disp(received_bits);