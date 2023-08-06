from typing import Optional, Union, List
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import itertools
import traceback

import numpy as np
import pandas as pd

from .. import _credentials
from .. import endpoints
from .. import utils

__all__ = [
    "get_batch_types",
    "get_batch_type_details",
    "get_single_batch",
    "get_batches",
    "update_batch_values",
    "update_batch_feature_values",
    "update_batch_features_and_values",
    "update_vector_batch_values",
    "create_or_update_batches",
]


def get_batch_types(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get the configured batch types from the OIAnalytics API

    Parameters
    ----------
    page: int, optional
        Page number to retrieve. If None, the first page will be retrieved.
        The argument is ignored if 'get_all_pages' is True.
    page_size: int, optional
        The size of each page to retrieve. By default, 20 elements are retrieved.
        The argument is ignored if 'get_all_pages' is True.
    get_all_pages: bool, default True
        If True, paging is ignored and all elements are retrieved.
    multithread_pages: bool, default False
        Only used when getting all pages. If True, pages are retrieved in multiple threads simultaneously.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A DataFrame listing batch types
    """

    # Init
    if get_all_pages is True:
        page = 0
        page_size = 500

    def get_page(page_num: int):
        page_response = endpoints.batches.get_batch_types(
            page=page_num, page_size=page_size, api_credentials=api_credentials
        )
        return page_response

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])

        # Expected columns if content is empty
        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(columns=["id", "name"])

        page_df.set_index("id", inplace=True)
        return page_df

    # Query endpoint
    df = utils.concat_pages_to_dataframe(
        getter=get_page,
        parser=parse_page,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )

    # Output
    return df


def get_batch_type_details(
    batch_type_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get details about a single batch type from the OIAnalytics API

    Parameters
    ----------
    batch_type_id: str
        The id of the batch type to be retrieved.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A tuple of 3 DataFrames listing various properties of the batch type:
        - Steps
        - Data
        - Features
    """

    # Query endpoint
    response = endpoints.batches.get_batch_type_details(
        batch_type_id=batch_type_id, api_credentials=api_credentials
    )

    # Split content
    steps = response["steps"]
    data = response["dataList"]
    features = response["features"]

    # Format dataframes
    if len(steps) > 0:
        df_steps = pd.DataFrame(steps).set_index("id")
    else:
        df_steps = pd.DataFrame(columns=["id", "name", "localisationKeys"]).set_index(
            "id"
        )

    if len(data) > 0:
        df_data = pd.DataFrame(data).set_index("id")
    else:
        df_data = pd.DataFrame(
            columns=["id", "dataType", "reference", "description"]
        ).set_index("id")

    if len(features) > 0:
        df_features = pd.DataFrame(features).set_index("id")
    else:
        df_features = pd.DataFrame(columns=["id", "key"]).set_index("id")

    # Output
    return df_steps, df_data, df_features


def get_single_batch(
    batch_type_id: str,
    batch_id: str,
    split_steps_and_values: bool = True,
    extract_from_localisation: Optional[str] = "value",
    expand_localisation: bool = True,
    extract_from_values: Optional[str] = "reference",
    expand_value_ids: bool = True,
    extract_from_features: Optional[str] = "value",
    expand_features: bool = True,
    append_unit_to_description: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    # Args validation
    if extract_from_localisation not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_localisation': {extract_from_localisation}"
        )

    if extract_from_localisation is None and expand_localisation is True:
        raise ValueError(
            "Localisation cannot be expanded if 'extract_from_values' is None"
        )

    if extract_from_values not in ["id", "reference", "description", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_values': {extract_from_values}"
        )

    if extract_from_values is None and expand_value_ids is True:
        raise ValueError("Values cannot be expanded if 'extract_from_values' is None")

    if extract_from_features not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_features': {extract_from_features}"
        )

    if extract_from_features is None and expand_features is True:
        raise ValueError(
            "Features cannot be expanded if 'extract_from_features' is None"
        )

    # Query endpoint
    response = endpoints.batches.get_single_batch(
        batch_type_id=batch_type_id, batch_id=batch_id, api_credentials=api_credentials
    )

    # Format response
    df = pd.Series(response).to_frame().T

    # Expected columns if content is empty
    if df.shape[0] == 0:
        df = pd.DataFrame(
            columns=["id", "name", "timestamp", "steps", "values", "features"]
        )

    # Rename columns
    df.rename(
        columns={
            "id": "batch_id",
            "name": "batch_name",
            "timestamp": "batch_timestamp",
        },
        inplace=True,
    )

    # Parse dates
    df["batch_timestamp"] = pd.to_datetime(df["batch_timestamp"])

    # Set index
    df.set_index(["batch_id", "batch_name", "batch_timestamp"], inplace=True)

    # Split steps and values
    if split_steps_and_values is True:
        # Split dataframe
        df_steps = df.drop(columns=["values", "features"])
        df_values = df.drop(columns="steps")

        # Format steps
        df_steps = df_steps.explode("steps")
        df_steps = utils.expand_dataframe_column(
            df_steps,
            "steps",
            add_prefix=False,
            expected_keys=[
                "step",
                "start",
                "end",
                "localisationType",
                "assetLocalisation",
                "tagValuesLocalisation",
            ],
        )
        df_steps = utils.expand_dataframe_column(
            df_steps, "step", expected_keys=["id", "name"]
        )

        df_steps["start"] = pd.to_datetime(df_steps["start"])
        df_steps["end"] = pd.to_datetime(df_steps["end"])

        if extract_from_localisation == "id":
            df_steps["assetLocalisation"] = df_steps["assetLocalisation"].map(
                lambda asset: None if asset is None else asset["id"]
            )

            df_steps["tagValuesLocalisation"] = df_steps["tagValuesLocalisation"].apply(
                lambda full_loc: {loc["tagKey"]["id"]: loc["id"] for loc in full_loc}
            )

        elif extract_from_localisation == "value":
            df_steps["assetLocalisation"] = df_steps["assetLocalisation"].map(
                lambda asset: None if asset is None else asset["name"]
            )

            df_steps["tagValuesLocalisation"] = df_steps["tagValuesLocalisation"].apply(
                lambda full_loc: {
                    loc["tagKey"]["key"]: loc["value"] for loc in full_loc
                }
            )

        if expand_localisation is True and extract_from_localisation is not None:
            df_steps = utils.expand_dataframe_column(
                df_steps, "tagValuesLocalisation", add_prefix=False
            )

        df_steps.set_index(["step_id"], append=True, inplace=True)

        # Format values
        if extract_from_values == "id":
            df_values["values"] = df_values["values"].apply(
                lambda values: {val["data"]["id"]: val["value"] for val in values}
            )
        elif extract_from_values == "reference":
            df_values["values"] = df_values["values"].apply(
                lambda values: {
                    val["data"]["reference"]: val["value"] for val in values
                }
            )
        elif extract_from_values == "description":
            if append_unit_to_description is True:
                df_values["values"] = df_values["values"].apply(
                    lambda values: {
                        f'{val["data"]["description"]} ({val["unit"]["label"]})': val[
                            "value"
                        ]
                        for val in values
                    }
                )
            else:
                df_values["values"] = df_values["values"].apply(
                    lambda values: {
                        val["data"]["description"]: val["value"] for val in values
                    }
                )

        if expand_value_ids is True and extract_from_values is not None:
            df_values = utils.expand_dataframe_column(
                df_values, "values", add_prefix=False
            )

        if extract_from_features == "id":
            df_values["features"] = df_values["features"].apply(
                lambda features: {feat["tagKey"]["id"]: feat["id"] for feat in features}
            )
        elif extract_from_features == "value":
            df_values["features"] = df_values["features"].apply(
                lambda features: {
                    feat["tagKey"]["key"]: feat["value"] for feat in features
                }
            )

        if expand_features is True and extract_from_features is not None:
            df_values = utils.expand_dataframe_column(
                df_values, "features", add_prefix=False
            )

        # Output
        return df_steps, df_values
    else:
        return df


def get_batches(
    batch_type_id: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    name: Optional[str] = None,
    features_value_ids: Optional[Union[str, List[str]]] = None,
    asset_ids: Optional[Union[str, List[str]]] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    get_all_pages: bool = True,
    multithread_pages: bool = True,
    split_steps_and_values: bool = True,
    extract_from_localisation: Optional[str] = "value",
    expand_localisation: bool = True,
    extract_from_values: Optional[str] = "reference",
    expand_value_ids: bool = True,
    extract_from_features: Optional[str] = "value",
    expand_features: bool = True,
    append_unit_to_description: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Get batch instances from the OIAnalytics API

    Parameters
    ----------
    batch_type_id: str
        The id of the batch type to be retrieved
    start_date: datetime or str
        The beginning of the period to be retrieved
    end_date: datetime or str
        The end of the period to be retrieved
    name: str, optional
        A string that should be contained by all batch names returned
    features_value_ids: str or list of str, optional
        Possibly multiple feature value ids each returned batch should match.
        If for a given feature multiple feature value ids are provided then a batch will be returned if it
        contains one of them.
    page: int, optional
        Page number to retrieve. If None, the first page will be retrieved.
        The argument is ignored if 'get_all_pages' is True.
    page_size: int, optional
        The size of each page to retrieve. By default, 20 elements are retrieved.
        The argument is ignored if 'get_all_pages' is True.
    get_all_pages: bool, default True
        If True, paging is ignored and all elements are retrieved.
    multithread_pages: bool, default False
        Only used when getting all pages. If True, pages are retrieved in multiple threads simultaneously.
    split_steps_and_values: bool, default True
        If True, the response will be split into two separate DataFrames instead of a single dense one.
    extract_from_localisation: {'id', 'value', None}, default 'value'
        What field should be extracted from localisation information. If None, the full dictionary is kept.
    expand_localisation: bool, default True
        Whether or not localisation information should be expanded into multiple columns.
    extract_from_values: {'id', 'reference', 'description', None}, default 'reference'
        What field should be extracted for naming data. If None, the full dictionary is kept.
    expand_value_ids: bool, default True
        Whether or not data should be expanded into multiple columns.
    extract_from_features: {'id', 'value', None}, default 'value'
        What field should be extracted for naming features. If None, the full dictionary is kept.
    expand_features: bool, default True
        Whether or not features should be expanded into multiple columns.
    append_unit_to_description: bool, default True
        Only used when 'extract_from_values' is 'description'. If True, the unit is added after the description.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    If 'split_steps_and_values' is False, a single DataFrame containing batches and their information in dictionaries
    is returned.
    If 'split_steps_and_values' is True (default behaviour), a tuple of 2 DataFrames is returned:
        - Batch steps
        - Batch data and features
    """

    # Args validation
    if extract_from_localisation not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_localisation': {extract_from_localisation}"
        )

    if extract_from_localisation is None and expand_localisation is True:
        raise ValueError(
            "Localisation cannot be expanded if 'extract_from_values' is None"
        )

    if extract_from_values not in ["id", "reference", "description", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_values': {extract_from_values}"
        )

    if extract_from_values is None and expand_value_ids is True:
        raise ValueError("Values cannot be expanded if 'extract_from_values' is None")

    if extract_from_features not in ["id", "value", None]:
        raise ValueError(
            f"Unexpected value for 'extract_from_features': {extract_from_features}"
        )

    if extract_from_features is None and expand_features is True:
        raise ValueError(
            "Features cannot be expanded if 'extract_from_features' is None"
        )

    # Init
    if get_all_pages is True:
        page = 0
        page_size = 500

    def get_page(page_num: int):
        page_response = endpoints.batches.get_batches(
            batch_type_id=batch_type_id,
            start_date=start_date,
            end_date=end_date,
            name=name,
            features_value_ids=features_value_ids,
            asset_ids=asset_ids,
            page=page_num,
            page_size=page_size,
            api_credentials=api_credentials,
        )
        return page_response

    def parse_page(page_response: dict):
        page_df = pd.DataFrame(page_response["content"])

        # Expected columns if content is empty
        if page_df.shape[0] == 0:
            page_df = pd.DataFrame(
                columns=["id", "name", "timestamp", "steps", "values", "features"]
            )

        # Rename columns
        page_df.rename(
            columns={
                "id": "batch_id",
                "name": "batch_name",
                "timestamp": "batch_timestamp",
            },
            inplace=True,
        )

        # Parse dates
        page_df["batch_timestamp"] = pd.to_datetime(page_df["batch_timestamp"])

        # Set index
        page_df.set_index(["batch_id", "batch_name", "batch_timestamp"], inplace=True)
        return page_df

    # Query endpoint
    df = utils.concat_pages_to_dataframe(
        getter=get_page,
        parser=parse_page,
        page=page,
        get_all_pages=get_all_pages,
        multithread_pages=multithread_pages,
    )

    # Split steps and values
    if split_steps_and_values is True:
        # Split dataframe
        df_steps = df.drop(columns=["values", "features"])
        df_values = df.drop(columns="steps")

        # Format steps
        df_steps = df_steps.explode("steps")
        df_steps = utils.expand_dataframe_column(
            df_steps,
            "steps",
            add_prefix=False,
            expected_keys=[
                "step",
                "start",
                "end",
                "localisationType",
                "assetLocalisation",
                "tagValuesLocalisation",
            ],
        )
        df_steps = utils.expand_dataframe_column(
            df_steps, "step", expected_keys=["id", "name"]
        )

        df_steps["start"] = pd.to_datetime(df_steps["start"])
        df_steps["end"] = pd.to_datetime(df_steps["end"])

        if extract_from_localisation == "id":
            df_steps["assetLocalisation"] = df_steps["assetLocalisation"].map(
                lambda asset: None if asset is None else asset["id"]
            )

            df_steps["tagValuesLocalisation"] = df_steps["tagValuesLocalisation"].apply(
                lambda full_loc: {loc["tagKey"]["id"]: loc["id"] for loc in full_loc}
            )

        elif extract_from_localisation == "value":
            df_steps["assetLocalisation"] = df_steps["assetLocalisation"].map(
                lambda asset: None if asset is None else asset["name"]
            )

            df_steps["tagValuesLocalisation"] = df_steps["tagValuesLocalisation"].apply(
                lambda full_loc: {
                    loc["tagKey"]["key"]: loc["value"] for loc in full_loc
                }
            )

        if expand_localisation is True and extract_from_localisation is not None:
            df_steps = utils.expand_dataframe_column(
                df_steps, "tagValuesLocalisation", add_prefix=False
            )

        df_steps.set_index(["step_id"], append=True, inplace=True)

        # Format values
        if extract_from_values == "id":
            df_values["values"] = df_values["values"].apply(
                lambda values: {val["data"]["id"]: val["value"] for val in values}
            )
        elif extract_from_values == "reference":
            df_values["values"] = df_values["values"].apply(
                lambda values: {
                    val["data"]["reference"]: val["value"] for val in values
                }
            )
        elif extract_from_values == "description":
            if append_unit_to_description is True:
                df_values["values"] = df_values["values"].apply(
                    lambda values: {
                        f'{val["data"]["description"]} ({val["unit"]["label"]})': val[
                            "value"
                        ]
                        for val in values
                    }
                )
            else:
                df_values["values"] = df_values["values"].apply(
                    lambda values: {
                        val["data"]["description"]: val["value"] for val in values
                    }
                )

        if expand_value_ids is True and extract_from_values is not None:
            df_values = utils.expand_dataframe_column(
                df_values, "values", add_prefix=False
            )

        if extract_from_features == "id":
            df_values["features"] = df_values["features"].apply(
                lambda features: {feat["tagKey"]["id"]: feat["id"] for feat in features}
            )
        elif extract_from_features == "value":
            df_values["features"] = df_values["features"].apply(
                lambda features: {
                    feat["tagKey"]["key"]: feat["value"] for feat in features
                }
            )

        if expand_features is True and extract_from_features is not None:
            df_values = utils.expand_dataframe_column(
                df_values, "features", add_prefix=False
            )

        # Output
        return df_steps, df_values
    else:
        return df


def update_batch_values(
    batch_type_id: str,
    data: Union[pd.Series, pd.DataFrame],
    unit_ids: Optional[dict] = None,
    batch_id_index_name: str = "batch_id",
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """

    Parameters
    ----------
    batch_type_id: str
        The id of the batch type to be retrieved
    data: pd.Series or pd.DataFrame
        Object containing the data to be uploaded, where the index contains the batches ids and the
    unit_ids: dict[str, str], optional
        Dictionary with the unit-ids of data to be uploaded.
        Each key is a data-id that points to the corresponding unit-id.
    batch_id_index_name: str, default 'batch_id'
        The name of the Series's or DataFrame's index
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------

    """
    # Init
    if unit_ids is None:
        unit_ids = {}

    if isinstance(data, pd.Series):
        data = pd.DataFrame(data)
    else:
        data = data.copy()

    data.index = data.index.get_level_values(batch_id_index_name)

    # Send each individual value
    def send_value(batch_value_tuple: tuple):
        batch_id = batch_value_tuple[0]
        data_id = batch_value_tuple[1]
        value = batch_value_tuple[2]
        endpoints.batches.update_batch_value(
            batch_type_id=batch_type_id,
            batch_id=batch_id,
            data_id=data_id,
            value=value,
            unit_id=unit_ids.get(data_id, None),
            api_credentials=api_credentials,
        )

    # Build the iterator over individual batch value tuples (batch_id, data_id, value)
    batch_values = list(
        itertools.chain.from_iterable(
            [
                [(idx,) + i for i in r.iteritems() if not np.isnan(i[1])]
                for idx, r in data.iterrows()
            ]
        )
    )

    with ThreadPoolExecutor() as pool:
        updates = pool.map(send_value, batch_values)

    try:
        print(f"{len(list(updates))} batch values sent to OIAnalytics")
    except Exception:
        print(f"Error during batch values update:\n{traceback.format_exc()}")


def update_batch_feature_values(
    batch_type_id: str,
    data: Union[pd.Series, pd.DataFrame],
    batch_id_index_name: str = "batch_id",
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Insert/update batches features values
    Parameters
    ----------
    batch_type_id: str
        The id of the batch type to be retrieved.
    data: pd.Series or pd.DataFrame
        Object containing the features values to be uploaded:
        - The index contains the batch-ids;
        - If the object is a DataFrame, the columns contains the features names;
        - If the object is a Series, the Series' name is the feature name being updated
        - The data contains the features values.
    batch_id_index_name: str, default 'batch_id'
        The name of the Dataframe's or Series's index.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------

    """
    # Init
    if isinstance(data, pd.Series):
        data = pd.DataFrame(data)
    else:
        data = data.copy()

    data.index = data.index.get_level_values(batch_id_index_name)

    # Send each individual value
    def send_value(batch_value_tuple: tuple):
        batch_id = batch_value_tuple[0]
        feature_id = batch_value_tuple[1]
        value = batch_value_tuple[2]
        endpoints.batches.update_batch_feature_value(
            batch_type_id=batch_type_id,
            batch_id=batch_id,
            feature_id=feature_id,
            value=value,
            api_credentials=api_credentials,
        )

    # Build the iterator over individual batch value tuples (batch_id, data_id, value)
    batch_values = list(
        itertools.chain.from_iterable(
            [
                [(idx,) + i for i in r.iteritems() if not np.isnan(i[1])]
                for idx, r in data.iterrows()
            ]
        )
    )

    with ThreadPoolExecutor() as pool:
        pool.map(send_value, batch_values)


def update_batch_features_and_values(
    batch_type_id: str,
    data: pd.DataFrame,
    feature_columns: Optional[List[str]] = None,
    unit_ids: Optional[dict[str, str]] = None,
    batch_id_index_name: str = "batch_id",
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    It updates many batches values and features values at once

    Parameters
    ----------
    batch_type_id: str
        The id of the batch type to be retrieved.
    data: pd.DataFrame
        Object containing the features values and values to be uploaded:
        - The index contains the batch-ids;
        - The columns contains the features-ids and data-ids;
        - The data contains the features values.
    feature_columns: list of str, optional
        List containing the names of the Dataframe's columns corresponding to the features-ids.
    unit_ids: dict[str, str], optional
        Dictionary with the unit-ids of data to be uploaded.
        Each key is a data-id that points to the corresponding unit-id.
    batch_id_index_name: str, default 'batch_id'
        The name of the Dataframe's or Series's index.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A dictionary of the response from the API, containing the data insert report
    """

    # Init
    if feature_columns is None:
        feature_columns = []

    if unit_ids is None:
        unit_ids = {}

    data.index = data.index.get_level_values(batch_id_index_name)

    payload = []
    for index in data.index:
        payload.append(
            {
                "batchId": index,
                "batchFeatureCommands": [
                    {
                        "batchTagKeyId": tag,
                        "batchTagValueValue": data.loc[index, tag],
                    }
                    for tag in feature_columns
                    if pd.notnull(data.loc[index, tag])
                ],
                "batchValueCommands": [
                    {
                        "dataId": data_id,
                        "value": float(data.loc[index, data_id]),
                        "unitId": unit_ids.get(data_id),
                    }
                    for data_id in [
                        col for col in data.columns if col not in feature_columns
                    ]
                    if pd.notnull(data.loc[index, data_id])
                ],
            }
        )

    response = endpoints.batches.update_batch_features_and_values(
        batch_type_id=batch_type_id, data=payload, api_credentials=api_credentials
    )

    return response


def update_vector_batch_values(
    data: Union[pd.DataFrame, List[pd.DataFrame]],
    data_reference: Union[str, List[str]],
    index_units: Optional[dict] = None,
    values_units: Optional[dict] = None,
    batch_id_index_name: str = "batch_id",
    use_external_reference: bool = False,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Insert time values stored in a DataFrame through the OIAnalytics API

    Parameters
    ----------
    data: list of dictionaries
        List where each element has a 'dataReference' as a key and a dataframe as a value.
    data_reference: string or list of strings
        The unique data reference for the data being inserted.
    index_units: dictionary, optional
        A dictionary indexed by data reference, specifying the values in which it is sent.
    values_units: dictionary, optional
        A dictionary indexed by data reference, specifying the values in which it is sent.
    batch_id_index_name: string, default 'batch_id'
        The name of the index of the DataFrame(s)
    use_external_reference: bool, default False
        If True, the data are named using their external reference; if False, the OIAnalytics reference is used.
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A dictionary of the response from the API, containing the data insert report
    """

    # Init 'index_units'
    if index_units is None:
        index_units = {}

    # Init 'values_units'
    if values_units is None:
        values_units = {}

    # Init list of data and list of data_reference
    if isinstance(data, pd.DataFrame):
        data = [data.copy()]
        data_reference = [data_reference]

    # Build DTO
    payload = []
    for reference, df in zip(data_reference, data):
        try:
            df.index = df.index.get_level_values(batch_id_index_name)
        except KeyError:
            raise KeyError("The dataframe must have an index level named 'batch_id'")
        # Build payload for the data
        payload.append(
            {
                "dataReference": reference,
                "indexUnit": index_units.get(reference, None),
                "valueUnit": values_units.get(reference, None),
                "batchIds": df.index.tolist(),
                "indexes": df.columns.tolist(),
                "values": df.to_numpy().tolist(),
            }
        )

    # Query endpoint
    response = endpoints.batches.update_vector_batch_values(
        data=payload,
        use_external_reference=use_external_reference,
        api_credentials=api_credentials,
    )

    # Output
    return response


def create_or_update_batches(
    batch_type_id: str,
    steps: pd.DataFrame,
    values: Optional[pd.DataFrame] = None,
    values_unit_ids: Optional[dict] = None,
    features: Optional[pd.DataFrame] = None,
    vector_data_values: Optional[Union[pd.DataFrame, List[pd.DataFrame]]] = None,
    vector_data_references: Optional[List[str]] = None,
    vector_data_index_units: Optional[dict] = None,
    vector_data_values_units: Optional[dict] = None,
    on_duplicates_keep: str = "last",
    batch_name_index_name: str = "batch_name",
    step_id_index_name: str = "step_id",
    start_date_name: str = "start",
    end_date_name: str = "end",
    asset_localisation_column: Optional[str] = None,
    tag_localisation_columns: Optional[Union[str, List[str]]] = None,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
):
    """
    Create or update batches, including steps, values, vector values and features

    Parameters
    ----------
    batch_type_id: str
        The id of the batch type to be retrieved.
    steps: pd.DataFrame
        The steps of the batches to insert. The DataFrame is indexed by batch name (named after batch_name_index_name).
        The content of this DataFrame must be:
            - The step ID (named after step_id_index_name)
            - The start and end dates of the steps (named after start_date_name and end_date_name)
            - Optional asset or tag localisation columns
    values: pd.DataFrame, optional
        The data values to update or insert. The DataFrame must be indexed by batch name (Cf. batch_name_index_name).
        Each column is named after the data ID.
    values_unit_ids: dict, optional
        A dictionary where keys are data IDs and values are the corresponding unit IDs
    features: pd.DataFrame, optional
        The feature values to update or insert. The DataFrame must be indexed by batch name (Cf. batch_name_index_name).
        Each column is named after the feature ID.
    vector_data_values: pd.DataFrame or list of pd.DataFrame, optional
        The vector data values to insert or update. Must be indexed by batch name (Cf. batch_name_index_name).
        Each column is a vector index.
    vector_data_references: list of str, optional
        The list of the vector data references matching the list  of vector data values DataFrames
    vector_data_index_units: dict, optional
        A dictionary where keys are vector data references and values are the corresponding unit labels for indexes
    vector_data_values_units: dict, optional
        A dictionary where keys are vector data references and values are the corresponding unit labels for values
    on_duplicates_keep: {'first', 'last', False}, default 'last'
        Indicate which DataFrame row to keep in case of duplicates (Cf. pd.DataFrame.drop_duplicates)
    batch_name_index_name: str, default 'batch_name'
        The name of the index level containing the batch name in the DataFrames
    step_id_index_name: str, default 'step_id'
        The name of the index level (or column) containing the step id in the steps DataFrame
    start_date_name: str, default 'start'
        The name of the column containing the start date of the steps id in the steps DataFrame
    end_date_name: str, default 'end'
        The name of the column containing the end date of the steps id in the steps DataFrame
    asset_localisation_column: str, optional
        The name of the column containing the asset IDs allowing the localisation of steps
    tag_localisation_columns: str or list of str, optional
        The name of the columns containing the tag value IDs allowing the localisation of steps
    api_credentials: OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    A dictionary of the response from the API, containing the list of created or updated batches
    """

    # Validate arguments
    if on_duplicates_keep not in ["first", "last"]:
        raise ValueError(
            f"Unexpected value for 'on_duplicates_keep': {on_duplicates_keep}. Only 'first' and 'last' are accepted."
        )

    # Init
    if values_unit_ids is None:
        values_unit_ids = {}

    if isinstance(tag_localisation_columns, str):
        tag_localisation_columns = [tag_localisation_columns]

    if isinstance(vector_data_values, pd.DataFrame):
        vector_data_values = [vector_data_values]

    # Build payload
    batches = []

    # Append each batch to the payload
    for batch_name in steps.index.get_level_values(batch_name_index_name).unique():
        # Init
        batch_command = {"name": batch_name}

        # Build steps command
        batch_steps = steps.loc[
            steps.index.get_level_values(batch_name_index_name) == batch_name
        ].reset_index()

        def build_single_step_payload(step):
            # Step dates
            step_payload = {
                "stepId": step[step_id_index_name],
                "start": utils.get_zulu_isoformat(step[start_date_name]),
                "end": utils.get_zulu_isoformat(step[end_date_name]),
            }

            # Localisation
            if (
                asset_localisation_column is not None
                and step.notna()[asset_localisation_column]
            ):
                step_payload["localisationType"] = "ASSET"
                step_payload["localisationTagValueIds"] = []
                step_payload["localisationAssetId"] = step[asset_localisation_column]

            elif (
                tag_localisation_columns is not None
                and len(tag_localisation_columns) > 0
                and step.notna()[tag_localisation_columns].any()
            ):
                step_payload["localisationType"] = "TAG_VALUES"
                step_payload["localisationTagValueIds"] = (
                    step[tag_localisation_columns].dropna().to_list()
                )
                step_payload["localisationAssetId"] = None

            else:
                step_payload["localisationType"] = "NO_LOCALISATION"
                step_payload["localisationTagValueIds"] = []
                step_payload["localisationAssetId"] = None

            return step_payload

        batch_command["steps"] = batch_steps.apply(
            build_single_step_payload, axis=1
        ).to_list()

        # Build values command
        if values is None:
            batch_command["values"] = []
        else:
            batch_values = values.loc[
                (values.index.get_level_values(batch_name_index_name) == batch_name)
                & (~values.index.duplicated(keep=on_duplicates_keep))
            ]

            if batch_values.shape[0] == 0:
                batch_command["values"] = []
            else:

                def build_single_value_payload(value):
                    return {
                        "dataId": value.name,
                        "value": float(value.iloc[0]),
                        "unitId": values_unit_ids.get(value.name),
                    }

                batch_command["values"] = (
                    batch_values.dropna().apply(build_single_value_payload).to_list()
                )

        # Build features command
        batch_command["tagValuesById"] = []  # Not used

        if features is None:
            batch_command["tagValuesByValue"] = []
        else:
            batch_features = features.loc[
                features.index.get_level_values(batch_name_index_name) == batch_name
            ].drop_duplicates(keep=on_duplicates_keep)

            if batch_features.shape[0] == 0:
                batch_command["tagValuesByValue"] = []
            else:

                def build_single_feature_payload(feature):
                    return {
                        "batchTagKeyId": feature.name,
                        "batchTagValueValue": feature.iloc[0],
                    }

                batch_command["tagValuesByValue"] = (
                    batch_features.dropna()
                    .apply(build_single_feature_payload)
                    .to_list()
                )

        # Append batch command
        batches.append(batch_command)

    # Query endpoint
    response = endpoints.batches.create_or_update_batches(
        batch_type_id=batch_type_id, batches=batches, api_credentials=api_credentials
    )

    # Update vector data values
    if vector_data_values is not None:
        batch_ids_renaming_dict = {b["name"]: b["id"] for b in response}

        # Rename batches to IDs
        vector_data_values_by_batch_id = []

        for vector_data_df in vector_data_values:
            vector_data_df_index = vector_data_df.index.to_frame()
            vector_data_df_index[batch_name_index_name] = vector_data_df_index[
                batch_name_index_name
            ].map(batch_ids_renaming_dict)
            vector_data_df_by_batch_id = vector_data_df.copy()
            vector_data_df_by_batch_id.index = pd.MultiIndex.from_frame(
                vector_data_df_index
            )
            vector_data_values_by_batch_id.append(
                vector_data_df_by_batch_id.loc[
                    ~vector_data_df_by_batch_id.index.duplicated(
                        keep=on_duplicates_keep
                    )
                ]
            )

        # Actually send vector data values
        update_vector_batch_values(
            data=vector_data_values_by_batch_id,
            data_reference=vector_data_references,
            index_units=vector_data_index_units,
            values_units=vector_data_values_units,
            batch_id_index_name=batch_name_index_name,
        )

    # Output
    return response
