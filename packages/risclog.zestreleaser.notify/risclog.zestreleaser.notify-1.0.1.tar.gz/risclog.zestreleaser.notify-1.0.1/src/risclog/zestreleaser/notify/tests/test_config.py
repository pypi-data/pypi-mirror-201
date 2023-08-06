def test_settings_are_read_from_env_file():
    from risclog.zestreleaser.notify.config import get_settings

    assert get_settings().package_name == 'risclog.zestreleaser.notify'
