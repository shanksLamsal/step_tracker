import time
import csv
import os
from datetime import datetime

# Constants
STEP_LENGTH_FACTOR = 0.415  # step length = height * 0.415 (in meters)

# File name for logging
LOG_FILE = "walk_log.csv"

def get_user_data():
    print("=== Enter Your Information ===")
    age = int(input("Age (years): "))
    weight = float(input("Weight (kg): "))
    height = float(input("Height (cm): "))
    return age, weight, height

def get_met(speed_kph):
    if speed_kph < 3:
        return 2.0
    elif speed_kph < 5:
        return 2.8
    elif speed_kph < 6.5:
        return 3.5
    elif speed_kph < 7.5:
        return 4.3
    else:
        return 5.0

def calculate_calories_burned(met, weight_kg, duration_minutes):
    return met * weight_kg * (duration_minutes / 60)

def write_log(date, age, weight, height, duration, steps, distance_km, avg_speed, calories):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Age", "Weight (kg)", "Height (cm)", "Duration (min)",
                             "Total Steps", "Distance (km)", "Avg Speed (km/h)", "Calories Burned"])
        writer.writerow([date, age, weight, height, duration, steps, f"{distance_km:.2f}",
                         f"{avg_speed:.2f}", f"{calories:.2f}"])

def track_walk(age, weight, height_cm, duration_minutes=10, cadence_spm=100):
    total_steps = 0
    step_length_m = (height_cm / 100) * STEP_LENGTH_FACTOR

    print(f"\nTracking walk for {duration_minutes} minutes at {cadence_spm} steps/min...")
    print(f"Step length estimated at: {step_length_m:.2f} meters\n")

    for minute in range(duration_minutes):
        steps = cadence_spm
        total_steps += steps

        distance_m = steps * step_length_m
        speed_kph = (distance_m / 1000) / (1 / 60)  # km/h
        met = get_met(speed_kph)
        calories = calculate_calories_burned(met, weight, 1)

        print(f"Minute {minute + 1}:")
        print(f"  Steps taken: {steps}")
        print(f"  Speed: {speed_kph:.2f} km/h")
        print(f"  Calories burned: {calories:.2f} kcal\n")

        time.sleep(1)  # simulate real-time tracking

    total_distance_km = total_steps * step_length_m / 1000
    avg_speed = total_distance_km / (duration_minutes / 60)
    total_calories = calculate_calories_burned(get_met(avg_speed), weight, duration_minutes)

    print("=== Summary ===")
    print(f"Total steps: {total_steps}")
    print(f"Total distance: {total_distance_km:.2f} km")
    print(f"Average speed: {avg_speed:.2f} km/h")
    print(f"Total calories burned: {total_calories:.2f} kcal")

    # Log the results
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_log(today, age, weight, height_cm, duration_minutes, total_steps,
              total_distance_km, avg_speed, total_calories)

    print(f"Session logged to '{LOG_FILE}'.")

# Main program
if __name__ == "__main__":
    age, weight, height = get_user_data()
    track_walk(age, weight, height, duration_minutes=5, cadence_spm=110)
