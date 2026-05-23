import logging
logger = logging.getLogger(__name__)

from typing import Any, Type
from datetime import datetime
from src.constants import PRIORITIES

def validate_string_field(name: str, instance: Any, value: Any, max_length: int) -> None:
    """
    Универсальная валидация строковых полей
    
    name - имя дескриптора (для логгирования)
    instance - объект
    value - валидируемая строка
    max_length - максимальная допустимая длина строки
    """
    # Проверка существования instance
    if instance is None:
        logger.error("Сущность не найдена")
        raise AttributeError("Сущность не найдена")
    
    # Проверка на None
    if value is None:
        logger.error(f"{name} не может быть None")
        raise AttributeError(f"{name} не может быть None")
    
    # Проверка типа
    if not isinstance(value, str):
        logger.error(f"{name} должен быть строкой")
        raise ValueError(f"{name} должен быть строкой")
    
    # Проверка на пустоту
    if value.strip() == "":
        logger.error(f"{name} не может быть пустым")
        raise ValueError(f"{name} не может быть пустым")
    
    # Проверка максимальной длины
    if len(value) > max_length:
        logger.error(f"{name}: превышен лимит длины")
        raise ValueError(f"{name}: превышен лимит длины")

class SampleDescriptor:
    """Шаблон-родитель для каждого дескриптора"""
    def __set_name__(self, owner, name: str) -> None:
        """Устанавливает имя при создании класса"""
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance, owner: Type | None = None) -> Any:
        """Getter"""
        if instance is None:
            return self
        
        return getattr(instance, self.private_name, None)

class IdDescriptor(SampleDescriptor):
    """DATA: Валидирует данные, запрещает изменение"""
    def __set__(self, instance, value: str) -> None:
        """Устанавливает значение атрибута"""

        # Универсальная валидация
        validate_string_field("ID", instance, value, 50)

        if hasattr(instance, self.private_name):
            logger.error("Изменение ID не допускается")
            raise ValueError("Изменение ID не допускается")
        
        setattr(instance, self.private_name, value)
        logger.info(f"{self.public_name} установлен: {value}")


class DescriptionDescriptor(SampleDescriptor):
    """DATA: Валидирует данные, разрешает изменение"""
    def __set__(self, instance: Any, value: str) -> None:
        """Устанавливает значение атрибута"""

        # Универсальная валидация
        validate_string_field("description", instance, value, 300)
        
        setattr(instance, self.private_name, value)
        logger.info(f"{self.public_name} установлен: {value}")


class PriorityDescriptor(SampleDescriptor):
    """DATA: Валидирует данные, разрешает изменение"""
    def __set__(self, instance: Any, value: int) -> None:
        """Устанавливает значение атрибута"""
        
        # Проверка типа данных
        if not isinstance(value, int):
            logger.error(f"Приоритет должен быть целым числом, получено: type({value}): {type(value)}")
            raise TypeError(f"Приоритет должен быть целым числом, получено: type({value}): {type(value)}")

        # Проверка значения
        if value not in PRIORITIES:
            raise ValueError(f"Приоритет должен быть целым числом от 1 до 5, получено: {value}")
        
        setattr(instance, self.private_name, value)
        logger.info(f"{self.public_name} установлен: {value}")


class StatusDescriptor(SampleDescriptor):
    """DATA: Валидирует данные, разрешает изменение"""
    def __set__(self, instance, value: str) -> None:
        """Устанавливает значение атрибута"""

        # Универсальная валидация
        validate_string_field("status", instance, value, 50)
        
        setattr(instance, self.private_name, value)
        logger.info(f"{self.public_name} установлен: {value}")


class CreationTimeDescriptor(SampleDescriptor):
    """NON-DATA, допускает только обращение"""
    def __get__(self, instance: Any, owner: Type | None = None) -> datetime:
        if instance is None:
            return self
        
        value = getattr(instance, self.private_name, None)
        
        # Если value не определено, создается автоматически
        if value is None:
            value = datetime.now()
            setattr(instance, self.private_name, value)
            logger.info(f"{self.public_name} автоматически установлен: {value}")
        
        return value


# class IsReadyDescriptor(SampleDescriptor):
#     """NON-DATA, допускает только обращение"""
#     def __get__(self, instance, owner: Type | None = None) -> bool | "IsReadyDescriptor":
#         if instance is None:
#             return self
#         result = instance.status.lower() in READY
#         return result