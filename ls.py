#!/usr/bin/env python3

import os
from pathlib import Path


def __get_closest_factor(target, number):
    for i in range(number):
        if number % (target + i) == 0:
            return target + 1
        elif number % (target - i) == 0:
            return target - 1
    return number


def __get_correct_rows(rows, column_count):
    norm = __get_closest_factor(rows // (column_count), rows)
    less = __get_closest_factor(rows // (column_count - 1), rows)
    if less == norm or less < column_count:
        return column_count
    return less if less % column_count == 0 else norm


def _get_extra_items(items, column_count):
    extra_items = []
    if len(items) % column_count == 0:
        return items, extra_items, column_count
    for i, v in enumerate(items[::-1]):
        if (len(items) - i) % column_count == 0:
            break
        extra_items.insert(0, v)
    rows = (len(items) - len(extra_items)) // column_count

    last_col_rows = __get_correct_rows(rows, column_count)
    for i, v in enumerate(items[: -len(extra_items)][::-1]):
        if i in range(last_col_rows):
            extra_items.insert(0, v)
    return items, extra_items, column_count


def _make_table(items, extra_items, column_count):
    output = [[] for _ in range(column_count)]
    counter = 0
    for i, v in enumerate(items[: -len(extra_items)] if extra_items else items):
        output[counter].append(v)
        if (i + 1) % ((len(items) - len(extra_items)) // column_count) == 0:
            counter += 1
    if extra_items:
        output.append(extra_items)
    return output, len(extra_items)


def _get_spaces_count(items, row, column):
    return len(max(items[column], key=len)) + 2 - len(items[column][row])


def _get_column_count(items):
    return os.get_terminal_size().columns // len(max(items, key=len))


def fprint_list(items, column_count=1):
    output, remaining = _make_table(*_get_extra_items(sorted(items), column_count))

    for row in range(len(output[0])):
        for column in range(column_count + (1 if remaining >= 1 else 0)):
            print(output[column][row], end=" " * _get_spaces_count(output, row, column))
        remaining -= 1
        print()


def main(items):
    return fprint_list(items, _get_column_count(items))

if __name__ == "__main__":
    import sys
    main(
        # os.listdir(os.path.abspath((Path(input()) or Path(__file__).parent)))
        os.listdir(sys.argv[1])
    )
