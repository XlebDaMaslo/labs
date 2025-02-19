#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <bitset>

using namespace std;

double autocorr_check(const vector<int>& seq) {
    int n = seq.size();
    double first_correlation = -1;

    for (int shift = 1; shift < n; ++shift) {
        vector<int> compare(n);
        for (int j = 0; j < n; ++j) {
            int shifted_index = (j + shift) % n;
            compare[j] = (seq[j] == seq[shifted_index]) ? 1 : 0;
        }
        int count1 = count(compare.begin(), compare.end(), 1);
        int count0 = count(compare.begin(), compare.end(), 0);
        double correlation = (1.0 / n) * (count1 - count0);

        if (first_correlation == -1) {
            first_correlation = correlation;
        } else if (correlation != first_correlation) {
            return false;
        }
    }

    return true;
}

vector<int> gen_gold_seq(int initial_state1, int initial_state2, string polynomial1_bin, string polynomial2_bin) {
    int n = polynomial1_bin.size();
    string init_poly1 = polynomial1_bin;
    string init_poly2 = polynomial2_bin;

    vector<int> x(n);
    vector<int> y(n);

    for (int i = 0; i < n; ++i) {
        x[i] = (initial_state1 >> (n - 1 - i)) & 1;
        y[i] = (initial_state2 >> (n - 1 - i)) & 1;
    }

    vector<int> polynomial1, polynomial2;
    for (int index = 0; index < n; ++index) {
        if (polynomial1_bin[index] == '1') polynomial1.push_back(index);
        if (polynomial2_bin[index] == '1') polynomial2.push_back(index);
    }

    vector<int> sequence;

    for (int i = 0; i < (1 << n) - 1; ++i) {
        int out = x.back() ^ y.back();

        int new_x = 0;
        for (int tap : polynomial1) {
            new_x ^= x[tap];
        }
        x.insert(x.begin(), new_x);
        x.pop_back();

        int new_y = 0;
        for (int tap : polynomial2) {
            new_y ^= y[tap];
        }
        y.insert(y.begin(), new_y);
        y.pop_back();

        sequence.push_back(out);
    }

    if (!autocorr_check(sequence)) {
        if (polynomial1_bin == "11111") {
            polynomial1_bin = init_poly1;
            polynomial2_bin = bitset<5>(stoi(polynomial2_bin, nullptr, 2) + 1).to_string();
            sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin);
        } else if (polynomial2_bin == "11111") {
            polynomial2_bin = init_poly2;
            polynomial1_bin = bitset<5>(stoi(polynomial1_bin, nullptr, 2) + 1).to_string();
            sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin);
        } else {
            polynomial1_bin = bitset<5>(stoi(polynomial1_bin, nullptr, 2) + 1).to_string();
            sequence = gen_gold_seq(initial_state1, initial_state2, polynomial1_bin, polynomial2_bin);
        }
    }
    
    return sequence;
}

void autocorr(const vector<int>& seq) {
    cout << "Сдвиг | ";
    for (size_t i = 0; i < seq.size(); ++i) {
        cout << i + 1 << " ";
    }
    cout << "| Автокорреляция" << endl;

    vector<int> new_seq = seq;

    for (size_t i = 0; i <= seq.size(); ++i) {
        vector<int> compare(seq.size());
        for (size_t j = 0; j < seq.size(); ++j) {
            compare[j] = (seq[j] == new_seq[j]) ? 1 : 0;
        }
        int count1 = count(compare.begin(), compare.end(), 1);
        int count0 = count(compare.begin(), compare.end(), 0);
        double correlation = (1.0 / (pow(2, log2(seq.size() + 1)) - 1)) * (count1 - count0);
        
        cout << i << " | ";
        for (int bit : compare) {
            cout << bit << " ";
        }
        cout << "| " << correlation << endl;
        
        rotate(new_seq.rbegin(), new_seq.rbegin() + 1, new_seq.rend());
    }
}

int correlation(const vector<int>& a, const vector<int>& b) {
    int result = 0;
    for (size_t i = 0; i < a.size(); ++i) {
        result += a[i] * b[i];
    }
    return result;
}

double normalized_correlation(const vector<int>& a, const vector<int>& b) {
    double sum_a = 0;
    double sum_b = 0;

    for (size_t i = 0; i < a.size(); ++i) {
        sum_a += a[i] * a[i];
        sum_b += b[i] * b[i];
    }
    return correlation(a, b) / sqrt(sum_a * sum_b);
}

void corr_print(const vector<int>& seq1, vector<int> seq2) {
    cout << "\nСдвиг | ";
    for (size_t i = 0; i < seq1.size(); ++i) {
        cout << i + 1 << " ";
    }
    cout << "| Корреляция | Норм. корреляция" << endl;

    for (size_t i = 0; i <= seq1.size(); ++i) {
        vector<int> compare(seq1.size());
        for (size_t j = 0; j < seq1.size(); ++j) {
            compare[j] = (seq1[j] == seq2[j]) ? 1 : 0;
        }
        int corr = correlation(seq1, seq2);
        double n_corr = normalized_correlation(seq1, seq2);

        cout << i << " | ";
        for (int bit : compare) {
            cout << bit << " ";
        }
        cout << "| " << corr << " | " << n_corr << endl;

        rotate(seq2.rbegin(), seq2.rbegin() + 1, seq2.rend());
    }
}

int main() {
    int number_st = 10; // Номер по списку
    int number_st2 = number_st + 7;

    // x^5 + x^4 + 1 первый регистр по схеме
    string polynomial1_bin = "00011";

    // x^5 + x^2 + 1 второй регистр по схеме
    string polynomial2_bin = "01001";

    vector<int> sequence1 = gen_gold_seq(number_st, number_st2, polynomial1_bin, polynomial2_bin);
    cout << "Sequence 1: ";
    for (int val : sequence1) {
        cout << val;
    }
    cout << endl;

    cout << "Count of 1s: " << count(sequence1.begin(), sequence1.end(), 1) << endl;
    cout << "Count of 0s: " << count(sequence1.begin(), sequence1.end(), 0) << endl;
    autocorr(sequence1);

    vector<int> sequence2 = gen_gold_seq(number_st + 1, (number_st + 7) - 5, polynomial1_bin, polynomial2_bin);
    cout << "Sequence 2: ";
    for (int val : sequence2) {
        cout << val;
    }
    cout << endl;
    corr_print(sequence1, sequence2);

    return 0;
}
