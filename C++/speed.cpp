#include <chrono>
#include <iostream>

using namespace std;

class Point_3D_1 {
  public:
    float x, y, z;

    Point_3D_1(float x, float y, float z) {
      this->x = x;
      this->y = y;
      this->z = z;
    }
};

class Point_3D_2 {
  public:
    float x, y, z;
    Point_3D_2(float x, float y, float z) : x(x), y(y), z(z) {}
};

class Point_3D_3 {
  public:
    float x, y, z;
    Point_3D_3(float a, float b, float c) {
      x = a;
      y = b;
      z = c;
    }
};

void function1() {
  Point_3D_1 my_point(10,5,3);
}
void function2() {
  Point_3D_2 my_point(10,5,3);
}
void function3() {
  Point_3D_3 my_point(10,5,3);
}

int main() {
  int run_amount;
  std::cout << "Enter the value for run_amount: ";
  std::cin >> run_amount;

  auto start1 = std::chrono::high_resolution_clock::now();
  for (int i = 0; i < run_amount; i++) {
    function1();
  }
  auto end1 = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> duration1 = end1 - start1;
  std::cout << "1 Execution time: " << duration1.count() << " seconds" << std::endl;


  auto start2 = std::chrono::high_resolution_clock::now();
  for (int i = 0; i < run_amount; i++) {
    function2();
  }
  auto end2 = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> duration2 = end2 - start2;
  std::cout << "2 Execution time: " << duration2.count() << " seconds" << std::endl;


  auto start3 = std::chrono::high_resolution_clock::now();
  for (int i = 0; i < run_amount; i++) {
    function3();
  }
  auto end3 = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> duration3 = end3 - start3;
  std::cout << "3 Execution time: " << duration3.count() << " seconds" << std::endl;

  return 0;
}