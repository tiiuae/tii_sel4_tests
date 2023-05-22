import pytest

@pytest.fixture(scope='function')
def bootloader_command(target, strategy, capsys, upload_fw):
    upload_fw()
    with capsys.disabled():
        strategy.transition('uboot')
    return target.get_active_driver('CommandProtocol')

@pytest.fixture(scope='function')
def vm_command(target, strategy, capsys):
    with capsys.disabled():
        strategy.transition('vm0')
    return target.get_active_driver('CommandProtocol')

def test_uboot(bootloader_command):
    stdout = bootloader_command.run_check('version')
    assert 'U-Boot' in '\n'.join(stdout)

def test_vm_boot(vm_command):
    stdout = vm_command.run_check('cat /proc/version')
    assert 'Linux' in stdout[0]

    stdout = vm_command.run_check('hostname')
    assert 'buildroot' in stdout[0]
