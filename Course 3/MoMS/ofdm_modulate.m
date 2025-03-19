function ofdm_symbols = ofdm_modulate(qpsk_symbols, delta_rs, c)
    n_qpsk = length(qpsk_symbols);
    cp_length = 1/4;

    % Расчет количества опорных поднесущих
    n_rs = floor(n_qpsk / delta_rs); % Округления вниз до ближайшего целого числа

    % Формирование опорного сигнала
    rs_symbols = repmat(0.707 + 0.707i, 1, n_rs); % Матрица повторения заданного элемента

    % Расчет индексов опорных поднесущих
    rs_indices = 1:delta_rs:(n_rs * delta_rs); % Вектор индексов опорных поднесущих

    % Размещение опорного сигнала (создание вектора, где будут и данные, и RS)
    ofdm_freq = zeros(1, n_qpsk + n_rs); % Инициализация нулями
    
    data_indices = []; % Массив с индексами поднесущих, предназначенных для передачи данных
    rs_count = 0; % Счетчик опорных сигналов
    data_count = 0; % Счетчик QPSK-символов

    for i = 1:length(ofdm_freq)
      if ismember(i, rs_indices) % Если i является опорной поднесущей
          ofdm_freq(i) = rs_symbols(rs_count+1);
          rs_count = rs_count+1;
      else
        data_indices = [data_indices,i]; % Добавление информационного сигнала
        data_count = data_count+1;
        if(data_count <= n_qpsk) % Ограничение data_count
              ofdm_freq(i) = qpsk_symbols(data_count);
        end
      end
    end

    % Добавление нулевого защитного интервала
    n_z = round(c * (n_rs + n_qpsk));
    ofdm_freq_with_zeros = [zeros(1, n_z), ofdm_freq, zeros(1, n_z)];

    % Обратное дискретное преобразование Фурье (IDFT) (из частотной области во временную)
    ofdm_time = ifft(ofdm_freq_with_zeros);
    
    cp_samples = round(cp_length * length(ofdm_time));
    % Добавление циклического префикса
    if cp_length > 0
        cyclic_prefix = ofdm_time(end-cp_samples+1:end);
        ofdm_symbols = [cyclic_prefix, ofdm_time];
    else
        ofdm_symbols = ofdm_time;
    end
    
end