# A quick little logging tool
class Logger:
    def __init__(self) -> None:
        
        # Keeps track of files that have been written to
        # Used to clear "a" files on first write
        self.wrote = []


    # Logs data it is passed, overwriting the file
    def log(self, file, *datas):
        
        # Location of the logs directory
        loc = 'logs'

        # Writes the data to the file
        # The data is overwritten
        with open(f'{loc}/{file}.txt', 'w') as f:
            for data in datas:
                for line in data:
                    f.write(line)
                f.write('\n\n-----------------\n\n\n')

    # Logs data is is passed, appending it to the file
    def loga(self, file, datum, clear = True):
        
        # Location of the logs directory
        loc = 'logs'

        # On first write, clear the file
        flag = 'a'
        if clear and file not in self.wrote:
            self.wrote.append(file)
            flag = 'w'

        # Write the data
        with open(f'{loc}/{file}.txt', flag) as f:
            f.write(f'{datum}\n')


# Globally accessible
logger = Logger()