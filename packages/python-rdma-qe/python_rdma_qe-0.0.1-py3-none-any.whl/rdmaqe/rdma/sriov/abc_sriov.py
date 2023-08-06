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
from abc import ABCMeta, abstractmethod


class ABCSriov(metaclass=ABCMeta):
    """ Abstract class
    """
    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def get_pf_name_from_pf_bus(pf_bus):
        pass

    @staticmethod
    @abstractmethod
    def get_pf_bus_from_pf_name(pf_name):
        pass

    @staticmethod
    @abstractmethod
    def get_all_vfs_from_pf_bus(pf_bus):
        pass

    @staticmethod
    @abstractmethod
    def create_vfs(pf_bus, num):
        pass

    @staticmethod
    @abstractmethod
    def delete_vfs(pf_bus):
        pass

    @staticmethod
    @abstractmethod
    def get_pf_name_from_vf_name(vf_name):
        pass

    # @staticmethod
    # @abstractmethod
    # def get_pf_bus_from_vf_name(vf_name):
    #     pass
