function S_rx = multipath_channel(S_tx, NB, N0_db, f0, B)

    c_light = 3e8;
    
    if isempty(S_tx)
        S_rx = [];
        return;
    end
    L = length(S_tx);
    Ts = 1/B;        

    original_S_tx_is_column = false;
    if size(S_tx, 1) > 1
        S_tx = S_tx.';
        original_S_tx_is_column = true;
    end

    D_min_meters = 10;
    D_max_meters = 1000;

    D_paths = D_min_meters + (D_max_meters - D_min_meters) * rand(1, NB);
    
    D1_direct_path = min(D_paths);

    max_delay_samples = 0;
    array_delayed_attenuated_signals = cell(1, NB);

    for i_path = 1:NB
        Di = D_paths(i_path);
        
        tau_i_samples = round((Di - D1_direct_path) / (c_light * Ts));
        
        if tau_i_samples > max_delay_samples
            max_delay_samples = tau_i_samples;
        end
        
        signal_path_i_delayed = [zeros(1, tau_i_samples), S_tx]; 
        
        Gi_attenuation = c_light / (4 * pi * Di * f0);
        
        array_delayed_attenuated_signals{i_path} = Gi_attenuation * signal_path_i_delayed;
    end

    L_S_mpy = L + max_delay_samples;
    
    S_mpy = complex(zeros(1, L_S_mpy));

    for i_path = 1:NB
        current_path_signal = array_delayed_attenuated_signals{i_path};
        
        padded_signal = [current_path_signal, complex(zeros(1, L_S_mpy - length(current_path_signal)))];
        S_mpy = S_mpy + padded_signal;
    end



    M_noise_len = length(S_mpy);
    
    noise_vector = wgn(1, M_noise_len, N0_db, 'complex'); 
        
    S_rx_full = S_mpy + noise_vector;

    if L > 0
        S_rx = S_rx_full(1:L);
    else
        S_rx = [];
    end
    
    if original_S_tx_is_column && ~isempty(S_rx)
        S_rx = S_rx.';
    end
end