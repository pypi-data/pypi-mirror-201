# coding: utf-8
from datetime import date, timedelta
from enum import Enum

from pyotrs.lib import DynamicField

from otrs_somconnexio.exceptions import TicketNotReadyToBeUpdatedWithSIMReceivedData
from otrs_somconnexio.services.update_ticket_DF import UpdateTicketDF


class GetSIM(Enum):
    SIM_RECEIVED = 1
    SIM_RECEIVED_AND_DADES = 2


class SetSIMRecievedMobileTicket(UpdateTicketDF):
    """
    Set DF SImRebuda to True to OTRS mobile tickets.
    """

    READY_QUEUES = (
        "Serveis mòbil::Provisió mòbil::01.1 Fibra finalitzada",
        "Serveis mòbil::Provisió mòbil",
        "Serveis mòbil::Provisió mòbil::01.0 Esperant fibra",
        "Serveis mòbil::Provisió mòbil::01. Sol·licitat",
    )

    def __init__(self, ticket_number, only_mobile, associated, portability, activation_date):
        self.only_mobile = only_mobile
        self.associated = associated
        self.portability = portability
        self.scheduled_activation = False
        self.activation_date = activation_date
        super().__init__(ticket_number)

    def _is_ready(self):
        self._get_ticket()
        # Si esta en las colas indicadas hacer las comprobaciones,
        # en caso contrario no hacer nada y que el cron vuelva a pasar
        if self.ticket.field_get("Queue") in self.READY_QUEUES:
            return True
        return False

    def _get_response(self):
        return self.scheduled_activation

    def _check_doc(self):
        return self.ticket.dynamic_field_get("confirmDoc").value == "si"

    def _prepare_dynamic_fields(self):
        if not self._is_ready():
            # No modificamos nada y dejar el CRMLead para que lo vuelva a consultar el cron.
            raise TicketNotReadyToBeUpdatedWithSIMReceivedData(self.ticket_number)

        today = date.today()
        num_days = 0
        days_decrement = 0
        mobile_line_activation_date = self.activation_date
        while num_days < 2:
            if (
                mobile_line_activation_date - timedelta(days=days_decrement)
            ).weekday() < 5:
                num_days += 1
            days_decrement += 1
        platform_intro_date = (
            mobile_line_activation_date - timedelta(days=days_decrement)
        )
        # Si tiene asociada y es alta nueva: Enviar SIM + Datas
        # Si tiene asociada y es portability: Enviar SIM + Datas
        # Si no tiene asociada y documentacion es true: Enviar SIM + Datas
        # Si no tiene asociada y documentacion es false: Enviar SIM
        if self.only_mobile:
            if self.associated:
                mode = GetSIM.SIM_RECEIVED_AND_DADES
            else:
                if self._check_doc():
                    mode = GetSIM.SIM_RECEIVED_AND_DADES
                else:
                    mode = GetSIM.SIM_RECEIVED
        else:
            if not self.associated and self._check_doc() and not self.portability:
                mode = GetSIM.SIM_RECEIVED_AND_DADES
            else:
                mode = GetSIM.SIM_RECEIVED

        if mode == GetSIM.SIM_RECEIVED_AND_DADES:
            self.scheduled_activation = today + timedelta(days=7)
            return [
                DynamicField(name='SIMrebuda', value=1),
                DynamicField(name="permetActivacio", value="si"),
                DynamicField(
                    name='dataActivacioLiniaMobil',
                    value=str(mobile_line_activation_date)
                ),
                DynamicField(
                    name='dataIntroPlataforma',
                    value=str(platform_intro_date)
                ),
            ]
        elif mode == GetSIM.SIM_RECEIVED:
            return [
                DynamicField(name='SIMrebuda', value=1)
            ]
