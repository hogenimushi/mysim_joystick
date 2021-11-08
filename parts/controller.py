from donkeycar.parts.controller import PyGameJoystick
from donkeycar.parts.controller import LogitechJoystickController

class PyGameLogitechJoystick(PyGameJoystick):
    '''
    PyGameパッケージ前提としたLogitechジョイスティッククラス。
    ボタンやアナログデバイスの割当を定義したモジュール。
    操作系は親クラスPyGameJoystickに存在する。
    '''
    def __init__(self, *args, **kwargs):
        super(PyGameLogitechJoystick, self).__init__(*args, **kwargs)

        """
        初期化処理。
        対象となるジョイスティックから入力データを読み取る準備を行う。
        引数：
            which_js        ジョイスティック番号
            log_filename    ログファイル名
            debug           デバッグフラグ（TrueにするとloggingレベルがDEBUGになる）
        戻り値：
            なし
        """

        self.axis_names = {
            0: 'left_stick_horz',
            1: 'left_stick_vert',
            4: 'trigger', # LT:1 RT:-1
            2: 'right_stick_horz',
            3: 'right_stick_vert',
        }

        self.button_names = {
            6: 'back', # select
            7: 'start',
            #10: 'Logitech',  # not assigned

            0: 'A', # cross
            1: 'B', # circle
            2: 'X', # square
            3: 'Y', # triangle

            4: 'LB', # L1
            5: 'RB', # R1

            8: 'left_stick_press',
            9: 'right_stick_press',

            10: 'dpad_up', # HAT 0: (0, 1)
            11: 'dpad_down', # HAT 0: (0, -1)
            12: 'dpad_left', # HAT 0: (-1, 0)
            13: 'dpad_right', # HAT 0: (1, 0)
        }



class PyGameLogitechJoystickController(LogitechJoystickController):
    def __init__(self, which_js=0, *args, **kwargs):
        super(PyGameLogitechJoystickController, self).__init__(*args, **kwargs)
        self.which_js=which_js

    def init_js(self):
        '''
        attempt to init joystick
        '''
        try:
            self.js = PyGameLogitechJoystick(which_js=self.which_js)
        except Exception as e:
            print(e)
            self.js = None
        return self.js is not None
    
def get_js_controller(cfg):
    cont_class = None
    from donkeycar.parts.controller import get_js_controller

    if cfg.CONTROLLER_TYPE == "F710_pygame":
        cont_class = PyGameLogitechJoystickController
        ctr = cont_class(throttle_dir=cfg.JOYSTICK_THROTTLE_DIR,
                                throttle_scale=cfg.JOYSTICK_MAX_THROTTLE,
                                steering_scale=cfg.JOYSTICK_STEERING_SCALE,
                                auto_record_on_throttle=cfg.AUTO_RECORD_ON_THROTTLE,
                                dev_fn=cfg.JOYSTICK_DEVICE_FILE)

        ctr.set_deadzone(cfg.JOYSTICK_DEADZONE)
        return ctr
    else:
        return get_js_controller(cfg)

if __name__ == "__main__":
 #   Testing the XboxOneJoystickController
    js = XboxOneJoystick('/dev/input/js0')
    js.init()

    while True:
        button, button_state, axis, axis_val = js.poll()
        if button is not None or axis is not None:
            print(button, button_state, axis, axis_val)
        time.sleep(0.1)
