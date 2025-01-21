import socket
import keyboard
import matplotlib.pyplot as plt
from fh5_telemetry import FH5Telemetry
import numpy as np

def generate_dyno_graph(data_points):
    rpm = [data['rpm'] for data in data_points]
    power = [data['power'] for data in data_points]
    torque = [data['torque'] for data in data_points]

    sorted_data = sorted(zip(rpm, power, torque))
    rpm_sorted, power_sorted, torque_sorted = zip(*sorted_data)

    plt.figure(figsize=(10, 6))
    plt.plot(rpm_sorted, power_sorted, label="Horsepower (HP)", color="red")
    plt.plot(rpm_sorted, torque_sorted, label="Torque (ft-lb)", color="blue")
    plt.title("Dyno Graph")
    plt.xlabel("RPM")
    plt.ylabel("Horsepower / Torque")
    plt.legend()
    plt.grid(True)

    max_rpm = max(rpm_sorted)
    x_ticks = np.arange(0, (max_rpm // 1000 + 1) * 1000, 500)
    y_ticks = np.arange(0, max(max(power_sorted), max(torque_sorted)) + 50, 50)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    plt.show()


def main():
    udp_ip = "127.0.0.1"
    udp_port = 5300
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    print(f"Listening for telemetry on {udp_ip}:{udp_port}")

    telemetry = FH5Telemetry()
    recording = False
    data_points = []
    last_f2_state = False

    print("Press 'F2' to start/stop recording. Press 'Esc' to exit.")

    while True:
        if keyboard.is_pressed("Esc"):
            print("Exiting...")
            break

        f2_pressed = keyboard.is_pressed("F2")
        if f2_pressed and not last_f2_state:
            recording = not recording
            print("Recording started." if recording else "Recording stopped.")
            if not recording and data_points:
                generate_dyno_graph(data_points)
                data_points = []
        last_f2_state = f2_pressed

        if recording:
            try:
                packet, _ = sock.recvfrom(1024)
                telemetry_data = telemetry.parse_packet(packet)
                if telemetry_data:
                    data_points.append(telemetry_data)
            except Exception as e:
                print(f"Error processing packet: {e}")

if __name__ == "__main__":
    main()
