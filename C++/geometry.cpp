#include <math.h>


class Point_3D {
  public:
    float x, y, z;

    Point_3D(float x, float y, float z) {
      this->x = round(x * 1e16) / 1e16;
      this->y = round(y * 1e16) / 1e16;
      this->z = round(z * 1e16) / 1e16;
    }

    Point_3D operator+(const Point_3D& other) const {
      return Point_3D(x + other.x, y + other.y, z + other.z);
    }
    Point_3D operator-(const Point_3D& other) const {
      return Point_3D(x - other.x, y - other.y, z - other.z);
    }
    Point_3D operator*(const Point_3D& other) const {
      return Point_3D(x * other.x, y * other.y, z * other.z);
    }
    Point_3D operator/(const Point_3D& other) const {
      return Point_3D(x / other.x, y / other.y, z / other.z);
    }
};


class Point_2D {
  public:
    float x, y;

    Point_2D(float x, float y) {
      this->x = round(x * 1e16) / 1e16;
      this->y = round(y * 1e16) / 1e16;
    }

    Point_2D operator+(const Point_3D& other) const {
      return Point_2D(x + other.x, y + other.y);
    }
    Point_2D operator-(const Point_3D& other) const {
      return Point_2D(x - other.x, y - other.y);
    }
    Point_2D operator*(const Point_3D& other) const {
      return Point_2D(x * other.x, y * other.y);
    }
    Point_2D operator/(const Point_3D& other) const {
      return Point_2D(x / other.x, y / other.y);
    }
};