# conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption('--boot-image', action='store', default='')

@pytest.fixture(scope='module')
def boot_image_path(request):
    return request.config.getoption('--boot-image')

@pytest.fixture(scope='module')
def switch_off(strategy, capsys):
    with capsys.disabled():
        strategy.transition('off')

@pytest.fixture(scope='module')
def hostname(env, target):
    hostname = env.config.data \
        .get('targets')        \
        .get(target.name)      \
        .get('resources')      \
        .get('RemotePlace')    \
        .get('name')

    return hostname

@pytest.fixture(scope='module')
def hostip(env, target):
    from labgrid.resource import NetworkService

    #TODO: here need to be a port?
    hostip = target.get_resource(NetworkService).address
    return hostip

@pytest.fixture(scope='module')
def tftpboot(env, target):
    from labgrid.resource.remote import RemoteTFTPProvider

    tftpboot = target.get_resource(RemoteTFTPProvider).internal
    return tftpboot

@pytest.fixture(scope='module')
def upload_fw(boot_image_path, hostname, hostip, tftpboot):
    def upload_call():
        from tii_sel4_tests.utils.scp import upload
        from paramiko.ssh_exception import SSHException
        try:
            upload(boot_image_path, hostip, tftpboot)
        except SSHException:
            upload(boot_image_path, hostname, tftpboot)
    return upload_call
