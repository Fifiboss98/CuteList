import sys

from PyQt5 import QtWidgets

from cutelist import Ui_CuteList

ui = Ui_CuteList()


# Errors handling
def empty_cell():
    """ Called if empty cell """
    error_message = QtWidgets.QMessageBox()
    error_message.setIcon(QtWidgets.QMessageBox.Critical)
    error_message.setText(
        "Error Message:\n\nEvery cell should be filled with numbers (starting from 1).")
    error_message.setWindowTitle("Empty Cell Error")
    error_message.exec_()


def invalid_data():
    """ Called if invalid input """
    error_message = QtWidgets.QMessageBox()
    error_message.setIcon(QtWidgets.QMessageBox.Critical)
    error_message.setText(
        "Error Message:\n\nPlease enter a valid number.")
    error_message.setWindowTitle("Invalid Data Error")
    error_message.exec_()


# Events handling
def add_row():
    """ Inserts a new row when a user clicks on the Add btn"""
    row_count = ui.cuttingList.rowCount()  # getting the current number of rows
    ui.cuttingList.insertRow(row_count)


def delete_row():
    """ Deletes the latest row in the loop """
    row = ui.cuttingList.indexAt(ui.deleteBtn.pos()).row()
    if row >= 1:
        ui.cuttingList.removeRow(row)


def get_data():
    """ Retrieves data from the table and checks if valid """
    global cell_dict

    cell_dict = {}
    col_count = ui.cuttingList.columnCount()  # getting the number of columns
    row_count = ui.cuttingList.rowCount()  # getting the number of rows

    for row in range(row_count):
        for col in range(col_count):
            item = ui.cuttingList.item(row, col)  # getting the content of each cell

            """ Checks if the item is only integers """
            if item is not None and item.text() != "":
                try:
                    content = int(item.text())
                    if content == 0:
                        empty_cell()
                    else:
                        pos = (row + 1, col + 1)  # getting the position of each cell
                        for i in range(row_count + 1):
                            cell_dict[pos] = content
                except ValueError:
                    invalid_data()
            else:
                empty_cell()
            print(cell_dict)

    return cell_dict


def process_data():
    """ Processes with the valid data as arguments to rectangle-packing-solver """
    number_of_items = len(cell_dict.keys())
    print(number_of_items)

    # guard clause
    if number_of_items >= 0 or number_of_items % 3 != 0:  # we have 3 columns
        print("nooo")

    else:  # we define the problem
        print("We can proceed with the map generating!")


def start_app():
    """ Holds the logic of the app execution """
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui.setupUi(window)

    # Listening to events
    ui.addBtn.clicked.connect(add_row)
    ui.generateBtn.clicked.connect(get_data)
    ui.generateBtn.clicked.connect(process_data)
    ui.deleteBtn.clicked.connect(delete_row)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_app()
