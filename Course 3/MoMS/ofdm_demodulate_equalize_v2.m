function [demodulated_qpsk_symbols, C_signal_vector_out, C_eq_out] = ofdm_demodulate_equalize_v2(S_rx_from_channel, cp_length_ratio, c_zero_padding_coeff, delta_rs, n_qpsk_original, rs_tx_value)

    demodulated_qpsk_symbols = [];
    C_signal_vector_out = [];
    C_eq_out = [];

    if isempty(S_rx_from_channel) || n_qpsk_original == 0
        return;
    end
    
    n_rs_calculated = floor(n_qpsk_original / delta_rs);
    if n_qpsk_original == 0 
        n_rs_calculated = 0; 
    end

    n_subcarriers_data_and_rs = n_qpsk_original + n_rs_calculated;
    
    n_z_padding = 0;
    if n_subcarriers_data_and_rs > 0
        n_z_padding = round(c_zero_padding_coeff * n_subcarriers_data_and_rs);
    end
    
    N_fft = n_subcarriers_data_and_rs + 2 * n_z_padding;

    if N_fft == 0
        return; 
    end

    cp_samples = round(cp_length_ratio * N_fft);
    
    if length(S_rx_from_channel) <= cp_samples
        demodulated_qpsk_symbols = []; 
        C_signal_vector_out = []; 
        C_eq_out = [];
        return;
    end
    signal_no_cp = S_rx_from_channel(cp_samples + 1 : end);

    if length(signal_no_cp) < N_fft
        signal_no_cp = [signal_no_cp, zeros(1, N_fft - length(signal_no_cp))];
    elseif length(signal_no_cp) > N_fft
        signal_no_cp = signal_no_cp(1:N_fft);
    end

    ofdm_spectrum_received_with_zeros = fft(signal_no_cp, N_fft);

    if (2 * n_z_padding >= length(ofdm_spectrum_received_with_zeros))
        C_signal_vector = [];
    else
        C_signal_vector = ofdm_spectrum_received_with_zeros(n_z_padding + 1 : end - n_z_padding);
    end
    C_signal_vector_out = C_signal_vector;
    
    if isempty(C_signal_vector) || length(C_signal_vector) ~= n_subcarriers_data_and_rs
         demodulated_qpsk_symbols = []; 
         C_signal_vector_out = C_signal_vector; % Still output what we have
         C_eq_out = [];
         return;
    end

    H_eq_interpolated = ones(1, n_subcarriers_data_and_rs); 

    if n_rs_calculated > 0
        rs_indices_in_C = 1:delta_rs:(n_rs_calculated * delta_rs);
        rs_indices_in_C = rs_indices_in_C(rs_indices_in_C <= length(C_signal_vector));

        if ~isempty(rs_indices_in_C)
            R_rx = C_signal_vector(rs_indices_in_C);
            R_tx = repmat(rs_tx_value, 1, length(R_rx));
            H_on_rs = R_rx ./ R_tx;
            H_on_rs(isinf(H_on_rs) | isnan(H_on_rs)) = 1;

            all_indices_in_C = 1:n_subcarriers_data_and_rs;
            if length(rs_indices_in_C) >= 2
                H_eq_interpolated = interp1(rs_indices_in_C, H_on_rs, all_indices_in_C, 'linear', 'extrap');
            elseif length(rs_indices_in_C) == 1
                H_eq_interpolated(:) = H_on_rs(1);
            end
            H_eq_interpolated(isinf(H_eq_interpolated) | isnan(H_eq_interpolated)) = 1;
        end
    end
    
    H_eq_interpolated_safe = H_eq_interpolated;
    H_eq_interpolated_safe(H_eq_interpolated_safe == 0) = 1e-9;
    C_eq = C_signal_vector ./ H_eq_interpolated_safe;
    C_eq_out = C_eq;

    if n_qpsk_original == 0
        demodulated_qpsk_symbols = [];
        return;
    end
    
    data_subcarrier_indices = [];
    if n_rs_calculated > 0
        rs_indices_final = 1:delta_rs:(n_rs_calculated * delta_rs);
        if ~isempty(rs_indices_final)
            rs_indices_final = rs_indices_final(rs_indices_final <= length(C_eq));
        end
        
        all_subcarrier_indices = 1:length(C_eq);
        data_subcarrier_indices = setdiff(all_subcarrier_indices, rs_indices_final);
    else
        data_subcarrier_indices = 1:length(C_eq);
    end

    if isempty(data_subcarrier_indices) && n_qpsk_original > 0
        demodulated_qpsk_symbols = complex(zeros(1, n_qpsk_original));
    elseif ~isempty(data_subcarrier_indices) && max(data_subcarrier_indices) <= length(C_eq)
        demodulated_qpsk_symbols_temp = C_eq(data_subcarrier_indices);
        if length(demodulated_qpsk_symbols_temp) >= n_qpsk_original
            demodulated_qpsk_symbols = demodulated_qpsk_symbols_temp(1:n_qpsk_original);
        else
            demodulated_qpsk_symbols = [demodulated_qpsk_symbols_temp, complex(zeros(1, n_qpsk_original - length(demodulated_qpsk_symbols_temp)))];
        end
    elseif n_qpsk_original > 0 % Fallback if indices are problematic
         demodulated_qpsk_symbols = complex(zeros(1, n_qpsk_original));
    else % n_qpsk_original is 0
        demodulated_qpsk_symbols = [];
    end
    
    if length(demodulated_qpsk_symbols) ~= n_qpsk_original
        if length(demodulated_qpsk_symbols) > n_qpsk_original
            demodulated_qpsk_symbols = demodulated_qpsk_symbols(1:n_qpsk_original);
        else 
            demodulated_qpsk_symbols = [demodulated_qpsk_symbols, complex(zeros(1, n_qpsk_original - length(demodulated_qpsk_symbols)))];
        end
    end
end