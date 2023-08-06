#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional

from pydantic import BaseModel, Field

# Включение проверки типов при присваивании
BaseModel.Config.validate_assignment = True


class Order(BaseModel):
    """Модель заказа на доставку груза."""

    id: int = Field(title="idmonopolia")
    force: bool = False  # Если true - пересоздать существующую заявку.
    hardPacking: bool = False
    insurance: bool = False


class Item(BaseModel):
    """Модель входящего запроса на сервис."""

    cargopickup: bool = False
    test: bool = Field(False, title="Режим тестирования.")
    arr: List[Order] = Field(title="Список заказов на доставку груза.")


class Token(BaseModel):
    """Модель токена задач."""

    token_id: str = Field(title="Токен, на получение результатов по созданию заявок.")


class Data(BaseModel):
    """Модель данных заявки."""

    request_id: int = Field(title="id заявки, полученной от Деловых Линий.")
    form: dict = Field(title="Форма заявки отправленная в Деловые Линии.")
    barcode: str = Field(title="Штрихкод, полученный от Деловых Линий.")


class RequestData(BaseModel):
    """Модель данных о результате создания заявки."""

    id: int = Field(title="idmonopolia")
    request_data: Optional[dict] = Field(title="Данные заявки.")
    data: Optional[Data] = Field(title="Данные о создании заявки.")
    error: Optional[str] = Field(title="Причина ошибки создания заявки.")


class Result(BaseModel):
    """Модель результа."""

    success: Optional[List[RequestData]] = Field(
        title="Список успешно созданных заявок."
    )
    fail: Optional[List[RequestData]] = Field(title="Список несозданных заявок.")
    total_pdf: Optional[str] = Field(title="Общий файл заявок на доставку груза.")
    status: Optional[str] = Field(title="Статус процесса создания заявок.")


class Response(BaseModel):
    """Модель ответа сервиса."""

    result: Optional[Result] = Field(title="Результат работы сервиса.")
