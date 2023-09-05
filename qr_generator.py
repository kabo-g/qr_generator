import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QPushButton, QFileDialog
from PyQt6 import uic
import qrcode
import os
import json
import time
import re
import ast
import shutil
from pathlib import Path
import ctypes


if os.name == "nt":

	appid = 'qrgenerator.qrcodes.kaboom.2.0.0.1.5' # arbitrary string
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi("qr_code_generator.ui", self)
        self.label_4.clear()
        self._translate = QtCore.QCoreApplication.translate
        self.pushButton_6.clicked.connect(self.submit_button_clicked)
        self.open_dialog.clicked.connect(self.open_file_dialog)
        self.open_file = QFileDialog()
        self.pushButton_4.clicked.connect(self.generate_bulk_codes)
        self.pushButton_3.clicked.connect(self.clear_selected_file)
        self.pushButton_5.clicked.connect(self.clear_after_submit)
        self.regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
        self.vcard = ""
        self.prefix = "+267"

    def validate_form_fields(self):
        self.fields = [
            self.fullNamesLineEdit,
            self.positionLineEdit,
            self.telephone1LineEdit,
            self.telephone2LineEdit,
            self.cellNumber1LineEdit,
            self.cellNumber2LineEdit,
            self.emailLineEdit,
            self.organizationLineEdit,
        ]

        for i in self.fields:
            if i == "":
                print("Empty Value Not Allowed")
                i.setFocus()
                self.label_4.setText(self._translate("MainWindow", "There is an empty field. Please check. {}".format(i)))

    def is_valid_email(self, email):
        if not re.fullmatch(self.regex, email):
            self.label_4.setText(self._translate("MainWindow", "Invalid email address."))

            return False



    # custom slot
    def submit_button_clicked(self):

        fullname = self.fullNamesLineEdit.text()
        position = self.positionLineEdit.text()
        telephone1 = self.prefix + self.telephone1LineEdit.text()
        telephone2 = self.prefix + self.telephone2LineEdit.text()
        cell = self.prefix + self.cellNumber1LineEdit.text()
        cell2 = self.prefix + self.cellNumber2LineEdit.text()
        email = self.emailLineEdit.text()
        organization = self.organizationLineEdit.text()

        if fullname == "" or position == "" or telephone1 == "" or cell == "" or email == "" or organization == "":
            self.label_4.setText(self._translate("MainWindow", "There is an empty field. Please check."))


        else:
            check_email = self.is_valid_email(
                email = email
            )
            if check_email != False:
                self.label_4.setText(self._translate("MainWindow", "QR Code for {} has been successfully generated".format(fullname)))

                self.vcard = "BEGIN:VCARD \nVERSION:3.0 \nN:{0} \nFN:{0} \nORG:{5} \nTITLE:{1} \nEMAIL;TYPE=work;TYPE=INTERNET:{4} \nTEL;TYPE=work:{2} \nTEL;TYPE=work:{6} \nTEL;TYPE=mobile:{3} \nTEL;TYPE=mobile:{7} \nEND:VCARD".format(
                    fullname, position, telephone1, cell, email, organization, telephone2, cell2
                )


                try:
                    self.save_path = os.path.expanduser('~'+"/Pictures/generated_qr_codes/")

                    if not os.path.exists(self.save_path):
                        os.makedirs(self.save_path)

                    else:
                        img = qrcode.make(self.vcard)
                        img.save("{1}{0}.jpg".format(fullname, self.save_path))

                        print(self.save_path)


                except FileExistsError:
                    pass




    def clear_after_submit(self):
        self.fullNamesLineEdit.clear()
        self.positionLineEdit.clear()
        self.telephone1LineEdit.clear()
        self.telephone2LineEdit.clear()
        self.cellNumber1LineEdit.clear()
        self.cellNumber2LineEdit.clear()
        self.emailLineEdit.clear()
        self.organizationLineEdit.clear()

    def clear_selected_file(self):
        self.open_file.destroy()
        self.show_selected_file.clear()
        self.success.clear()


    def open_file_dialog(self):

        self.a = self.open_file.getOpenFileName(self, "Open Json file", "", "All files (*);; TEXT files (*.txt);; JSON files (*.json)",)


        opened_filename = str(self.a).split("/")[-1].split("'")[0]
        self.show_selected_file.setText(self._translate("MainWindow", "Selected file -:  {}".format(opened_filename)))
        if not self.open_file:
            return

    def generate_bulk_codes(self):
        with open(Path(self.a[0]), "r") as f:
            data = f.read()

            if data.empty():
                self.success.setText(self._translate("MainWindow", "No file is selected. Please select a .json file"))
            else:

                data = ast.literal_eval(data)

                for key, value in data.items():
                    inner_dict =  value
                    name = inner_dict.get('name')
                    position = inner_dict.get('position')
                    telephone = inner_dict.get('telephone')
                    cell = inner_dict.get('cell')
                    email = inner_dict.get('email')
                    organization = inner_dict.get('organization')
                    telephone2 = inner_dict.get("telephone2")



                    try:
                        if "telephone2" in inner_dict:
                            telephone2 = inner_dict.get("telephone2")
                    except:
                        if "telephone2" not in inner_dict:
                            " "

                    vcard = "BEGIN:VCARD \nVERSION:3.0 \nN:{0} \nFN:{0} \nORG:{5} \nTITLE:{1} \nEMAIL;TYPE=work;TYPE=INTERNET:{4} \nTEL;TYPE=work:{2} \nTEL;TYPE=work:{6} \nTEL;TYPE=mobile:{3} \nEND:VCARD".format(
                            name, position, telephone, cell, email, organization, telephone2
                        )

                    try:
                        self.save_path = os.path.expanduser('~'+"/Pictures/generated_qr_codes/")

                        if not os.path.exists(self.save_path):
                            os.makedirs(self.save_path)

                        else:

                            img = qrcode.make(vcard)
                            img.save("{1}{0}.jpg".format(name, self.save_path))





                    except FileExistsError:
                        pass
                else:
                    self.success.setText(self._translate("MainWindow", "QR Codes Sucessfully saved at Pictures/generated_qr_codes"))


# agrv for command line arguments

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setWindowFlags(
    QtCore.Qt.WindowType.CustomizeWindowHint |
    QtCore.Qt.WindowType.WindowCloseButtonHint |
    QtCore.Qt.WindowType.WindowMinimizeButtonHint
)
window.setWindowTitle("QR Code Generator")
window.setWindowIcon(QtGui.QIcon("Icon/icon.jpg"))
window.show()

# start the event loop
app.exec()
