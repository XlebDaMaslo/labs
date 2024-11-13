#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

string generate_data(int N) {
    string data;
    for (int i = 0; i < N; ++i) {
        data += to_string(rand() % 2);
    }
    return data;
}

string calculate_crc(string data, const string& polynomial) {
    int polynomial_len = polynomial.length();
    data += string(polynomial_len - 1, '0');

    int data_len = data.length();
    for (int i = 0; i <= data_len - polynomial_len; ++i) {
        if (data[i] == '1') {
            for (int j = 0; j < polynomial_len; ++j) {
                data[i + j] = ((data[i + j] - '0') ^ (polynomial[j] - '0')) + '0';
            }
        }
    }

    return data.substr(data_len - polynomial_len + 1);
}

pair<string, bool> calculate_crc_receiver(string data_with_crc, const string& polynomial) {
    int polynomial_len = polynomial.length();
    int data_len = data_with_crc.length();

    for (int i = 0; i <= data_len - polynomial_len; ++i) {
        if (data_with_crc[i] == '1') {
            for (int j = 0; j < polynomial_len; ++j) {
                data_with_crc[i + j] = ((data_with_crc[i + j] - '0') ^ (polynomial[j] - '0')) + '0';
            }
        }
    }

    string crc = data_with_crc.substr(data_len - polynomial_len + 1);
    bool error = false;
    for (char bit : crc) {
        if (bit == '1') {
            error = true;  // Ошибка, если CRC не все нули
            break;
        }
    }

    return {crc, error};
}

string bit_distortion(const string& data, int index) {
    string distorted_data = data;
    distorted_data[index] = (data[index] == '0') ? '1' : '0';
    return distorted_data;
}

int main() {
    srand(static_cast<unsigned int>(time(0)));

    // 1, 2
    int N = 20 + 10;  // порядковый номер в журнале
    string polynomial = "11011110"; // G=x^7+x^6+x^4+x^3+x^2+x
    string data = generate_data(N);

    string crc = calculate_crc(data, polynomial);
    cout << "CRC на передатчике: " << crc << endl;

    // 3
    string data_with_crc = data + crc;
    auto [crc_receiver, has_error] = calculate_crc_receiver(data_with_crc, polynomial);

    cout << "CRC на приемнике: " << crc_receiver << endl;

    if (has_error) {
        cout << "Ошибка обнаружена!" << endl;
    } else {
        cout << "Ошибок не обнаружено." << endl;
    }

    // 4
    N = 250;
    data = generate_data(N);

    crc = calculate_crc(data, polynomial);
    data_with_crc = data + crc;

    // 5
    int errors_detected = 0;
    int errors_not_detected = 0;

    for (size_t i = 0; i < data_with_crc.length(); ++i) {
        string corrupted_data_with_crc = bit_distortion(data_with_crc, i);
        auto [crc_receiver, has_error] = calculate_crc_receiver(corrupted_data_with_crc, polynomial);

        if (has_error) {
            ++errors_detected;
        } else {
            ++errors_not_detected;
        }
    }

    cout << "Обнаружено ошибок: " << errors_detected << endl;
    cout << "Не обнаружено ошибок: " << errors_not_detected << endl;

    return 0;
}
