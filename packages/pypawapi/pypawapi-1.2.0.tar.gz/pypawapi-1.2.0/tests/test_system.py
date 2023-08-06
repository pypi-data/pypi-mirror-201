from typing import TYPE_CHECKING

import pytest
from responses.matchers import urlencoded_params_matcher

from pawapi.system import SystemImage

if TYPE_CHECKING:
    from responses import RequestsMock


def test_system_image() -> None:
    assert SystemImage.DANGERMOUSE.value == "dangermouse"
    assert SystemImage.EARLGREY.value == "earlgrey"
    assert SystemImage.FISHNCHIPS.value == "fishnchips"
    assert SystemImage.GLASTONBURY.value == "glastonbury"
    assert SystemImage.HAGGIS.value == "haggis"


@pytest.mark.usefixtures("paw_api_client")
class TestSystem:

    def test_get_version(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.get(f"{self.url}/system_image/")
        self.api.system.get_current_image()

    def test_set_version(self, mock_responses: 'RequestsMock') -> None:
        mock_responses.patch(
            url=f"{self.url}/system_image/",
            match=(
                urlencoded_params_matcher({"system_image": "glastonbury"}),
            ),
        )
        self.api.system.set_image(SystemImage.GLASTONBURY)
