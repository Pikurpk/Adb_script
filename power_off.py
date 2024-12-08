import subprocess

def shutdown_all_devices():
    # List all connected devices
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devices = [line.split()[0] for line in result.stdout.splitlines() if "\tdevice" in line]

    if not devices:
        print("No devices connected.")
        return

    print(f"Connected devices: {devices}")

    # Shut down each device
    for device_id in devices:
        print(f"Shutting down device: {device_id}")
        command = ["adb", "-s", device_id, "shell", "reboot", "-p"]
        try:
            subprocess.run(command, check=True)
            print(f"Device {device_id} is shutting down.")
        except subprocess.CalledProcessError:
            print(f"Failed to shut down device {device_id}.")

if __name__ == "__main__":
    shutdown_all_devices()
