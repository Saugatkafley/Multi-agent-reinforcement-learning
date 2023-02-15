import random
import numpy as np

# Set the simulation parameters
arrival_rate = 1.0 / 6.0  # One part every 6 minutes
inspection_time_mean_A = 4.0  # Mean inspection time for type A parts (minutes)
inspection_time_std_A = 2.0  # Standard deviation of inspection time for type A parts (minutes)
inspection_time_mean_B = 20.0  # Mean inspection time for type B parts (minutes)
inspection_time_std_B = 10.0  # Standard deviation of inspection time for type B parts (minutes)
rejection_rate = 0.1  # 10% rejection rate
num_parts = 50  # Number of type A parts to simulate

# Initialize variables to track statistics
idle_time_inspector_A = 0.0  # Idle time for inspector A (minutes)
idle_time_inspector_B = 0.0  # Idle time for inspector B (minutes)
total_time_in_system = 0.0  # Total time spent in the system by all parts (minutes)

# Simulate the system
time = 0.0  # Current time in the simulation (minutes)
num_accepted_A = 0  # Number of type A parts that have been accepted
while num_accepted_A < num_parts:
    # Generate a random arrival time for the next part
    arrival_time = random.expovariate(arrival_rate)
    time += arrival_time
    
    # Determine if the part is type A or B
    if random.uniform(0, 1) < 0.9:
        # Type A part
        inspector = "A"
        inspection_time = np.random.normal(inspection_time_mean_A, inspection_time_std_A)
        
        # Check if the part is rejected
        if random.uniform(0, 1) < rejection_rate:
            continue  # Reject the part and move on to the next one
    else:
        # Type B part
        inspector = "B"
        inspection_time = np.random.normal(inspection_time_mean_B, inspection_time_std_B)
        
        # Check if the part is rejected
        if random.uniform(0, 1) < rejection_rate:
            continue  # Reject the part and move on to the next one
    
    # Update the idle time for the inspector
    if inspector == "A":
        idle_time_inspector_A += time - arrival_time
    else:
        idle_time_inspector_B += time - arrival_time
    
    # Update the total time in the system for the part
    total_time_in_system += time - arrival_time + inspection_time
    
    # Update the number of accepted type A parts
    if inspector == "A":
        num_accepted_A += 1

# Calculate the average time in the system
average_time_in_system = total_time_in_system / num_parts

# Print the results
print(f"Idle time for inspector A: {idle_time_inspector_A} ")