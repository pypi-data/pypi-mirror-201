from typing import List


class Machine(object):
    def __init__(self, machine_id, available_ops: List[str], unit_times):
        """

        :param machine_id:
        :param available_ops:
        """
        self.id = machine_id
        self.available_ops = available_ops
        self.unit_times = unit_times  # {('product_id','process'):单个的节拍 }
