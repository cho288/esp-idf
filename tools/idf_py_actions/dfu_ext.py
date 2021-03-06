from idf_py_actions.tools import is_target_supported, ensure_build_directory, run_target
from idf_py_actions.errors import FatalError


def action_extensions(base_actions, project_path):

    SUPPORTED_TARGETS = ['esp32s2']

    def dfu_target(target_name, ctx, args):
        ensure_build_directory(args, ctx.info_name)
        run_target(target_name, args)

    def dfu_flash_target(target_name, ctx, args, path):
        ensure_build_directory(args, ctx.info_name)

        try:
            run_target(target_name, args, {"ESP_DFU_PATH": path})
        except FatalError:
            # Cannot capture the error from dfu-util here so the best advise is:
            print('Please have a look at the "Device Firmware Upgrade through USB" chapter in API Guides of the '
                  'ESP-IDF documentation for solving common dfu-util issues.')
            raise

    dfu_actions = {
        "actions": {
            "dfu": {
                "callback": dfu_target,
                "short_help": "Build the DFU binary",
                "dependencies": ["all"],
            },
            "dfu-list": {
                "callback": dfu_target,
                "short_help": "List DFU capable devices",
                "dependencies": [],
            },
            "dfu-flash": {
                "callback": dfu_flash_target,
                "short_help": "Flash the DFU binary",
                "order_dependencies": ["dfu"],
                "options": [
                    {
                        "names": ["--path"],
                        "default": "",
                        "help": "Specify path to DFU device. The default empty path works if there is just one "
                                "ESP device with the same product identificator. See the device list for paths "
                                "of available devices."
                    }
                ],
            },
        }
    }

    return dfu_actions if is_target_supported(project_path, SUPPORTED_TARGETS) else {}
