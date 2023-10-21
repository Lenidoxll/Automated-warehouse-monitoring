from datetime import datetime, timedelta
from random import randint, uniform
from config import path_lib
from Task import TaskQueue
import websockets
import asyncio

uri = "ws://75.119.142.124:8001/ws"
class Path:
    """
    Path class.
    Store all attributes and methods of specific path from warehouse map
    """

    def __init__(self,
                 path_id: int
                 ):
        self.id = path_id  # unique id of the path
        self.target_rack_id = path_lib[self.id]["target_rack_id"]  # target rack in warehouse
        self.path_sequence = (path for path in path_lib[self.id][
            "path_sequence"])  # sequence of control points with their id, names and distance
        pass

    def get_next_checkpoint(self):
        # iterate over checkpoints forward
        try:
            point = self.path_sequence.__next__()
        # but when catch StopIteration exception revert points sequence and continue to iterate backward
        except StopIteration:
            self.path_sequence = (path for path in path_lib[self.id]["path_sequence"][::-1])
            raise StopIteration("You have reach the end of the path, time to solve your task and go back")
        else:
            return point


class Forklift:

    async def connect_to_server(self, uri):
        while True:
            try:
                self.websocket = await websockets.connect(uri)
                return self.websocket
            except websockets.exceptions.WebSocketException:
                print("WebSocket connection failed. Retrying...")
                await asyncio.sleep(5)

    async def send_message_to_server(self, message):
        while True:
            try:
                if not self.websocket:
                    await self.connect_to_server(uri)
                await self.websocket.send(message)
                response = await self.websocket.recv()
                print(f"Server response: {response}")
                break
            except websockets.exceptions.ConnectionClosedError:
                print("WebSocket connection closed. Reconnecting...")
                self.websocket = None 
    """
    Forklift class.
    Represents one specific forklift on warehouse
    """

    def __init__(self, forklift_id: int, warehouse_id: int, task_queue: TaskQueue):
        self.id = forklift_id  # unique id of forklift
        # random date of last maintenance
        self.last_service_date = datetime.today() - timedelta(days=(randint(10, 173)))
        self.warehouse_id = warehouse_id
        self.task_queue = task_queue
        self.task = None  # current task
        self.status = "chill"  # current status
        self.current_path = None
        self.path_direction = None  # path direction, if forward - forklift go to target, if bask - go to start point
        self.current_point = None
        self.next_point = None
        self.next_point_time = None
        self.speed = uniform(0.9, 1.1)  # random speed in m/s
        self.websocket = None  # Соединение будет храниться здесь


    def get_task(self):
        # method to get new task, if forklift is free and chilling
        self.task = self.task_queue.get_task()
        if self.task:
            asyncio.get_event_loop().run_until_complete(self.send_message_to_server(f"START;{self.id};{self.warehouse_id};{self.task.id};K1;{datetime.now()}"))
            print(
                f"Forklift #{self.id} of warehouse #{self.warehouse_id} "
                f"have started the task #{self.task.id} "
                f"at {datetime.now()}")
            self.task.start()  # change task status, maybe needed later. Or not =)
            self.current_path = Path(self.task.path_id)  # get Path object
            self.current_point = self.current_path.get_next_checkpoint()  # and first point
            asyncio.get_event_loop().run_until_complete(self.send_message_to_server(f"WORK;{self.id};{self.warehouse_id};{self.task.id};{self.current_point['check_point_name']};{datetime.now()}"))
            print(
                f"Forklift #{self.id} of warehouse #{self.warehouse_id} "
                f"have reach the point {self.current_point['check_point_name']} "
                f"at {datetime.now()}")
            self.next_point = self.current_path.get_next_checkpoint()  # get next point to know were to go
            self.next_point_time = datetime.now() + timedelta(
                seconds=self.current_point['next_check_point_distance'] / self.speed)  # calculate time to next point
            self.path_direction = "forward"
            self.status = 'working'
        else:
            pass
            # there can be message that there is no tasks in queue, but it's annoying
            # print(f"TaskQueue of warehouse #{self.warehouse_id} is empty "
            #       f"Forklift #{self.id} stay chill")
        if self.task.id == 42:
            print(f"Forklift #{self.id} say: 'Hmm.. seems like I found the answer to life the universe and everything'")

    def work(self):
        # first of all check status
        if self.status == 'chill':
            # if forklift chilling we need to make it work. We need, really?
            self.get_task()
        if self.status == 'working':
            # if forklift have next_point_time attribute - it have next point to go
            if self.next_point_time:
                # check if forklift reach the next point by time
                if datetime.now() > self.next_point_time:
                    # if forklift have next point - then let it go
                    if self.next_point:
                        asyncio.get_event_loop().run_until_complete(self.send_message_to_server(f"WORK;{self.id};{self.warehouse_id};{self.task.id};{self.next_point['check_point_name']};{datetime.now()}"))
                        print(
                            f"Forklift #{self.id} of warehouse #{self.warehouse_id} "
                            f"have reach the point {self.next_point['check_point_name']} "
                            f"at {datetime.now()}")
                        # reassign next point to current
                        self.current_point = self.next_point
                        # and try to get next point
                        try:
                            self.next_point = self.current_path.get_next_checkpoint()
                            # calculate next point time
                            self.next_point_time = datetime.now() + timedelta(
                                seconds=self.current_point['next_check_point_distance'] / self.speed)
                        except StopIteration:
                            # if there is no more points and forklift go forward - it reach the target
                            if self.path_direction == "forward":
                                asyncio.get_event_loop().run_until_complete(self.send_message_to_server(f"WORK;{self.id};{self.warehouse_id};{self.task.id};{self.current_path.target_rack_id};{datetime.now()}"))
                                print(
                                    f"Forklift #{self.id} of warehouse #{self.warehouse_id} "
                                    f"have reach the target {self.current_path.target_rack_id} "
                                    f"at {datetime.now()}")
                                # set time of solving the task (load or unload target rack)
                                self.next_point_time = datetime.now() + timedelta(seconds=self.task.execution_time)
                                # and get next point (now Path iterator set to backward mode)
                                self.next_point = self.current_path.get_next_checkpoint()
                                self.path_direction = "back"
                            # but if it was back path, it means that forklift reach warehouse gate
                            elif self.path_direction == "back":
                                # set time to finish the task and a little rest
                                self.next_point_time = datetime.now() + timedelta(seconds=uniform(3, 5))
                                # and make next_point None, to reach next else condition next time
                                self.next_point = None
                    # if we reach this else condition then forklift finish the task
                    else:
                        asyncio.get_event_loop().run_until_complete(self.send_message_to_server(f"FINISH;{self.id};{self.warehouse_id};{self.task.id};K1;{datetime.now()}"))                    
                        print(
                            f"Forklift #{self.id} of warehouse #{self.warehouse_id} "
                            f"have finished the task #{self.task.id} "
                            f"at {datetime.now()}")
                        # set task to finished state
                        self.task.finish()
                        # set forklift to chilling status. Next time we will give him a task
                        self.status = 'chill'
                        self.current_path = None
                        self.path_direction = None
                        self.current_point = None
                        self.next_point_time = None
            else:
                # if forklift have next_point_time but tima hasn't come - we need to wait more and check it next time
                pass
