from dataclasses import dataclass

@dataclass
class Packet:
    source_ip: str
    dest_ip: str
    payload: str
    priority: int 


def fifo_scheduler(packet_list: list) -> list:
   return packet_list[:]  


def priority_scheduler(packet_list: list) -> list:
    return sorted(packet_list, key=lambda pkt: pkt.priority)


if __name__ == "__main__":
    packets = [
        Packet("10.0.0.1", "10.0.0.2", "Data Packet 1", 2),
        Packet("10.0.0.1", "10.0.0.2", "Data Packet 2", 2),
        Packet("10.0.0.3", "10.0.0.4", "VOIP Packet 1", 0),
        Packet("10.0.0.5", "10.0.0.6", "Video Packet 1", 1),
        Packet("10.0.0.7", "10.0.0.8", "VOIP Packet 2", 0),
    ]

    fifo_result = [p.payload for p in fifo_scheduler(packets)]
    priority_result = [p.payload for p in priority_scheduler(packets)]

    print("FIFO Scheduler Order:", fifo_result)
    print("Priority Scheduler Order:", priority_result)
