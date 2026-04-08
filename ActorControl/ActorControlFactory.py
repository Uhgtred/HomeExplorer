#!/usr/bin/env python3
# @author: Markus Kösters
import logging
import typing

from BusTransactions import Bus
from BusTransactions.DefaultBusFactory import DefaultBusFactory
from .ActorController import ActorController


class ActorControlFactory:

    __logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def createActorController() -> ActorController:
        actorBus: type[Bus] = DefaultBusFactory.produceSerialTransceiver()
        return ActorController(actorBus.writeSingleMessage)

    @staticmethod
    def produceActorControlXbox(transmitterMethod: typing.Callable = None) -> ActorController:
        """
        Creates and returns an instance of ActorController based on the provided
        transmitter method or a default serial bus transceiver. If a custom
        transmitter method is supplied, it is used; otherwise, a serial transceiver
        is automatically used.

        :param transmitterMethod: A callable to serve as the transmitter method.
            If not provided, a serial transceiver's `writeSingleMessage` method
            will be used.
        :return: Instance of ActorController initialized with the specified or
            default transmitter method.
        :rtype: ActorController
        """
        if transmitterMethod:
            return ActorController(transmitterMethod)
        actorBus: type[Bus] = DefaultBusFactory.produceSerialTransceiver()
        return ActorController(actorBus.writeSingleMessage)

    @staticmethod
    def produceActorControlStub() -> ActorController:
        """
        Produces a mock of ActorController using a stubbed bus for testing purposes.

        This static method is responsible for creating an instance of
        ActorController, using a bus stub produced by the BusFactory. The
        bus stub mimics serial transceiver behavior and allows testing
        ActorController functionality in isolation without relying on an
        actual hardware setup.

        :returns: A mocked instance of ActorController.
        :rtype: ActorController
        """
        ActorControlFactory.__logger.debug(f'ActorControlFactory: Creating stub bus')
        actorBus: type[Bus] = DefaultBusFactory.produceSerialTransceiverWithStub()
        ActorControlFactory.__logger.debug(f'Using stub bus: {actorBus}')
        actorController: ActorController = ActorController(actorBus.writeSingleMessage)
        ActorControlFactory.__logger.debug(f'ActorController created: {actorController}')
        return actorController
