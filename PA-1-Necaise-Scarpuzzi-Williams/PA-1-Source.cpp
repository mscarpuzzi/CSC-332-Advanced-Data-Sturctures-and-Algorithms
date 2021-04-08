// Team-Necaise-Scarpuzzi-Williams
// Advanced Data Structures
// PA-1
// GCD, four ways
#include <fstream>
#include <cstdlib>
#include <chrono>
#include <vector>
#include <algorithm>

using namespace std;

constexpr auto rand_seed = 42;
constexpr auto iterations = 1000;
constexpr auto max_value = 10000000;

// Runtime statistic info
struct Time_Info {
	int max_time = 0;
	int min_time = max_value;
	int sum = 0;
	vector<int> run_time;
};

ofstream open_and_prep_results(const char[]);
int time_and_output(int (*)(int, int), int, int, ofstream&);
void update_time_info(Time_Info &, int);
void output_stats(const char[], Time_Info);
int bf_v1(int, int);
int bf_v2(int, int);
int oe(int, int);
int se(int, int);

int main() 
{
	srand(rand_seed);

	// Open and initialize results files.
	auto bf_v1_results = open_and_prep_results("BF_v1_Results.csv");
	auto bf_v2_results = open_and_prep_results("BF_v2_Results.csv");
	auto oe_results = open_and_prep_results("OE_Results.csv");
	auto se_results = open_and_prep_results("SE_Results.csv");


	// Hold execution time info for later processing.
	Time_Info bf_v1_info, bf_v2_info, oe_info, se_info;

	// Generate and check 1000 random numbers pairs.
	for (auto i = 0; i < iterations; ++i) {
		auto number_one = rand() % max_value;
		auto number_two = rand() % max_value;

		// Ensure no zeros were generated
		while (!number_one || !number_two) {
			number_one = rand() % max_value;
			number_two = rand() % max_value;
		}

		int time;
		
		// Call fuction to time and output to .csv file.
		time = time_and_output(bf_v1, number_one, number_two, bf_v1_results);
		update_time_info(bf_v1_info, time);
		
		time = time_and_output(bf_v2, number_one, number_two, bf_v2_results);
		update_time_info(bf_v2_info, time);
		
		time = time_and_output(oe, number_one, number_two, oe_results);
		update_time_info(oe_info, time);
		
		time = time_and_output(se, number_one, number_two, se_results);
		update_time_info(se_info, time);
	}

	// Create statistics files
	output_stats("BF_v1_Statisticts.csv", bf_v1_info);
	output_stats("BF_v2_Statisticts.csv", bf_v2_info);
	output_stats("OE_Statisticts.csv", oe_info);
	output_stats("SE_Statisticts.csv", se_info);

	// Close output files.
	bf_v1_results.close();	
	bf_v2_results.close();	
	oe_results.close();	
	se_results.close();
		
	return EXIT_SUCCESS;
}


// Input: Name of file to create
// Returns: Filestream object open for writing
ofstream open_and_prep_results(const char name[])
{
	ofstream file;
	file.open(name);

	file << "Number One, Number Two, Their GCD, Time Spent (Nanoseconds)" << endl;

	return file;
}


// Input: Function to test, two numbers to test, filestream object for output
// Output: CSV file with two numbers, their gcd, and execution time
// Returns: Execution time
int time_and_output(int (*gcd_func)(int, int), 
					int number_one, 
					int number_two, 
					ofstream& file)
{
		
	// Time the execution.
	auto start = chrono::high_resolution_clock::now();
	auto gcd = gcd_func(number_one, number_two);
	auto stop = chrono::high_resolution_clock::now();
	auto elapsed = chrono::duration_cast<chrono::nanoseconds>(stop - start);
	
	file << number_one << ", " << number_two << ", " 
		<< gcd << ", " << elapsed.count() << endl;

	return (int)elapsed.count();
}

// Input: Time_Info for a function, execution time
// Updates: Execution time
void  update_time_info(Time_Info &time_info, int time) {
	// Update maximum runtime
	if (time_info.max_time < time) {
		time_info.max_time = time;
	}
	
	// Update minimum runtime
	if (time_info.min_time > time) {
		time_info.min_time = time;
	}

	// Data for final anaylsis
	time_info.sum += time;
	time_info.run_time.push_back(time);
	
}

// Input: Filename to open, Time_Info of coresponding function
// Output: Statistics of function execution to .csv
void output_stats(const char name[], Time_Info time_info)
{
	ofstream file;
	file.open(name);

	sort(time_info.run_time.begin(), time_info.run_time.end());

	auto median = (time_info.run_time[iterations / 2 - 1] + 
				   time_info.run_time[iterations / 2]) / 2;

	file << "Statistics, Nanoseconds" << endl
		<< "Maximum Time, " << time_info.max_time << endl
		<< "Minimum Time, " << time_info.min_time << endl
		<< "Average Time, "	<< time_info.sum / iterations << endl
		<< "Median Time, " << median << endl;

	file.close();
}

// Input: Two intergers
// Return: GCD of inputs found by Brute Force v1
int bf_v1(int number_one, int number_two)
{
	// Stop at lower of given numbers	.
	auto stop = number_one < number_two ? number_one : number_two;
	auto gcd = 1;
	
	// Start at 2 and check all numbers up to stop.
	// Record any that divide both numbers evenly.
	for (auto i = 2; i <= stop; ++i) {
		if (number_one % i == 0 && number_two % i == 0) {
			gcd = i;
		}
	}

	return gcd;
}

// Input: Two intergers
// Return: GCD of inputs found by Brute Force v2
int bf_v2(int number_one, int number_two) 
{
	// Use smaller given number as first divisor.
	auto divisor = number_one < number_two ? number_one : number_two;

	// Run until dividor divides both evenly, decreasing by one each time.
	while (number_one % divisor != 0 || number_two % divisor != 0) {
		--divisor;
	}

	return divisor;
}

// Input: Two intergers
// Return: GCD of inputs found by Original Euclid algorithm
int oe(int number_one, int number_two)
{
	int remainder;

	do {
		remainder = number_one % number_two;
		number_one = number_two;
		number_two = remainder;
	} while (remainder);

	return number_one;
}

// Input: Two intergers
// Return: GCD of inputs found by Extended Euclid Algorithm.
int se(int number_one, int number_two)
{
	// Ensure number_one >= number_two
	if (number_two > number_one) {
		auto temp = number_one;
		number_one = number_two;
		number_two = temp;
	}

	int remainder;

	do {
		remainder = number_one - number_two;
		if (remainder >= number_two) {
			remainder -= number_two;
			if (remainder >= number_two) {
				remainder -= number_two;
				if (remainder >= number_two) {
					remainder = number_one % number_two;
				}
			}
		}
		number_one = number_two;
		number_two = remainder;
	} while (remainder);

	return number_one;
}