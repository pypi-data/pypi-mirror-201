from email.message import Message
import os

import extract_msg
import mailparser
from encoo.logger import Logger


class EmlMessage(object):

    __logger = Logger("emlmessage")

    eml = None
    msg = None

    def __init__(self, fp) -> None:

        try:
            with open(fp) as f:
                eml_str = f.read()
            self.eml = mailparser.parse_from_string(eml_str)
        except UnicodeDecodeError as e:
            self.msg = extract_msg.Message(fp)
        except Exception as e:
            self.__logger.error(f"__init__ {e}")

    def __get_eml(self):
        return {
            "subject": self.eml.headers.get("Subject", ""),
            "from": self.eml.headers.get("From", ""),
            "to": self.eml.headers.get("To", ""),
            "date": self.eml.headers.get("Date", ""),
            "body": self.eml.text_plain}

    def __get_msg(self):
        return {
            "subject": self.msg.subject,
            "from": self.msg.sender,
            "to": self.msg.to,
            "date": self.msg.date,
            "body": self.msg.body
        }

    def extract(self):
        if self.msg is not None:
            return self.__get_msg()
        elif self.eml is not None:
            return self.__get_eml()


if __name__ == "__main__":

    root_dir = r"D:\Repos\encoo_ecs\emls"
    for f in os.listdir(root_dir):
        eml = EmlMessage(os.path.join(root_dir, f)).extract()
        '''print("subject", eml.get("subject"))
        print("from", eml.get("from"))
        print("date", eml.get("date"))'''
        print("body\n", eml.get("body"))
        