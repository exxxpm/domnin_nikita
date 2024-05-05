#include <iostream>
#include <random>
#include <bitset>

using namespace std;

string generateUniqueBinarySequence() {
    random_device device;
    mt19937_64 generator(device());
    uniform_int_distribution<unsigned long long> distribution;

    string binarySequence;
    binarySequence.reserve(128);

    for (int i = 0; i < 2; ++i) {
        unsigned long long randomNumber = distribution(generator);
        binarySequence += std::bitset<64>(randomNumber).to_string();
    }

    return binarySequence;
}

int main() {
    string uniqueBinarySequence = generateUniqueBinarySequence();
    cout << "Unique binary sequence: " << uniqueBinarySequence << endl;
    return 0;
}