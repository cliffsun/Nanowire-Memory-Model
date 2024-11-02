#include <iostream>
#include <cassert>
#include "model/nanowire.h"

using namespace std;

int main(int argc, char *argv[]) {
    if (argc < 2) {
        cout << "Usage: <arrayOfWires> <criticalPhases> optional: [vorticityStates...]\n";
        return -1;
    }

    string base_path = "src/csv/";

    string arrayOfWiresStr = argv[1];
    string criticalPhasesStr = argv[2];
    
    vector<double> arrayOfWires = getArrayFromString(arrayOfWiresStr);
    vector<double> criticalPhases = getArrayFromString(criticalPhasesStr);

    int bottom_vn = -5, upper_vn = 5;
    vector<vector<int>> vorticity_states;

    assert(arrayOfWires.size() == criticalPhases.size() && "Both arrays must be the same length");

    // Check if custom vorticity states are provided
    if (argc > 3) {
        for (int i = 3; i < argc; ++i) {
            string curr_vn = argv[i];
            vector<int> custom_vorticity = int_getArrayFromString(curr_vn);
            assert(custom_vorticity.size() == arrayOfWires.size() - 1 && "# of vorticity states must be (# wires - 1)");
            vorticity_states.push_back(custom_vorticity);
        }
    } else {
        // Default vorticity states generation
        vector<int> vorticities;
        for (int i = bottom_vn; i <= upper_vn; ++i) {
            vorticities.push_back(i);
        }
        for (int vn = bottom_vn; vn <= upper_vn; ++vn) {
            auto vorticity_arr = arrayOfVorticityNumbers(vn, vorticities, arrayOfWires);
            vorticity_states.insert(vorticity_states.end(), vorticity_arr.begin(), vorticity_arr.end());
        }
    }

    int discretations = 1000;
    vector<double> initialPhaseDiffs(discretations);
    vector<double> MagField(discretations);
    for (int i = 0; i < discretations; ++i) {
        initialPhaseDiffs[i] = -criticalPhases[0] + i * (2 * criticalPhases[0] / (discretations - 1));
        MagField[i] = -10 + i * (20.0 / (discretations - 1));
    }

    vector<vector<double>> I_c_max, I_c_min;

    for (const auto &vorticity_arr : vorticity_states) {
        auto [ic_max, ic_min] = MagField_v_Critical_Current(arrayOfWires, criticalPhases, vorticity_arr, initialPhaseDiffs, MagField);
        I_c_max.push_back(ic_max);
        I_c_min.push_back(ic_min);
    }

    save_2d_vector_to_file(base_path + "Ic_max.csv", I_c_max);
    save_2d_vector_to_file(base_path + "Ic_min.csv", I_c_min);
    save_2d_vector_to_file(base_path + "vorticies.csv", vorticity_states);

    return 0;
}