#!/usr/bin/env python3
# @author: Markus Kösters

from BusTransactions.BusFactory import BusFactory
from .ActorController import ActorController


class ActorControlFactory:

    @staticmethod
    def produceActorControl(stub: bool = False):
        actorBus = BusFactory.produceSerialTransceiver(stub=stub)
        return ActorController(actorBus.writeSingleMessage)
