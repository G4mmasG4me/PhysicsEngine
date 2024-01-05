#define UNICODE

#include <windows.h>
#include <iostream>
#include <vector>
#include <commdlg.h> // Include for common dialog functions
#include <string>
#include <cmath>
#include "window_node.h"
#pragma comment(lib, "comdlg32.lib") // Link with the comdlg32 library

HWND file_button;

HWND button_1;
std::vector<int> button_1_size = {100,50};
HWND button_2;
std::vector<int> button_2_size = {100,50};

const wchar_t main_window_class_name[] = L"mainWindowClass";
const wchar_t sub_window_class_name[] = L"subWindowClass";

#define IDC_FILE_BUTTON 1001
#define IDC_BUTTON_1 1002
#define IDC_BUTTON_2 1003

#define UNICODE

int screen_width;
int screen_height;

int width, height;

wchar_t szFile[260];

int edgeThreshold = 10;
int xPos;
int yPos;
HCURSOR waitCursor = LoadCursor(NULL, IDC_HAND);
HCURSOR sizensCursor = LoadCursor(NULL, IDC_SIZENS);
HCURSOR sizeweCursor = LoadCursor(NULL, IDC_SIZEWE);

// define windows
Window_Node child_node_1("child 1", {}, RGB(100,50,50), CreateSolidBrush(RGB(100,50,50)), 2, {}, "h", 0.5, 1, 0, 0);
Window_Node child_node_2("child 2", {}, RGB(50,100,50), CreateSolidBrush(RGB(50,100,50)), 3, {}, "h", 0.5, 1, 0.5, 0);

Window_Node root_node("root", {}, RGB(50,50,50), CreateSolidBrush(RGB(50,50,50)), 1, {child_node_1, child_node_2}, "h", 400, 400, 0, 0);



HWND child_hwnd;

CREATESTRUCT* pCreate;

RECT rect;

bool resizing = FALSE;
// sub window process
LRESULT CALLBACK SubWindowProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
  PAINTSTRUCT ps;
  HDC hdc;
  Window_Node* node;
  Window_Node* parent_node;
  Window_Node* parent_parent_node;

  int index, parent_index;
  std::vector<Window_Node*> node_siblings(4, nullptr); // left, right, top, bottom

  int xPos, yPos;


  switch (msg) {
    
    case WM_CREATE:
      
      pCreate = reinterpret_cast<CREATESTRUCT*>(lParam);
      node = reinterpret_cast<Window_Node*>(pCreate->lpCreateParams);
      node->hwnd = hwnd;
      // paint
      if (node != nullptr) {
        // node->paint();
        hdc = BeginPaint(hwnd, &ps);
        GetClientRect(hwnd, &rect);
        FillRect(hdc, &rect, node->brush);
        EndPaint(hwnd, &ps);
      };
      break;
    case WM_PAINT:
      node = root_node.search_tree(hwnd);
      if (node != nullptr) {
        hdc = BeginPaint(hwnd, &ps);
        GetClientRect(hwnd, &rect);
        FillRect(hdc, &rect, node->brush);
        EndPaint(hwnd, &ps);
      };
      break;
    case WM_SIZE:
      break;
    case WM_COMMAND:
      break;
    case WM_LBUTTONDOWN:
      std::cout << "Pressed hwnd" << std::endl;
      node = root_node.search_tree(hwnd);
      break;
    case WM_MOUSEMOVE:
      node_siblings = {nullptr, nullptr, nullptr, nullptr}; // left, right, top, bottom
      xPos = LOWORD(lParam); 
      yPos = HIWORD(lParam); 

      // get sibling children
      parent_node = root_node.search_parent(hwnd);

      // find index of current hwnd
      for (int i = 0; i < parent_node->children.size(); i++) {
        if (parent_node->children[i].hwnd == hwnd) {
          index = i;
          break;
        }
      }
      // get siblings
      if (index != 0) { // gets first sibling
        if (parent_node->direction == "h") {
          node_siblings[0] = (&parent_node->children[index-1]);
        }
        else if (parent_node->direction == "v") {
          node_siblings[2] = (&parent_node->children[index-1]);
        }
        
      }
      if (index+1 <= parent_node->children.size()-1) { // gets second sibling
        if (parent_node->direction == "h") {
          node_siblings[1] = (&parent_node->children[index+1]);
        }
        else if (parent_node->direction == "v") {
          node_siblings[3] = (&parent_node->children[index+1]);
        }
      }
      // get parents siblings
      parent_parent_node = root_node.search_parent(parent_node->hwnd);

      if (parent_parent_node != nullptr && parent_parent_node->direction != parent_node->direction) {
        // find index of parent in parents siblings
        for (int i = 0; i < parent_parent_node->children.size(); i++) {
          if (parent_parent_node->children[i].hwnd == parent_node->hwnd) {
            parent_index = i;
            break;
          }
        }
        // gets upper sibling
        if (parent_index != 0) {
          if (parent_parent_node->direction == "h") {
            node_siblings[0] = (&parent_parent_node->children[parent_index-1]);
          }
          else if (parent_parent_node->direction == "v") {
            node_siblings[2] = (&parent_parent_node->children[parent_index-1]);
          }
        }
        // gets lower sibling
        if (parent_index+1 <= parent_parent_node->children.size()-1) {
          if (parent_parent_node->direction == "h") {
            node_siblings[1] = (&parent_parent_node->children[parent_index+1]);
          }
          else if (parent_parent_node->direction == "v") {
            node_siblings[3] = (&parent_parent_node->children[parent_index+1]);
          }
        }
      }
      break;
    default:
      return DefWindowProc(hwnd, msg, wParam, lParam);
  }
  return 0;
};

// main window process
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
  switch(msg)
  {
    case WM_CREATE:
    {
      Window_Node* node;
      pCreate = reinterpret_cast<CREATESTRUCT*>(lParam);
      node = reinterpret_cast<Window_Node*>(pCreate->lpCreateParams);
      node->hwnd = hwnd;

      RECT clientRect;

      GetClientRect(hwnd, &clientRect);

      int clientWidth = clientRect.right - clientRect.left;
      int clientHeight = clientRect.bottom - clientRect.top;
      
      /* // Create the menu bar
      HMENU hMenu = CreateMenu();

      // Create "File" menu
      HMENU hSubMenu = CreatePopupMenu();
      AppendMenuW(hSubMenu, MF_STRING, 101, L"New");
      AppendMenuW(hSubMenu, MF_STRING, 102, L"Open");
      AppendMenuW(hSubMenu, MF_STRING, 103, L"Save");
      AppendMenuW(hSubMenu, MF_SEPARATOR, 0, NULL);o .
      AppendMenuW(hSubMenu, MF_STRING, 104, L"Exit");
      AppendMenuW(hMenu, MF_POPUP, (UINT_PTR)hSubMenu, L"File");

      // Attach the menu bar to the window
      SetMenu(hwnd, hMenu); */

      // create sub windows
      for (int i = 0; i < node->children.size(); i++) {
        int x = node->width * node->children[i].x;
        int y = node->height * node->children[i].y;
        int width = node->width * node->children[i].width;
        int height = node->height * node->children[i].height;

        rect.left = x;
        rect.right = x + width;

        rect.top = y;
        rect.bottom = y + height;

        AdjustWindowRect(&rect, WS_CHILD, FALSE);

        x = rect.left;
        y = rect.top;
        width = rect.right - rect.left;
        height = rect.bottom - rect.top;
        child_hwnd = CreateWindowExW(0, sub_window_class_name, L"Name", WS_CHILD | WS_VISIBLE, x, y, width, height, hwnd, (HMENU)(INT_PTR)node->children[i].id, NULL, &(node->children[i]));
      }
      break;
    }

    case WM_COMMAND:
      switch (LOWORD(wParam))
      {
        case IDC_BUTTON_1:
          std::cout << "button 1" << std::endl;
          break;
        case IDC_BUTTON_2:
          std::cout << "button 2" << std::endl;
          break;
        case 101: // Open
          OPENFILENAMEW ofn;
          szFile[260] = { 0 };

          ZeroMemory(&ofn, sizeof(ofn));
          ofn.lStructSize = sizeof(ofn);
          ofn.hwndOwner = hwnd;
          ofn.lpstrFile = szFile;
          ofn.nMaxFile = sizeof(szFile);
          ofn.lpstrFilter = L"All Files\0*.*\0";
          ofn.nFilterIndex = 1;
          ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;

          if (GetOpenFileNameW(&ofn) == TRUE)
          {
            MessageBoxW(hwnd, ofn.lpstrFile, L"File Selected", MB_OK);
          }
          break;
        case 102: // Save
          MessageBoxW(hwnd, L"Save clicked!", L"Info", MB_OK);
          break;
        case 103: // Exit
          DestroyWindow(hwnd);
          break;
      }
      break;

    case WM_SIZE:
      width = LOWORD(lParam);  // New width of the client area
      height = HIWORD(lParam);

      // set root node width and height;
      root_node.width = width;
      root_node.height = height;

      for (int i = 0; i < root_node.children.size(); i++) {
        int x = std::round(root_node.width * root_node.children[i].x);
        int y = std::round(root_node.height * root_node.children[i].y);
        int width = std::round(root_node.width * root_node.children[i].width);
        int height = std::round(root_node.height * root_node.children[i].height);
        SetWindowPos(root_node.children[i].hwnd, HWND_TOP, x, y, width, height, SWP_NOZORDER);
        // InvalidateRect(root_node.children[i].hwnd, NULL, TRUE);
      };
      std::cout << "Width: " << width << " | Height: " << height << std::endl;
      break;

    // resize containers
    case WM_LBUTTONDOWN:
      break;
    case WM_LBUTTONUP:
      break;
    case WM_MOUSELEAVE:
      break;
    case WM_CLOSE:
      DestroyWindow(hwnd);
    break;
    case WM_DESTROY:
      PostQuitMessage(0);
    break;
    default:
      return DefWindowProc(hwnd, msg, wParam, lParam);
  }
  return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
  LPSTR lpCmdLine, int nCmdShow)
{
  // main window class
  WNDCLASSEXW wc;
  HWND hwnd;
  MSG Msg;
  wc.cbSize        = sizeof(WNDCLASSEXW);
  wc.style         = CS_OWNDC;
  wc.lpfnWndProc   = WndProc;
  wc.cbClsExtra    = 0;
  wc.cbWndExtra    = 0;
  wc.hInstance     = hInstance;
  wc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
  wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
  wc.hbrBackground = (HBRUSH)(COLOR_WINDOW);
  wc.lpszMenuName  = NULL;
  wc.lpszClassName = main_window_class_name;
  wc.hIconSm       = LoadIcon(NULL, IDI_APPLICATION);
  RegisterClassExW(&wc);

  // sub window class
  WNDCLASSEX swc;
  swc.cbSize        = sizeof(WNDCLASSEXW);
  swc.style         = 0;
  swc.lpfnWndProc   = SubWindowProc; // Assign your custom window procedure
  swc.cbClsExtra    = 0;
  swc.cbWndExtra    = 0;
  swc.hInstance     = hInstance;
  swc.hIcon         = LoadIcon(NULL, IDI_APPLICATION);
  swc.hCursor       = LoadCursor(NULL, IDC_ARROW);
  swc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
  swc.lpszMenuName  = NULL;
  swc.lpszClassName = sub_window_class_name;
  swc.hIconSm       = LoadIcon(NULL, IDI_APPLICATION);
  RegisterClassExW(&swc);


  RECT mainRect = {0, 0, 400, 400};

  AdjustWindowRect(&mainRect, WS_OVERLAPPEDWINDOW, FALSE);

  int width = mainRect.right - mainRect.left;
  int height = mainRect.bottom - mainRect.top;

  // create main window
  hwnd = CreateWindowExW(
    0,
    main_window_class_name,
    L"The title of my window",
    WS_OVERLAPPEDWINDOW,
    CW_USEDEFAULT, CW_USEDEFAULT, mainRect.right-mainRect.left, mainRect.bottom-mainRect.top,
    NULL, NULL, hInstance, &root_node);
  
  ShowWindow(hwnd, nCmdShow);
  // UpdateWindow(hwnd);

  // Step 3: The Message Loop
  while(GetMessage(&Msg, NULL, 0, 0) > 0)
  {
    TranslateMessage(&Msg);
    DispatchMessage(&Msg);
  }
  return Msg.wParam;
}