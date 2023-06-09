import xlrd
import xlwt
import re


def match(directory_pattern: str,
          directory_main: str,
          sheet_pattern: str,
          sheet_main: str,
          column_pattern: str,
          column_main: str) -> [int]:
    """
    Match data in main column with data in pattern column

    :param directory_pattern: pattern file path
    :param directory_main: main file path
    :param sheet_pattern: pattern sheet index, start by 0
    :param sheet_main: main sheet index, start by 0
    :param column_pattern: pattern column index, start by 0
    :param column_main: main column index, start by 0
    :return: list of the matched index
    """
    # get column data and transferred to list
    column_data_pattern = list(map(str, xlrd.open_workbook(directory_pattern)
                                   .sheet_by_index(int(sheet_pattern))
                                   .col_values(int(column_pattern))))
    column_data_main = list(map(str, xlrd.open_workbook(directory_main)
                                .sheet_by_index(int(sheet_main))
                                .col_values(int(column_main))))
    dictionary_main = {}
    match_result = []

    # create dictionary
    for string in column_data_main:
        dictionary_main[string] = 1

    for index in range(len(column_data_pattern)):
        for main in dictionary_main.keys():
            # flag=re.S means every character will be matched
            if re.search(re.escape(column_data_pattern[index]), main, re.S):
                match_result.append(index)
                break

    return match_result


def export(directory_pattern: str,
           directory_main: str,
           sheet_pattern: str,
           sheet_main: str,
           column_pattern: str,
           column_main: str,
           match_result) -> None:
    """
    Export matched data

    :param directory_pattern: pattern file path
    :param directory_main: main file path
    :param sheet_pattern: pattern sheet index, start by 0
    :param sheet_main: main sheet index, start by 0
    :param column_pattern: pattern column index, start by 0
    :param column_main: main column index, start by 0
    :param match_result:
    :return: None
    """
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = workbook.add_sheet('result', cell_overwrite_ok=False)
    column_data_pattern = list(map(str, xlrd.open_workbook(directory_pattern)
                                   .sheet_by_index(int(sheet_pattern))
                                   .col_values(int(column_pattern))))
    column_data_main = list(map(str, xlrd.open_workbook(directory_main)
                                .sheet_by_index(int(sheet_main))
                                .col_values(int(column_main))))
    style = xlwt.XFStyle()
    cell_pattern = xlwt.Pattern()
    cell_pattern.pattern = 1
    cell_pattern.pattern_fore_colour = 0x0D
    style.pattern = cell_pattern

    sheet.write(0, 0, 'Main')
    for index in range(len(column_data_main)):
        sheet.write(index + 1, 0, column_data_main[index])

    sheet.write(0, 1, 'Pattern')
    for index in range(len(column_data_pattern)):
        if index in match_result:
            sheet.write(index + 1, 1, column_data_pattern[index], style)
        else:
            sheet.write(index + 1, 1, column_data_pattern[index])

    try:
        workbook.save('./result.xls')
        print('Export Successfully')
    except BaseException as exception:
        print(exception)


if __name__ == '__main__':
    dp = input('Please input the pattern excel file path.\n')
    dm = input('Please input the main excel file path.\n')
    sp = input('Please input the sheet number of the pattern excel, start by 0.\n')
    cp = input('Please input the column index of the pattern excel, start by 0.\n')
    sm = input('Please input the sheet number of the main excel, start by 0.\n')
    cm = input('Please input the column index of the main excel, start by 0.\n')

    export(dp, dm, sp, sm, cp, cm, match(dp, dm, sp, sm, cp, cm))
