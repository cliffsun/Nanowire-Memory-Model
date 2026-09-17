#include "nanowire.h"

vector<double> getArrayFromString(const string &input_string) {
    stringstream ss(input_string);
    vector<double> arr;
    double num;
    while (ss >> num) {
        arr.push_back(num);
    }
    return arr;
}

vector<int> int_getArrayFromString(const string &input_string) {
    stringstream ss(input_string);
    vector<int> arr;
    int num;
    while (ss >> num) {
        arr.push_back(num);
    }
    return arr;
}

void backtrackWithRepetitions(vector<int>& candidate_values, int num_of_values, int start, vector<int>& current_combination, vector<vector<int>>& result) {
    if (current_combination.size() == num_of_values) {
        result.push_back(current_combination);
        return;
    }

    for (int i = start; i < candidate_values.size(); ++i) {
        current_combination.push_back(candidate_values[i]);
        backtrackWithRepetitions(candidate_values, num_of_values, 0, current_combination, result);
        current_combination.pop_back();
    }
}

vector<vector<int>> getAllPermutationsWithRepetitions(vector<int>& candidate_values, int num_of_values) {
    vector<vector<int>> result;
    vector<int> current_combination;
    backtrackWithRepetitions(candidate_values, num_of_values, 0, current_combination, result);
    return result;
}

vector<vector<int>> possibleSums(int target, vector<int> possible_values, int numOfLoops) {
    vector<vector<int>> permutations = getAllPermutationsWithRepetitions(possible_values, numOfLoops);
    vector<vector<int>> valid_combinations;

    set<vector<int>> unique_permutations;

    for (const auto& combination : permutations) {
        int sum = accumulate(combination.begin(), combination.end(), 0);
        if (sum == target) {
            unique_permutations.insert(combination);
        }
    }
    valid_combinations.assign(unique_permutations.begin(), unique_permutations.end());

    return valid_combinations;
}

vector<vector<int>> arrayOfVorticityNumbers(int vn, const vector<int> vorticies, const vector<double> &arrayOfWires) {
    int numOfWires = arrayOfWires.size();
    int numOfLoops = numOfWires - 1;
    return possibleSums(vn, vorticies, numOfLoops);
}


double supercurrent(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents,
                    const vector<int> &vorticity_arr, double initialPhaseDiff, double B) {
    vector<double> devicePhaseDiff(arrayOfWires.size(), 0);
    int numOfWires = arrayOfWires.size();
    int numOfLoops = numOfWires - 1;
    double currPhaseDiff = initialPhaseDiff;

    for (int i = 0; i < numOfLoops; ++i) {
        devicePhaseDiff[i] = currPhaseDiff;
        devicePhaseDiff[i + 1] = currPhaseDiff + 2 * M_PI * B * (arrayOfWires[i + 1] - arrayOfWires[i]) - 2 * M_PI * vorticity_arr[i];
        currPhaseDiff = devicePhaseDiff[i + 1];
    }

    for (int i = 0; i < numOfWires; ++i) {
        if (abs(devicePhaseDiff[i]) > abs(criticalPhases[i])) {
            return NAN;
        }
    }
    double a = 0;

    double curr = 0;
    for (int i = 0; i < numOfWires; ++i) {
        curr += criticalCurrents[i] * ((devicePhaseDiff[i] / criticalPhases[i]) - a * pow((devicePhaseDiff[i] / criticalPhases[i]),3));
    }

    return curr;
}



vector<double> current_v_phase(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents,
                               const vector<int> &vorticity_arr, const vector<double> &initialPhaseDiffs, double B) {
    vector<double> supercurrent_array;
    for (double phase : initialPhaseDiffs) {
        double curr = supercurrent(arrayOfWires, criticalPhases, criticalCurrents, vorticity_arr, phase, B);
        supercurrent_array.push_back(curr);
    }
    return supercurrent_array;
}

pair<vector<double>, vector<double>> MagField_v_Critical_Current(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents,
                                                                 const vector<int> &vorticity_arr, const vector<double> &initialPhaseDiffs, const vector<double> &MagField) {
    vector<double> I_c_max, I_c_min;

    for (double B : MagField) {
        vector<double> supercurrent_array = current_v_phase(arrayOfWires, criticalPhases, criticalCurrents, vorticity_arr, initialPhaseDiffs, B);
        supercurrent_array.erase(remove_if(supercurrent_array.begin(), supercurrent_array.end(), [](double x) { return isnan(x); }), supercurrent_array.end());

        if (!supercurrent_array.empty()) {
            I_c_max.push_back(*max_element(supercurrent_array.begin(), supercurrent_array.end()));
            I_c_min.push_back(*min_element(supercurrent_array.begin(), supercurrent_array.end()));
        } else {
            I_c_max.push_back(NAN);
            I_c_min.push_back(NAN);
        }
    }
    return {I_c_max, I_c_min};
}

vector<vector<tuple<double,double>>> calculate_kinetic_inductance(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents, const vector<int> &vorticity_arr, vector<double> phaseDiff, const vector<double> &MagField) {
    vector<vector<tuple<double,double>>> KI_I_values;
    for (double B : MagField) {
        vector<tuple<double,double>> KI_per_b = calculate_kinetic_inductance_per_mag(arrayOfWires, criticalPhases, criticalCurrents, vorticity_arr, phaseDiff, B);
        KI_I_values.push_back(KI_per_b);
    }  
    return KI_I_values;
}

vector<tuple<double,double>> calculate_kinetic_inductance_per_mag(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents, const vector<int> &vorticity_arr, vector<double> &phaseDiff, double B) {
    vector<tuple<double,double>> KI_per_b; 
    for (double phase : phaseDiff) {
        double KI_val = KI(arrayOfWires, criticalPhases, criticalCurrents, vorticity_arr, phase, B);
        double current = supercurrent(arrayOfWires, criticalPhases, criticalCurrents, vorticity_arr, phase, B);
        tuple<double,double> temp = make_tuple(KI_val, current);
        KI_per_b.push_back(temp);
    }
    return KI_per_b;
}

double KI(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents, const vector<int> &vorticity_arr, double phaseDiff, double B) {
    vector<double> devicePhaseDiff(arrayOfWires.size(), 0);
    double currPhaseDiff = phaseDiff;
    double KI_inv = 0;

    for (size_t i = 0; i < arrayOfWires.size() - 1; ++i) {
        devicePhaseDiff[i] = currPhaseDiff;
        devicePhaseDiff[i + 1] = currPhaseDiff + 2 * M_PI * B * (arrayOfWires[i + 1] - arrayOfWires[i]) - 2 * M_PI * vorticity_arr[i];
        currPhaseDiff = devicePhaseDiff[i+1];
    }

    for (int i = 0; i < arrayOfWires.size(); ++i) {
        if (abs(devicePhaseDiff[i]) > abs(criticalPhases[i])) {
            return NAN;
        }
    }
    double a = 0.3333;
    
    for (size_t i = 0; i < arrayOfWires.size(); ++i) {
        KI_inv += (criticalCurrents[i] * ((1.0/criticalPhases[i]) - a * 3.0/criticalPhases[i]*pow((devicePhaseDiff[i]/criticalPhases[i]),2)));
    }
    // if (std::abs(KI) < 5e-1) {
    //     return NAN; // or 0, or some sentinel value
    // }
    return 1.0 / KI_inv;
}


void save_vector_to_file(const string &filename, const vector<double> &vec) {
    ofstream file(filename);
    if (file.is_open()) {
        for (const auto &val : vec) {
            file << val << "\n";
        }
        file.close();
    }
}

void save_2d_vector_to_file(const string &filename, const vector<vector<double>> &matrix) {
    ofstream file(filename);
    if (file.is_open()) {
        for (const auto &row : matrix) {
            for (size_t i = 0; i < row.size(); ++i) {
                if (i != 0) file << ",";
                file << row[i];
            }
            file << "\n";
        }
        file.close();
    }
}

void save_2d_vector_to_file(const string &filename, const vector<vector<int>> &matrix) {
    ofstream file(filename);
    if (file.is_open()) {
        for (const auto &row : matrix) {
            for (size_t i = 0; i < row.size(); ++i) {
                if (i != 0) file << ",";
                file << row[i];
            }
            file << "\n";
        }
        file.close();
    }
}

std::string vectorToPythonSyntax(const std::vector<int>& vec) {
    std::string result = "[";
    for (size_t i = 0; i < vec.size(); ++i) {
        result += std::to_string(vec[i]);
        if (i < vec.size() - 1) {
            result += ", ";
        }
    }
    result += "]";
    return result;
}

void saveToCSV_tuple(const vector<vector<tuple<double, double>>>& KI_vn, const string& filename) {
    ofstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: Could not open " << filename << endl;
        return;
    }

    for (const auto& row : KI_vn) {
        for (size_t j = 0; j < row.size(); ++j) {
            auto [val1, val2] = row[j];
            file << val1 << "|" << val2; // or val2, depending on which you want
            if (j < row.size() - 1)
                file << ",";
        }
        file << "\n";
    }

    file.close();
}