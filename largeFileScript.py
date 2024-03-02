def create_large_txt_file(filename, size_in_mb):
    num_chars = int(size_in_mb * 1e6)
    with open(filename, 'w') as f:
        f.write('0' * num_chars)


if __name__ == '__main__':
    create_large_txt_file('large.txt', 30)