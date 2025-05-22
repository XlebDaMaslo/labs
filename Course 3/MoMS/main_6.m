%% 1
text = 'Test text!';
bits = encoder(text);
decoded_text = decoder(bits);
disp('%% 1: Encoder/Decoder');
disp(['Original text: ', text]);
disp(['Decoded text: ', decoded_text]);
disp(' ');

%% 2
input_bits = [0 1 0 1 1 0 0 0 1 1];

encoded_bits = conv_encoder(input_bits);
%disp(encoded_bits);

decoded_bits = viterbi_decoder(encoded_bits);
%disp(decoded_bits);
disp('%% 2: Convolutional Encoder/Viterbi Decoder');
disp('Input bits for conv_encoder:'); disp(input_bits);
disp('Decoded bits from viterbi_decoder:'); disp(decoded_bits(1:length(input_bits))); % Truncate to original length for comparison
if isequal(input_bits, decoded_bits(1:length(input_bits)))
    disp('Convolutional coding and Viterbi decoding successful (ignoring trailing zeros).');
else
    disp('Error in convolutional coding/Viterbi decoding.');
end
disp(' ');

%% 3
disp('%% 3: Interleaver/Deinterleaver');
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
disp(' ');

%% 4
disp('%% 4: QPSK Modulation/Demodulation');
% Note: The provided QPSK modulator and demodulator might be inconsistent.
% Modulator maps: 00->Q1, 01->Q4, 10->Q2, 11->Q3
% Demodulator (active part) maps: Q1->00, Q2->01, Q3->11, Q4->10
% This will lead to mismatches for 01 and 10 bit pairs.
qpsk_test_bits = input_bits; % Use the same input_bits for testing
if mod(length(qpsk_test_bits),2) ~= 0
    qpsk_test_bits_padded = [qpsk_test_bits, 0]; % Ensure even length for QPSK
else
    qpsk_test_bits_padded = qpsk_test_bits;
end

symbols = qpsk_modulate(qpsk_test_bits_padded);
disp('Модулированные символы (первые 5):');
disp(symbols(1:min(5, length(symbols))));

received_bits = qpsk_demodulate(symbols);
disp('Демодулированные биты:');
disp(received_bits);
disp('Ожидаемые биты (с возможным паддингом):');
disp(qpsk_test_bits_padded);

if isequal(qpsk_test_bits_padded, received_bits)
    disp('QPSK модуляция и демодуляция успешны!');
else
    disp('Ошибка QPSK модуляции/демодуляции.');
end
disp(' ');

%% 5
disp('%% 5: OFDM Modulation');
delta_rs = 6;
c_null_carriers_coeff = 1/4;

qpsk_output_symbols_for_ofdm = qpsk_modulate(input_bits); % Modulate 'input_bits'

ofdm_symbols = ofdm_modulate(qpsk_output_symbols_for_ofdm, delta_rs, c_null_carriers_coeff);
disp('OFDM Модулированные символы (первые 10 комплексных отсчетов):');
if length(ofdm_symbols) > 10
    disp(ofdm_symbols(1:10));
else
    disp(ofdm_symbols);
end
disp(['Количество OFDM символов (отсчетов во временной области): ', num2str(length(ofdm_symbols))]);
disp(' ');

%% 6
disp('%% 6: Модель многолучевого канала передачи');

NB_rays = 20;
N0_dbW = -120;

f0_carrier_freq = 2.4e9;
B_signal_bw = 5e6;

S_tx_channel_input = ofdm_symbols;

if isempty(S_tx_channel_input)
    disp('Входной сигнал S_tx_channel_input для канала пуст.');
else
    disp(['Длина входного сигнала для канала (S_tx_channel_input): ', num2str(length(S_tx_channel_input))]);
    
    S_rx_channel_output = multipath_channel(S_tx_channel_input, NB_rays, N0_dbW, f0_carrier_freq, B_signal_bw);
    
    disp('Сигнал на выходе канала (S_rx_channel_output), первые 10 отсчетов:');
    if length(S_rx_channel_output) > 10
        disp(S_rx_channel_output(1:10));
    else
        disp(S_rx_channel_output);
    end
    disp(['Длина выходного сигнала с канала: ', num2str(length(S_rx_channel_output))]);
    
    if length(S_tx_channel_input) == length(S_rx_channel_output)
        disp('Длины входного и выходного сигналов канала совпадают.');
    else
        disp('Длины входного и выходного сигналов канала НЕ совпадают.');
    end
end