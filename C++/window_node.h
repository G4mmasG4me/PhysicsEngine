#pragma once
#include <vector>
#include <windows.h>
#include <string>

class Window_Node {
  public:
  // variables
    std::string name;
    HWND hwnd;
    COLORREF color;
    HBRUSH brush;
    UINT id;
    std::vector<Window_Node> children;
    std::string direction; // tb, bt, lr, rl
    float width;
    float height;
    float x;
    float y;

    // constructor
    Window_Node(std::string name, HWND hwnd, COLORREF color, HBRUSH brush, UINT id, std::vector<Window_Node> children, std::string direction, float width, float height, float x, float y);

    // functions
    Window_Node* search_tree(HWND hwnd);

    Window_Node* search_parent(HWND hwnd, Window_Node* parent = nullptr);

    void paint();
};

std::string horiz_or_vert(std::string direction);