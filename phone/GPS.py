import gps
import time
from geopy.distance import geodesic  # To calculate distance between two points

# Coordinates for Home and Destination (use actual coordinates)
home_coords = (12.9715987, 77.5945627)  # Replace with actual home GPS coordinates
destination_coords = (12.935192, 77.624481)  # Replace with actual destination coordinates

# Tolerance in meters (for deviation alert)
deviation_threshold = 50

def get_current_location():
    # Connect to the GPS daemon
    session = gps.gps(mode=gps.WATCH_ENABLE)
    while True:
        try:
            report = session.next()
            if report['class'] == 'TPV':
                lat = getattr(report, 'lat', 0.0)
                lon = getattr(report, 'lon', 0.0)
                return (lat, lon)
        except KeyError:
            pass
        except KeyboardInterrupt:
            break
        except StopIteration:
            session = None
            print("GPSD has terminated")
            break
        time.sleep(1)

def check_deviation(current_coords, path_coords):
    distance_to_home = geodesic(current_coords, home_coords).meters
    distance_to_destination = geodesic(current_coords, destination_coords).meters
    
    if distance_to_home <= deviation_threshold or distance_to_destination <= deviation_threshold:
        return False  # No deviation
    return True  # Deviated from path

if __name__ == "__main__":
    while True:
        current_location = get_current_location()
        print(f"Current Location: {current_location}")
        
        if check_deviation(current_location, [home_coords, destination_coords]):
            print("You have deviated from the path!")
            # Add code to send an alert (e.g., SMS via SIM module)
        else:
            print("You are on the correct path.")
        
        time.sleep(5)
