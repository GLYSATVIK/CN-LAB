# ip_utils.py

def ip_to_binary(ip_address: str) -> str:
    octets = ip_address.split('.')
    binary_octets = [format(int(octet), '08b') for octet in octets]
    return ''.join(binary_octets)


def get_network_prefix(ip_cidr: str) -> str:
    ip, prefix_length = ip_cidr.split('/')
    prefix_length = int(prefix_length)
    binary_ip = ip_to_binary(ip)
    return binary_ip[:prefix_length]
