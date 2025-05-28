from dataclasses import dataclass
from typing import List
from src.config.constants import DATA_TYPE, QNAME

@dataclass
class TwoDimensionalAxis:
    row_text: str
    data_points: List[str]
    column_texts: List[str]
    data_typ: str = DATA_TYPE
    qname: str = QNAME

@dataclass
class OneDimensionalAxis:
    text: str
    data_points: List[str]
    data_typ: str = DATA_TYPE
    qname: str = QNAME
    axis: str = ""  # miejsce na okreslenie osi arkusza


@dataclass
class FinalDataItem:
    value_row: str
    data_points: List[str]
    value_columns: str
    datatype: str
    qname: str
    sheet_name: str

@dataclass
class FinalData:
    form_name: str
    data: dict[str, FinalDataItem]