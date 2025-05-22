%% 1 Text Encoding/Decoding
disp('%% 1 Text Encoding/Decoding');
text_input = 'Test text!';
bits_from_text = encoder(text_input);
decoded_text_output = decoder(bits_from_text);
disp(['Original text: ', text_input]);
disp(['Decoded text: ', decoded_text_output]);
if strcmp(text_input, decoded_text_output)
    disp('Text encode/decode successful!');
else
    disp('Error in text encode/decode.');
end
disp('------------------------------------');

%% 2 Convolutional Encoding/Viterbi Decoding
disp('%% 2 Convolutional Encoding/Viterbi Decoding');
input_bits_conv = [0 1 0 1 1 0 0 0 1 1];
disp('Input bits for conv encoder:');
disp(input_bits_conv);

encoded_bits_conv = conv_encoder(input_bits_conv);
disp('Convolutionally encoded bits (first 10):');
disp(encoded_bits_conv(1:min(10,length(encoded_bits_conv))));

% Note: Viterbi decoder performance is highly dependent on noise.
% Here, we test it in a noiseless scenario by directly feeding encoded bits.
decoded_bits_viterbi = viterbi_decoder(encoded_bits_conv);
disp('Viterbi decoded bits:');
disp(decoded_bits_viterbi);

% Compare original input_bits_conv with decoded_bits_viterbi
% Viterbi decoder might have a delay or requires proper termination for exact recovery.
% The 'trunc' method can lead to differences, especially at the end.
% We should compare the relevant part of the decoded sequence.
% For 'trunc' mode, output length matches input length to vitdec / 2
% So length of decoded_bits_viterbi should be length of input_bits_conv
if length(input_bits_conv) == length(decoded_bits_viterbi) && isequal(input_bits_conv, decoded_bits_viterbi)
    disp('Convolutional encoding/Viterbi decoding successful!');
else
    disp('Error or mismatch in convolutional encoding/Viterbi decoding.');
    disp('Note: Mismatch might occur due to trellis termination or traceback depth in Viterbi.');
end
disp('------------------------------------');

%% 3 Interleaving/Deinterleaving
disp('%% 3 Interleaving/Deinterleaving');
input_bits_interleave = [0 1 0 1 1 0 0 0 1 1 1 0 1 0 0 1];
disp('Original bits for interleaver:');
disp(input_bits_interleave);

permuted_bits = forward_interleaver(input_bits_interleave);
disp('Interleaved bits:');
disp(permuted_bits);

original_bits_from_deinterleaver = reverse_interleaver(permuted_bits);
disp('Deinterleaved (restored) bits:');
disp(original_bits_from_deinterleaver);

if isequal(input_bits_interleave, original_bits_from_deinterleaver)
    disp('Interleaving/Deinterleaving successful!');
else
    disp('Error in interleaving/deinterleaving.');
end
disp('------------------------------------');

%% 4 QPSK Modulation/Demodulation
disp('%% 4 QPSK Modulation/Demodulation');
input_bits_qpsk = [0 1 0 1 1 0 0 0 1 1];
disp('Input bits for QPSK modulator:');
disp(input_bits_qpsk);

qpsk_symbols = qpsk_modulate(input_bits_qpsk);
disp('QPSK modulated symbols:');
disp(qpsk_symbols);

received_bits_qpsk = qpsk_demodulate(qpsk_symbols);
disp('QPSK demodulated bits:');
disp(received_bits_qpsk);

original_length_qpsk = length(input_bits_qpsk);
if mod(original_length_qpsk, 2) ~= 0
    comparison_bits_qpsk = input_bits_qpsk;
    recovered_comparison_bits = received_bits_qpsk(1:original_length_qpsk);
else
    comparison_bits_qpsk = input_bits_qpsk;
    recovered_comparison_bits = received_bits_qpsk;
end

if isequal(comparison_bits_qpsk, recovered_comparison_bits(1:length(comparison_bits_qpsk)))
    disp('QPSK modulation/demodulation successful!');
else
    disp('Error in QPSK modulation/demodulation.');
end
disp('------------------------------------');

%% 5 OFDM Modulation
disp('%% 5 OFDM Modulation');
if isempty(qpsk_symbols)
    disp('QPSK symbols are empty, skipping OFDM modulation.');
    ofdm_modulated_symbols = [];
else
    delta_rs_ofdm = 6; 
    c_guard_ofdm = 1/4;
    
    disp(['Input QPSK symbols for OFDM (length ', num2str(length(qpsk_symbols)), '):']);
    disp(qpsk_symbols);

    ofdm_modulated_symbols = ofdm_modulate(qpsk_symbols, delta_rs_ofdm, c_guard_ofdm);
    disp('OFDM Modulated symbols (time-domain, with cyclic prefix):');
    disp(ofdm_modulated_symbols);
end
