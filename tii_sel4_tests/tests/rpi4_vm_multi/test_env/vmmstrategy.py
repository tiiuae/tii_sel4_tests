import enum

import attr

from labgrid.factory import target_factory
from labgrid.strategy import Strategy, StrategyError


class Status(enum.Enum):
    unknown    = 0
    off        = 1
    uboot      = 2
    vm0        = 3


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
            self.console.set_double_n(False)
        elif status == Status.uboot:
            self.transition(Status.off)
            self.target.activate(self.console)
            # cycle power
            self.power.cycle()
            # interrupt uboot
            self.target.activate(self.uboot)
        elif status == Status.vm0:
            # transition to uboot
            self.transition(Status.uboot)
            self.uboot.boot("")
            self.uboot.await_boot()
            self.console.set_double_n(True)
            self.target.activate(self.shell)
        else:
            raise StrategyError(f"no transition found from {self.status} to {status}")
        self.status = status
