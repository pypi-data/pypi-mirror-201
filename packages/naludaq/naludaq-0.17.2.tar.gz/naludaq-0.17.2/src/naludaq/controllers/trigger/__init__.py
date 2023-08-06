"""
"""
from naludaq.controllers.trigger.trbhm import TriggerControllerTrbhm

from .aodsoc import TriggerControllerAodsoc
from .default import TriggerController
from .hdsoc import TriggerControllerHdsoc
from .siread import TriggerControllerSiread
from .upac import TriggerControllerUpac
from .upac96 import TriggerControllerUpac96


def get_trigger_controller(board):
    """Get the controller for the model you are using.

    This is a small factory to give you the correct class without the user caring.

    Args:
        board (Board): the board object.

    Returns:
        Instantiated TriggerController
    """
    return {
        "aodsoc_aods": TriggerControllerAodsoc,
        "aodsoc_asoc": TriggerControllerAodsoc,
        "hdsocv1": TriggerControllerHdsoc,
        "hdsocv1_evalr1": TriggerControllerHdsoc,
        "hdsocv1_evalr2": TriggerControllerHdsoc,
        "upac32": TriggerControllerUpac,
        "upac96": TriggerControllerUpac96,
        "upaci": TriggerControllerUpac,
        "zdigitizer": TriggerControllerUpac,
        "siread": TriggerControllerSiread,
    }.get(board.model, TriggerController)(board)
