import struct
#import math

class FH5Telemetry:
    def __init__(self):
        self.packet_size = 324

    def parse_packet(self, packet):
        if len(packet) != self.packet_size:
            print(f"Warning: Packet size mismatch: expected {self.packet_size}, got {len(packet)}")
            return None

        try:
            current_engine_rpm = struct.unpack('<f', packet[16:20])[0]
            # spd = struct.unpack('<f', packet[256:260])[0]
            power_hp = struct.unpack('<f', packet[260:264])[0]
            torque_ftlb = struct.unpack('<f', packet[264:268])[0]

            power_test = power_hp / 745.7
            torque_test = torque_ftlb * 0.73756
            #spd_set = spd * 2.23694
            #spd_test = math.ceil(spd_set)

            #print(f"{current_engine_rpm} | {spd_test} | {p_test} | {t_test}")
            if power_test and torque_test > 0:
                return {
                    'rpm': current_engine_rpm,
                    'power': power_hp / 745.7,
                    'torque': torque_ftlb * 0.73756
                }

        except struct.error as e:
            print(f"Error parsing packet: {e}")
            return None

