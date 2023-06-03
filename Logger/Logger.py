from datetime import datetime


class Logger(object):

    def __init__(self, file_base_name: str, topics: list):
        self._file_base_name = file_base_name
        self._topics = topics
        self._filename = self._file_base_name + "_" + datetime.now().isoformat(timespec='seconds').replace("-", "_").replace(":", "_") + ".csv"
        # writing the topics header
        with open(self._filename, "w") as f:
            f.write("timestamp")
            for t in topics:
                f.write(f",{t}")
            f.write("\n")


    def log(self, data: list):
        with open(self._filename, "a") as f:
            f.write(datetime.now().isoformat(sep=" ", timespec="seconds"))
            for d in data:
                f.write(f",{d}")
            f.write("\n")
