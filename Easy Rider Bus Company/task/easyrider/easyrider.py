import json
import random
import re
import string


class Parser:

    bus_id = 0
    stop_id = 0
    stop_name = 0
    next_stop = 0
    stop_type = 0
    a_time = 0

    lines = {"id_128": 0, "id_256": 0, "id_512": 0, "id_1024": 0}

    stops = {}
    times = {}
    on_demand = set()
    all_stops = set()

    def handle_dict(self, jdata):
        """
        Main function to handle the json structure
        :param jdata:
        :return:
        """
        for dict in jdata:
            for k, v in dict.items():
                if k == "bus_id":
                    id = v
                    if not isinstance(v, int):
                        self.bus_id += 1
                elif k == "stop_id":
                    stop_id = v
                    if not isinstance(v, int):
                        self.stop_id += 1
                elif k == "stop_name":
                    stop_name = v
                    if not isinstance(v, str):
                        self.stop_name += 1
                    else:
                        self.check_stop_name(v)
                elif k == "next_stop":
                    if not isinstance(v, int):
                        self.next_stop += 1
                elif k == "stop_type":
                    stop_type = v
                    if not isinstance(v, str):
                        self.stop_type += 1
                    else:
                        self.check_stop_type(v)
                elif k == "a_time":
                    a_time = v
                    if not isinstance(v, str):
                        self.a_time += 1
                    else:
                        self.check_time(v)

    def check_stop_name(self, stop_name):
        """
        Check the names of the stops
        :param stop_name:
        :return:
        """
        string_lst = ['Road$', 'Avenue$', 'Boulevard$', 'Street$']
        if re.search(r"(?=("+'|'.join(string_lst)+r"))", stop_name) is None:
            self.stop_name += 1
        elif stop_name[0].islower():
            self.stop_name += 1
        elif len(stop_name.split(" ")) == 1:
            self.stop_name += 1

    def check_stop_type(self, stop_type):
        """
        Check the names of the stops
        :param stop_type:
        :return:
        """
        if stop_type != "S" and stop_type != "F" and stop_type != "O" and stop_type != "":
            self.stop_type += 1

    def check_time(self, a_time):
        """
        Check time format
        :param a_time:
        :return:
        """
        if not re.match("^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", a_time):
            self.a_time += 1

    def check_lines(self, v):
        if v == 128:
            self.lines["id_128"] += 1
        elif v == 256:
            self.lines["id_256"] += 1
        elif v == 512:
            self.lines["id_512"] += 1
        else:
            self.lines["id_1024"] += 1

    def update_stops(self, k, stop_type, stop_name):
        if k not in self.stops:
            self.stops[k] = {}
        if stop_type in self.stops[k]:
            stop_type = random.choice(string.ascii_lowercase)
        self.stops[k][stop_type] = stop_name

    def check_stops(self):
        empty = False
        for k, info in self.stops.items():
            for _ in info:
                if "S" not in info or "F" not in info:
                    print(f"There is no start or end stop for the line: {k}.")
                    empty = True
                break
        if empty is False:
            self.print_stops()

    def update_times(self, k, a_time, stop_name):
        if k not in self.times:
            self.times[k] = {}

        self.times[k][stop_name] = a_time

    def check_times(self):
        print("Arrival time test:")
        incorrect = False
        for k, info in self.times.items():
            times = []
            names = []
            for key, value in info.items():
                names.append(key)
                times.append(value)
            for i in range(0, len(times) - 1):
                if times[i] > times[i + 1]:
                    print(f"bus_id line {k}: "
                          f"wrong time on station {names[i + 1]}")
                    incorrect = True
                    break
        if incorrect is False:
            print("OK")

    def print_stops(self):
        starts = set()
        transfer = {}
        finish = set()

        for k, info in self.stops.items():
            for key in info:
                if info[key] in transfer:
                    transfer[info[key]] += 1
                else:
                    transfer[info[key]] = 1
                if key == 'S':
                    starts.add(info[key])
                elif key == 'F':
                    finish.add(info[key])
        transfer_set = set()
        for k, v in transfer.items():
            if v > 1:
                transfer_set.add(k)

        print(f"Start stops: {len(starts)} {sorted(starts)}")
        print(f"Transfer stops: {len(transfer_set)} {sorted(transfer_set)}")
        print(f"Finish stops: {len(finish)} {sorted(finish)}")

    def collect_stops(self, stop_name, stop_type):
        if stop_type == 'O':
            self.on_demand.add(stop_name)
        else:
            self.all_stops.add(stop_name)

    def checkOnDemand(self):
        wrong = [name for name in self.all_stops if name in self.on_demand]
        print("On demand stops test:")
        if len(wrong) == 0:
            print("OK")
        else:
            print(f"Wrong stop type: {sorted(wrong)}")

    def print_result(self):
        tot_count = self.a_time + self.bus_id + self.stop_id + \
                    self.stop_type + self.next_stop + self.stop_name
        print(f"Type and required field validation: {tot_count} errors")

        print(f"bus_id: {self.bus_id}")
        print(f"stop_id: {self.stop_id}")
        print(f"stop_name: {self.stop_name}")
        print(f"next_stop: {self.next_stop}")
        print(f"stop_type: {self.stop_type}")
        print(f"a_time: {self.a_time}")

    def print_result_validation(self):
        tot_count = self.a_time + self.stop_type + self.stop_name
        print(f"Format validation: {tot_count} errors")

        print(f"stop_name: {self.stop_name}")
        print(f"stop_type: {self.stop_type}")
        print(f"a_time: {self.a_time}")

    def print_lines(self):
        print("Line names and number of stops:")
        print(f"bus_id: 128, stops: {self.lines['id_128']}")
        print(f"bus_id: 256, stops: {self.lines['id_256']}")
        print(f"bus_id: 512, stops: {self.lines['id_512']}")
        if self.lines['id_1024'] > 0:
            print(f"bus_id: 1024, stops: {self.lines['id_1024']}")


def main():
    pars = Parser()
    s = input()
    jdata = json.loads(s)
    pars.handle_dict(jdata)

    # Choose the function
    # pars.checkOnDemand()


if __name__ ==  '__main__':
    main()