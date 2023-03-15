import enum

import attr

from labgrid.factory import target_factory
from labgrid.strategy import Strategy, StrategyError


class Status(enum.Enum):
    unknown   = 0
    off       = 1
    uboot     = 2
    drivervm  = 3
    uservm    = 4
    uservmgui = 5


@target_factory.reg_driver
@attr.s(eq=False)
class VMMStrategy(Strategy):
    """VMMStrategy - Strategy to switch to uboot or shell"""
    bindings = {
        "power": "PowerProtocol",
        "console": "ConsoleProtocol",
        "uboot": "UBootDriver",
        "shell": "ShellDriver",
    }

    status = attr.ib(default=Status.unknown)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

    def transition(self, status):
        if not isinstance(status, Status):
            status = Status[status]
        if status == Status.unknown:
            raise StrategyError(f"can not transition to {status}")
        elif status == self.status:
            return # nothing to do
        elif status == Status.off:
            self.target.deactivate(self.console)
            self.target.activate(self.power)
            self.power.off()
        elif status == Status.uboot:
            self.transition(Status.off)
            self.target.activate(self.console)
            # cycle power
            self.power.cycle()
            # interrupt uboot
            self.target.activate(self.uboot)
        elif status == Status.drivervm:
            # transition to uboot
            self.transition(Status.uboot)
            self.uboot.boot("")
            self.uboot.await_boot()
            self.target.activate(self.shell)
        elif status == Status.uservm:
            # transition to drivervm
            self.transition(Status.drivervm)
            # Don't use shell here, will stuck here...
            # self.shell.run("qemu-sel4")
            self.console.sendline("qemu-sel4")
            self.target.deactivate(self.shell)
            self.target.activate(self.shell)
        elif status == Status.uservmgui:
            # transition to drivervm
            self.transition(Status.drivervm)
            # Don't use shell here, will stuck here...
            # self.shell.run("qemu-sel4")
            self.console.sendline("qemu-sel4-gui")
            self.target.deactivate(self.shell)
            self.target.activate(self.shell)
        else:
            raise StrategyError(f"no transition found from {self.status} to {status}")
        self.status = status
