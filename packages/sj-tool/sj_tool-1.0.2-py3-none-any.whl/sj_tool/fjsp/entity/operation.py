from typing import List, Tuple


class Operation:
    def __init__(self, job_id, op_id, machine_times: List[Tuple[int, float]] = None):
        """

        :param op_id:操作的id
        :param machine_times: 操作在不同机器上的所需时间列表，例：[(0,2),(1,3),(2,4)],
                其中每个tuple的第一个元素表示机器id，第二个元素表示工序在对应机器上的单个所需时间
        """
        self.job_id = job_id
        self.id = op_id
        # op ids
        self.pre_ops = []
        self.next_ops = []
        self.machine_times = machine_times
