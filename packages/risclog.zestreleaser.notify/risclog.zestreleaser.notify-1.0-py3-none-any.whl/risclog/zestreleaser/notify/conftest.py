import mock
import pytest


class TestSettings:
    package_name = 'risclog.zestreleaser.notify'


@pytest.fixture(autouse=True)
def settings():
    patcher = mock.patch(
        'risclog.zestreleaser.notify.config.Settings', side_effect=TestSettings
    )
    patcher.start()
    yield patcher
    patcher.stop()
