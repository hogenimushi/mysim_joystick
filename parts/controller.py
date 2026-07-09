from donkeycar.parts.controller import PyGameJoystick
from donkeycar.parts.controller import LogitechJoystickController


class PyGameLogitechJoystick(PyGameJoystick):
    """
    Logitech gamepad mapping for pygame (Windows XInput).
    Axis/button names are defined here; polling lives in PyGameJoystick.
    Tested with Logicool F710 in XInput mode.
    """

    def __init__(self, *args, **kwargs):
        super(PyGameLogitechJoystick, self).__init__(*args, **kwargs)

        # Axis indices for F710 XInput under pygame on Windows
        self.axis_names = {
            0: 'left_stick_horz',
            1: 'left_stick_vert',
            4: 'trigger',  # LT:1 RT:-1
            2: 'right_stick_horz',
            3: 'right_stick_vert',
        }

        # Button indices; HAT directions are mapped as virtual buttons by PyGameJoystick
        self.button_names = {
            6: 'back',  # select
            7: 'start',

            0: 'A',
            1: 'B',
            2: 'X',
            3: 'Y',

            4: 'LB',
            5: 'RB',

            8: 'left_stick_press',
            9: 'right_stick_press',

            10: 'dpad_up',     # HAT 0: (0, 1)
            11: 'dpad_down',   # HAT 0: (0, -1)
            12: 'dpad_left',   # HAT 0: (-1, 0)
            13: 'dpad_right',  # HAT 0: (1, 0)
        }


class PyGameLogitechJoystickController(LogitechJoystickController):
    """
    JoystickController wired to PyGameLogitechJoystick.
    Trigger maps use pygame button names (LB/RB, dpad_*) rather than
    Linux js names (L1/R1, dpad axes) used by LogitechJoystickController.
    """

    def __init__(self, which_js=0, *args, **kwargs):
        super(PyGameLogitechJoystickController, self).__init__(*args, **kwargs)
        self.which_js = which_js

    def init_js(self):
        """Attempt to initialize the pygame joystick device."""
        try:
            self.js = PyGameLogitechJoystick(which_js=self.which_js)
        except Exception as e:
            print(e)
            self.js = None
        return self.js is not None

    def init_trigger_maps(self):
        """Map pygame F710 control names to JoystickController actions."""
        self.button_down_trigger_map = {
            'start': self.toggle_mode,
            'B': self.toggle_manual_recording,
            'Y': self.erase_last_N_records,
            'A': self.emergency_stop,
            'back': self.toggle_constant_throttle,
            'RB': self.chaos_monkey_on_right,
            'LB': self.chaos_monkey_on_left,
            'dpad_up': self.increase_max_throttle,
            'dpad_down': self.decrease_max_throttle,
        }

        self.button_up_trigger_map = {
            'RB': self.chaos_monkey_off,
            'LB': self.chaos_monkey_off,
        }

        self.axis_trigger_map = {
            'left_stick_horz': self.set_steering,
            'right_stick_vert': self.set_throttle,
        }


def get_js_controller(cfg):
    """
    Return a joystick controller for cfg.CONTROLLER_TYPE.
    Uses the local F710_pygame mapping when requested; otherwise delegates
    to donkeycar.parts.controller.get_js_controller.
    """
    from donkeycar.parts.controller import get_js_controller as dk_get_js_controller

    if cfg.CONTROLLER_TYPE == "F710_pygame":
        ctr = PyGameLogitechJoystickController(
            throttle_dir=cfg.JOYSTICK_THROTTLE_DIR,
            throttle_scale=cfg.JOYSTICK_MAX_THROTTLE,
            steering_scale=cfg.JOYSTICK_STEERING_SCALE,
            auto_record_on_throttle=cfg.AUTO_RECORD_ON_THROTTLE,
            dev_fn=cfg.JOYSTICK_DEVICE_FILE,
        )
        ctr.set_deadzone(cfg.JOYSTICK_DEADZONE)
        return ctr

    return dk_get_js_controller(cfg)
