# Form implementation generated from reading ui file 'ui\edit_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditDialog(object):
    def setupUi(self, EditDialog):
        EditDialog.setObjectName("EditDialog")
        EditDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(parent=EditDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.titleFrame = QtWidgets.QFrame(parent=self.frame)
        self.titleFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.titleFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.titleFrame.setObjectName("titleFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.titleFrame)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.titleLabel = QtWidgets.QLabel(parent=self.titleFrame)
        self.titleLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.titleLabel.setObjectName("titleLabel")
        self.horizontalLayout.addWidget(self.titleLabel)
        self.titleInput = QtWidgets.QLineEdit(parent=self.titleFrame)
        self.titleInput.setObjectName("titleInput")
        self.horizontalLayout.addWidget(self.titleInput)
        self.verticalLayout_2.addWidget(self.titleFrame)
        self.releasedateFrame = QtWidgets.QFrame(parent=self.frame)
        self.releasedateFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.releasedateFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.releasedateFrame.setObjectName("releasedateFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.releasedateFrame)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.releasedateLabel = QtWidgets.QLabel(parent=self.releasedateFrame)
        self.releasedateLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.releasedateLabel.setObjectName("releasedateLabel")
        self.horizontalLayout_2.addWidget(self.releasedateLabel)
        self.releasedateInput = QtWidgets.QLineEdit(parent=self.releasedateFrame)
        self.releasedateInput.setObjectName("releasedateInput")
        self.horizontalLayout_2.addWidget(self.releasedateInput)
        self.verticalLayout_2.addWidget(self.releasedateFrame)
        self.imageFrame = QtWidgets.QFrame(parent=self.frame)
        self.imageFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.imageFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.imageFrame.setObjectName("imageFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.imageFrame)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.imageLabel = QtWidgets.QLabel(parent=self.imageFrame)
        self.imageLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.imageLabel.setObjectName("imageLabel")
        self.horizontalLayout_3.addWidget(self.imageLabel)
        self.uploadImgButton = QtWidgets.QPushButton(parent=self.imageFrame)
        self.uploadImgButton.setObjectName("uploadImgButton")
        self.horizontalLayout_3.addWidget(self.uploadImgButton)
        self.verticalLayout_2.addWidget(self.imageFrame)
        self.ratingFrame = QtWidgets.QFrame(parent=self.frame)
        self.ratingFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ratingFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ratingFrame.setObjectName("ratingFrame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.ratingFrame)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ratingLabel = QtWidgets.QLabel(parent=self.ratingFrame)
        self.ratingLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.ratingLabel.setObjectName("ratingLabel")
        self.horizontalLayout_4.addWidget(self.ratingLabel)
        self.ratingInput = QtWidgets.QLineEdit(parent=self.ratingFrame)
        self.ratingInput.setObjectName("ratingInput")
        self.horizontalLayout_4.addWidget(self.ratingInput)
        self.verticalLayout_2.addWidget(self.ratingFrame)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=EditDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EditDialog)
        self.buttonBox.accepted.connect(EditDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(EditDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(EditDialog)

    def retranslateUi(self, EditDialog):
        _translate = QtCore.QCoreApplication.translate
        EditDialog.setWindowTitle(_translate("EditDialog", "Edit Anime"))
        self.titleLabel.setText(_translate("EditDialog", "New Title"))
        self.releasedateLabel.setText(_translate("EditDialog", "New Release Date"))
        self.imageLabel.setText(_translate("EditDialog", "New Image"))
        self.uploadImgButton.setText(_translate("EditDialog", "Choose from file..."))
        self.ratingLabel.setText(_translate("EditDialog", "New Rating"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditDialog = QtWidgets.QDialog()
    ui = Ui_EditDialog()
    ui.setupUi(EditDialog)
    EditDialog.show()
    sys.exit(app.exec())
