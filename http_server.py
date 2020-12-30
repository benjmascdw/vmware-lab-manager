import web
from vmware_helper import VwareHelper


user = "administrator@vsphere.local"
pw = "C1sc0-cdw"
host = "10.89.49.9"

URLS = (
        '/', 'root'
        )


class root:


    def GET(self):

        vc = VwareHelper()
        vc.connect(user, pw, host)

        header = "<html><head><title>test</title></head><body>\n"

        vm_list = vc.run_on_all_vms(vc.get_vm_struct)

        body = ""

        for line in vm_list:
            body += "<br>named: " + line['name'] + ", powerstate: " + line['powerstate'] + "\n"

        footer = "</body></html>\n"

        return header + body + footer



if __name__ == "__main__":
    app = web.application(URLS, globals())
    app.run()