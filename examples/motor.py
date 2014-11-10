#!/usr/bin/env python2.7
'''
A simple test for :class:`EpicsMotor`
'''

import time

import config
from ophyd.controls import EpicsMotor


def test():
    def callback(sub_type=None, timestamp=None, value=None, **kwargs):
        logger.info('[callback] [%s] (type=%s) value=%s' % (timestamp, sub_type, value))

    def done_moving(**kwargs):
        logger.info('Done moving %s' % (kwargs, ))

    loggers = ('ophyd.controls.signal',
               'ophyd.controls.positioner',
               'ophyd.session',
               )

    config.setup_loggers(loggers)
    logger = config.logger

    motor_record = config.motor_recs[0]

    m1 = EpicsMotor(motor_record)
    # m2 = EpicsMotor('MLL:bad_record')
    m1.subscribe(callback, event_type=m1.SUB_DONE)

    m1.user_readback.subscribe(callback)
    # print(m1.user_readback.read())
    # print(m1.read())

    logger.info('---- test #1 ----')
    logger.info('--> move to 1')
    m1.move(1)
    logger.info('--> move to 0')
    m1.move(0)

    logger.info('---- test #2 ----')
    logger.info('--> move to 1')
    m1.move(1, wait=False)
    time.sleep(0.2)
    logger.info('--> stop')
    m1.stop()
    logger.info('--> sleep')
    time.sleep(1)
    logger.info('--> move to 0')
    m1.move(0, wait=False, moved_cb=done_moving)
    time.sleep(2)

    # m2.move(1)


if __name__ == '__main__':
    test()