import win32serviceutil
import win32service
import win32event
from nvos import file
import logging
import json
import os
import time

logging.basicConfig(filename=os.path.expanduser(os.path.join("~","auto_service_logger.log")), level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Ndtc_auto_script"
    _svc_display_name_ = "Ndtc Auto Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        import servicemanager
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        while True:
            with open(os.path.expanduser(os.path.join("~", "workspace")),"r") as f:
                all_workspace_path = json.loads(f.readline().strip())
            for temp in all_workspace_path.keys():
                logger.info("command_async current run workspace is " + temp)
                file.pull_data_from_cloud(temp)
            time.sleep(10)
        pass


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)