import threading, time
import queue

ext = 0


class Process:
    __p_count = 1

    def __init__(self, *args):
        """
        :param args:[arrival_time, dead_line, burst_time, priority]
        """
        self.__id = Process.__p_count
        Process.__p_count += 1
        self.__arrival_time = args[0]
        self.__dead_line = args[1]
        self.__burst_time = args[2]
        self.__priority = args[3]

    def is_consistent(self):
        return self.__dead_line >= self.__arrival_time + self.__burst_time

    def getArrivalTime(self):
        return self.__arrival_time

    def getDeadline(self):
        return self.__dead_line

    def getBurstTime(self):
        return self.__burst_time

    def getPriority(self):
        return self.__priority

    def getName(self):
        return "Process" + str(self.__id)

    def __str__(self):
        return "Process " + str(self.__id) + ":\n Arrival : " + str(self.__arrival_time) + " Priority : " + str(
            self.__priority) + " Burst Time : " + str(self.__burst_time) + " Dead Line : " + str(
            self.__dead_line) + "\n"


class Server(threading.Thread):
    turn_around = 0

    def __init__(self, id, name, q):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.q = q

    def run(self) -> None:
        print("Starting " + self.name)
        serve_process(self.name, self.q)
        print("Exiting " + self.name)
        # print(Server.turn_around)


def serve_process(name, q):
    global t_time
    while not ext:
        queuelock.acquire()
        if not ProcessQueue.empty():
            next = q.get()
            queuelock.release()
            print("%s is processing %s\n" % (name, next.getName()))
            t_time += next.getArrivalTime() + next.getBurstTime()
        else:
            queuelock.release()
        time.sleep(1)
        # return t_time


if __name__ == '__main__':
    t_time = 0
    with open('ep1.txt', 'r') as file:
        file_input = [i.strip() for i in file.readlines()]
        print(file_input)
        n, m = tuple(map(int, file_input[0].split()))
        process = []
        for i in range(n):
            p = Process(
                *tuple(
                    map(int, file_input[i + 1].split())))
            if p.is_consistent():
                process.append(p)

        process = sorted(process, key=lambda i: (i.getArrivalTime(), i.getPriority()) if i.getPriority() > 1 else (
            (i.getArrivalTime(), i.getPriority() + 2) if i.getPriority() == 1 else (
                i.getArrivalTime(), i.getPriority() + 5)))  # Sort the processes

        print("listing down all the consistent processes: ", *process, sep="\n")

        ProcessQueue = queue.Queue(len(process))
        queuelock = threading.Lock()

        servers = []

        # Creating new servers
        for cnt in range(1, m + 1):
            server = Server(cnt, "server" + str(cnt), ProcessQueue)
            server.start()
            servers.append(server)
        # fill in the process queue
        queuelock.acquire()
        for p in process:
            ProcessQueue.put(p)
        queuelock.release()

        # Wait for all the process to be completed
        while not ProcessQueue.empty():
            pass

        # Notify all the servers that all the process have been served
        ext = 1

        for s in servers:
            s.join()
        print("No. of successful completion : ", len(process))
        print("Average turn around time : ", t_time // len(process))
        print("Task Completed.\nAborting...")
