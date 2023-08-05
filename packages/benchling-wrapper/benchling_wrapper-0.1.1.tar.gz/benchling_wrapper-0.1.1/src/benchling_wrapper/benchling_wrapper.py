from benchling_api_client.v2.stable.models.dna_sequence import DnaSequence
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2
from benchling_api_client.models.naming_strategy import NamingStrategy
from benchling_sdk.helpers.pagination_helpers import PageIterator
from benchling_sdk.helpers.serialization_helpers import fields
from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.benchling import Benchling
from benchling_sdk import models
from benchling_sdk.models import CustomEntity, AssayResult

from httpx import TransportError
from typing import Callable, Any
from math import log2
from time import sleep

_RETRY_STRATEGY_MAX_TRIES = 17  # 65535.5 secs
_REQUEST_STEP_BASE_DELAY = 60
REQUESTS_RETRY_COUNT = 623  # 23:58:05


def _with_retry(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        for i in range(REQUESTS_RETRY_COUNT + 1):
            try:
                return func(*args, **kwargs)

            # TransportError: decorate Benchling Limitation
            except TransportError as e:
                if i == REQUESTS_RETRY_COUNT:
                    raise e
                delay = _REQUEST_STEP_BASE_DELAY + log2(i+1) * 10
                # log here
                sleep(delay)

    return wrapper


class BenchlingWrapper:
    """
    Wrapper over Benchling SDK.
    Allow to initialize Benchling object, get entity by its id, by field value, update entity.

    Attributes
    ----------
    benchling: Type(benchling_sdk.benchling)
        determined in __init__(). Instance of Benchling SDK object

    benchling_url: str
        determined in config. URL of Benchling Tenant

    benchling_access_token: str
        determined in config. Access token for API of Benchling Tenant

    app_client_id: str
    determined in .env. App Client ID

    app_client_secret: str
        determined in .env. App Client Secret

    benchling_registry_id: str
        determined in __init__(). Benchling  registry  associates with tenant
        (such as bostongene). This parameter is common for all objects.

    """

    def __init__(self,
                 benchling_url: str,
                 benchling_access_token: str,
                 app_client_id: str,
                 app_client_secret: str
                 ) -> None:
        self.benchling_url = benchling_url
        self.benchling_access_token = benchling_access_token
        self.app_client_id = app_client_id
        self.app_client_secret = app_client_secret

        """
        Get a Benchling object with the client credentials OAuth2 flow. Get registry id.
        """

        oauth2 = ClientCredentialsOAuth2(
            client_id=self.app_client_id,
            client_secret=self.app_client_secret,
            token_url=self.benchling_access_token
        )  # Authentication with client credentials OAuth2 flow

        self.benchling = Benchling(url=self.benchling_url,
                                   auth_method=oauth2,
                                   retry_strategy=RetryStrategy(max_tries=_RETRY_STRATEGY_MAX_TRIES)
                                   )  # initialize Benchling object

        self.benchling_registry_id = self.benchling.registry.registries()[0].id  # registry id

    @_with_retry
    def get_entity_by_name(self, entity_name: str) -> CustomEntity:
        """
        Get the entity for the given entity name.

        :param: entity_name - name of the entity.
        :return: entity - entity for the given entity name
        """
        return self.benchling.custom_entities.list(name=entity_name).first()

    @_with_retry
    def get_entities_by_names(self, entity_names: list[str]) -> PageIterator[CustomEntity]:
        """
        Get the entity for the given list of entity names.

        :param: entity_names - name of the entity.
        :return: entity - entity for the given entity name
        """
        return self.benchling.custom_entities.list(names_any_of=entity_names)

    @_with_retry
    def get_entity_by_id(self, entity_id: str) -> CustomEntity:
        """
        Get the entity for the given entity id.

        :param: entity_id - id of the entity
        :return: entity - entity for the given entity id
        """
        return self.benchling.custom_entities.get_by_id(entity_id)

    @_with_retry
    def get_entities_by_ids(self,
                            entity_ids: list[str]) -> PageIterator[CustomEntity]:
        """
        Get the entity by the registry ids.

        :param: entity_registry_ids_any_of - list of registry ids
        :return: page iterator with entities - list of entities for the given registry ids
        """
        registry_id = self.benchling_registry_id
        return self.benchling.custom_entities.list(registry_id=registry_id,
                                                   entity_registry_ids_any_of=entity_ids)

    @_with_retry
    def get_sequence_by_name(self, entity_name: str) -> CustomEntity:
        """
        Get the entity for the given entity name.

        :param: entity_name - name of the entity
        :return: entity - entity for the given entity name
        """
        return self.benchling.dna_sequences.list(name=entity_name).first()

    @_with_retry
    def get_sequence_by_id(self, entity_id: str) -> DnaSequence:
        """
        Get the entity for the given entity id.

        :param: entity_id - id of the entity.
        :return: entity - entity for the given entity id
        """
        return self.benchling.dna_sequences.get_by_id(entity_id)

    @_with_retry
    def get_sequences_by_ids(self, entity_ids: list[str]) -> PageIterator[DnaSequence]:
        """
        Get the entity for the given entity id.

        :param: entity_id - id of the entity.
        :return: entity - entity for the given entity id
        """
        registry_id = self.benchling_registry_id
        return self.benchling.dna_sequences.list(registry_id=registry_id,
                                                 entity_registry_ids_any_of=entity_ids)

    @_with_retry
    def get_entity_by_modified(self, schema_id: str, modified_at: str) -> PageIterator[CustomEntity]:
        """
        Get the entity by the modified_at entity attribute.

        :param: schema_id - id of the schema
        :param: modified_at - modified_at attribute of the entity (datetime, RFC 3339 format)
        :return: page iterator with entities - list entity for the given (field name, field value) pair
        """
        return self.benchling.custom_entities.list(schema_id=schema_id, modified_at=f'> {modified_at}')

    @_with_retry
    def get_entity_by_schema_and_fields(self, schema_id: str, fields_dict: dict) -> PageIterator[CustomEntity]:
        """
        Get the entity by the schema id.

        :param: schema_id - id of the schema
        :return: page iterator with entities - list entity for the given schema id
        """
        return self.benchling.custom_entities.list(schema_id=schema_id,
                                                   schema_fields=fields_dict,
                                                   page_size=100)

    @_with_retry
    def get_results_by_schema_field(self, schema_id: str, entity_ids: list[str]) -> PageIterator[AssayResult]:
        """
        Get the result by the schema and entity id.

        :param: schema_id - id of the schema
        :return: page iterator with entities - list entity for the given schema id
        """
        return self.benchling.assay_results.list(schema_id=schema_id,
                                                 entity_ids=entity_ids
                                                 )

    @_with_retry
    def update_entity(self, entity: CustomEntity, fields_dict: dict) -> None:
        """
        Update the entity with the given fields_dict.

        :param: entity - entity to update
        :param: fields_dict - fields to update in the format of {field_name: field_value}
        :return: None
        """
        entity_id = entity.id
        update_entity = models.CustomEntityUpdate(fields=fields(fields_dict_converter(fields_dict)))
        self.benchling.custom_entities.update(entity_id=entity_id, entity=update_entity)

    def construct_entity(self, folder_id: str, schema_id: str, entity_name: str, fields_dict: dict,
                         naming_strategy: NamingStrategy) -> models.CustomEntityCreate:
        """
        Construct the entity with the given schema_id and fields_dict for push to Benchling.
        :param: folder_id - id of the folder to push the entity to
        :param: schema_id - id of the entity schema
        :param: fields_dict - fields to update in the format of {field_name: field_value}
        :param: naming_strategy - naming strategy for the entity registration
        :return: entity - constructed entity
        """
        registry_id = self.benchling_registry_id
        entity = models.CustomEntityCreate(
            fields=fields(fields_dict_converter(fields_dict)),
            folder_id=folder_id,
            name=entity_name,
            registry_id=registry_id,
            naming_strategy=naming_strategy,
            schema_id=schema_id
        )
        return entity

    @_with_retry
    def register_entity(self, entity: models.CustomEntityCreate) -> None:
        """
        Register the entity in Benchling.
        :param: entity - entity to register
        :return: None
        """
        self.benchling.custom_entities.create(entity=entity)

    @_with_retry
    def unregister_entities(self, entity_ids: list[str], folder_id: str) -> None:
        """
        Unregister the entity in Benchling.
        :param: entity_id - id of the entity to unregister
        :return: None
        """
        registry_id = self.benchling_registry_id
        self.benchling.registry.unregister(registry_id=registry_id,
                                           entity_ids=entity_ids,
                                           folder_id=folder_id)

    @_with_retry
    def get_dropdown_options(self, dropdown: models.Dropdown) -> dict:
        """
        Get dropdown variants by dropdown id.
        :param dropdown: dropdown object.
        :type dropdown: models.Dropdown.
        :return: dropdown options with corresponding api ids.
        :rtype: dict.
        """
        options = dropdown.options
        options = {option.name: option.id for option in options}
        return options

    @_with_retry
    def update_dropdown(self, dropdown_id: str, options_to_add: list) -> None:
        """
        Update a dropdown by dropdown_id with the given options.

        :param dropdown_id: id of a dropdown
        :type dropdown_id: str
        :param options_to_add: options to add
        :type options_to_add: list
        :return: None
        """
        dropdown = self.benchling.dropdowns.get_by_id(dropdown_id)
        dropdown_options = self.get_dropdown_options(dropdown=dropdown)
        dropdown_options_for_upd = construct_dropdown_update(dropdown_options=dropdown_options)

        for option in options_to_add:
            dropdown_options_for_upd.append(models.DropdownOptionUpdate(name=option))

        self.benchling.dropdowns.update(dropdown_id=dropdown_id, dropdown=models.DropdownUpdate(
            options=dropdown_options_for_upd))

    @_with_retry
    def register_assay_results(self, assay_results: list[models.AssayResultCreate]) -> None:
        """
        Register the assay result in Benchling.
        :param: assay_result - assay result to register - accepts a list
        :return: None
        """
        self.benchling.assay_results.create(assay_results=assay_results)


def get_entity_name(entity: CustomEntity) -> str:
    """
    Get the name of the entity.

    :param: entity - benchling entity
    :return: entity name - name of the entity
    """
    try:
        return entity.name
    except IndexError:
        raise ValueError("Can not get entity name")


def get_entity_id(entity: CustomEntity) -> str:
    """
    Get the entity id of the entity.

    :param: entity - benchling entity
    :return: entity id - entity id of the entity
    """
    try:
        return entity.id
    except IndexError:
        raise ValueError("Can not get entity id")


def get_field_value(entity: CustomEntity, field_name: str) -> str:
    """
    Get the value of the field with the given name.

    :param: entity - benchling entity
    :param: field_name - name of the field
    :return: field value - value of the field with the given name
    """
    try:
        return entity.fields[field_name].value
    except IndexError:
        raise ValueError(f"Can not get field value for {field_name}")


def get_display_field_value(entity: CustomEntity, field_name: str) -> str:
    """
    Get the display value of the field with the given name.

    :param: entity - benchling entity
    :param: field_name - name of the field
    :return: field display value - display value of the field with the given name
    """
    try:
        return entity.fields[field_name].display_value
    except IndexError:
        raise ValueError(f"Can not get field display value for {field_name}")


def get_empty_entity_fields(entity: CustomEntity) -> list:
    """
    Get empty fields (value=None) for a given CustomEntity.

    :param entity: benchling custom entity
    :type entity: models.CustomEntity
    :return: names of the empty fields for a given entity
    :rtype: list
    """
    empty_entity_fields = []
    for field_name, field_value in entity.fields.to_dict().items():
        if field_value['value'] in (None, []):  # [] for multi-select fields
            empty_entity_fields.append(field_name)

    return empty_entity_fields


def fields_dict_converter(fields_dict: dict) -> dict:
    """
    Convert the fields_dict without "value" keyword
    to the format of {field_name: {'value': field_value}}.

    :param: fields_dict - fields to update in the format of {field_name: field_value}
    :return: converted fields_dict
    """
    converted_fields_dict = {}
    for field_name, field_value in fields_dict.items():
        converted_fields_dict[field_name] = {'value': field_value}
    return converted_fields_dict


def construct_dropdown_update(dropdown_options: dict) -> list[models.DropdownOptionUpdate]:
    """
    Construct the list of existing dropdown options for dropdown updating.

    :param dropdown_options: dict with key - option name, value - option api id
    :type dropdown_options: dict
    :return: list of existing dropdown options for dropdown updating
    :rtype: list[models.DropdownOptionUpdate]
    """
    return [models.DropdownOptionUpdate(id=id_, name=name) for name, id_ in dropdown_options.items()]


def construct_assay_result(schema_id: str, fields_dict: dict, project_id: str) -> models.AssayResultCreate:
    """
    Construct the assay result with the given schema_id and fields_dict for push to Benchling.
    :param: schema_id - id of the assay result schema
    :param: fields_dict - fields to update in the format of {field_name: field_value}
    :param: project_id - id of the project to push the assay result to
    :return: assay result - constructed assay result
    """
    assay_result = models.AssayResultCreate(
        schema_id=schema_id,
        fields=fields(fields_dict_converter(fields_dict)),
        project_id=project_id
    )
    return assay_result
