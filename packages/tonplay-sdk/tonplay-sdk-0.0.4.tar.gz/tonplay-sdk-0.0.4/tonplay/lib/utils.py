import base64

from tonplay.error import ParameterValueError


def check_enum_parameter(value, enum_class):
    if value not in set(item.name for item in enum_class):
        raise ParameterValueError([value])


bounceable_tag, non_bounceable_tag = b'\x11', b'\x51'
b64_abc = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890+/')
b64_abc_urlsafe = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-')


def check_ton_address(address, argument_name):
    if set(address).issubset(b64_abc):
        address_bytes = base64.b64decode(address.encode('utf8'))
    elif set(address).issubset(b64_abc_urlsafe):
        address_bytes = base64.urlsafe_b64decode(address.encode('utf8'))
    else:
        raise Exception(f"{argument_name} Not an address")
    if not calcCRC(address_bytes[:-2]) == address_bytes[-2:]:
        raise Exception(f"{argument_name} Wrong checksum")


def calcCRC(message):
    poly = 0x1021
    reg = 0
    message += b'\x00\x00'
    for byte in message:
        mask = 0x80
        while(mask > 0):
            reg <<= 1
            if byte & mask:
                reg += 1
            mask >>= 1
            if reg > 0xffff:
                reg &= 0xffff
                reg ^= poly
    return reg.to_bytes(2, "big")
