# -*- coding: utf-8 -*-
#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL license version 2 under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the
# terms of the CeCILL license version 2 as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.
from brainvisa.processes import *
from brainvisa.processing.qt4gui.neuroProcessesGUI import mainThreadActions
from soma.spm import csv_converter

userLevel = 0
name = 'Covariate manager'
roles = ('viewer',)
# ------------------------------------------------------------------------------

signature = Signature(
    'input_table', ReadDiskItem('Covariate table for SPM', 'CSV file'),
    'output_table', WriteDiskItem('Covariate table for SPM', 'CSV file'),
)


# ------------------------------------------------------------------------------

def initialization(self):
    self.linkParameters("output_table", "input_table")


def execution(self, context):
    mainThreadActions().call(self.showInterface, context)


def showInterface(self, context):
    csv_dict, csv_row_header = csv_converter.reverse(self.input_table.fullPath())
    csv_editor = CSVEditor(csv_dict, csv_row_header)
    csv_editor.show()
    r = csv_editor.exec_()

    if csv_editor.save_new_csv:
        csv_dict = csv_editor.csv_dict
        csv_converter.convert(csv_dict, self.output_table.fullPath(), csv_row_header)
    else:
        pass  # modification is not saved
    return r


# ==============================================================================
# ==============================================================================
# # Interface PyQt
# ==============================================================================
# ==============================================================================

from soma.qt_gui.qt_backend.QtGui import QDialog
from soma.qt_gui.qt_backend.QtGui import QVBoxLayout, QHBoxLayout
from soma.qt_gui.qt_backend.QtGui import QTableWidget, QHeaderView, QTableWidgetItem
from soma.qt_gui.qt_backend.QtGui import QListWidget, QPushButton, QDialogButtonBox, QGroupBox, QWidget
from soma.qt_gui.qt_backend.QtGui import QApplication, QDesktopWidget, QAbstractItemView, QMessageBox
from soma.qt_gui.qt_backend.QtGui import QLabel, QLineEdit
from soma.qt_gui.qt_backend.QtGui import QFileDialog
from soma.qt_gui.qt_backend.QtCore import Qt

import copy


class CSVEditor(QDialog):
    def __init__(self, csv_dict, csv_row_header):
        QDialog.__init__(self)
        self.setWindowTitle('Covariate Manager')
        # ==============================================================================
        # Variables member
        # ==============================================================================
        self.factor = 0.5
        self.csv_dict = csv_dict
        self.csv_row_header = csv_row_header
        self.csv_column_header = self._getAllColumnHeader()
        self.native_csv_dict = copy.deepcopy(csv_dict)
        self.native_csv_row_header = copy.deepcopy(csv_row_header)
        self.native_csv_column_header = copy.deepcopy(self.csv_column_header)
        self.save_new_csv = False
        self.displaying_configuration_dict = None
        # ==============================================================================
        # Qt Objects
        # ==============================================================================
        self.results_filter_button = QPushButton('Results filter')
        self.extract_csv_button = QPushButton('Extract current table')
        self.add_covariate_button = QPushButton('Add new covariate')
        self.remove_covariate_button = QPushButton('Remove covariate')
        self.table = TableWidgetCustom()
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)

        self.button_box = QDialogButtonBox()
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Reset | QDialogButtonBox.Discard | QDialogButtonBox.Save)
        # ==============================================================================
        # Layout Design
        # ==============================================================================
        main_layout = QVBoxLayout(self)

        parameters_layout = QHBoxLayout()
        parameters_layout.addStretch(1)
        parameters_layout.addWidget(self.results_filter_button)
        parameters_layout.addStretch(1)
        parameters_layout.addWidget(self.extract_csv_button)
        parameters_layout.addStretch(1)
        parameters_layout.addWidget(self.add_covariate_button)
        parameters_layout.addWidget(self.remove_covariate_button)
        parameters_layout.addStretch(1)
        main_layout.addLayout(parameters_layout)
        main_layout.addWidget(self.table, 1)
        main_layout.addWidget(self.button_box)
        # ==============================================================================
        # signal connection
        # ==============================================================================
        self.results_filter_button.clicked.connect(self._showViewerParams)
        self.extract_csv_button.clicked.connect(self._extractCurrentTable)
        self.add_covariate_button.clicked.connect(self._addCovariate)
        self.remove_covariate_button.clicked.connect(self._removeCovariate)
        self.button_box.button(QDialogButtonBox.Reset).clicked.connect(self._resetTable)
        self.button_box.button(QDialogButtonBox.Discard).clicked.connect(self._closeWithoutSaving)
        self.button_box.button(QDialogButtonBox.Save).clicked.connect(self._closeAndSaving)
        # ==============================================================================
        # Initialisation
        # ==============================================================================
        self._setQDialogSize()
        self._centerOnScreen()

        self._fillHeaderTable()
        self._fillValueTable()

    def _setQDialogSize(self):
        resolution = QDesktopWidget().screenGeometry()
        width = int(float(resolution.width()) * self.factor)
        height = int(float(resolution.height()) * self.factor)
        self.setGeometry(0, 0, width, height)

    def _centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        width = int(float(resolution.width()) * (1 - self.factor) / 2)
        height = int(float(resolution.height()) * (1 - self.factor) / 2)
        self.move(width, height)

    def _fillHeaderTable(self):
        self.csv_column_header = sorted(self.csv_column_header)
        row_count = len(self.csv_dict.keys())
        self.table.setRowCount(row_count)
        self.table.setColumnCount(len(self.csv_row_header + self.csv_column_header))
        self.table.setHorizontalHeaderLabels(self.csv_row_header + self.csv_column_header)
        for row_id_header_index in range(len(self.csv_row_header)):
            self.table.horizontalHeader().setResizeMode(row_id_header_index, QHeaderView.ResizeToContents)

        for value_header_index in range(len(self.csv_row_header), len(self.csv_row_header + self.csv_column_header)):
            self.table.horizontalHeader().setResizeMode(value_header_index, QHeaderView.Stretch)

        self._adjustTableSizetoContents()

    def _resetTable(self):
        self.csv_dict = copy.deepcopy(self.native_csv_dict)
        self.csv_row_header = copy.deepcopy(self.native_csv_row_header)
        self.csv_column_header = copy.deepcopy(self.native_csv_column_header)
        self.displaying_configuration_dict = None
        self._refreshTable()

    def _refreshTable(self):
        self.table.clear()
        self.table.setSortingEnabled(False)
        self._fillHeaderTable()
        self._fillValueTable()
        self._setCurrentDisplayingConfiguration(self.displaying_configuration_dict)
        self.table.setSortingEnabled(True)

    def _fillValueTable(self):
        table_row_index = 0
        for row_id in sorted(self.csv_dict.keys()):
            column_index = 0
            row_id_splitted = row_id.split(';')
            for row_id_item in row_id_splitted:
                cell = QTableWidgetItem(row_id_item)
                cell.setTextAlignment(Qt.AlignCenter)
                cell.setFlags(~(Qt.ItemIsSelectable | Qt.ItemIsEditable))  # tilde to invert comportment
                cell.setBackground(Qt.lightGray)
                self.table.setItem(table_row_index, column_index, cell)
                column_index += 1

            tmp_value_dict = self.csv_dict[row_id]
            while column_index < self.table.columnCount():
                column_header = str(self.table.horizontalHeaderItem(column_index).text())
                if column_header in tmp_value_dict.keys():
                    cell = QTableWidgetItem(tmp_value_dict[column_header])
                else:
                    cell = QTableWidgetItem('')
                cell.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(table_row_index, column_index, cell)
                column_index += 1
            table_row_index += 1

    def _getAllColumnHeader(self):
        column_header_list = []
        for row_id in self.csv_dict.keys():
            column_header_list = list(set(column_header_list + self.csv_dict[row_id].keys()))
        return sorted(column_header_list)

    def _adjustTableSizetoContents(self):
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def _showViewerParams(self):
        subject_id_dict = {}
        for column_index, column_header in enumerate(self.csv_row_header):
            subject_id_dict[column_header] = self._getColumnItemList(column_index)
        subject_id_dict["covariate"] = self.csv_column_header
        params_viewer = ListWidgetCheckBoxDialog(subject_id_dict)
        params_viewer.show()
        r = params_viewer.exec_()

        self._setCurrentDisplayingConfiguration(params_viewer.item_selected_dict)

        self._askAgainIfEmpty()

    def _setCurrentDisplayingConfiguration(self, displaying_configuration_dict=None):
        if displaying_configuration_dict is not None:
            self.displaying_configuration_dict = displaying_configuration_dict
        else:
            self.displaying_configuration_dict = {}
            for column_index, column_header in enumerate(self.csv_row_header):
                self.displaying_configuration_dict[column_header] = self._getColumnItemList(column_index)
            self.displaying_configuration_dict["covariate"] = copy.deepcopy(self.csv_column_header)
        self._updateTable(self.displaying_configuration_dict)

    def _askAgainIfEmpty(self):
        visible_row = 0
        for row_index in range(self.table.rowCount()):
            if not self.table.isRowHidden(row_index):
                visible_row += 1
        if visible_row == 0:
            QMessageBox.warning(self,
                                'No results',
                                'No results matching with these choices, please try again',
                                QMessageBox.Ok)
            self._showViewerParams()
        else:
            pass

    def _extractCurrentTable(self):
        current_table_dict = {}
        for row_index in range(self.table.rowCount()):
            if not self.table.isRowHidden(row_index):
                row_id_list = []
                for column_index, column_header in enumerate(self.csv_row_header):
                    row_id_list.append(str(self.table.item(row_index, column_index).text()))
                row_id = ';'.join(row_id_list)

                current_table_dict[row_id] = {}
                for column_index in range(len(self.csv_row_header), self.table.columnCount()):
                    if not self.table.isColumnHidden(column_index):
                        column_header = str(self.table.horizontalHeaderItem(column_index).text())
                        value = str(self.table.item(row_index, column_index).text())
                        current_table_dict[row_id][column_header] = value

        fileName = QFileDialog.getSaveFileName(self, "Export CSV",
                                               '', "CSV Files (*.csv);;CSV Files (*.csv)")
        if fileName:
            csv_converter.convert(current_table_dict, fileName, self.csv_row_header)
        else:
            pass

    def _addCovariate(self):
        dialog = UserAskDialog("What is the new covariate name ?",
                               unvalid_field=self.csv_column_header + [''])
        dialog.show()
        r = dialog.exec_()
        if dialog.getChoice() is not None:
            self.addCovariateInTable(dialog.getChoice())
        else:
            pass  # the user cancelled
        dialog.destroy()

    def addCovariateInTable(self, covariate_name):
        for subject_id in self.csv_dict.keys():
            self.csv_dict[subject_id][covariate_name] = ''
        self.csv_column_header.append(covariate_name)
        if self.displaying_configuration_dict is not None:
            self.displaying_configuration_dict['covariate'].append(covariate_name)
        self._refreshTable()

    def _removeCovariate(self):
        dialog = UserAskDialog("Choose the covariate which will be deleted :",
                               valid_field=self.csv_column_header)
        dialog.show()
        r = dialog.exec_()
        if dialog.getChoice() is not None:
            self.removeCovariateInTable(dialog.getChoice())
        else:
            pass  # the user cancelled
        dialog.destroy()

    def removeCovariateInTable(self, covariate_name):
        for subject_id in self.csv_dict.keys():
            del self.csv_dict[subject_id][covariate_name]

        self.csv_column_header.remove(covariate_name)
        if self.displaying_configuration_dict is not None:
            if covariate_name in self.displaying_configuration_dict['covariate']:
                self.displaying_configuration_dict['covariate'].remove(covariate_name)
        self._refreshTable()

    def _getColumnItemList(self, column_index):
        item_list = []
        for row_index in range(self.table.rowCount()):
            item_list.append(str(self.table.item(row_index, column_index).text()))
        return list(set(item_list))

    def _updateTable(self, item_selected_dict):

        covariate_selected_list = item_selected_dict['covariate']
        length_header = len(item_selected_dict.keys()) - 1  # without covariate
        for column_header_index in range(length_header, self.table.columnCount()):
            if str(self.table.horizontalHeaderItem(column_header_index).text()) in covariate_selected_list:
                self.table.setColumnHidden(column_header_index, False)
            else:
                self.table.setColumnHidden(column_header_index, True)

        for row_index in range(self.table.rowCount()):
            hidden = False
            for column_index, column_header in enumerate(self.csv_row_header):
                if not str(self.table.item(row_index, column_index).text()) in item_selected_dict[column_header]:
                    hidden = True
            self.table.setRowHidden(row_index, hidden)

    def _closeWithoutSaving(self):
        self.close()

    def _closeAndSaving(self):
        self.csv_dict = {}
        for row_index in range(self.table.rowCount()):
            row_id_list = []
            for column_index, column_header in enumerate(self.csv_row_header):
                row_id_list.append(str(self.table.item(row_index, column_index).text()))
            row_id = ';'.join(row_id_list)

            self.csv_dict[row_id] = {}
            for column_index in range(len(self.csv_row_header), self.table.columnCount()):
                column_header = str(self.table.horizontalHeaderItem(column_index).text())
                value = str(self.table.item(row_index, column_index).text())
                self.csv_dict[row_id][column_header] = value

        self.save_new_csv = True
        self.close()


class TableWidgetCustom(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self)
        self.clip = QApplication.clipboard()
        self.csv_delimiter = '\t'

    def keyPressEvent(self, e):
        """Allow the copy/past from and to QTable, and it specific works with hidden row/column"""
        if (e.modifiers() & Qt.ControlModifier):
            selected = self.selectedRanges()
            if e.key() == Qt.Key_V:  # past
                first_row = selected[0].topRow()
                first_col = selected[0].leftColumn()
                # copied text is split by '\n' and '\t' to paste to the cells
                row_hidden_increment = 0
                for r, row in enumerate(self.clip.text().split('\n')):
                    column_hidden_increment = 0
                    if self.isRowHidden(first_row + row_hidden_increment + r):
                        while self.isRowHidden(first_row + row_hidden_increment + r) or (
                                first_row + row_hidden_increment + r) > self.rowCount():
                            row_hidden_increment += 1
                    else:
                        pass  # row
                    for c, text in enumerate(row.split(self.csv_delimiter)):
                        if self.isColumnHidden(first_col + column_hidden_increment + c):
                            while self.isColumnHidden(first_col + column_hidden_increment + c) or (
                                    first_col + column_hidden_increment + c) > self.columnCount():
                                column_hidden_increment += 1
                        else:
                            pass  # column is not hidden
                        if text != '':
                            if (first_row + row_hidden_increment + r) < self.rowCount() and (
                                    first_col + column_hidden_increment + c) < self.columnCount():
                                self.item(first_row + row_hidden_increment + r,
                                          first_col + column_hidden_increment + c).setText(text)
                            else:
                                QMessageBox.warning(self,
                                                    'Unvalid copy',
                                                    'The table is too small compared to the cells to be copied',
                                                    QMessageBox.Ok)
                                # raise ValueError('This table is too small compared to the cells to be copied')
            elif e.key() == Qt.Key_C:  # copy
                s = ""
                for r in range(selected[0].topRow(), selected[0].bottomRow() + 1):
                    for c in range(selected[0].leftColumn(), selected[0].rightColumn() + 1):
                        if self.item(r, c) is not None:
                            s += str(self.item(r, c).text()) + self.csv_delimiter
                        else:
                            s += self.csv_delimiter
                    s = s[:-1] + "\n"  # eliminate last '\t'
                    self.clip.setText(s)
            else:
                pass

        elif e.key() == Qt.Key_Delete:
            selected = self.selectedRanges()
            first_selected_row = selected[0].topRow()
            last_selected_row = selected[0].bottomRow()
            first_selected_col = selected[0].leftColumn()
            last_selected_col = selected[0].rightColumn()
            for row_index in range(first_selected_row, last_selected_row + 1):
                if not self.isRowHidden(row_index):
                    for column_index in range(first_selected_col, last_selected_col + 1):
                        if not self.isColumnHidden(column_index):
                            self.item(row_index, column_index).setText('')
                        else:
                            pass  # column is hidden
                else:
                    pass  # row is hidden
        else:
            selected = self.selectedRanges()
            first_selected_row = selected[0].topRow()
            first_selected_col = selected[0].leftColumn()
            self.editItem(self.item(first_selected_row, first_selected_col))
            self.item(first_selected_row, first_selected_col).setText(str(chr(e.key()).lower()))


# ==============================================================================
# ==============================================================================
# ==============================================================================
class UserAskDialog(QDialog):
    def __init__(self, question, unvalid_field=None, valid_field=None):
        QDialog.__init__(self)
        # ==============================================================================
        # Variables member
        # ==============================================================================
        self.unvalid_field = unvalid_field
        self.valid_field = valid_field
        self.user_choice = None
        # ==============================================================================
        # Qt Objects
        # ==============================================================================
        main_layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()
        self.label = QLabel(question)
        self.label.setAlignment(Qt.AlignCenter)
        self.line_edit = QLineEdit()
        self.cancel_button = QPushButton("Cancel")
        self.validate_button = QPushButton("Validate")
        self.validate_button.setDefault(True)
        # ==============================================================================
        # Layout Design
        # ==============================================================================
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.validate_button)
        self.button_layout.addStretch()

        main_layout.addWidget(self.label)
        main_layout.addWidget(self.line_edit)
        main_layout.addLayout(self.button_layout)
        # ==============================================================================
        # signal connection
        # ==============================================================================
        self.line_edit.textChanged.connect(self._checkIfValid)
        self.validate_button.clicked.connect(self._storeCovariateName)
        self.cancel_button.clicked.connect(self.close)
        # ==============================================================================
        # Initialisation
        # ==============================================================================
        self._checkIfValid()

    def _checkIfValid(self):
        valid = True
        current_text = str(self.line_edit.text())
        if self.unvalid_field is not None:
            if current_text in self.unvalid_field:
                valid = False
        if self.valid_field is not None:
            if not current_text in self.valid_field:
                valid = False

        if valid:
            self.validate_button.setEnabled(True)
            self.line_edit.setStyleSheet('background-color: none')
        else:
            self.validate_button.setEnabled(False)
            self.line_edit.setStyleSheet('background-color: rgb(255,255,153);')

    def _storeCovariateName(self):
        self.user_choice = str(self.line_edit.text())
        self.close()

    def getChoice(self):
        return self.user_choice


# ==============================================================================
# ==============================================================================
# ==============================================================================
class ListWidgetCheckBoxDialog(QDialog):
    def __init__(self, subject_id_dict):
        QDialog.__init__(self)
        # ==============================================================================
        # Variables member
        # ==============================================================================
        self.subject_id_dict = subject_id_dict
        self.item_selected_dict = {}

        # ===============================================================================
        #
        # ===============================================================================
        self.widget_dict = {}
        for key in subject_id_dict.keys():
            self.widget_dict[key] = {}
            self.widget_dict[key]["GroupBoxCustom"] = GroupBoxCustom(key, custom_style_sheet=True)
            self.widget_dict[key]["QListWidget"] = QListWidget()
            self.widget_dict[key]["QListWidget"].setSelectionMode(QAbstractItemView.ExtendedSelection)

        for key in self.widget_dict.keys():
            self.widget_dict[key]["GroupBoxCustom"].addWidgetInLayout(self.widget_dict[key]["QListWidget"])


            # ===============================================================================
        #
        # ===============================================================================
        # ==============================================================================
        # Qt Objects
        # ==============================================================================
        self.select_all_button = QPushButton('Select all')
        self.validate_button = QPushButton('Validate')
        # ==============================================================================
        # Layout Design
        # ==============================================================================
        select_all_layout = QHBoxLayout()
        select_all_layout.addStretch(0)
        select_all_layout.addWidget(self.select_all_button)
        select_all_layout.addStretch(0)

        main_layout = QVBoxLayout(self)
        group_box_layout = QHBoxLayout()
        for key in self.widget_dict.keys():
            group_box_layout.addWidget(self.widget_dict[key]["GroupBoxCustom"])

        main_layout.addLayout(select_all_layout)
        main_layout.addLayout(group_box_layout)
        main_layout.addWidget(self.validate_button)
        # ==============================================================================
        # signal connection
        # ==============================================================================
        self.select_all_button.clicked.connect(self.selectAll)
        self.validate_button.clicked.connect(self._saveSelection)
        # ==============================================================================
        # Initialisation
        # ==============================================================================
        for key, values in self.subject_id_dict.items():
            self.widget_dict[key]["QListWidget"].addItems(sorted(values))
            self.widget_dict[key]["QListWidget"].setCurrentRow(0)

    def selectAll(self):
        for key in self.widget_dict.keys():
            for item_index in range(self.widget_dict[key]["QListWidget"].count()):
                item = self.widget_dict[key]["QListWidget"].item(item_index)
                item.setSelected(True)

    def _saveSelection(self):
        for key in self.widget_dict.keys():
            self.item_selected_dict[key] = []
            for item_selected in self.widget_dict[key]["QListWidget"].selectedItems():
                self.item_selected_dict[key].append(str(item_selected.text()))

        self.close()


class GroupBoxCustom(QGroupBox):
    """This class is use to customize groupBox with border line
    and hidden option corresponding to its checked state"""

    def __init__(self, title, concealable=False, custom_style_sheet=False):
        QGroupBox.__init__(self, title)
        if custom_style_sheet:
            self.setObjectName('GroupBoxCustomStyleSheet')
        else:
            self.setObjectName('GroupBoxCustom')
            # ==============================================================================
        # Qt Objects
        # ==============================================================================
        self.container_widget = QWidget(self)
        self.custom_style_sheet = custom_style_sheet

        # ==============================================================================
        # Layout Design
        # ==============================================================================
        layout = QVBoxLayout(self)
        layout.addWidget(self.container_widget)
        self.layout = QVBoxLayout(self.container_widget)

        # ==============================================================================
        # signal connection
        # ==============================================================================
        self.clicked.connect(self.setDisplayingState)

        # ==============================================================================
        # Initialisation
        # ==============================================================================
        self.setAlignment(Qt.AlignHCenter)
        self.setCheckable(concealable)

        if concealable:
            self.setDisplayingState(False)
        else:
            self.setDisplayingState(True)

    def _defineUnselectedStyleSheet(self):
        #    QGroupBox#GroupBoxCustomStyleSheet  {
        #                  background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
        #                                                    stop: 0 #E0E0E0, stop: 1 #FFFFFF);
        #                  border: 0px solid gray;
        #                  border-radius: 5px;
        #                  margin-top: 1ex; /* leave space at the top for the title */
        #              }
        return """QGroupBox#GroupBoxCustomStyleSheet  {
                  border: 0px solid gray;
                  border-radius: 5px;
                  margin-top: 1ex; /* leave space at the top for the title */
              }
              QGroupBox#GroupBoxCustomStyleSheet::title  {
                  subcontrol-origin: margin;
                  subcontrol-position: top center; /* position at the top center */
                  padding: 0 3px;
              }
          """

    def _defineSelectedStyleSheet(self):
        return """QGroupBox#GroupBoxCustomStyleSheet  {
                  border: 1px solid gray;
                  border-radius: 5px;
                  margin-top: 1ex; /* leave space at the top for the title */
              }
              QGroupBox#GroupBoxCustomStyleSheet::title  {
                  subcontrol-origin: margin;
                  subcontrol-position: top center; /* position at the top center */
                  padding: 0 3px;
              }
          """

    def setDisplayingState(self, checked):
        self.setChecked(checked)
        if checked:
            self.container_widget.show()
            if self.custom_style_sheet:
                self.setStyleSheet(self._defineSelectedStyleSheet())
        else:
            self.container_widget.hide()
            if self.custom_style_sheet:
                self.setStyleSheet(self._defineUnselectedStyleSheet())

    def addWidgetInLayout(self, widget):
        self.layout.addWidget(widget)

    def addLayoutInLayout(self, layout):
        self.layout.addLayout(layout)

    def addStretchInLayout(self, stretch_factor):
        self.layout.addStretch(stretch_factor)

    def isConcealed(self):
        return self.container_widget.hidden()
