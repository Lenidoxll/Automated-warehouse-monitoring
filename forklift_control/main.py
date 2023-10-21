from Warehouse import Warehouse
import multiprocessing
from pathos.multiprocessing import ProcessPool
from config import cities
from random import randint


def run_warehouse(w: Warehouse):
    """
    Just run work() method of Warehouse class.
    Need it for multiprocessing parallel run of a few warehouses
    :param w: instance of warehouse class
    :return: Nothing
    """
    w.work()


if __name__ == '__main__':
    # list to store all processes
    print(int(multiprocessing.cpu_count() * 0.4))
    print("press any key to start")
   # input()
    processes = []
    # list to store all warehouses
    warehouses = []
    # parallel all tasks by approx 80% of CPUs

    for i in range(int(multiprocessing.cpu_count() * 0.4)):
        # create new warehouse with random city from cities list
        warehouses.append(Warehouse(warehouse_id=i, city=cities[randint(0, len(cities) - 1)]))
    # here we use ProcessPool from pathos lib.
    # The reason why we don't use standard multiprocessing lib is because it does not support classes pickling
    pool = ProcessPool(nodes=int(multiprocessing.cpu_count() * 0.4))  # we use 80% of cores
    pool.map(run_warehouse, warehouses)
