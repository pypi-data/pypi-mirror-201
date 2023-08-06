#!/usr/bin/env python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Author: Zhaojuan Guo <zguo@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2023 Red Hat, Inc.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from python_rdma_qe.sriov.abc_sriov import ABCSriov
import python_rdma_qe.common.cmd as cd
import os


class SRIOV(ABCSriov):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_pf_name_from_pf_bus(pf_bus):
        """
        :param pf_bus: e.g. 0000:c4:00.0
        :return: e.g. mlx5_roce
        """
        if not pf_bus:
            return None
        _path = "/sys/bus/pci/devices/{}/net".format(pf_bus)
        try:
            return os.listdir(_path)
        except OSError:
            print('No such device.')
            return None

    @staticmethod
    def get_pf_bus_from_pf_name(pf_name):
        """
        :param pf_name: e.g. mlx5_ib0
        :return: e.g. 0000:07:00.0
        """
        if not pf_name:
            return None
        _cmd_str = "ethtool -i {} | grep bus-info | awk '{{print $2}}'".format(pf_name)
        ret = cd.run_cmd_str(_cmd_str)
        if ret.stdout:
            return cd.run_cmd_str(_cmd_str).stdout
        else:
            print('No such device.')
            return None

    @staticmethod
    def get_all_vfs_from_pf_bus(pf_bus):
        """
        :param pf_bus: e.g. 0000:07:00.0
        :return: ['ibs2f2v0', 'ibs2f3v1']
        """
        vf_names = []
        _base_dir = "/sys/bus/pci/devices/{}".format(pf_bus)
        try:
            for _vf_path in os.listdir(_base_dir):
                if _vf_path.startswith("virtfn"):
                    print(_vf_path)
                    vf_path = "/sys/bus/pci/devices/{}/{}/net".format(pf_bus, _vf_path)
                    print(vf_path)
                    vf_names = vf_names + os.listdir(vf_path)
            return vf_names
        except OSError:
            return None

    def create_vfs(pf_bus, num):
        """
        Usage: create_vfs("0000:07:00.0", "2")
        Return: None
        """
        _total_path = "/sys/bus/pci/devices/{}/sriov_totalvfs".format(pf_bus)
        with open(_total_path, "r") as ft:
            total_vfs = ft.read()
        if num > total_vfs or num < "1":
            print("VFs number should be between 1 and {}".format(total_vfs))
            return 1

        _num_path = "/sys/bus/pci/devices/{}/sriov_numvfs".format(pf_bus)

        with open(_num_path, "w+") as fn:
            current_num = int(fn.read())
            if current_num > 0:
                fn.write("0")
                fn.read()
            fn.write(num)

    def delete_vfs(pf_bus):
        """
        Usage: delete_vfs("0000:07:00.0")
        :return:  None
        """
        _num_path = "/sys/bus/pci/devices/{}/sriov_numvfs".format(pf_bus)

        with open(_num_path, "w") as fn:
                fn.write("0")

    def get_pf_name_from_vf_name(vf_name):
        """
        :param vf_name: e.g. ibs2f2v0
        :return: ['mlx5_ib0']
        """
        _path = "/sys/class/net/{}/device/physfn/net".format(vf_name)
        try:
            return os.listdir(_path)
        except OSError:
            return None



s = SRIOV()
#d = s.get_pf_name_from_pf_bus("0000:04:00.0")
#print(d)
bus = s.get_pf_bus_from_pf_name("wlp4s0o")
print(bus)