import numpy as np
import time

# Define the incident ray, normal, and angles
incident = np.array([1, -1, 0])  # Example values
normal = np.array([0, 1, 0])  # Example values
theta_r = np.arcsin(1/1.5)  # Example for n1=1 (air) and n2=1.5 (glass)

# Ensure normalization
incident = incident / np.linalg.norm(incident)
normal = normal / np.linalg.norm(normal)

# Method 1: Using trigonometric functions directly
def method1(incident, normal, theta_r):
    return np.sin(theta_r) * np.cross(-normal, np.cross(incident, normal)) + np.cos(theta_r) * (-normal)

# Method 2: Provided equation
def method2(incident, normal, theta_r):
    # Assuming theta_1 and theta_2 are known from Snell's law
    sin_theta_2 = np.sin(theta_r)  # Directly using theta_r for simplicity
    cos_theta_1 = -np.dot(incident, normal)
    t = 1 / 1.5  # n1/n2 for air to glass
    return t * incident + (t * cos_theta_1 - np.sqrt(1 - sin_theta_2**2)) * normal

# Timing setup
num_iterations = 100000

# Test Method 1
start_time = time.time()
for _ in range(num_iterations):
    result1 = method1(incident, normal, theta_r)
method1_time = time.time() - start_time

# Test Method 2
start_time = time.time()
for _ in range(num_iterations):
    result2 = method2(incident, normal, theta_r)
method2_time = time.time() - start_time

# Print results
print("Method 1 Time:", method1_time)
print("Method 2 Time:", method2_time)

# Compare and print which method is faster
if method1_time < method2_time:
    print("Method 1 is faster.")
else:
    print("Method 2 is faster.")