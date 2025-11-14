from io import StringIO
from typing import Any, Hashable

import pandas as pd

MODALITY_ORDER = {"Virtual": 1, "Semipresencial": 2, "Presencial": 3}
TYPE_ORDER = {"Laboratorio": 1, "Teoria": 2}


def filter_sessions(csv_file: StringIO) -> tuple[list[dict[Hashable, str]], bool]:
    df = pd.read_csv(csv_file)

    # NOTE: check is the subject is 70/30
    is7030 = df["Tipo"].nunique() == 2

    filtered_sessions = df[
        ~df["Horario"].str.contains("^(0[0-9]|1[0-2])", regex=True, na=False)
        & ~df["Días"].str.contains("SA", na=False)
        & ~df["Horario"].str.contains("2[1-4]$", regex=True, na=False)
    ]

    nrcs_duplicated = df[df.duplicated(subset=["NRC"], keep=False)]["NRC"].unique()

    # NOTE:
    # set(df["NRC"]) - set(filtered_sessions["NRC"])
    # return the df's NRCs that aren't on filtered_sessions
    nrcs_totally_exclured = set(df["NRC"]) - set(filtered_sessions["NRC"])

    nrcs_partially_exclured = set(nrcs_duplicated) - nrcs_totally_exclured

    filtered_sessions = filtered_sessions[
        ~filtered_sessions["NRC"].isin(nrcs_partially_exclured)
    ]

    filtered_sessions = filtered_sessions.sort_values(
        by="Modalidad", key=lambda x: x.map(MODALITY_ORDER)
    )

    filtered_sessions = filtered_sessions.sort_values(
        by="Tipo", key=lambda x: x.map(TYPE_ORDER)
    )

    return (filtered_sessions.to_dict("records"), is7030)


def get_sessions_as_list_of_dicts(csv_file: StringIO) -> list[dict[Hashable, str]]:
    return pd.read_csv(csv_file).to_dict("records")
