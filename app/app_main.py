import sys

import rectangle_packing_solver as rps
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
    error_message.setWindowTitle("empty cell error".title())
    error_message.exec_()


def invalid_data():
    """ Called if invalid input """
    error_message = QtWidgets.QMessageBox()
    error_message.setIcon(QtWidgets.QMessageBox.Critical)
    error_message.setText(
        "Error Message:\n\nPlease enter a valid number.")
    error_message.setWindowTitle("invalid data error".title())
    error_message.exec_()


def panel_size_error():
    """ Called if the panel can not hold the rectangles """
    error_message = QtWidgets.QMessageBox()
    error_message.setIcon(QtWidgets.QMessageBox.Critical)
    error_message.setText(
        "Error Message:\n\nOne or more input(s) exceed(s) the given panel size. \nPlease check again")
    error_message.setWindowTitle("out of size error".title())
    error_message.exec_()


def entities_error():
    """ Called if there are 2 or more valid rows in the table """
    error_message = QtWidgets.QMessageBox()
    error_message.setIcon(QtWidgets.QMessageBox.Critical)
    error_message.setText(
        "Error Message:\n\nPlease enter at least 02 entities in the table.")
    error_message.setWindowTitle("entities error".title())
    error_message.exec_()


# Events handling
def add_row():
    """ Inserts a new row when a user clicks on the Add btn"""
    row_count = ui.cuttingList.rowCount()  # getting the current number of rows
    ui.cuttingList.insertRow(row_count)


def delete_row():
    """ Deletes the latest row in the loop """
    row = ui.cuttingList.indexAt(ui.deleteBtn.pos()).row()
    if row:
        ui.cuttingList.removeRow(row)


def get_cutting_list_data():
    """ Get the data from the Cutting List Table """
    global cell_dict

    cell_dict = {}
    col_count = ui.cuttingList.columnCount()  # getting the number of columns
    row_count = ui.cuttingList.rowCount()  # getting the number of rows

    for row in range(row_count):
        for col in range(col_count):
            item = ui.cuttingList.item(row, col)  # getting the content of each cell

            """ Checks if the item is only integers """
            if item and item.text() != "":
                try:
                    content = int(item.text())
                    if not content:
                        empty_cell()
                    else:
                        pos = (row + 1, col + 1)  # getting the position of each cell
                        for i in range(row_count + 1):
                            cell_dict[pos] = content
                except ValueError:
                    invalid_data()
            else:
                empty_cell()

    return cell_dict


def check_cutting_list_data():
    """ Checks if the data gathered from the Cutting List Table is valid """
    global entity, height, width, height_list, width_list, quantity, max_height, max_width, rectangles

    height_list = []
    width_list = []
    rectangles = []

    number_of_items = len(cell_dict.keys())
    values = list(cell_dict.values())
    # entity represents all rectangles with a tuple of (height, width, qty) for each
    entity = [values[i: i + 3] for i in
              range(0, number_of_items, 3)]

    if not number_of_items or number_of_items % 3 != 0:  # we have 3 columns
        return False

    else:
        for size in enumerate(entity, 1):
            height = size[1][0]  # height of each rectangle
            width = size[1][1]  # width of each rectangle
            quantity = size[1][2]  # quantity of each rectangle

            height_list.append(height)
            width_list.append(width)
            max_height = max(height_list)
            max_width = max(width_list)

            rectangle = (width, height)

            for _ in range(quantity):
                rectangles.append(rectangle)

    return height_list, width_list, quantity, max_height, max_width, rectangles


def check_panel_size():
    """ Checks if the panel can hold all the given rectangles """
    global panel_height, panel_width, panel_quantity

    # For the moment, we proceed with only one panel, this could change in the future
    panel = {}  # size of the panel
    row_stock_panel = ui.stockPanel.rowCount()
    col_stock_panel = ui.stockPanel.columnCount()

    # We check if the data is valid as well
    for row in range(row_stock_panel):
        for col in range(col_stock_panel):
            panel_size = ui.stockPanel.item(row, col)
            if panel_size and panel_size.text() != "":
                try:
                    content = int(panel_size.text())
                    if not content:
                        empty_cell()
                    else:
                        for i in range(row_stock_panel + 1):
                            panel[(row, col)] = content
                except ValueError:
                    invalid_data()

            else:
                empty_cell()
    if panel and len(panel.values()) % 3 == 0:
        panel_values = list(panel.values())
        panel_height = panel_values[0]
        panel_width = panel_values[1]
        panel_quantity = panel_values[2]

        if panel_height and panel_width:
            process_data()  # we call that function immediately if valid data from the panel

        return panel_height, panel_width, panel_quantity


def process_data():
    """ Processes with the gathered data from both tables """

    # Called only if panel_height, panel_width, max_height and max_width exist
    if panel_height < max_height or panel_width < max_width:
        panel_size_error()

    elif len(cell_dict.values()) >= 6 and len(cell_dict.values()) % 3 == 0:
        # we need at least 2 entities (rows) before proceeding, otherwise rps throws an error
        # we define the problem
        problem = rps.Problem(rectangles=rectangles)
        print("problem:", problem)

        # we define the solution
        solution = rps.Solver().solve(problem=problem, height_limit=panel_height, show_progress=True, seed=1111)
        print("solution:", solution)

        # visualization (to cutelist.png)
        rps.Visualizer().visualize(solution=solution, path="./cutelist.png")

    else:
        entities_error()


def generate_map():
    """ Generate the cutting map """
    get_cutting_list_data()
    check_cutting_list_data()
    check_panel_size()


def start_app():
    """ Holds the logic of the app execution """
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui.setupUi(window)

    # Listening to events
    ui.addBtn.clicked.connect(add_row)
    ui.generateBtn.clicked.connect(generate_map)
    ui.deleteBtn.clicked.connect(delete_row)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_app()
