#ifndef NANOWIRE_H
#define NANOWIRE_H

#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <filesystem>
#include <numeric>
#include <iomanip>
#include <set>

using namespace std;

vector<double> getArrayFromString(const string &input_string);
vector<int> int_getArrayFromString(const string &input_string);
void backtrackWithRepetitions(vector<int>& candidate_values, int num_of_values, int start, vector<int>& current_combination, vector<vector<int>>& result);
vector<vector<int>> getAllPermutationsWithRepetitions(vector<int>& candidate_values, int num_of_values);
vector<vector<int>> possibleSums(int target, vector<int> possible_values, int numOfLoops);
vector<vector<int>> arrayOfVorticityNumbers(int vn, const vector<int> vorticies, const vector<double> &arrayOfWires);
double supercurrent(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents, const vector<int> &vorticity_arr, double initialPhaseDiff, double B);
vector<double> current_v_phase(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents, const vector<int> &vorticity_arr, const vector<double> &initialPhaseDiffs, double B);
pair<vector<double>, vector<double>> MagField_v_Critical_Current(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents, const vector<int> &vorticity_arr, const vector<double> &initialPhaseDiffs, const vector<double> &MagField);
void save_vector_to_file(const string &filename, const vector<double> &vec);
void save_2d_vector_to_file(const string &filename, const vector<vector<double>> &matrix);
void save_2d_vector_to_file(const string &filename, const vector<vector<int>> &matrix);
std::string vectorToPythonSyntax(const std::vector<int>& vec);
vector<vector<tuple<double,double>>> calculate_kinetic_inductance(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents, const vector<int> &vorticity_arr, vector<double> phaseDiff, const vector<double> &MagField);
vector<tuple<double,double>> calculate_kinetic_inductance_per_mag(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents, const vector<int> &vorticity_arr, vector<double> &phaseDiff, double B);
double KI(const vector<double> &arrayOfWires, const vector<double> &criticalPhases, const vector<double> &criticalCurrents, const vector<int> &vorticity_arr, double phaseDiff, double B);
void saveToCSV_tuple(const vector<vector<tuple<double, double>>>& KI_vn, const string& filename);

#endif