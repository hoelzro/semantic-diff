def get_prefix(a, b):
    prefix = []

    for element_a, element_b in zip(a, b):
        if element_a == element_b:
            prefix.append(element_a)
        else:
            break
    return prefix

# inefficient
def get_suffix(a, b):
    return list(reversed(get_prefix(reversed(a), reversed(b))))

def build_lcs_matrix(a, b):
    matrix = [0] * (len(a) + 1) * (len(b) + 1);
    row_len = len(a) + 1

    for row in range(1, len(b) + 1):
        for offset in range(1, len(a) + 1):
            index = row * row_len + offset # inefficient
            if a[offset - 1] == b[row - 1]:
                matrix[index] = matrix[index - row_len - 1] + 1
            else:
                matrix[index] = max(matrix[index - row_len], matrix[index - 1])

    return matrix

def lcs(a, b):
    prefix = get_prefix(a, b)
    suffix = get_suffix(a, b)
    a_middle = a[len(prefix):len(a)-len(suffix)]
    b_middle = b[len(prefix):len(b)-len(suffix)]

    if a_middle and b_middle:
        matrix = build_lcs_matrix(a_middle, b_middle)
        row_len = len(a_middle) + 1
        i = len(matrix) - 1
        result = []

        while i > 0 and matrix[i] > 0:
            current_length  = matrix[i]
            next_row_length = matrix[i - row_len]
            next_col_length = matrix[i - 1]

            if current_length > next_row_length and next_row_length == next_col_length:
                result.append(b_middle[i / row_len - 1])
                i -= (row_len + 1)
            elif next_row_length < next_col_length:
                i -= 1
            elif next_col_length <= next_row_length:
                i -= row_len
            else:
                assert False, 'I should never reach this point'
        return prefix + list(reversed(result)) + suffix
    else:
        return prefix + suffix

