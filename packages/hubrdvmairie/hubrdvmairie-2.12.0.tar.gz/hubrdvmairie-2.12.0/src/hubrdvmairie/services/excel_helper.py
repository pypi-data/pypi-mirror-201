import io
import os
from pathlib import Path

import msoffcrypto
from dotenv import load_dotenv
from openpyxl import Workbook, load_workbook

load_dotenv()


def read_password_protected_excel(file_rel_path: Path) -> Workbook:
    decrypted_workbook = io.BytesIO()

    with open(file_rel_path, "rb") as file:
        office_file = msoffcrypto.OfficeFile(file)
        office_file.load_key(password=os.environ.get("EXCEL_PASSWORD"))
        office_file.decrypt(decrypted_workbook)

    # `filename` can also be a file-like object.
    workbook = load_workbook(filename=decrypted_workbook)

    return workbook
