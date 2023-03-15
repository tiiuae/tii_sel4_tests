import pytest

@pytest.fixture(scope='function')
def bootloader_command(target, strategy, capsys, upload_fw):
    upload_fw()
    with capsys.disabled():
        strategy.transition('uboot')
    return target.get_active_driver('CommandProtocol')


def test_sel4(bootloader_command):
    stdout = bootloader_command.run_check('version')
    assert 'U-Boot' in '\n'.join(stdout)

    stdout = bootloader_command.run_check('boot', timeout=60)
    print("-"*10)
    print('\n'.join(stdout))
    print("-"*10)
    assert 'All is well in the universe' in '\n'.join(stdout)
