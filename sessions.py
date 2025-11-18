from io import StringIO
from typing import Hashable

import pandas as pd

MODALITY_ORDER = {"Virtual": 1, "Semipresencial": 2, "Presencial": 3}
TYPE_ORDER = {"Laboratorio": 1, "Teoria": 2}


def filter_sessions(
    csv_file: StringIO, days_to_exclude: list[str], hours_to_exclude: list[str]
) -> tuple[list[dict[Hashable, str]], bool]:
    original_sessions = pd.read_csv(csv_file)

    # NOTE: check is the subject is 70/30
    is7030 = original_sessions["Tipo"].nunique() == 2

    filtered_sessions = original_sessions[
        ~original_sessions["Días"].isin(days_to_exclude)
    ]

    filtered_sessions = filtered_sessions[
        ~filtered_sessions["Horario"].isin(hours_to_exclude)
    ]

    nrcs_duplicated = original_sessions[
        original_sessions.duplicated(subset=["NRC"], keep=False)
    ]["NRC"].unique()

    # NOTE:
    # set(df["NRC"]) - set(filtered_sessions["NRC"])
    # return the df's NRCs that aren't on filtered_sessions
    nrcs_totally_excluded = set(original_sessions["NRC"]) - set(
        filtered_sessions["NRC"]
    )

    nrcs_duplicated_and_partially_excluded = (
        set(nrcs_duplicated) - nrcs_totally_excluded
    )

    filtered_sessions = filtered_sessions[
        ~filtered_sessions["NRC"].isin(nrcs_duplicated_and_partially_excluded)
    ]

    filtered_sessions = filtered_sessions.sort_values(
        by="Modalidad", key=lambda x: x.map(MODALITY_ORDER)
    )

    filtered_sessions = filtered_sessions.sort_values(
        by="Tipo", key=lambda x: x.map(TYPE_ORDER)
    )

    return (filtered_sessions.to_dict("records"), is7030)


def get_unfiltered_sessions_as_list_of_dicts(
    csv_file: StringIO,
) -> list[dict[Hashable, str]]:
    df = pd.read_csv(csv_file)

    df = df.sort_values(by="Modalidad", key=lambda x: x.map(MODALITY_ORDER))
    df = df.sort_values(by="Tipo", key=lambda x: x.map(TYPE_ORDER))

    return df.to_dict("records")


def get_unique_days_and_hours(
    csv_file: StringIO,
) -> tuple[list[str], list[str]]:
    df = pd.read_csv(csv_file)
    days: list[str] = df["Días"].unique().astype(str).tolist()
    hours: list[str] = df["Horario"].unique().astype(str).tolist()

    return (days, hours)
