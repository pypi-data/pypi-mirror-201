
def format_bytes(size, data_format):
    if not data_format in ['b', 'Kb', 'Mb', 'Gb', 'Tb']: return size
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : 'b', 1: 'Kb', 2: 'Mb', 3: 'Gb', 4: 'Tb'}
    while power_labels[n] != data_format:
        size /= power
        n += 1
    return round(size, 1)

