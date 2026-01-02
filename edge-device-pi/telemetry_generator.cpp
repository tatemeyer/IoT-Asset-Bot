#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <ctime>
#include <unistd.h>
#include <iomanip>
#include <sstream>

// Convert time_t to ISO 8601 string
std::string getISO8601Timestamp() {
    std::time_t t = std::time(nullptr);
    std::tm tm = *std::gmtime(&t); // UTC time
    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y-%m-%dT%H:%M:%SZ");
    return oss.str();
}

void generateTelemetry(const std::string& filename) {
    std::ofstream file;
    file.open(filename, std::ios::app);

    if (file.is_open()) {
        // Schema fields
        int asset_id = 101; // Unique identifier
        float mileage = 5000.0f + static_cast<float>(rand() % 100); // Mileage
        int battery_health = 80 + (rand() % 20); // 0-100
        float usage_hours = 1200.0f + static_cast<float>(rand() % 10); // Usage hours
        std::string error_code = (rand() % 10 > 8) ? "FAIL" : "OK"; // System status
        std::string timestamp = getISO8601Timestamp(); // ISO 8601 timestamp

        // Write CSV line
        file << asset_id << ","
             << timestamp << ","
             << mileage << ","
             << battery_health << ","
             << usage_hours << ","
             << error_code << "\n";

        file.close();
        std::cout << "Telemetry recorded for Asset " << asset_id << std::endl;
    } else {
        std::cerr << "Failed to open file: " << filename << std::endl;
    }
}

int main() {
    srand(static_cast<unsigned int>(time(0)));
    while (true) {
        generateTelemetry("telemetry.csv");
        sleep(10); // Wait 10 seconds before next record
    }
    return 0;
}
