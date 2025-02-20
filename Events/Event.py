#!/usr/bin/env python3
# @author: Markus Kösters
import ProjectLogging


class Event:
    """
    Class that represents an event which can be subscribed to and posted to.
    """

    __subscribers: set = set()
    # Initializing a logger. Loglevel can globally be set in ProjectLogging.Logger.
    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('Events',
                                                                      'Events.log').getLogger

    def subscribe(self, callbackMethod: callable) -> None:
        """
        Subscribing to Event, receiving any updates occurring.
        :param callbackMethod: Method that the event-update is going to be sent to.
        """
        self.__subscribers.add(callbackMethod)

    def notifySubscribers(self, data: any, verbose: bool = False) -> None:
        """
        Notifies all registered subscribers by invoking their callback methods
        and passing the provided data. Optionally logs information about the
        event if verbosity is enabled.

        :param data: The data to be passed to each subscriber's callback method.
        :type data: any
        :param verbose: Indicates whether detailed logging should be performed.
        :type verbose: bool
        :return: None
        """
        for callbackMethod in self.__subscribers:
            if verbose:
                self.__logger.info(f'Event:\n\tCallback-method: {callbackMethod.__name__}\n\tArgument: {data}')
            callbackMethod(data)
