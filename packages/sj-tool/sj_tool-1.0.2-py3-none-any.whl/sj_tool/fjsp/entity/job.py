import pandas as pd


class BaseJob(object):
    def __init__(self, job_id: str, MAD: str, STD: str, demand: float):
        """

        :param job_id:
        :param MAD:
        :param STD:
        :param demand:
        """
        self.id = job_id
        self.MAD = pd.to_datetime(MAD)
        self.STD = pd.to_datetime(STD)
        self.demand = demand
        self.start_operations = []
        self.operations = []
