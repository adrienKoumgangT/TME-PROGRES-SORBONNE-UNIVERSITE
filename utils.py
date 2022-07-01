import socket
import struct

header_struct = struct.Struct('>i')


def diff_time(time_begin, time_end):
    r = 0
    h = 0
    m = 0
    try:
        milliseconds = int(time_end[9:]) - int(time_begin[9:])
        seconds = int(time_end[6:8]) - int(time_begin[6:8])
        if seconds < 0:
            seconds += 60
            m = 1
        minutes = int(time_end[3:5]) - int(time_begin[3:5]) - m
        if minutes < 0:
            minutes += 60
            h = 1
        hours = int(time_end[0:2]) - int(time_begin[0:2]) - h
        if hours < 0:
            hours *= -1
            r = 1
        return [hours, minutes, seconds, milliseconds, r]
    except ValueError:
        return []


def diff_localtime(time_begin, time_end):
    r = 0
    h = 0
    m = 0
    seconds = time_end.tm_sec - time_begin.tm_sec
    if seconds < 0:
        seconds += 60
        m = 1
    minutes = time_end.tm_min - time_begin.tm_min - m
    if minutes < 0:
        minutes += 60
        h = 1
    hours = time_end.tm_hour - time_begin.tm_hour - h
    if hours < 0:
        hours *= -1
        r = 1
    return [hours, minutes, seconds, r]


def receive_all(sock, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with %d bytes left'
                           ' in this block', format(length))
        length -= len(block)
        blocks.append(block)
    return b''.join(blocks)


def put_block(sock, message):
    block_length = len(message)
    sock.sendall(header_struct.pack(block_length))
    sock.sendall(message)


def get_block(sock):
    data = receive_all(sock, header_struct.size)
    (block_length, ) = header_struct.unpack(data)
    return receive_all(sock, block_length)
