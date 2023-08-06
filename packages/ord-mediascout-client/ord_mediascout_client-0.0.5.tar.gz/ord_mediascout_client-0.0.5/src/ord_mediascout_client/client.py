from typing import Any, Optional, Type

import requests
from pydantic.error_wrappers import ValidationError
from pydantic.main import BaseModel
from pydantic.tools import parse_raw_as
from requests.auth import HTTPBasicAuth

from .config import ORDMediascoutConfig
from .models import (
    BadRequestWebApiDto,
    ClearInvoiceDataWebApiDto,
    ClientWebApiDto,
    CreateClientWebApiDto,
    CreateCreativeWebApiDto,
    CreateFinalContractWebApiDto,
    CreateInitialContractWebApiDto,
    CreateInvoiceWebApiDto,
    CreateOuterContractWebApiDto,
    CreatePlatformWebApiDto,
    CreativeWebApiDto,
    EditCreativeWebApiDto,
    EditFinalContractWebApiDto,
    EditInitialContractWebApiDto,
    EditInvoiceDataWebApiDto,
    EditInvoiceStatisticsWebApiDto,
    EditOuterContractWebApiDto,
    EditPlatformWebApiDto,
    EntityIdWebApiDto,
    FinalContractWebApiDto,
    GetClientsWebApiDto,
    GetCreativesWebApiDto,
    GetFinalContractsWebApiDto,
    GetInitialContractsWebApiDto,
    GetInvoicesWebApiDto,
    GetOuterContractsWebApiDto,
    InitialContractWebApiDto,
    InvoiceSummaryWebApiDto,
    InvoiceWebApiDto,
    OuterContractWebApiDto,
    PlatformCardWebApiDto,
    SelfPromotionContractWebApiDto,
    SupplementInvoiceWebApiDto,
)


class APIError(Exception):
    pass


class BadResponseError(APIError):
    def __init__(self, response: requests.Response, error: Optional[BadRequestWebApiDto] = None):
        super().__init__(error and error.errorType or f'Bad response from API: {response.status_code}')
        self.response = response
        self.error = error


class UnexpectedResponseError(APIError):
    def __init__(self, response: requests.Response):
        super().__init__(f'Unexpected response with STATUS_CODE: {response.status_code}')
        self.response = response


class ORDMediascoutClient:
    def __init__(self, config: ORDMediascoutConfig):
        self.config = config
        self.auth = HTTPBasicAuth(self.config.username, self.config.password)

    def _call(
        self,
        method: str,
        url: str,
        obj: Optional[BaseModel] = None,
        return_type: Optional[Type[Any]] = None,
        **kwargs: dict[str, Any],
    ) -> Any:
        response = requests.request(
            method,
            f'{self.config.url}{url}',
            data=obj and obj.json(),
            auth=self.auth,
            headers={'Content-Type': 'application/json-patch+json'},
            **kwargs,
        )

        match response.status_code:
            case 400 | 401:
                try:
                    bad_response = BadRequestWebApiDto.parse_raw(response.text)
                except ValidationError as e:
                    raise UnexpectedResponseError(response) from e
                raise BadResponseError(response, bad_response)
            case 500:
                raise BadResponseError(response)
            case 200 | 201:
                if return_type is not None:
                    try:
                        return parse_raw_as(return_type, response.text)
                    except ValidationError as e:
                        raise UnexpectedResponseError(response) from e
            case _:
                raise UnexpectedResponseError(response)

    # Clients
    def create_client(self, client: CreateClientWebApiDto) -> ClientWebApiDto:
        client: ClientWebApiDto = self._call('post', '/webapi/Clients/CreateClient', client, ClientWebApiDto)
        return client

    def get_clients(self, parameters: GetClientsWebApiDto) -> list[ClientWebApiDto]:
        clients: list[ClientWebApiDto] = self._call(
            'post', '/webapi/Clients/GetClients', parameters, list[ClientWebApiDto]
        )
        return clients

    # Contracts
    def create_initial_contract(self, contract: CreateInitialContractWebApiDto) -> InitialContractWebApiDto:
        contract: InitialContractWebApiDto = self._call(
            'post', '/webapi/Contracts/CreateInitialContract', contract, InitialContractWebApiDto
        )
        return contract

    def edit_initial_contract(self, contract: EditInitialContractWebApiDto) -> InitialContractWebApiDto:
        contract: InitialContractWebApiDto = self._call(
            'post', '/webapi/Contracts/EditInitialContract', contract, InitialContractWebApiDto
        )
        return contract

    def get_initial_contracts(self, parameters: GetInitialContractsWebApiDto) -> list[InitialContractWebApiDto]:
        contracts: list[InitialContractWebApiDto] = self._call(
            'post', '/webapi/Contracts/GetInitialContracts', parameters, list[InitialContractWebApiDto]
        )
        return contracts

    def create_final_contract(self, contract: CreateFinalContractWebApiDto) -> FinalContractWebApiDto:
        contract: FinalContractWebApiDto = self._call(
            'post', '/webapi/Contracts/CreateFinalContract', contract, FinalContractWebApiDto
        )
        return contract

    def edit_final_contract(self, contract: EditFinalContractWebApiDto) -> FinalContractWebApiDto:
        contract: FinalContractWebApiDto = self._call(
            'post', '/webapi/Contracts/EditFinalContract', contract, FinalContractWebApiDto
        )
        return contract

    def get_final_contracts(self, parameters: GetFinalContractsWebApiDto) -> list[FinalContractWebApiDto]:
        contracts: list[FinalContractWebApiDto] = self._call(
            'post', '/webapi/Contracts/GetFinalContracts', parameters, list[FinalContractWebApiDto]
        )
        return contracts

    def create_outer_contract(self, contract: CreateOuterContractWebApiDto) -> OuterContractWebApiDto:
        contract: OuterContractWebApiDto = self._call(
            'post', '/webapi/Contracts/CreateOuterContract', contract, OuterContractWebApiDto
        )
        return contract

    def edit_outer_contract(self, contract: EditOuterContractWebApiDto) -> OuterContractWebApiDto:
        contract: OuterContractWebApiDto = self._call(
            'post', '/webapi/Contracts/EditOuterContract', contract, OuterContractWebApiDto
        )
        return contract

    def get_outer_contracts(self, parameters: GetOuterContractsWebApiDto) -> list[OuterContractWebApiDto]:
        contracts: list[OuterContractWebApiDto] = self._call(
            'post', '/webapi/Contracts/GetOuterContracts', parameters, list[OuterContractWebApiDto]
        )
        return contracts

    def create_self_promotion_contract(
        self, contract: SelfPromotionContractWebApiDto
    ) -> SelfPromotionContractWebApiDto:
        contract: SelfPromotionContractWebApiDto = self._call(
            'post', '/webapi/Contracts/CreateSelfPromotionContract', contract, SelfPromotionContractWebApiDto
        )
        return contract

    def get_self_promotion_contracts(self) -> list[SelfPromotionContractWebApiDto]:
        contracts: list[SelfPromotionContractWebApiDto] = self._call(
            'post', '/webapi/Contracts/GetSelfPromotionContracts', None, list[SelfPromotionContractWebApiDto]
        )
        return contracts

    # Creatives
    def create_creative(self, creative: CreateCreativeWebApiDto) -> EntityIdWebApiDto:
        entity: EntityIdWebApiDto = self._call('post', '/webapi/creatives/CreateCreative', creative, EntityIdWebApiDto)
        return entity

    def edit_creative(self, creative: EditCreativeWebApiDto) -> CreativeWebApiDto:
        updated_creative: CreativeWebApiDto = self._call(
            'post', '/webapi/creatives/EditCreative', creative, CreativeWebApiDto
        )
        return updated_creative

    def get_creatives(self, parameters: GetCreativesWebApiDto) -> list[CreativeWebApiDto]:
        creatives: list[CreativeWebApiDto] = self._call(
            'post', '/webapi/creatives/GetCreatives', parameters, list[CreativeWebApiDto]
        )
        return creatives

    # Invoices
    def create_invoice(self, invoice: CreateInvoiceWebApiDto) -> EntityIdWebApiDto:
        entity: EntityIdWebApiDto = self._call('post', '/webapi/Invoices/CreateInvoice', invoice, EntityIdWebApiDto)
        return entity

    def edit_invoice(self, invoice: EditInvoiceDataWebApiDto) -> InvoiceWebApiDto:
        invoice: InvoiceWebApiDto = self._call('post', '/webapi/Invoices/EditInvoice', invoice, InvoiceWebApiDto)
        return invoice

    def overwrite_invoice(self, invoice: EditInvoiceStatisticsWebApiDto) -> None:
        self._call('post', '/webapi/Invoices/OverwriteInvoice', invoice)

    def clear_invoice(self, invoice: ClearInvoiceDataWebApiDto) -> None:
        self._call('post', '/webapi/Invoices/ClearInvoice', invoice)

    def supplement_invoice(self, invoice: SupplementInvoiceWebApiDto) -> EntityIdWebApiDto:
        entity: EntityIdWebApiDto = self._call('post', '/webapi/Invoices/SupplementInvoice', invoice, EntityIdWebApiDto)
        return entity

    def get_invoices(self, parameters: GetInvoicesWebApiDto) -> list[InvoiceWebApiDto]:
        invoices: list[InvoiceWebApiDto] = self._call(
            'post', '/webapi/Invoices/GetInvoices', parameters, list[InvoiceWebApiDto]
        )
        return invoices

    def get_invoice_summary(self, entity: EntityIdWebApiDto) -> InvoiceSummaryWebApiDto:
        invoice_summary: InvoiceSummaryWebApiDto = self._call(
            'post', '/webapi/Invoices/GetInvoiceSummary', entity, InvoiceSummaryWebApiDto
        )
        return invoice_summary

    def confirm_invoice(self, entity: EntityIdWebApiDto) -> None:
        self._call('post', '/webapi/Invoices/ConfirmInvoice', entity)

    def delete_invoice(self, entity: EntityIdWebApiDto) -> None:
        self._call('post', '/webapi/Invoices/DeleteInvoices', entity)

    # WebApiPlatform
    def create_platform(self, platform: CreatePlatformWebApiDto) -> EntityIdWebApiDto:
        entity: EntityIdWebApiDto = self._call('post', '/webapi/Platforms/CreatePlatform', platform, EntityIdWebApiDto)
        return entity

    def edit_platform(self, platform: EditPlatformWebApiDto) -> PlatformCardWebApiDto:
        updated_platform: PlatformCardWebApiDto = self._call(
            'post', '/webapi/Platforms/EditPlatform', platform, PlatformCardWebApiDto
        )
        return updated_platform

    # PING
    def ping(self) -> bool:
        tmp_auth, self.auth = self.auth, None
        self._call('get', '/webapi/Ping')
        self.auth = tmp_auth
        return True

    def ping_auth(self) -> bool:
        self._call('get', '/webapi/PingAuth')
        return True
