import xlwt
import xlrd


def read_xl(xl_path, sheet_name):
    xls = xlrd.open_workbook(xl_path, formatting_info=True)
    sheet = xls.sheet_by_name(sheet_name)
    for row_idx in range(1, sheet.nrows):
        for col_idx in range(sheet.ncols):
            print(sheet.cell(row_idx, col_idx).value)


def write_xl(xl_path, dict_list):
    xl = xlwt.Workbook(encoding="uft-8")
    sheet = xl.add_sheet("sheet1", cell_overwrite_ok=False)
    for row_idx in range(0, len(dict_list)):
        col_idx = 0
        for k, v in dict_list[row_idx].items():
            sheet.write(row_idx, col_idx, v)
            col_idx = col_idx+1
    xl.save(xl_path)


def write_txt(txt_path, dict_list):
    with open(txt_path, "w") as txt_file:
        for row_idx in range(0, len(dict_list)):
            col_idx = 0
            for k, v in dict_list[row_idx].items():
                txt_file.writelines(str(v)+"\n")
                col_idx = col_idx+1
