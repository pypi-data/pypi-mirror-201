#!/usr/bin/env python

"""roce.py: Module to check or configure RDMA. """

__author__ = "Zhaojuan Guo"
__copyright__ = "Copyright (c) 2023 Red Hat, Inc. All rights reserved."

import os

RDMA_BASE = '/sys/class/infiniband'


def is_rdma_device() -> bool:
    return os.path.exists(RDMA_BASE)


def is_opa_device() -> bool:
    """
    Check if it contains OPA device
    :return:
    True: if yes
    False: if no
    """
    if is_rdma_device():
        for _ in os.listdir(RDMA_BASE):
            return 'hfi' in _


def get_ibdev():
    # return: ['mlx5_1', 'mlx5_0']
    _ibdev = []
    for dev in os.listdir(RDMA_BASE):
        _ibdev.append(dev)

    return _ibdev


def get_netdev(dev):
    """
    :param dev: ibdev, like mlx5_0
    :return: netdev, like ['mlx5_roce']
    """
    if not dev:
        return None
    _netdev = []
    _dir = '/sys/class/infiniband/{}/device/net/'.format(dev)
    for dev in os.listdir(_dir):
        _netdev.append(dev)

    return _netdev