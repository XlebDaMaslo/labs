clear all; clc; close all;

text_length = 35;         
NB = 7;                  
TCP_ratio = 1/16;         
delta_rs = 6;             
B = 13e6;                 
f0 = 1.9e9;               

c_zero_padding = 1/4;
rs_tx_value = 0.707 + 0.707i;

SNR_dB_range = 0:10:200;
% SNR_dB_range = 100; 

constraint_length = 7;
trellis = poly2trellis(constraint_length, [133, 171]);
traceback_depth_viterbi = 5 * constraint_length; 

chars = [char('A':'Z'), char('a':'z'), char('0':'9'), ' ', '.', '!', '?'];

BER_values = zeros(1, length(SNR_dB_range));

plot_snr_index = floor(length(SNR_dB_range) / 2) + 1;
if isempty(plot_snr_index) || plot_snr_index == 0, plot_snr_index = 1; end

saved_tx_ofdm_spectrum_freq = [];
saved_rx_ofdm_spectrum_freq_no_eq = [];
saved_rx_ofdm_spectrum_freq_eq = [];
saved_tx_qpsk_symbols = [];
saved_rx_qpsk_symbols_demod_input = [];

% Генерация исходного сообщения
rng(text_length);
original_message_indices = randi([1, length(chars)], 1, text_length);
original_message = chars(original_message_indices);

fprintf('Исходное сообщение: %s\n', original_message);

% 1. Передатчик
bits_source = encoder(original_message);
fprintf('Длина бит источника: %d\n', length(bits_source));

bits_conv_encoded = conv_encoder(bits_source);
fprintf('Длина сверточно-кодированных бит: %d\n', length(bits_conv_encoded));

bits_interleaved = forward_interleaver(bits_conv_encoded);
fprintf('Длина перемеженных бит: %d\n', length(bits_interleaved));

symbols_qpsk = qpsk_modulate(bits_interleaved);
n_qpsk_original = length(symbols_qpsk);
fprintf('Количество QPSK символов: %d\n', n_qpsk_original);
saved_tx_qpsk_symbols = symbols_qpsk; % Сохраняем для графика

[symbols_ofdm_tx, freq_domain_signal_mod_plot] = ofdm_modulate(symbols_qpsk, delta_rs, c_zero_padding, rs_tx_value, TCP_ratio);
saved_tx_ofdm_spectrum_freq = freq_domain_signal_mod_plot; % Сохраняем для графика

n_active_subcarriers_mod = n_qpsk_original + floor(n_qpsk_original / delta_rs);
if n_qpsk_original == 0, n_active_subcarriers_mod = 0; end % Edge case
n_z_padding_mod = 0;
if n_active_subcarriers_mod > 0
    n_z_padding_mod = round(c_zero_padding * n_active_subcarriers_mod);
end
N_fft_mod = n_active_subcarriers_mod + 2 * n_z_padding_mod;

fprintf('Длина OFDM TX символов: %d (Размер ОБПФ: %d, Отношение ЦП: %.3f)\n', length(symbols_ofdm_tx), N_fft_mod, TCP_ratio);

if isempty(symbols_ofdm_tx) && n_qpsk_original > 0 % Allow empty if n_qpsk_original is 0
    error('OFDM модуляция дала пустой вывод. Проверьте параметры.');
end



for snr_idx = 1:length(SNR_dB_range)
    current_SNR_dB = SNR_dB_range(snr_idx);
    
    P_signal_tx_watts = mean(abs(symbols_ofdm_tx).^2);
    if isempty(symbols_ofdm_tx) || P_signal_tx_watts == 0 % If no signal transmitted
        P_signal_tx_watts = 1e-12; % Avoid log(0) or division by zero, assume very small power
    end
    
    N0_db_param_for_channel = 10*log10(P_signal_tx_watts) - current_SNR_dB;

    fprintf('Симуляция для SNR = %d дБ (N0_db для канала = %.2f дБВт)\n', current_SNR_dB, N0_db_param_for_channel);

    % 2. Канал
    symbols_rx_channel = multipath_channel(symbols_ofdm_tx, NB, N0_db_param_for_channel, f0, B);
    if isempty(symbols_rx_channel) && ~isempty(symbols_ofdm_tx)
        warning('Выход канала пуст для SNR %f дБ. Пропуск.', current_SNR_dB);
        BER_values(snr_idx) = NaN;
        continue;
    end
    fprintf('Длина принятых символов из канала: %d\n', length(symbols_rx_channel));

    % 3. Приемник
    [symbols_qpsk_demod, spectrum_no_eq, spectrum_eq] = ofdm_demodulate_equalize(...
        symbols_rx_channel, TCP_ratio, c_zero_padding, delta_rs, n_qpsk_original, rs_tx_value, N_fft_mod);

    if isempty(symbols_qpsk_demod) && n_qpsk_original > 0
        warning('OFDM демодуляция дала пустой вывод для SNR %f дБ. Пропуск BER.', current_SNR_dB);
        BER_values(snr_idx) = 0.5; % Максимальная ошибка
        if snr_idx == plot_snr_index
            saved_rx_ofdm_spectrum_freq_no_eq = spectrum_no_eq;
            saved_rx_ofdm_spectrum_freq_eq = spectrum_eq;
        end
        continue;
    end
    fprintf('Длина демодулированных QPSK символов: %d\n', length(symbols_qpsk_demod));

    if snr_idx == plot_snr_index
        saved_rx_ofdm_spectrum_freq_no_eq = spectrum_no_eq;
        saved_rx_ofdm_spectrum_freq_eq = spectrum_eq;
        saved_rx_qpsk_symbols_demod_input = symbols_qpsk_demod;
    end

    bits_demod_qpsk = qpsk_demodulate(symbols_qpsk_demod);
    fprintf('Длина QPSK-демодулированных бит: %d\n', length(bits_demod_qpsk));

    bits_deinterleaved = reverse_interleaver(bits_demod_qpsk);
    fprintf('Длина деперемеженных бит: %d\n', length(bits_deinterleaved));
    
    if length(bits_deinterleaved) > length(bits_conv_encoded)
        bits_deinterleaved = bits_deinterleaved(1:length(bits_conv_encoded));
    elseif length(bits_deinterleaved) < length(bits_conv_encoded) && ~isempty(bits_conv_encoded)
        warning('Длина деперемеженных бит (%d) короче, чем сверточно-кодированных (%d). Дополнение нулями.', length(bits_deinterleaved), length(bits_conv_encoded));
        bits_deinterleaved = [bits_deinterleaved, zeros(1, length(bits_conv_encoded) - length(bits_deinterleaved))];
    end
    
    if isempty(bits_deinterleaved) && ~isempty(bits_source)
        decoded_bits_viterbi = randi([0 1], 1, length(bits_source));
        warning('Пустой вход для декодера Витерби. BER будет высоким.');
    elseif isempty(bits_deinterleaved) && isempty(bits_source)
        decoded_bits_viterbi = [];
    else
        decoded_bits_viterbi = vitdec(bits_deinterleaved, trellis, traceback_depth_viterbi, 'trunc', 'hard');
    end
    fprintf('Длина декодированных Витерби бит: %d\n', length(decoded_bits_viterbi));

    len_compare = min(length(bits_source), length(decoded_bits_viterbi));
    decoded_bits_viterbi_comp = decoded_bits_viterbi;

    if length(decoded_bits_viterbi) > length(bits_source)
        decoded_bits_viterbi_comp = decoded_bits_viterbi(1:length(bits_source));
    elseif length(decoded_bits_viterbi) < length(bits_source) && ~isempty(bits_source)
        warning('Выход Витерби короче исходных бит. BER рассчитывается по меньшей длине.');
        %decoded_bits_viterbi_comp = [decoded_bits_viterbi, zeros(1, length(bits_source) - length(decoded_bits_viterbi))];
    end
    
    if isempty(decoded_bits_viterbi_comp) && ~isempty(bits_source)
        received_text = repmat('?',1,text_length); % Ошибка
    elseif isempty(decoded_bits_viterbi_comp) && isempty(bits_source)
        received_text = '';
    else
        received_text = decoder(decoded_bits_viterbi_comp);
    end

    if snr_idx == plot_snr_index || length(SNR_dB_range) == 1
         fprintf('Декодированный текст (SNR %d dB): %s\n', current_SNR_dB, received_text);
    end

    % 4. Расчет BER
    if len_compare == 0 && ~isempty(bits_source)
        num_errors = length(bits_source);
        BER = 0.5;
    elseif len_compare == 0 && isempty(bits_source)
        num_errors = 0;
        BER = 0;
    else
        num_errors = sum(bits_source(1:len_compare) ~= decoded_bits_viterbi_comp(1:len_compare));
        BER = num_errors / len_compare;
    end
    BER_values(snr_idx) = BER;
    fprintf('SNR = %d дБ, BER = %f (%d ошибок / %d бит)\n', current_SNR_dB, BER, num_errors, len_compare);
    fprintf('---------------------------------------------------\n');
end

% 5. Построение графиков
% BER vs SNR
figure;
semilogy(SNR_dB_range, BER_values, 'o-');
xlabel('SNR (дБ)');
ylabel('Вероятность битовой ошибки (BER)');
title('BER vs SNR для OFDM системы');
grid on;
ylim([max(1e-5, min(BER_values(BER_values>0))/2) , 1]); % Адаптивный нижний предел


% Графики спектров и созвездий
figure;
subplot(3,2,1);
if ~isempty(saved_tx_ofdm_spectrum_freq)
    plot(abs(saved_tx_ofdm_spectrum_freq));
    title('1. Спектр OFDM на передаче (до ОБПФ)'); xlabel('Индекс поднесущей'); ylabel('Амплитуда');
else
    title('1. Спектр OFDM TX (нет данных)');
end

subplot(3,2,2);
if ~isempty(saved_rx_ofdm_spectrum_freq_no_eq)
    plot(abs(saved_rx_ofdm_spectrum_freq_no_eq));
    title('2. Спектр OFDM на приеме (до EQ)'); xlabel('Индекс поднесущей'); ylabel('Амплитуда');
else
    title('2. Спектр OFDM RX до EQ (нет данных)');
end

subplot(3,2,3);
if ~isempty(saved_rx_ofdm_spectrum_freq_eq)
    plot(abs(saved_rx_ofdm_spectrum_freq_eq));
    title('3. Спектр OFDM на приеме (после EQ)'); xlabel('Индекс поднесущей'); ylabel('Амплитуда');
else
    title('3. Спектр OFDM RX после EQ (нет данных)');
end

subplot(3,2,4);
if ~isempty(saved_tx_qpsk_symbols)
    plot(real(saved_tx_qpsk_symbols), imag(saved_tx_qpsk_symbols), '.');
    title('4. QPSK-созвездие на передаче'); xlabel('Синфазная компонента'); ylabel('Квадратурная компонента'); axis equal; grid on;
    xlim([-1.5 1.5]); ylim([-1.5 1.5]);
else
    title('4. QPSK TX созвездие (нет данных)');
end

subplot(3,2,5);
if ~isempty(saved_rx_qpsk_symbols_demod_input)
    plot(real(saved_rx_qpsk_symbols_demod_input), imag(saved_rx_qpsk_symbols_demod_input), '.');
    title('5. QPSK-созвездие на приеме (вход демодулятора)'); xlabel('Синфазная компонента'); ylabel('Квадратурная компонента'); axis equal; grid on;
    max_val = 1.5 * max(1, max(abs(saved_rx_qpsk_symbols_demod_input(:))));
    if isempty(max_val) || isnan(max_val) || max_val == 0, max_val = 1.5; end
    xlim([-max_val max_val]); ylim([-max_val max_val]);
else
    title('5. QPSK RX созвездие (нет данных)');
end

sgtitle(sprintf('Анализ OFDM системы (графики для SNR = %g дБ)', SNR_dB_range(plot_snr_index) ));

disp('Симуляция завершена.');
disp('Исходное сообщение:'); disp(original_message);
if exist('received_text', 'var') && (snr_idx == plot_snr_index || length(SNR_dB_range) == 1)
elseif exist('received_text', 'var')
    fprintf('Принятое сообщение (для последнего SNR %d дБ): %s\n',current_SNR_dB, received_text);
else
    disp('Принятое сообщение: Недоступно из-за ошибок.');
end