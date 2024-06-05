# Reads a data file, returning the data as a numpy array

from numpy import array

def read(file: str) -> tuple[list[int], list[str]]:
    data = []
    metadata = []
    with open(file, 'r') as f:
        for line in f:

            # Gets each item
            splits = line.split(',', 4)

            # Converts first two items to integers
            splits[0] = int(splits[0])
            splits[1] = int(splits[1])

            # Adds the data to the arrays
            data.append(array(splits[:2]))
            metadata.append(array(splits[2:]))

    return array(data), array(metadata)