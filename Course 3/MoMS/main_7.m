clear all; clc; close all;

text_length = 35;
NB = 7;
TCP_ratio = 1/16;
delta_rs = 6;
B = 13e6;                 % Гц
f0 = 1.9e9;               % Гц

c_zero_padding = 1/4;     
rs_tx_value = 0.707 + 0.707i;

SNR_dB = 95;              % дБ

chars = [char('A':'Z'), char('a':'z'), char('0':'9'), ' ', '.', '!', '?'];

rng(text_length);
original_message_indices = randi([1, length(chars)], 1, text_length);
original_message = chars(original_message_indices);

fprintf('Исходное сообщение: %s\n', original_message);

%% 1. Передатчик
bits_source = encoder(original_message);
fprintf('Длина бит источника: %d\n', length(bits_source));

bits_conv_encoded = conv_encoder(bits_source);
fprintf('Длина сверточно-кодированных бит: %d\n', length(bits_conv_encoded));

bits_interleaved = forward_interleaver(bits_conv_encoded);
fprintf('Длина перемеженных бит: %d\n', length(bits_interleaved));

symbols_qpsk_tx = qpsk_modulate(bits_interleaved);
n_qpsk_original = length(symbols_qpsk_tx);
fprintf('Количество QPSK символов на передаче: %d\n', n_qpsk_original);

[symbols_ofdm_tx, freq_domain_tx_for_plot] = ofdm_modulate(...
    symbols_qpsk_tx, delta_rs, c_zero_padding, rs_tx_value, TCP_ratio);

n_active_subcarriers_mod = 0;
if n_qpsk_original > 0 || (n_qpsk_original == 0 && delta_rs > 0)
    n_rs_calc_mod = 0;
    if n_qpsk_original > 0 && delta_rs > 0
        n_rs_calc_mod = floor(n_qpsk_original / delta_rs);
    end
    n_active_subcarriers_mod = n_qpsk_original + n_rs_calc_mod;
end

n_z_padding_mod = 0;
if n_active_subcarriers_mod > 0
    n_z_padding_mod = round(c_zero_padding * n_active_subcarriers_mod);
end
N_fft_mod = n_active_subcarriers_mod + 2 * n_z_padding_mod;

fprintf('Длина OFDM TX символов: %d (Размер ОБПФ: %d)\n', length(symbols_ofdm_tx), N_fft_mod);

if isempty(symbols_ofdm_tx) && n_qpsk_original > 0
    error('OFDM модуляция дала пустой вывод. Проверьте параметры.');
elseif isempty(symbols_ofdm_tx) && n_qpsk_original == 0
    disp('OFDM модуляция: нет QPSK символов для передачи, выход пуст (ожидаемо).');
end

%% 2. Канал
P_signal_tx_watts = mean(abs(symbols_ofdm_tx).^2);
if isempty(symbols_ofdm_tx) || P_signal_tx_watts == 0
    P_signal_tx_watts = 1e-12;
end
N0_db_param_for_channel = 10*log10(P_signal_tx_watts) - SNR_dB;

fprintf('Симуляция канала для SNR = %d дБ (N0_db для канала = %.2f дБВт)\n', SNR_dB, N0_db_param_for_channel);

symbols_rx_channel = multipath_channel(symbols_ofdm_tx, NB, N0_db_param_for_channel, f0, B);

if isempty(symbols_rx_channel) && ~isempty(symbols_ofdm_tx)
    error('Выход канала пуст. Проверьте multipath_channel.');
elseif isempty(symbols_rx_channel) && isempty(symbols_ofdm_tx)
     disp('Канал: вход пуст, выход пуст (ожидаемо).');
end
fprintf('Длина принятых символов из канала: %d\n', length(symbols_rx_channel));

%% 3. Приемник
[symbols_qpsk_rx_demod, spectrum_rx_no_eq, spectrum_rx_eq] = ...
    ofdm_demodulate_equalize(...
    symbols_rx_channel, TCP_ratio, c_zero_padding, delta_rs, ...
    n_qpsk_original, rs_tx_value, N_fft_mod); % N_fft_mod важен здесь

if isempty(symbols_qpsk_rx_demod) && n_qpsk_original > 0
    warning('OFDM демодуляция дала пустой вывод. Проверьте ofdm_demodulate_equalize.');
    % Инициализируем для графиков, чтобы избежать ошибок
    if isempty(spectrum_rx_no_eq), spectrum_rx_no_eq = complex(zeros(1,N_fft_mod - 2*n_z_padding_mod)); end
    if isempty(spectrum_rx_eq), spectrum_rx_eq = complex(zeros(1,N_fft_mod - 2*n_z_padding_mod)); end
elseif isempty(symbols_qpsk_rx_demod) && n_qpsk_original == 0
    disp('OFDM демодуляция: нет QPSK символов для демодуляции, выход пуст (ожидаемо).');
end

fprintf('Количество QPSK символов после OFDM демодуляции: %d\n', length(symbols_qpsk_rx_demod));

%% 4. Построение графиков
figure;

subplot(3,2,1);
if ~isempty(freq_domain_tx_for_plot)
    plot(abs(freq_domain_tx_for_plot));
    title('1. Спектр OFDM на Tx (до ОБПФ)'); xlabel('Индекс поднесущей'); ylabel('Амплитуда'); grid on;
else
    title('1. Спектр OFDM Tx (нет данных)');
end

subplot(3,2,2);
if ~isempty(spectrum_rx_no_eq)
    plot(abs(spectrum_rx_no_eq));
    title('2. Спектр OFDM на Rx (до EQ)'); xlabel('Индекс поднесущей'); ylabel('Амплитуда'); grid on;
else
    title('2. Спектр OFDM Rx до EQ (нет данных)');
end

subplot(3,2,3);
if ~isempty(spectrum_rx_eq)
    plot(abs(spectrum_rx_eq));
    title('3. Спектр OFDM на Rx (после EQ)'); xlabel('Индекс поднесущей'); ylabel('Амплитуда'); grid on;
else
    title('3. Спектр OFDM Rx после EQ (нет данных)');
end

subplot(3,2,4);
if ~isempty(symbols_qpsk_tx)
    plot(real(symbols_qpsk_tx), imag(symbols_qpsk_tx), '.b');
    title('4. QPSK-созвездие на Tx'); xlabel('I'); ylabel('Q'); axis equal; grid on;
    xlim([-1.5 1.5]); ylim([-1.5 1.5]);
else
    title('4. QPSK Tx созвездие (нет данных)');
end

subplot(3,2,5);
if ~isempty(symbols_qpsk_rx_demod)
    plot(real(symbols_qpsk_rx_demod), imag(symbols_qpsk_rx_demod), '.r');
    title('5. QPSK-созвездие на Rx (после OFDM демодуляции)'); xlabel('I'); ylabel('Q'); axis equal; grid on;
    
    max_val_rx = 1.5 * max(1, max(abs(symbols_qpsk_rx_demod(:))));
     if isempty(max_val_rx) || isnan(max_val_rx) || max_val_rx == 0, max_val_rx = 1.5; end
    xlim([-max_val_rx max_val_rx]); ylim([-max_val_rx max_val_rx]);
else
    title('5. QPSK Rx созвездие (нет данных)');
end

sgtitle(sprintf('Анализ OFDM (SNR = %d дБ)', SNR_dB));