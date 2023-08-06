from configparser import ConfigParser

import xlrd
from encoo.logger import Logger


class Config(object):

    __cfg_parser = None

    def __init__(self, cfg_path) -> None:
        if cfg_path is not None:
            try:
                cfg_parser = ConfigParser()
                cfg_parser.read(cfg_path, encoding='utf-8')
                self.__cfg_parser = cfg_parser
            except Exception as e:
                Logger("encoo\config.py").error(f"Config __init__ {e}")

    def get_config(self, section, key=None):

        if key != None:
            return self.__cfg_parser.get(section, key)
        else:
            return self.__cfg_parser.items(section)

    @staticmethod
    def get_excel_cfg(cfg_path, sheet_name=None, inc_header=True):
        data_list = []
        try:
            xls = xlrd.open_workbook(cfg_path, formatting_info=True)

            if sheet_name:
                sheet = xls.sheet_by_name(sheet_name)
            else:
                sheet = xls.sheet_by_index(0)
            row_start_idx = 0
            if inc_header:
                row_start_idx = 1

            for row in range(row_start_idx, sheet.nrows):
                data_list.append(sheet.row_values(row))
        except Exception as e:
            Logger("encoo\config.py").error(f"get_excel_cfg {e}")

        return data_list


if __name__ == "__main__":
    cfg = Config.get_excel_cfg(
        r"C:\Users\renjunfeng\Desktop\流水汇总文件2023-03-28.xls", inc_header=True)
    print(len(cfg))
    
    cfg= Config(r"D:\Repos\pbc_gov\cfg\config.cfg").get_config("file","zh_file_dir")
    print(cfg)
