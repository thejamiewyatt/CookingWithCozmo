from abc import ABC, abstractmethod


class Robot(ABC):
    """Abstract robot interface."""
    @abstractmethod
    def speak(self, text) -> None:
        pass

    @abstractmethod
    def set_start_position(self) -> None:
        pass

    @abstractmethod
    def turn_in_place(self) -> None:
        pass

    @abstractmethod
    def react_positively(self) -> None:
        pass

    @abstractmethod
    def react_negatively(self) -> None:
        pass
    
    @abstractmethod
    def check_plate_and_celebrate(self, distance, speed, deg) -> None:
        pass
