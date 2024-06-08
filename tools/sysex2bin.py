import os
import re
import sys
import argparse


def read_txt(filename):
    with open(filename) as f:
        txt = f.read()
        syx = bytes([int(s, 16) for s in re.findall(r'[\da-f]{2}', txt, re.M | re.I)])
        sysexs = re.findall(rb'\xf0[\x00-\x7f]+\xf7', syx)
        return sysexs


def read_syx(filename):
    with open(filename, 'rb') as f:
        syx = f.read()
        sysexs = re.findall(rb'\xf0[\x00-\x7f]+\xf7', syx)
        return sysexs


def read_mid(filename):
    with open(filename, 'rb') as f:
        mid = f.read()
        sysexs = [f0 + left for f0, left in re.findall(rb'(\xf0)[\x80-\xff]*[\x00-\x7f]([\x00-\x7f]+\xf7)', mid)]
        return sysexs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='SYSEX_FILE', help='An input file containing SysExs received from modified SC-55')
    parser.add_argument('output', metavar='MCU_BIN', nargs='?', default='mcu.bin', help='SC-55 MCU firmware file recovered from SysExs')
    parser.add_argument('--type', choices=['txt', 'syx', 'mid'], help='Input file type')
    args = parser.parse_args()

    readers = {
        'txt': read_txt,
        'syx': read_syx,
        'mid': read_mid,
    }

    type = args.type if args.type != None else os.path.splitext(args.input)[1][1:]
    if type not in readers:
        sys.exit('Use "--type" to specify the type of input file')

    sysexs = readers[type](args.input)
    if len(sysexs) == 0:
        sys.exit(f'No valid SysEx in {args.input}')

    rom = bytearray()
    for sysex in sysexs:
        hexstr = ' '.join([f'{b:02x}' for b in sysex])
        f0, mfr, dev, mdl, cmd, addr_h, addr_m, addr_l = sysex[:8]
        payload = sysex[8:-2]

        assert f0 == 0xf0
        if mfr != 0x41 or not (0x10 <= dev <= 0x1f) or mdl != 0x42 or cmd != 0x12:
            sys.exit(f'Invalid SysEx: {hexstr}')
        if addr_h != 0x48 or addr_m != 0x7f or addr_l != 0x7f:
            print(f'Warning: Unexpected address: {hexstr}', file=sys.stderr)
        if not all([0x00 <= b <= 0x0f for b in payload]):
            sys.exit(f'Invalid payload: {hexstr}')
        if sum(sysex[5:-1]) & 0x7f != 0x00:
            sys.exit(f'Check sum error: {hexstr}')

        for i in range(0, len(payload), 2):
            rom.append((payload[i] << 4) | payload[i + 1])

    if len(rom) != 32768:
        print(f'Warning: The size of the generated MCU firmware file is not 32KB: {len(rom)}', file=sys.stderr)

    with open(args.output, 'wb') as f:
        f.write(rom)


if __name__ == '__main__':
    main()
