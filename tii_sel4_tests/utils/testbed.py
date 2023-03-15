import os

class Testbed(object):
    def __init__(self, name, crossbar_ip, crossbar_port='20408', proxy_ip='', **kwargs):
        '''
        '''
        self.__name          = name
        self.__crossbar_ip   = crossbar_ip
        self.__crossbar_port = crossbar_port
        self.__proxy_ip      = proxy_ip

        self.__crossbar_hostname = kwargs.pop('crossbar_hostname', '')
        self.__proxy_hostname    = kwargs.pop('proxy_hostname', '')

        self.__parse_additionla_options(**kwargs)
        self.__init_env()

    def __parse_additionla_options(self, **kwargs):
        if (kwargs):
            raise Exception(f"Unknown options: {kwargs}")

    def __init_env(self):
        os.environ['LG_CROSSBAR'] = self.crossbar_address
        os.environ['LG_PROXY'] = self.proxy_hostname or self.proxy_ip or ''
        os.environ['LG_PLACE'] = self.name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def crossbar_ip(self) -> str:
        return self.__crossbar_ip

    @property
    def crossbar_port(self) -> str:
        return f'{self.__crossbar_port}'

    @property
    def crossbar_hostname(self) -> str:
        return self.__crossbar_hostname

    @property
    def crossbar_address(self) -> str:
        crossbarhost = self.__crossbar_hostname if self.__crossbar_hostname else self.crossbar_ip
        crossbarport = self.__crossbar_port if self.__crossbar_port else '20408'
        return f'ws://{crossbarhost}:{crossbarport}/ws'

    @property
    def proxy_ip(self) -> str:
        return self.__proxy_ip

    @property
    def proxy_hostname(self) -> str:
        return self.__proxy_hostname
