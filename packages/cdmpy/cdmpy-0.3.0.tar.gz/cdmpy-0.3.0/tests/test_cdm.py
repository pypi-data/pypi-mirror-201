# Author: Lu Xu <oliver_lew@outlook.com">
# License: MIT
# Original Repo: https://github.com/OliverLew/fio-cdm
# Packaging: https://github.com/Pythoniasm/pycdm

import tests

from subprocess import Popen, PIPE
from cdm import entrypoint


__all__ = ["tests"]


def test_entrypoint():
    entrypoint()


def test_script():
    command = "cdm -s 1m"
    res = Popen(command.split(" "), stdout=PIPE)
    output, _ = res.communicate()
    assert output != ""
