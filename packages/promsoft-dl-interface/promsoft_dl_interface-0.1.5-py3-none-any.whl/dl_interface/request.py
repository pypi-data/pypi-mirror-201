#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

# Включение проверки типов при присваивании
BaseModel.Config.validate_assignment = True


class Counteragent(BaseModel):
    """Общий класс для контрагентов."""

    form: Optional[str]
    name: str = ""


class AnonCounteragent(Counteragent):
    """Класс контрагента анонимного получателя."""

    isAnonym: bool
    phone: str


class IndCounteragent(Counteragent):
    """Класс для контрагента физического лица."""

    class Document(BaseModel):
        """Класс для паспорта."""

        type: str
        serial: str
        number: str

    document: Document


class CustomForm(BaseModel):
    """Класс ОПФ в форме набора параметров."""

    formName: str
    countryUID: str
    juridical: bool


class OrgCounteragent(Counteragent):
    """Класс контрагента юридического лица."""

    customForm: CustomForm
    inn: str


class Person(BaseModel):
    name: str


class Number(BaseModel):
    number: str


class Address(BaseModel):
    search: str


class Time(BaseModel):  # Время передачи груза.
    worktimeStart: str
    worktimeEnd: str


class Delivery(BaseModel):
    class DeliveryType(BaseModel):
        type: str = "auto"

    class Derival(BaseModel):
        produceDate: str
        variant: str = "address"  # 'terminal'
        payer: str = "receiver"
        # terminalID: str
        address: Address
        time: Time = Time(
            worktimeStart="09:00",
            worktimeEnd=(
                "19:00" if datetime.today().weekday() not in (5, 6) else "17:00"
            ),
        )

    class Package(BaseModel):
        """Тип упаковки."""

        uid: str  # uid типа упаковки.
        payer: str = "receiver"

    class Arrival(BaseModel):
        variant: str
        payer: str = "receiver"
        terminalID: Optional[str]
        city: Optional[str]
        address: Optional[Address]
        time: Optional[Time]

    deliveryType: DeliveryType
    packages: Optional[List[Package]]
    derival: Derival
    arrival: Arrival
    comment: Optional[str]


class DataForReceipt(BaseModel):
    send: Optional[bool]
    phone: str
    email: Optional[str]


class Members(BaseModel):
    class Requester(BaseModel):
        role: str = "sender"
        uid: str

    class Sender(BaseModel):
        counteragent: Counteragent
        contactPersons: List[Person]
        phoneNumbers: List[Number]
        email: str

    class Receiver(BaseModel):
        counteragent: Counteragent
        contactPersons: Optional[List[Person]]
        phoneNumbers: Optional[List[Number]]
        dataForReceipt: Optional[DataForReceipt]
        email: Optional[str]

    requester: Requester
    sender: Sender
    receiver: Optional[Receiver]


class Cargo(BaseModel):
    length: float = 0.1
    width: float = 0.1
    height: float = 0.1
    totalVolume: float = 0.001
    totalWeight: float = 0.5  # Решение Назарова
    freightName: str = "Оборудование"
    oversizedVolume: Optional[float]
    oversizedWeight: Optional[float]


class Payment(BaseModel):
    type: str = "cash"
    primaryPayer: str = "receiver"


class RequestForm(BaseModel):
    appkey: str
    sessionID: str
    delivery: Delivery
    members: Members
    cargo: Cargo
    payment: Payment
