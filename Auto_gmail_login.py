import uiautomator2 as u2
import time
import subprocess

# Specify the ADB path
adb_path = r"C:\auto\platform-tools\adb.exe"

# Function to get connected devices
def get_connected_devices():
    try:
        result = subprocess.run(
            [adb_path, "devices"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        devices = []
        for line in result.stdout.splitlines()[1:]:
            if "\tdevice" in line:
                devices.append(line.split("\t")[0])
        return devices
    except Exception as e:
        print(f"Error fetching devices: {e}")
        return []

# Function to log in to Google Play Store (UI automation)
def login_to_play_store(device_id, email, password):
    print(f"Connecting to device: {device_id}")
    d = u2.connect(device_id)

    # Launch Google Play Store
    print("Launching Google Play Store...")
    d.app_start("com.android.vending")
    time.sleep(5)  # Wait for the Play Store to load

    # Check if the sign-in button exists
    if d(text="Sign in").exists(timeout=10):
        d(text="Sign in").click()
        time.sleep(5)  # Wait for the sign-in page to load
    else:
        print(f"Sign-in button not found on device: {device_id}")
        return

    # Debugging: Dump the UI to check for the email field
    print("Dumping UI hierarchy to inspect the layout...")
    print(d.dump_hierarchy())

    # Enter the email
    print("Entering email...")
    if d(resourceId="identifierId").exists(timeout=10):
        d(resourceId="identifierId").set_text(email)
        d(text="Next").click()
        time.sleep(5)
    elif d(className="android.widget.EditText").exists(timeout=10):
        d(className="android.widget.EditText").set_text(email)
        d(text="Next").click()
        time.sleep(5)
    else:
        print(f"Email field not found on device: {device_id}")
        return

    # Enter the password
    print("Entering password...")
    if d(resourceId="com.google.android.gms:id/password").exists(timeout=10):
        d(resourceId="com.google.android.gms:id/password").set_text(password)
    elif d(className="android.widget.EditText").exists(timeout=10):
        d(className="android.widget.EditText").set_text(password)
    else:
        print("Password field not found! Dumping UI hierarchy for debugging...")
        print(d.dump_hierarchy())  # Debugging output
        return

    # Click Next
    if d(text="Next").exists(timeout=10):
        d(text="Next").click()
        time.sleep(5)
    else:
        print("Next button not found!")
        return

    # Confirm login
    print("Completing login process...")
    if d(text="I agree").exists(timeout=10):
        d(text="I agree").click()
        time.sleep(5)

    print(f"Login completed on device: {device_id}")

# Main function to detect devices, prompt for credentials, and log in
def main():
    # Prompt for Gmail credentials
    email = input("Enter your Gmail email: ")
    password = input("Enter your Gmail password: ")

    # Get the list of connected devices
    devices = get_connected_devices()
    if not devices:
        print("No devices connected. Please check your ADB connections.")
        return

    print(f"Connected devices: {devices}")

    # Log in to Google Play Store on each device
    for device_id in devices:
        login_to_play_store(device_id, email, password)

if __name__ == "__main__":
    main()
