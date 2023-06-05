from openpyxl import load_workbook, Workbook


def read_excel(path: str) -> {'': []}:
    data = {}
    wb = load_workbook(filename=path)
    for sheet in wb.worksheets:
        for col in sheet.iter_cols():
            li = []
            for cell in col:
                li.append(cell.value)
            data[li[0]] = li[1:]
    return data


def export_excel(title='sheet 0'):
    wb = Workbook()
    ws = wb.active
    ws.title = title


if __name__ == '__main__':
    print(read_excel('./tests/test_import.xlsx'))
