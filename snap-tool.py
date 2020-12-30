
from __future__ import print_function

import argparse
from vmware_helper import VwareHelper

def GetArgs():
    """
    Supports the command-line arguments listed below.
    """
    parser = argparse.ArgumentParser(description='Process args for retrieving all the Virtual Machines')
    parser.add_argument('-s', '--host', required=True, action='store',
                        help='Remote host to connect to')
    parser.add_argument('-o', '--port', type=int, default=443, action='store',
                        help='Port to connect on')
    parser.add_argument('-u', '--user', required=True, action='store',
                        help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=False, action='store',
                        help='Password to use when connecting to host')
    # parser.add_argument('-o', '--operation', required=True, action='store',
    #                     help='choose operation')

    args = parser.parse_args()
    
    return args


def main():
   
    args = GetArgs()

    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and '
                                    'user %s: ' % (args.host,args.user))


    vc = VwareHelper()
    vc.connect(args.user, args.password, args.host)
    print("Connected to VCENTER SERVER %s!" % args.host)

    print("List of all Snapshots")
    vc.run_on_all_vms(vc.print_current_snap_vm_obj)

    # print("list all VMs")
    # vc.run_on_all_vms(vc.print_vm_info)

    # test_struct = vc.run_on_all_vms(vc.get_vm_struct)
    # print(test_struct)


    # vm = vc.get_vm_obj_by_name("csateng-conn-2")

    # print(vc.get_current_snap_vm_obj(vm))

    # vm = vc.get_vm_obj_by_name("csateng-dc2")
    # snap = vc.get_current_snap_vm_obj(vm)
    # print (snap.name)

    # snaps = vc.run_on_all_vms(vc.get_current_snap_vm_obj)
    # print(dir(snaps[4].snapshot))



# Start program
if __name__ == "__main__":
    main()