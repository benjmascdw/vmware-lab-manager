#!/usr/bin/python

from __future__ import print_function

import ssl
import atexit
# import sys

#from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect # , Getvsphere_connection
from pyVim.task import WaitForTask
from pyVmomi import vim #, vmodl

class VwareHelper(object):

    def __init__(self):
        self.vsphere_connection = ''

    def connect(self, username, password, hostname, port='443'):

        context = None
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()

        vsphere_connection = SmartConnect(host=hostname,
                                          user=username,
                                          pwd=password,
                                          port=int(port),
                                          sslContext=context)
        if not vsphere_connection:
            print("Could not connect to the specified host uvsphere_connectionng specified "
                  "username and password")
            return -1

        atexit.register(Disconnect, vsphere_connection)

        self.vsphere_connection = vsphere_connection

    def run_on_all_vms(self, function):
        """
            Run passed function on vm object of all virtual machines
            Input: function
            Return: list of return valused from function
        """

        return_val = []

        vsphere_connection = self.vsphere_connection
        content = vsphere_connection.RetrieveContent()

        vm_view = content.viewManager.CreateContainerView(content.rootFolder,
                                                          [vim.VirtualMachine],
                                                          True)
        obj = [vm for vm in vm_view.view]

        for vm in obj:
            return_val.append(function(vm))

        return return_val

    def get_vm_obj_by_name(self, name):
        """
            Get the vsphere object associated with a given text name
        """

        vsphere_connection = self.vsphere_connection
        content = vsphere_connection.RetrieveContent()

        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True)

        for curr_container in container.view:
            if curr_container.name == name:
                return_val = curr_container
                break

        return return_val

    def get_vm_struct(self, vm):
        """
            Create Strcuture entry from vm obj data
        """

        vminfo = {}

        vminfo['name'] = vm.summary.config.name
        vminfo['vmpathname'] = vm.summary.config.vmPathName
        vminfo['guestfullname'] = vm.summary.config.guestFullName
        vminfo['powerstate'] = vm.summary.runtime.powerState
        vminfo['annotation'] = vm.summary.config.annotation
        vminfo['ipaddress'] = vm.summary.guest.ipAddress
        if vm.summary.runtime.question != None:
            vminfo['question'] = vm.summary.runtime.question.text

        return vminfo

    def print_vm_info(self, vm):
        """
            Print information from vm object
        """

        summary = vm.summary
        print("Name       : ", summary.config.name)
        print("Path       : ", summary.config.vmPathName)
        print("Guest      : ", summary.config.guestFullName)
        annotation = summary.config.annotation
        # if annotation != None and annotation != "":
        #     print("Annotation : ", annotation)
        print("State      : ", summary.runtime.powerState)
        if summary.guest != None:
            ip = summary.guest.ipAddress
            if ip != None and ip != "":
                print("IP         : ", ip)
        if summary.runtime.question != None:
            print("Question  : ", summary.runtime.question.text)

        print("")


    # Snapshot functions
    def get_snap_obj(self, snapshot_list, snapshot_reference):
        """
            Get snapshot object by referecne
            Input: vm.snapshot.rootSnapshotList, vm.snapshot.currentSnapshot
            Return: vim.vm.SnapshotTree
        """

        for snapshot in snapshot_list:
            if snapshot.snapshot == snapshot_reference:
                snap_obj = snapshot
                break

        return snap_obj

    def get_current_snap_vm_obj(self, vm):
        """
            Get current snapshot for a VM
            Input: vm object
            return: 0 if no snapshot, else vim.vm.SnapshotTree
        """

        try:
            current_snap_obj = self.get_snap_obj(vm.snapshot.rootSnapshotList, vm.snapshot.currentSnapshot)

            """
                current_snap_obj.name
                current_snap_obj.createTime
                current_snap_obj.state
            """
            return current_snap_obj
        except:
            # print("Unexpected error:", sys.exc_info()[0])
            return 0

    def print_current_snap_vm_obj(self, vm):
        """
            Get current snapshot for a VM
            Input: vm object
        """

        try:
            current_snap_obj_list = self.get_snap_obj(vm.snapshot.rootSnapshotList, vm.snapshot.currentSnapshot)

            print("Name: %s; CreateTime: %s; State: %s" % (
                current_snap_obj_list.name,
                current_snap_obj_list.createTime,
                current_snap_obj_list.state))
        except:
            # print("Unexpected error:", sys.exc_info()[0])
            return 0


    def revert_to_snap_obj(self, snap):
        """
            Revert to specific snapshot object
            Input:
        """

        snap_obj = snap.snapshot

        try:
            WaitForTask(snap_obj.RevertToSnapshot_Task())
            return 1
        except:
            return 0
