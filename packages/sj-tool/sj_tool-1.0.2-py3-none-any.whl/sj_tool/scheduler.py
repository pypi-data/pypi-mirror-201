from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler


def add_interval_job(job_fn, seconds, use_background_scheduler=True, args=None):
    """
    添加定期执行的任务
    :param job_fn: 要运行的函数
    :param seconds: 间隔时间，单位：秒
    :param use_background_scheduler: 是否使用后台线程运行任务。若为True，则不会阻塞主线程
    :param args: 要运行函数的参数
    :return:
    """
    # 注意：BlockingScheduler会阻塞当前线程，直到调度器被关闭。
    # 创建一个调度器实例
    scheduler = BackgroundScheduler() if use_background_scheduler else BlockingScheduler()
    # 添加一个定时任务
    scheduler.add_job(job_fn, "interval", seconds=seconds, args=args)
    # 开始调度任务
    scheduler.start()


def add_fix_time_job(job_fn, hour, minute=0, second=0, use_background_scheduler=True, args=None):
    """
    添加定期执行的任务
    :param job_fn: 要运行的函数
    :param hour: 时
    :param minute: 分
    :param second: 秒
    :param use_background_scheduler: 是否使用后台线程运行任务。若为True，则不会阻塞主线程
    :param args: 要运行函数的参数
    :return:
    """
    # 注意：BlockingScheduler会阻塞当前线程，直到调度器被关闭。
    # 创建一个调度器实例
    scheduler = BackgroundScheduler() if use_background_scheduler else BlockingScheduler()
    # 添加一个定时任务
    scheduler.add_job(job_fn, "cron", hour=hour, minute=minute, second=second, args=args)
    # 开始调度任务
    scheduler.start()
