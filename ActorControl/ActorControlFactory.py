#!/usr/bin/env python3
# @author: Markus Kösters

from .ActorController import ActorController


class ActorControlFactory:

    @staticmethod
    def produceActorControl():
        actorBus = BusFactory.produceSerialTransceiver()
        return ActorController(actorBus.writeSingleMessage)