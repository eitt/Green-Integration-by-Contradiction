from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"


FILES = {
    "full_database": "ejatlas_lng_database.csv",
    "empirical_table": "ejatlas_lng_empirical_table.csv",
    "core_26": "ejatlas_lng_core_26.csv",
    "map_verification": "ejatlas_lng_map_verification.csv",
}


def autofit_worksheet(worksheet, dataframe):
    for idx, column in enumerate(dataframe.columns, start=1):
        values = [str(column)] + [str(v) if v is not None else "" for v in dataframe[column].head(200)]
        width = min(max(len(v) for v in values) + 2, 60)
        worksheet.column_dimensions[chr(64 + idx) if idx <= 26 else worksheet.cell(row=1, column=idx).column_letter].width = width


def main():
    dataframes = {}
    for sheet_name, filename in FILES.items():
        dataframes[sheet_name] = pd.read_csv(PROCESSED / filename)

    for sheet_name, dataframe in dataframes.items():
        dataframe.to_excel(PROCESSED / f"{sheet_name}.xlsx", index=False)

    workbook_path = PROCESSED / "ejatlas_lng_workbook.xlsx"
    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        for sheet_name, dataframe in dataframes.items():
            dataframe.to_excel(writer, sheet_name=sheet_name[:31], index=False)
            worksheet = writer.sheets[sheet_name[:31]]
            worksheet.freeze_panes = "A2"
            autofit_worksheet(worksheet, dataframe)


if __name__ == "__main__":
    main()
