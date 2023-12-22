import wifi

def scan_wifi_networks():
    cells = wifi.Cell.all('wlan0')
    for cell in cells:
        print(f"SSID: {cell.ssid}, Signal Strength: {cell.signal}")

if __name__ == "__main__":
    scan_wifi_networks()
