class OperationType(object):
    def __init__(self, idx, name):
        self.id = idx
        self.name = name


class Changeover(object):
    def __init__(self):
        self.info = {}

    def add(self, pre_mtm, pre_op_type, cur_mtm, cur_op_type, processing_time):
        self.info[(pre_op_type, cur_op_type)] = processing_time

    def get(self, pre_mtm, pre_op_type, cur_mtm, cur_op_type):
        return self.info[(pre_op_type, cur_op_type)]
