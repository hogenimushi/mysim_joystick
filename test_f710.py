# -*- coding: utf-8 -*-
"""
Smoke-test F710_pygame joystick wiring without starting the simulator.
"""
import time
import numpy as np
import donkeycar as dk


class PrintJoy:
    """Print joystick outputs for manual verification."""

    def run(self, steering, throttle, mode, rec):
        print(f'steering:{steering} throttle:{throttle} mode:{mode}, rec:{rec}')


def test_joy(cfg):
    """
    Verify that F710 inputs produce expected steering/throttle/mode/recording.
    Requires a connected F710 (XInput) and CONTROLLER_TYPE F710_pygame.
    """
    V = dk.vehicle.Vehicle()

    V.mem['cam/image_array'] = np.zeros((120, 160, 3))

    from parts.controller import get_js_controller
    ctr = get_js_controller(cfg)
    V.add(
        ctr,
        inputs=['cam/image_array', 'user/mode', 'recording'],
        outputs=['user/steering', 'user/throttle', 'user/mode', 'recording'],
        threaded=True,
    )

    V.add(
        PrintJoy(),
        inputs=['user/steering', 'user/throttle', 'user/mode', 'recording'],
    )

    try:
        print('start')
        V.start(rate_hz=cfg.DRIVE_LOOP_HZ, max_loop_count=cfg.MAX_LOOPS)
    except KeyboardInterrupt:
        print('halt')
    finally:
        print('stop')


if __name__ == '__main__':
    cfg = dk.load_config()
    setattr(cfg, 'CONTROLLER_TYPE', 'F710_pygame')
    test_joy(cfg)
