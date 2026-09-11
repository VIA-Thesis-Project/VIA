"""The normal Huaura command must use the reviewed INI without rewriting crops."""
import contextlib
import io
from pathlib import Path
import unittest
from unittest.mock import patch

import run_cropsuitelite as runner

ROOT = Path(__file__).resolve().parents[1]


class HuauraEntrypointTest(unittest.TestCase):
    def test_reviewed_config_bypasses_parameter_generation(self):
        with patch.object(runner, 'CropSuiteLite') as model, \
             patch.object(runner, 'create_crop_parameters') as create_params, \
             patch.object(runner, 'modify_initial_cropsuite_config') as create_config, \
             contextlib.redirect_stdout(io.StringIO()):
            runner.main(str(ROOT / 'yaml_configurations/general_config_huaura.yaml'))
        model.assert_called_once_with(config_file=str(ROOT / 'config_access_esm1_5_ssp126_2021_2040.ini'))
        model.return_value.run.assert_called_once_with()
        create_params.assert_not_called()
        create_config.assert_not_called()
