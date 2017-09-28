import os
import subprocess as sp
import time

from collections import OrderedDict
from contextlib import contextmanager

from django_q.tasks import async, result, async_chain, result_group
from django.conf import settings


RScript = settings.R_BIN


@contextmanager
def cd(newdir):
    """
    Context manager for changing working directory.

    Ref: http://stackoverflow.com/a/24176022
    """
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)


def run_command_under_r_root(cmd, catched=True):
    with cd(newdir=os.path.join(settings.BASE_DIR, 'radars')):
        if catched:
            process = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        else:
            process = sp.run(cmd)
        return process


def r_etl(equipment, process, r='Analysis_Main.R', project='815'):
    """
    :type equipment: str, ex:cvdu01, cvdu02
    :type process: str, ex:ETL, EHM
    :rtype: OrderedDict()
    """
    etl_proesses = OrderedDict()
    commands = OrderedDict([
        (project, [RScript, r, process, equipment]),
    ])
    for cmd_name, cmd in commands.items():
        etl_proesses[cmd_name] = run_command_under_r_root(cmd)
    return etl_proesses


def etl_task():
    """
    :rtype: QuerySet()
    """
    group_id = async_chain([('radars.rtasks.r_etl', ('cvdu01', 'ETL')),
                            ('radars.rtasks.r_etl', ('cvdu01', 'EHM')),
                            ('radars.rtasks.r_etl', ('cvdu01', 'AVM')),
                            ('radars.rtasks.r_etl', ('cvdu01', 'XSPC')),
                            ('radars.rtasks.r_etl', ('cvdu01', 'AVM_Batch')), ])  # , group='ETL')
    return result_group(group_id, count=5)
