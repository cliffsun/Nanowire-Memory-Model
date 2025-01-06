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

    double curr = 0;
    for (int i = 0; i < numOfWires; ++i) {
        curr += criticalCurrents[i] * devicePhaseDiff[i] / criticalPhases[i];
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
