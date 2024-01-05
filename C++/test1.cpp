// main.cpp
#include <iostream>
#include "test.h"

int main() {
    // Create an instance of MyClass
    MyClass obj(10, 20);

    // Use the member function add()
    int result = obj.add(obj.x, obj.y);
    std::cout << "The sum of " << obj.x << " and " << obj.y << " is " << result << std::endl;

    return 0;
}