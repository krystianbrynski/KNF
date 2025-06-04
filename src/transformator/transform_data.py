from typing import Dict

from src.config.data_classes import FinalDataItem, FinalData
from src.config.constants import EMPTY


def transform_data(data_with_types, column_flag: bool, sheet_name: str, form_name: str) -> FinalData:
    """Funkcja przygotowuje finalną strukturę danych, która może zostać zapisana do pliku JSON."""

    transformed_data: Dict[str, FinalDataItem] = {}

    for key, values in data_with_types.items():
        if column_flag:  # Obsługa jeśli arkusz jest dwuwymiarowy
            label_row = values.row_text
            data_point = values.data_points
            label_col = values.column_texts
            datatype = values.data_typ
            qname = values.qname

        else:  # Obsługa jeśli arkusz jest jednowymiarowy
            if values.axis == 'y':
                label_row = values.text
                label_col = [EMPTY]
            else:
                label_col = [values.text]
                label_row = EMPTY

            data_point = values.data_points
            datatype = values.data_typ
            qname = values.qname

        transformed_data[key] = FinalDataItem(
            value_row=label_row,
            data_points=data_point,
            value_columns=label_col,
            datatype=datatype,
            qname=qname,
            sheet_name=sheet_name
        )

    return FinalData(form_name=form_name, data=transformed_data)
