
from srsgui.inst.instrument import Instrument
from srsgui.inst.communications import SerialInterface
from srsgui.task.inputs import FindListInput

from .components import Config, Operate, Setup, Interface, Status


class SR542(Instrument):
    _IdString = 'SR542'

    available_interfaces = [
        [
            SerialInterface,
            {
                'port': FindListInput(),
                'baud_rate': 115200,
            }
        ]
    ]

    def __init__(self, interface_type=None, *args):
        super().__init__(interface_type, *args)
        self.config = Config(self)
        self.operate = Operate(self)
        self.setup = Setup(self)
        self.interface = Interface(self)
        self.status = Status(self)

    def connect(self, interface_type, *args):
        super().connect(interface_type, *args)
        self.send('TOKN OFF')
        self.send('TERM LF')

    def reset(self):
        self.send('*RST')
        self.send('TOKN OFF')
        self.send('TERM LF')

    def get_status(self):
        return self.status.get_status_text()
