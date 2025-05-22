function [ofdm_symbols, ofdm_freq_active_plus_zeros_for_plot] = ofdm_modulate(qpsk_symbols, delta_rs, c_zero_padding_coeff, rs_tx_val_mod, cp_length_ratio_param)
    n_qpsk = length(qpsk_symbols);
    
    n_rs = 0;
    if n_qpsk > 0 && delta_rs > 0
         n_rs = floor(n_qpsk / delta_rs);
    elseif n_qpsk == 0
         n_rs = 0;
    end

    rs_symbols = repmat(rs_tx_val_mod, 1, n_rs);

    rs_indices = [];
    if n_rs > 0 && delta_rs > 0
        rs_indices = 1:delta_rs:(n_rs * delta_rs);
    end

    n_active_subcarriers = n_qpsk + n_rs;
    ofdm_freq = complex(zeros(1, n_active_subcarriers));

    rs_count = 0;
    data_count = 0;

    if n_active_subcarriers == 0
        ofdm_freq_active_plus_zeros_for_plot = [];
        ofdm_symbols = [];
        return;
    end

    for i = 1:n_active_subcarriers
      is_rs_subcarrier = false;
      if ~isempty(rs_indices) && ismember(i, rs_indices)
          is_rs_subcarrier = true;
      end

      if is_rs_subcarrier
          rs_count = rs_count + 1;
          if rs_count <= length(rs_symbols)
              ofdm_freq(i) = rs_symbols(rs_count);
          else
              warning('OFDM Mod: rs_count превышает длину rs_symbols.');
              ofdm_freq(i) = 0;
          end
      else
        data_count = data_count + 1;
        if data_count <= n_qpsk
            ofdm_freq(i) = qpsk_symbols(data_count);
        end
      end
    end
    
    n_z = 0;
    if n_active_subcarriers > 0
        n_z = round(c_zero_padding_coeff * n_active_subcarriers);
    end
    ofdm_freq_with_zeros = [complex(zeros(1, n_z)), ofdm_freq, complex(zeros(1, n_z))];
    ofdm_freq_active_plus_zeros_for_plot = ofdm_freq_with_zeros;

    ofdm_time = ifft(ofdm_freq_with_zeros);

    N_fft_actual = length(ofdm_time);
    cp_samples = 0;
    if N_fft_actual > 0
        cp_samples = round(cp_length_ratio_param * N_fft_actual);
    end

    if cp_length_ratio_param > 0 && N_fft_actual > 0 && cp_samples > 0 && cp_samples < N_fft_actual
        cyclic_prefix = ofdm_time(end-cp_samples+1:end);
        ofdm_symbols = [cyclic_prefix, ofdm_time];
    else
        ofdm_symbols = ofdm_time;
    end
end