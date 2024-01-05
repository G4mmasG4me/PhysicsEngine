#include <string>
#include <iostream>

class Measurement
{
  public:
    float value;
    std::string type;

    Measurement(std::string input) {
      
      for (char c : input) {
        if (std::isdigit(c) || c == '.') {
          digits += c;
        }
        else {
          non_digits += c;
        }
      };
      if (non_digits != "%" && non_digits != "px") {
        std::cout << "Error" << std::endl;
      }
      this->value = stof(digits);
      this->type = non_digits;
    }
  private:
    std::string digits;
    std::string non_digits;
};


int main() {
  Measurement my_measurement("15px");
  std::cout << "Value: " << my_measurement.value << " | Type: " << my_measurement.type << std::endl;
}
