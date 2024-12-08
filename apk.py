import subprocess

# Path to adb executable and APK file
adb_path = r"C:\auto\platform-tools\adb"
apk_path = r"P:\apk\instagram.apk"


# Get list of connected devices
def get_connected_devices():
    try:
        result = subprocess.run([adb_path, 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip()

        # Parse device IDs from the adb devices output
        devices = []
        for line in output.splitlines():
            if '\tdevice' in line:
                device_id = line.split()[0]
                devices.append(device_id)
        return devices
    except Exception as e:
        print(f"Error getting devices: {e}")
        return []


# Install APK on each device
def install_apk(devices, apk_path):
    for device in devices:
        try:
            print(f"Installing APK on device: {device}")
            result = subprocess.run([adb_path, '-s', device, 'install', apk_path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                print(f"APK installed successfully on {device}")
            else:
                print(f"Failed to install APK on {device}: {result.stderr}")
        except Exception as e:
            print(f"Error installing APK on {device}: {e}")


if __name__ == "__main__":
    devices = get_connected_devices()
    if devices:
        install_apk(devices, apk_path)
    else:
        print("No devices connected.")
