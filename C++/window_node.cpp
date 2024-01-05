#include <string>
#include <vector>
#include <windows.h>
#include "window_node.h"
#include <iostream>


Window_Node::Window_Node(std::string name, HWND hwnd, COLORREF color, HBRUSH brush, UINT id, std::vector<Window_Node> children, std::string direction, float width, float height, float x, float y) {
  this->name = name;
  this->hwnd = hwnd;
  this->color = color;
  this->brush = brush;
  this->id = id;
  this->children = children;
  this->direction = direction;
  this->width = width;;
  this->height = height;
  this->x = x;
  this->y = y;
}

Window_Node* Window_Node::search_tree(HWND target_hwnd) {
  if (target_hwnd == this->hwnd) {
    return this;
  }
  for (int i = 0; i < this->children.size(); i++) {
    Window_Node* node = this->children[i].search_tree(target_hwnd);
    if (node != nullptr) {
      return node;
    }
  }
  return nullptr;
}

Window_Node* Window_Node::search_parent(HWND target_child_hwnd, Window_Node* parent) {
  if (target_child_hwnd == this->hwnd) {
    return parent;
  }
  for (int i = 0; i < this->children.size(); i++) {
    Window_Node* node = this->children[i].search_parent(target_child_hwnd, this);
    if (node != nullptr) {
      return node;
    }
  }
  return nullptr;
}

void Window_Node::paint() {
  PAINTSTRUCT ps;
  RECT rect;
  HDC hdc = BeginPaint(hwnd, &ps);
  GetClientRect(this->hwnd, &rect);
  FillRect(hdc, &rect, this->brush);

  EndPaint(hwnd, &ps);
}