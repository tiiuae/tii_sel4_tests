import pytest

@pytest.fixture(scope='function')
def bootloader_command(target, strategy, capsys, upload_fw):
    upload_fw()
    with capsys.disabled():
        strategy.transition('uboot')
    return target.get_active_driver('CommandProtocol')

@pytest.fixture(scope='function')
def drivervm_command(target, strategy, capsys):
    with capsys.disabled():
        strategy.transition('drivervm')
    return target.get_active_driver('CommandProtocol')

@pytest.fixture(scope='function')
def uservm_command(target, strategy, capsys):
    with capsys.disabled():
        strategy.transition('uservm')
    return target.get_active_driver('CommandProtocol')

@pytest.fixture(scope='function')
def uservmgui_command(target, strategy, capsys):
    with capsys.disabled():
        strategy.transition('uservmgui')
    return target.get_active_driver('CommandProtocol')

def test_uboot(bootloader_command):
    stdout = bootloader_command.run_check('version')
    assert 'U-Boot' in '\n'.join(stdout)

def test_drivervm(drivervm_command):
    stdout = drivervm_command.run_check('cat /proc/version')
    assert 'Linux' in stdout[0]

    stdout = drivervm_command.run_check('hostname')
    assert 'driver-vm' in stdout[0]

def test_uservm(uservm_command):
    stdout = uservm_command.run_check('cat /proc/version')
    assert 'Linux' in stdout[0]

    stdout = uservm_command.run_check('hostname')
    assert 'user-vm' in stdout[0]

@pytest.mark.skip(reason='not supported yet')
def test_uservmgui(uservmgui_command):
    stdout = uservmgui_command.run_check('cat /proc/version')
    assert 'Linux' in stdout[0]

    stdout = uservmgui_command.run_check('hostname')
    assert 'user-vm-gui' in stdout[0] #TODO: need to update host name for user-vm-gui
