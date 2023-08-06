import pymem


class PyWare:
    def __init__(self, process: str, dll: str):
        self.process = process
        self.dll = dll
        self.pm = pymem.Pymem(f"{self.process}.exe")
        self.module = pymem.pymem.process.module_from_name(self.pm.process_handle, f"{self.dll}.dll").lpBaseOfDll

    def m_ihealth(self, entity: str):
        value = self.pm.read_int(entity + 0x100)
        return value
