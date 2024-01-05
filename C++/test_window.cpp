#include <windows.h>
#include <iostream>

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR pCmdLine, int nCmdShow)
{
    // The window class
    WNDCLASSEX wc;

    // Fill in the struct with the needed information
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = CS_OWNDC;
    wc.lpfnWndProc = WindowProc;
    wc.cbClsExtra = 0;
    wc.cbWndExtra = 0;
    wc.hInstance = hInstance;
    wc.hIcon = NULL;
    wc.hCursor = NULL;
    wc.hbrBackground = (HBRUSH)COLOR_WINDOW;
    wc.lpszMenuName = NULL;
    wc.lpszClassName = "MyWindowClass";
    wc.hIconSm = NULL;

    // Register the window class
    RegisterClassEx(&wc);

    // Calculate dimensions to make the client area the size we want
    RECT wr = {0, 0, 400, 400};
    AdjustWindowRect(&wr, WS_OVERLAPPEDWINDOW, FALSE);

    // Create the window and use the result as the handle
    HWND hwnd = CreateWindowExW(
        0,                              // Optional extended window style
        L"MyWindowClass",                // Window class
        L"A 400x400 Window",             // Window title
        WS_OVERLAPPEDWINDOW,            // Window style
        CW_USEDEFAULT, CW_USEDEFAULT,   // Window initial position
        wr.right - wr.left,             // Width
        wr.bottom - wr.top,             // Height
        NULL,                           // Parent window
        NULL,                           // Menu
        hInstance,                      // Instance handle
        NULL                            // Additional application data
    );

    if (hwnd == NULL)
    {
        return 0;
    }

    // Show the window
    ShowWindow(hwnd, nCmdShow);

    // Message loop
    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    switch (uMsg)
    {
        case WM_CREATE:
          RECT rect;
          GetClientRect(hwnd, &rect);
          std::cout << "Width: " << rect.right - rect.left << " | Height: " << rect.bottom - rect.top << std::endl;
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;

        case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            // Painting code here

            EndPaint(hwnd, &ps);
        }
        return 0;
    }

    // Handle any messages the switch statement didn't
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}