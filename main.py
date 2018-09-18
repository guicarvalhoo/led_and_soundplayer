<<<<<<< HEAD
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VilatecClientApp.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtCore import Qt
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Q_ARG, QAbstractItemModel,
        QFileInfo, qFuzzyCompare, QMetaObject, QModelIndex, QObject, Qt,
        QThread, QTime, QUrl)
from PyQt5.QtGui import QColor, qGray, QImage, QPainter, QPalette
from PyQt5.QtMultimedia import (QAbstractVideoBuffer, QMediaContent,
        QMediaMetaData, QMediaPlayer, QMediaPlaylist, QVideoFrame, QVideoProbe)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog,
        QFormLayout, QHBoxLayout, QLabel, QListView, QMessageBox, QPushButton,
        QSizePolicy, QSlider, QStyle, QToolButton, QVBoxLayout, QWidget)
from fnmatch import fnmatch
import btnStyle
import config
import random
import json
import sys
import os
import time
import re
import pygame
import paho.mqtt.client as paho
from flux_led import WifiLedBulb, BulbScanner, LedTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer,  QPoint, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap, qRgb, QColor, QImage, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget,\
     QAction, QTabWidget,QVBoxLayout, QLabel, QRadioButton, QHBoxLayout, QGroupBox, QMessageBox, QColorDialog
from math import *
import subprocess

_excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
     _excepthook(exctype, value, traceback)
     sys.exit(1)
sys.excepthook = exception_hook

global picker
picker = True
global Cena
global previousImgIndex
global Controlador
global midia_usb
midia_usb = ""
global remove_midia
remove_midia = False
global play_list
play_list = []

total_de_controladores = len(config.controllers)
Controlador = 1 # do index da cmbIDS

Cena = -1
previousImgIndex, imgIndex = (0, 1)

#pub = paho.Client("ClientID")
#pub.connect("iotgate.me",1883)
cor = "(255, 255, 255, 255)"
im = "123"
rgb = "123"

contador = 1
global BULB
BULB = []

global previousColor
bulb_info_list = []
previousColor = ""


def findControllers():
    global bulb_info_list
    scanner = BulbScanner()
    scanner.scan(timeout=2)
    bulb_info_list = scanner.getBulbInfo()  # Scaneia todos na rede

    #print(scanner)

    print("=============================================")
    print("Bulb list")
    print("=============================================")
    for i in bulb_info_list:
        print(i)
    print("=============================================")

    return bulb_info_list
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

def find_from_prompt():
   global bulb_info_list
   for i in config.controllers:
        bulb_info_list.append(i)        
   return bulb_info_list


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        sys._excepthook = sys.excepthook 
        MainWindow.setObjectName("MainWindow")
        #MainWindow.setWindowModality(QtCore.Qt.ApplicationModal) # manter aplicação em primeiro plano
        MainWindow.setEnabled(True)
        MainWindow.resize(1024, 600)
        self.color_chooser = QColorDialog()
        self.color_chooser.currentColorChanged.connect(self.color_pick)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icones/logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
##        MainWindow.setSizeGripEnabled(False)
        self.tabsWidget = QtWidgets.QTabWidget(MainWindow)        
        
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabsWidget.sizePolicy().hasHeightForWidth())
        self.tabsWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabsWidget.setFont(font)
        
        
        self.tabsWidget.setElideMode(QtCore.Qt.ElideNone)
        #self.tabsWidget.setObjectName("tabsWidget")
        
##        self.tabsWidget.setTabBar(TabBar(self))
##        self.tabsWidget.setTabPosition(2)        
        self.tabsWidget.setStyleSheet(btnStyle.get_QTabBar_style())
        
        self.tab_1 = QtWidgets.QWidget()
 
        
        
        self.conteiner_bnt_cenas = QtWidgets.QWidget(self.tab_1)
        
        #self.conteiner_bnt_cenas.setObjectName("conteiner_bnt_cenas")
        self.conteiner_selectImg = QtWidgets.QHBoxLayout(self.conteiner_bnt_cenas)
        self.conteiner_selectImg.setContentsMargins(0, 0, 0, 0)
        #self.conteiner_selectImg.setObjectName("conteiner_selectImg")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.conteiner_selectImg.addItem(spacerItem)
        self.btnArrowLeft_2 = QtWidgets.QPushButton(self.conteiner_bnt_cenas)
        self.btnArrowLeft_2.setMaximumSize(QtCore.QSize(300, 100))
        self.btnArrowLeft_2.setStyleSheet(btnStyle.btn_style())
        #self.btnArrowLeft_2.setObjectName("btnArrowLeft_2")
        
        self.btnApagar = QtWidgets.QPushButton(self.conteiner_bnt_cenas)
        self.btnApagar.setMaximumSize(QtCore.QSize(300, 100))
        self.btnApagar.setStyleSheet(btnStyle.btn_style())
        
        
        self.conteiner_selectImg.addWidget(self.btnArrowLeft_2)
        self.btnSelectImage = QtWidgets.QPushButton(self.conteiner_bnt_cenas)
        self.btnSelectImage.setMaximumSize(QtCore.QSize(300, 100))
        self.btnSelectImage.setStyleSheet(btnStyle.btn_style())
        self.btnSelectImage.clicked.connect(self.changeScenario)
        
        #self.btnSelectImage.setObjectName("btnSelectImage")
        self.conteiner_selectImg.addWidget(self.btnSelectImage)
        self.btnArrowRight = QtWidgets.QPushButton(self.conteiner_bnt_cenas)
        self.btnArrowRight.setMaximumSize(QtCore.QSize(300, 100))
        self.btnArrowRight.setStyleSheet(btnStyle.btn_style())
        #self.btnArrowRight.setObjectName("btnArrowRight")
        self.conteiner_selectImg.addWidget(self.btnArrowRight)
        self.conteiner_selectImg.addWidget(self.btnApagar)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, 900, 10)
        self.conteiner_selectImg.addItem(spacerItem1)        
        
        self.label_3 = QtWidgets.QLabel(self.tab_1)
        self.label_noImage = QtWidgets.QLabel(self.tab_1)
        self.label_noImage.setGeometry(QtCore.QRect(0, 0, 1005, 400))
        self.label_noImage.setAlignment(QtCore.Qt.AlignCenter)

        #label para mostrar a falta de imagem
        
        
        
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_noImage.setFont(font)
        
        self.label_3.setStyleSheet("background-color:rgb(200,200,200,200)")
        
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setObjectName("label_3")

        
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/colorPicker/wheel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabsWidget.addTab(self.tab_1, icon1, "")

        ################ TAB 2 ###################
        
        self.tab_2 = QtWidgets.QWidget()
        self.frameAudioUsb = QtWidgets.QFrame(self.tab_2)
        self.frameAudioUsb.setGeometry(QtCore.QRect(0, 0, 1000, 530))
        self.frameAudioUsb.setStyleSheet("border-color: rgb(239, 41, 41);")
        self.frameAudioUsb.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameAudioUsb.setFrameShadow(QtWidgets.QFrame.Raised)

        root = '/usr/share/APP/' 
        #~ root = '/usr/share/scratch/Media/Sounds/'        
                       
        pattern = "*.mp3"
        lista = []
        for path, subdirs, files in os.walk(root):
           for name in files:
             if fnmatch(name, pattern):
                lista.append(os.path.join(path, name))


		#~ lista = lista.split("\n")
                          
        self.playerWidget = Player()
        self.playerWidget.addToPlaylist(lista)

        
        histogramLayout = QHBoxLayout(self.frameAudioUsb)
        histogramLayout.addWidget(self.playerWidget)
        
        self.frameAudioLocal = QtWidgets.QFrame(self.tab_2)
        #self.tabsWidget.setGeometry(QtCore.QRect(6, 9, 1010, 585))
        self.frameAudioLocal.setGeometry(QtCore.QRect(5, 5, 995, 520))
        self.frameAudioLocal.setStyleSheet("border-color: rgb(239, 41, 41);")
        self.frameAudioLocal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameAudioLocal.setFrameShadow(QtWidgets.QFrame.Raised)
       
        self.sliderVolume = QtWidgets.QSlider(self.frameAudioLocal)
        
        self.sliderVolume.setMinimumSize(QtCore.QSize(150, 80))
        
        self.sliderVolume.setStyleSheet("QSlider::groove:horizontal {\n"
"    border: 1px solid;\n"
"    background-color: grey;\n"
"    height: 15px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background-color: blue;\n"
"    border: 1px solid;\n"
"    border-style: outset;\n"
"    border-radius: 5px;\n"
"    height: 120px;\n"
"    width: 40px;\n"
"    margin: -30px 0px;\n"
"}")
        self.sliderVolume.setMaximum(100)
        self.sliderVolume.setMinimum(0)
        self.sliderVolume.setProperty("value", 0)
        self.sliderVolume.setOrientation(QtCore.Qt.Horizontal)
        self.sliderVolume.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderVolume.setTickInterval(25)
        #self.sliderVolume.setObjectName("sliderVolume")
        self.labelVolume = QtWidgets.QLabel(self.frameAudioLocal)
        
        
        self.labelVolume.setFont(font)
        self.labelVolume.setObjectName("labelVolume")
        self.lcdVolume = QtWidgets.QLCDNumber(self.frameAudioLocal)
        
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lcdVolume.setFont(font)
        self.lcdVolume.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdVolume.setProperty("value", 0.0)
        #self.lcdVolume.setObjectName("lcdVolume")
        self.gridLayoutWidget = QtWidgets.QWidget(self.frameAudioLocal)
        
        #self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        #self.gridLayout.setObjectName("gridLayout")
        self.btnMusica4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica4.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica4.setStyleSheet(btnStyle.btn_style())
        #self.btnMusica4.setObjectName("btnMusica4")
        self.gridLayout.addWidget(self.btnMusica4, 0, 1, 1, 1)
        self.btnMusica1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica1.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica1.setStyleSheet(btnStyle.btn_style())
        #self.btnMusica1.setObjectName("btnMusica1")
        self.gridLayout.addWidget(self.btnMusica1, 0, 0, 1, 1)
        self.btnMusica6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica6.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica6.setStyleSheet(btnStyle.btn_style())
        #self.btnMusica6.setObjectName("btnMusica6")
        self.gridLayout.addWidget(self.btnMusica6, 1, 1, 1, 1)
        self.btnMusica5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica5.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica5.setStyleSheet(btnStyle.btn_style())
        #self.btnMusica5.setObjectName("btnMusica5")
        self.gridLayout.addWidget(self.btnMusica5, 1, 0, 1, 1)
        self.btnMusica3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica3.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica3.setStyleSheet(btnStyle.btn_style())
        #self.btnMusica3.setObjectName("btnMusica3")
        self.gridLayout.addWidget(self.btnMusica3, 2, 1, 1, 1)
        self.btnMusica2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica2.setEnabled(False)
        self.btnMusica2.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica2.setStyleSheet(btnStyle.btn_style())
        #self.btnMusica2.setObjectName("btnMusica2")
        self.gridLayout.addWidget(self.btnMusica2, 2, 0, 1, 1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icones/musica.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabsWidget.addTab(self.tab_2, icon2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
       
        

        # Seta a color wheel
       
        #self.img = QImage("wheel.png").mirrored() #inverte a imagem
        self.img = QImage("/usr/share/APP/img/wheel.png")
        
        self._img = QImage(1, 1, QImage.Format_ARGB32)
        self.img =self.img.scaled(400, 400, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)        
        pixmap = QtGui.QPixmap(QtGui.QPixmap.fromImage(self.img))       
        self.labelColorWheel = QtWidgets.QLabel(self.tab)
        self.labelColorWheel.setPixmap(pixmap)
        self.labelColorWheel.mouseMoveEvent = self.getPos

        
        self.labelColorWheel.resize(pixmap.width(),pixmap.height())

        #self.labelColorWheel.setObjectName("labelColorWheel")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        
        #self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        #self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioButton_6 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_6.setFont(font)
        #self.radioButton_6.setObjectName("radioButton_6")
        self.gridLayout_2.addWidget(self.radioButton_6, 3, 2, 1, 1)
        self.radioButton_10 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_10.setFont(font)
        #self.radioButton_10.setObjectName("radioButton_10")
        self.gridLayout_2.addWidget(self.radioButton_10, 5, 2, 1, 1)
        self.radioButton_7 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_7.setFont(font)
        #self.radioButton_7.setObjectName("radioButton_7")
        self.gridLayout_2.addWidget(self.radioButton_7, 4, 1, 1, 1)
        self.radioButton_9 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_9.setFont(font)
        #self.radioButton_9.setObjectName("radioButton_9")
        self.gridLayout_2.addWidget(self.radioButton_9, 5, 1, 1, 1)
        self.radioButton_5 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_5.setFont(font)
        #self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout_2.addWidget(self.radioButton_5, 3, 1, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton.setFont(font)
        #self.radioButton.setObjectName("radioButton")
        self.gridLayout_2.addWidget(self.radioButton, 1, 1, 1, 1)
        self.radioButton_8 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_8.setFont(font)
        #self.radioButton_8.setObjectName("radioButton_8")
        self.gridLayout_2.addWidget(self.radioButton_8, 4, 2, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_4.setFont(font)
        #self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout_2.addWidget(self.radioButton_4, 2, 2, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_3.setFont(font)
        #self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout_2.addWidget(self.radioButton_3, 2, 1, 1, 1)
        
        self.btnSave = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btnChooseColor = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        
        self.btnSave.setMinimumSize(QtCore.QSize(0, 80))
        self.btnChooseColor.setMinimumSize(QtCore.QSize(0, 80))
        
        self.btnSave.setStyleSheet(btnStyle.btn_style())
        self.btnChooseColor.setStyleSheet(btnStyle.btn_style())
        #self.btnSave.setObjectName("btnSave")
        
        self.btnSave.clicked.connect(self.salvaCena)
        self.btnChooseColor.clicked.connect(self.chooseColor)
        
        self.gridLayout_2.addWidget(self.btnSave, 6, 1, 1, 2)
        self.gridLayout_2.addWidget(self.btnChooseColor, 7, 1, 1, 2)
        self.cmbIDS = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cmbIDS.setFont(font)
        self.cmbIDS.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        #self.cmbIDS.setObjectName("cmbIDS")
        self.gridLayout_2.addWidget(self.cmbIDS, 0, 1, 1, 2)
        self.radioButton_2 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        #self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout_2.addWidget(self.radioButton_2, 1, 2, 1, 1)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        
        #self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        #self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.horizontalLayoutWidget_2)
        self.graphicsView.setStyleSheet("background-color: rgb(85, 170, 127);")
        #self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.graphicsView.setFixedSize(QtCore.QSize(100, 100))
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        #self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icones/gears.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabsWidget.addTab(self.tab, icon3, "")

        #tab 3
        self.tab_3 = QtWidgets.QWidget()
        #self.tab_3.setObjectName("tab_3")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        
        #self.label_2.setObjectName("label_2")
        self.tabsWidget.addTab(self.tab_3, icon, "")

        self.retranslateUi(MainWindow)
        self.tabsWidget.setCurrentIndex(0)        
##        self.tabsWidget.setTabEnabled(2, False)
        self.cmbIDS.setCurrentIndex(1)
        self.cmbIDS.highlighted[int].connect(self.mudouControlador)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ########
##        self.sliderVolume.sliderMoved.connect(self.setVolume)
        self.sliderVolume.valueChanged.connect(self.changeValue)
        self.btnMusica1.clicked.connect(self.tocaMusicaMpb)
        self.btnMusica2.clicked.connect(self.tocaMusicaClass)
        self.btnMusica3.clicked.connect(self.popup)
        self.btnMusica4.clicked.connect(self.tocaMusicaGospel)
        self.btnMusica5.clicked.connect(self.tocaMusicaClass)
        self.btnMusica6.clicked.connect(self.tocaMusicaCatolica)
        
        self.setupCmbIDS()
        self.btnApagar.clicked.connect(self.apagar_leds)
        self.btnArrowLeft_2.clicked.connect(self.moveEsq)
        self.btnArrowRight.clicked.connect(self.moveDir)
        self.tabsWidget.setIconSize(QtCore.QSize(35, 35))
        ''' SET GEOMETRY'''
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 30, 941, 361))
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(630, 70, 281, 441))
        #COLOR PICKER
        self.labelColorWheel.setGeometry(QtCore.QRect(80, 30, 400, 400))
        
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(160, 450, 251, 73))
        #BOTÃO DE SELEÇÃO DAS CENAS
        self.conteiner_bnt_cenas.setGeometry(QtCore.QRect(24, 475, 941, 50))
        #LABEL COM IMAGEM DAS CENAS
        self.label_3.setGeometry(QtCore.QRect(0, 0, 1005, 472))
        self.label2_img = QImage("/usr/share/APP/img/logo.png")

        label_pixmap = QtGui.QPixmap(QtGui.QPixmap.fromImage(self.label2_img))
##            pixmap = pixmap.scaled(900, 350, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        label_pixmap = label_pixmap.scaled(1100, 200)
        self.label_2.setPixmap(label_pixmap)
        
        self.label_2.setGeometry(QtCore.QRect(0, 0, 1005, 400))
        self.lcdVolume.setGeometry(QtCore.QRect(830, 420, 131, 101))
        self.labelVolume.setGeometry(QtCore.QRect(40, 440, 141, 61))
        self.sliderVolume.setGeometry(QtCore.QRect(200, 410, 400, 131))
        self.tabsWidget.setGeometry(QtCore.QRect(6, 9, 1010, 585))
        self.color_chooser.setWindowModality(QtCore.Qt.ApplicationModal) # manter aplicação em primeiro plano
        #~ pygame.mixer.music.set_volume(self.sliderVolume.value() / 100)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("Vilatec app")
        self.tabsWidget.setWhatsThis("<html><head/><body><p>Aba &quot;sobre&quot; explicando o que é a empresa.</p></body></html>")
        self.btnArrowLeft_2.setText("<")
        self.btnApagar.setText("APAGAR")
        self.btnSelectImage.setText("Selecionar")
        self.btnArrowRight.setText(">")
       
        self.label_noImage.setText("")
        self.im = QImage("/usr/share/APP/img/imagem1.jpg")
        pixmap = QtGui.QPixmap(QtGui.QPixmap.fromImage(self.im))        
               
        if pixmap.width() < 1 and pixmap.height() < 1:
                
                self.label_noImage.setText('Scenário '+str(imgIndex))
                pixmap = pixmap.scaled(1, 1)
                self.label_3.setPixmap(pixmap)
            

        else:
            self.label_noImage.setText('')
            pixmap = pixmap.scaled(1005, 472)
            self.label_3.setPixmap(pixmap)
            
            

        self.tabsWidget.setTabText(self.tabsWidget.indexOf(self.tab_1), "Iluminação")
        self.labelVolume.setText("Volume:")
        self.btnMusica4.setText("GOSPEL")
        self.btnMusica1.setText("MPB")
        self.btnMusica6.setText("CATÓLICAS")
        self.btnMusica5.setText("CLÁSSICAS")
        self.btnMusica3.setText("NATUREZA")
        self.btnMusica2.setText("OUTRAS")        
        self.tabsWidget.setTabText(self.tabsWidget.indexOf(self.tab_2), "Músicas")
        self.radioButton_6.setText("Cena 6")
        self.radioButton_10.setText("Cena 10")
        self.radioButton_7.setText("Cena 7")
        self.radioButton_9.setText("Cena 9")
        self.radioButton_5.setText("Cena 5")
        self.radioButton.setText("Cena 1")
        self.radioButton_8.setText("Cena 8")
        self.radioButton_4.setText("Cena 4")
        self.radioButton_3.setText("Cena 3")
        
        self.btnSave.setText("Salvar")
        self.btnChooseColor.setText("Escolher Cor")
        
        self.radioButton_2.setText("Cena 2")
        self.label.setText("(Red, Green, Blue)")
        self.tabsWidget.setTabText(self.tabsWidget.indexOf(self.tab), "Ajustes")
        
##        self.label_2.setText("<html><head/><body><p><img src=\":/icones/logo.jpg\"/></p></body></html>")
        self.tabsWidget.setTabText(self.tabsWidget.indexOf(self.tab_3), "Sobre")
        self.radioButton.toggled.connect(self.mudouCena)
        self.radioButton_2.toggled.connect(self.mudouCena)
        self.radioButton_3.toggled.connect(self.mudouCena)
        self.radioButton_4.toggled.connect(self.mudouCena)
        self.radioButton_5.toggled.connect(self.mudouCena)
        self.radioButton_6.toggled.connect(self.mudouCena)
        self.radioButton_7.toggled.connect(self.mudouCena)
        self.radioButton_8.toggled.connect(self.mudouCena)
        self.radioButton_9.toggled.connect(self.mudouCena)
        self.radioButton_10.toggled.connect(self.mudouCena)
        self.list_radioButton = [self.radioButton, self.radioButton_2, self.radioButton_3,\
                             self.radioButton_4, self.radioButton_5, self.radioButton_6,\
                             self.radioButton_7, self.radioButton_8, self.radioButton_9,\
                             self.radioButton_10]
                             
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
                if self.tabsWidget.isTabEnabled(2):
                        self.tabsWidget.setTabEnabled(2, False)
				
                else:
                        self.tabsWidget.setTabEnabled(2, True)				
				
            #~ self.playerWidget.open_file()
        event.accept()
        #~ elif event.key() == Qt.Key_Enter and event.modifiers() & Qt.Key_Alt:
            #~ self.setFullScreen(not self.isFullScreen())
            #~ event.accept()
        #~ else:
            #~ super(MainWindow, self).keyPressEvent(event)

    def changeScenario(self, index):
        global imgIndex        
        global previousImgIndex
        #if imgIndex != previousImgIndex:
            #previousImgIndex = imgIndex
        try:
                  with open('/usr/share/APP/CENAS/CENA'+str(imgIndex)+'.txt') as f:
                      line = f.readlines()
                      for self.itens in line:
                         self.thread = Thread(self.itens,"")
                         self.thread.start()
                         time.sleep(.1)
                      time.sleep(.5)
                  time.sleep(1)

                          
        except FileNotFoundError:

                buttonReply = QMessageBox.question(self, "Informação","Cena "+str(imgIndex)+ ' está sem dados,  Deseja Configurar?' , QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if buttonReply == QMessageBox.Yes:
                    
                    self.tabsWidget.setCurrentIndex(2)
                    box = self.list_radioButton[imgIndex - 1]
                    box.setChecked(True)
        

    def mudouControlador(self, index):
        '''SETA O INDICE DO CONTROLADOR'''
        global Controlador
        Controlador = index + 1
        
    def apagar_leds(self):
        if self.btnApagar.text() == 'APAGAR':
             self.btnApagar.setText("ACENDER")
             #cmd = 'flux_led -sS --off'
             
             for self.itens in bulb_info_list:
                  
                  ip = str(self.itens[1])
                  self.thread = Thread("flux_led "+ip+" -0","")
                  self.thread.start()
                  time.sleep(.1)
             time.sleep(1)
             
        else:
             self.btnApagar.setText("APAGAR")        
             global imgIndex        
             global previousImgIndex
             #cmd = 'flux_led -sS --on'
             for self.itens in bulb_info_list:                               
                  ip = str(self.itens[1])
                  self.thread = Thread("flux_led "+ip+" -1","")                                    
                  self.thread.start()
                  time.sleep(.1)
             time.sleep(1)
             
             #if imgIndex != previousImgIndex:
                 #previousImgIndex = imgIndex
             try:
                       with open('/usr/share/APP/CENAS/CENA'+str(imgIndex)+'.txt') as f:
                           line = f.readlines()
                           self.btnApagar.setText("APAGAR")        
                           for self.itens in line:
                              self.thread = Thread(self.itens,"")
                              self.thread.start()
                              time.sleep(.1)
                           time.sleep(1)
                       

                               
             except FileNotFoundError:

                     buttonReply = QMessageBox.question(self, "Informação","Cena "+str(imgIndex)+ ' está sem dados,  Deseja Configurar?' , QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                     if buttonReply == QMessageBox.Yes:
                         
                         self.tabsWidget.setCurrentIndex(2)
                         box = self.list_radioButton[imgIndex - 1]
                         box.setChecked(True)            


             
    def moveDir(self):
        global imgIndex
        if(imgIndex < 10):
            imgIndex = imgIndex + 1
            self.mudaImagem()

        
    def moveEsq(self):
        global imgIndex
        if(imgIndex > 1):
            imgIndex = imgIndex - 1
            self.mudaImagem()
    
           
    def mudaImagem(self):
        _translate = QtCore.QCoreApplication.translate        
        try:
            self.im = QImage("/usr/share/APP/img/imagem" + str(imgIndex) + ".jpg")           

            pixmap = QtGui.QPixmap(QtGui.QPixmap.fromImage(self.im))
            
            if pixmap.width() < 1 and pixmap.height() < 1:
                
                self.label_noImage.setText('Scenário '+str(imgIndex))
                pixmap = pixmap.scaled(1, 1)
                self.label_3.setPixmap(pixmap)            

            else:
                self.label_noImage.setText('')
                pixmap = pixmap.scaled(1005, 472)
                self.label_3.setPixmap(pixmap)
             
            
        except Exception as e:
            print(e)


    def mudouCena(self, param):
        global Cena        
        for obj in range(len(self.list_radioButton)):
            if self.list_radioButton[obj].isChecked():
                Cena = obj + 1
                
                


    def tocaMusicaClass(self):
        pygame.mixer.music.load('/usr/share/APP/musicas/classicas.mp3')
        pygame.mixer.music.play(-1)  # 0 - toca uma vez, -1 - toca infinitamente em loop


    def tocaMusicaMpb(self):
        pygame.mixer.music.load('/usr/share/APP/musicas/mpb.mp3')
        pygame.mixer.music.play(-1)  # 0 - toca uma vez, -1 - toca infinitamente em loop

    def tocaMusicaGospel(self):
        pygame.mixer.music.load('/usr/share/APP/musicas/gospel.mp3')
        pygame.mixer.music.play(-1)  # 0 - toca uma vez, -1 - toca infinitamente em loop


    def tocaMusicaCatolica(self):
        pygame.mixer.music.load('/usr/share/APP/musicas/catolicas.mp3')
        pygame.mixer.music.play(-1)  # 0 - toca uma vez, -1 - toca infinitamente em loop

    def tocaSomChuva(self):
        pygame.mixer.music.load('/usr/share/APP/musicas/chuva.mp3')
        pygame.mixer.music.play(-1)

    def tocaSomCachoeira(self):
        pygame.mixer.music.load('/usr/share/APP/musicas/cachoeira.mp3')
        pygame.mixer.music.play(-1)

    def tocaSomPassaros(self):
        pygame.mixer.music.load('/usr/share/APP/musicas/passaros.mp3')
        pygame.mixer.music.play(-1)

    def tocaSomMar(self):
        pygame.mixer.music.load('/usr/share/APP/musicas/mar.mp3')
        pygame.mixer.music.play(-1)

    def setVolume(self):
        print("passou")
        pass

##        print(self.sliderVolume.value())
##        if self.sliderVolume.value() < 2:
##            pygame.mixer.music.pause()
##        elif self.sliderVolume.value() > 1:
##            pygame.mixer.music.unpause()
##            pygame.mixer.music.set_volume(self.sliderVolume.value() / 100)

    def changeValue(self):
##        INCLUIR
        #~ pygame.mixer.music.set_volume(self.sliderVolume.value() / 100)
        valor = self.sliderVolume.value()
        self.lcdVolume.setProperty("value", valor)

    def popup(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Seletor - Sons de Natureza')
        msgBox.setIconPixmap(QPixmap('/usr/share/APP/img/bannerpopup2.png'))
        #msgBox.setText('<h3>Escolha abaixo o tipo de som que você gostaria de ouvir</h3>') ## SEM TEXTO, SE USAR IMAGEM
        bt1   = QPushButton('CACHOEIRA')
        bt1.setStyleSheet(btnStyle.btn_style())
        bt1.setMinimumWidth(180)
        bt1.setMaximumWidth(180)
        bt1.setMinimumHeight(80)
        bt1.clicked.connect(self.tocaSomCachoeira)
        msgBox.addButton(bt1, QMessageBox.YesRole)
        bt2   = QPushButton('PÁSSAROS')
        bt2.setStyleSheet(btnStyle.btn_style())
        bt2.setMinimumWidth(180)
        bt2.setMaximumWidth(180)
        bt2.setMinimumHeight(80)
        bt2.clicked.connect(self.tocaSomPassaros)
        msgBox.addButton(bt2, QMessageBox.YesRole)
        bt3   = QPushButton('CHUVA')
        bt3.setStyleSheet(btnStyle.btn_style())
        bt3.setMinimumWidth(180)
        bt3.setMaximumWidth(180)
        bt3.setMinimumHeight(80)
        bt3.clicked.connect(self.tocaSomChuva)
        msgBox.addButton(bt3, QMessageBox.YesRole, Qt.WindowStaysOnTopHint)
        bt4   = QPushButton('MAR / PRAIA')
        bt4.setStyleSheet(btnStyle.btn_style())
        bt4.setMinimumWidth(180)
        bt4.setMaximumWidth(180)
        bt4.setMinimumHeight(80)
        bt4.clicked.connect(self.tocaSomMar)
        msgBox.addButton(bt4, QMessageBox.NoRole)
        # bt5   = QPushButton('SAIR')
        # bt5.setStyleSheet(btnStyle.btn_style())
        # msgBox.addButton(bt5, QMessageBox.NoRole)
        flags = Qt.WindowFlags()
        flags |= Qt.X11BypassWindowManagerHint
        msgBox.setWindowFlags(flags)
        
        ret = msgBox.show()
        

    def recurring_timer(self):
        ''' SÓ PROCESSA O COLOR PICKER SE FOR VERDADEIRO '''
        global cor
        
        setCor = str(cor)
        if self.tabsWidget.currentIndex()== 2:
              
              setCor = str(setCor).replace('(',"").replace(")","").replace(" ","")
              setCor = setCor[:-4]
              self.graphicsView.setStyleSheet("background-color:rgb"+setCor)
              self.label.setText(setCor)
              global bulb_info_list
              global Cena
              global Controlador
             
##                        print(Cena, len(bulb_info_list), Controlador)
             
              ip = str(bulb_info_list[Controlador -1][1])                       
              
              cmd="flux_led -c " + setCor +' '+ip
              self.thread = Thread(cmd,"")
              self.thread.start()
              time.sleep(.1)
             
             
        global picker
        if picker:
            picker = False

        else:
            picker = True
            
        global remove_midia
        global midia_usb
 
        try:
	        if len(os.listdir("/media/pi/")) > 0 and remove_midia == False and midia_usb == "":
	            self.playerWidget.playlist.clear()
	            time.sleep(3)
	            midia_usb = os.listdir("/media/pi/")[0]            
	            print(midia_usb)            
	            if midia_usb != "":
	                
	                root = '/media/pi/'                
	                pattern = "*.mp3"
	                lista = []
	                for path, subdirs, files in os.walk(root):
	                    for name in files:
	                       if fnmatch(name, pattern):
	                         lista.append(os.path.join(path, name))
	
	
		            #~ lista = lista.split("\n")
	                        
		
	                self.playerWidget.addToPlaylist(lista)

        except:
           pass			
           
        if remove_midia == True :
            self.playerWidget.playlist.clear()
            p = subprocess.Popen("sudo eject /media/pi/"+midia_usb, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
	                close_fds=False)
            midia_usb = p.stdout.read().decode().rstrip() #show response in 'status
            remove_midia = False                        

			
            
            
            #~ while midia_usb != "":
                #~ p = subprocess.Popen("sudo eject /media/pi/"+midia_usb, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                     #~ close_fds=False)
                #~ midia_usb = p.stdout.read().decode() #show response in 'status
               
            
            if midia_usb == "":
                msgBox = QMessageBox()
		        #~ msgBox.setWindowTitle('Ejetar '+ str(midia_usb)+" ?")
                msgBox.setText('''<h1><strong><span style="color: #0000ff;">\
					A midia pode ser removida</span></strong></h1>''')
		        
                bt1   = QPushButton('Midia ejetada')
                bt1.setStyleSheet(btnStyle.btn_style())
                bt1.setMinimumWidth(180)
                bt1.setMaximumWidth(180)
                bt1.setMinimumHeight(80)
                #~ bt1.clicked.connect(self.abort_remove)
                msgBox.addButton(bt1, QMessageBox.YesRole)
                bt2   = QPushButton('Sim')
                bt2.setStyleSheet(btnStyle.btn_style())
                bt2.setMinimumWidth(180)
                bt2.setMaximumWidth(180)
                bt2.setMinimumHeight(80)
                #~ bt2.clicked.connect(self.remove_midia)
                #~ msgBox.addButton(bt2, QMessageBox.YesRole)
                flags = Qt.WindowFlags()
                flags |= Qt.SplashScreen
                msgBox.setWindowFlags(flags)   
                msg = msgBox.exec_()
                		            
                root = '/usr/share/APP/'                
                pattern = "*.mp3"
                lista = []
                for path, subdirs, files in os.walk(root):
                   for name in files:
                     if fnmatch(name, pattern):
                       lista.append(os.path.join(path, name))		
				#~ lista = lista.split("\n")	        
                self.playerWidget.addToPlaylist(lista)
		
    def setupCmbIDS(self):
        list = find_from_prompt()
        if list:
            for item in list:
                self.cmbIDS.addItem(item[0])
                
##            for item in list:
##                self.cmbIDS.addItem(item['id'])

        else:
            buttonReply = QMessageBox.question(self, 'Nenhum controlador encontrado',\
                "Tentar novamente", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                while not list:
                     list = find_from_prompt()
                     if list:
                        for item in list:
                           self.cmbIDS.addItem(item[0])
                     else:
                          buttonReply = QMessageBox.question(self, 'Nenhum controlador encontrado',\
                          "Tentar novamente", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                          if buttonReply == QMessageBox.Yes:
                                pass
            else:
               print('No clicked.')            
        
            

    def change_cmbIDS(self, ids):
         pass
##        ''' Função chamada pela thread na função: def setupCmbIDS(self): '''
##        cmd="flux_led -s"
##        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
##                      close_fds=False)
##        print(p.stdout.read()) #show response in 'status
##          
##        if ids !='a':
##            print("veio")
##            list = json.loads(ids) #converte a string ids em lista
##            self.cmbIDS.addItem(list['id'])
            
##
##        else:
##            buttonReply = QMessageBox.question(self, 'Erro',\
##                "Nenhum controlador encontrado\n       Tentar novamente?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
##            if buttonReply == QMessageBox.Yes:
##                '''Chama a thread novamente para buscar bulbs'''
##                self.thread = Thread("list","")          
##                self.thread.tempSignal.connect(self.change_cmbIDS)
##                self.thread.start()
##            else:
##                self.thread = Thread("list","")          
##                self.thread.tempSignal.connect(self.change_cmbIDS)
        
##            print(json.loads(cor))
##                self.graphicsView.setStyleSheet("background-color:rgb"+cor)
##                self.label.setText(str(cor))

    def responseThread(self,data):
        ''' Função chamada pela thread na função: a definir: def salvaCena(self):'''
        
        global cor
        print("desativar esse print")
        


    def chooseColor(self):

          self.color_chooser.showFullScreen()

    def salvaCena(self):
        global bulb_info_list
        global Cena
        global cor
        global Controlador
        CONTROLADOR = Controlador -1
        setCor = str(cor)
        if Cena > -1:
            setCor = str(setCor).replace('(',"").replace(")","").replace(" ","")
            setCor = setCor[:-4]        
    ##        print(Cena, len(bulb_info_list), Controlador)
            
            ip = bulb_info_list[CONTROLADOR][1]
            print(ip)
            
            
            cmd="flux_led " + ip +' -C gradual 90 '+ setCor
    ##        cmd="flux_led -c " + setCor +' '+ip
            try:
                 with open('/usr/share/APP/CENAS/CENA'+str(Cena)+'.txt') as f:
                     line = f.readlines()
                     
                     line[CONTROLADOR] = line[CONTROLADOR].replace(line[CONTROLADOR], cmd +'\n')
                     
                     
                     
                 with open('/usr/share/APP/CENAS/CENA'+str(Cena)+'.txt', "w") as f:
                      f.writelines(line)
    ##                 f.write(line)
                         
            except FileNotFoundError:
                 if os.path.exists('/usr/share/APP/CENAS') == False:
                      os.mkdir('/usr/share/APP/CENAS')
                 
                      
                 with open('/usr/share/APP/CENAS/CENA'+str(Cena)+'.txt', 'w') as f:
                     
                     for i in range(0, total_de_controladores):
                         '''se não tiver arquivo grava x x a mesma cor'''
                         f.write(cmd+'\n')

            buttonReply = QMessageBox.question(self, 'Informação',\
              "Scenário " +str(Cena)+" gravado com sucesso", QMessageBox.Ok)
##            if buttonReply == QMessageBox.Yes:
##                pass
        else:
            buttonReply = QMessageBox.question(self, 'Informação',\
              "Escolha uma Cena para proseguir", QMessageBox.Ok)

    def color_pick(self, color):
        
        global picker
        global cor
        cor = color.getRgb()
        setCor = str(cor)
        if picker:
            try:

                   
                   
                        
                        
                        setCor = str(setCor).replace('(',"").replace(")","").replace(" ","")
                        setCor = setCor[:-4]
                        self.graphicsView.setStyleSheet("background-color:rgb"+setCor)
                        self.label.setText(cor)
                        global bulb_info_list
                        global Cena
                        global Controlador
                       
##                        print(Cena, len(bulb_info_list), Controlador)
                       
                        ip = bulb_info_list[Controlador -1][1]
                        
                        
                        cmd="flux_led -c " + setCor +' '+ip
                        self.thread = Thread(cmd,"")
                        self.thread.start()
                        time.sleep(.1)
               
                 


##
            except Exception as e:
                print(e)

        picker = False
        

    def getPos(self , event):        
            
        global picker
        global cor
##        if picker:
##            try:
##
##                    centerX = 200
##                    centerY = 200
##                    radius = 200                    
##                    x = event.pos().x()
##                    y = event.pos().y()
##                    position = sqrt((x - centerX)**2 + (y - centerY)**2)
##                    c = self.img.pixel(x,y)  # color code (integer): 3235912
##                    # depending on what kind of value you like (arbitary examples)
##                    c_qobj = QColor(c)  # color object
##                    c_rgb = str(QColor(c).getRgb())  # 8bit RGBA: (255, 23, 0, 255)
####                    print( x, y, c_rgb)
##                    if (position < radius):
##                        
##                        cor = c_rgb
##                        cor = cor.replace('(',"").replace(")","").replace(" ","")
##                        cor = cor[:-4]
##                        self.graphicsView.setStyleSheet("background-color:rgb"+c_rgb)
##                        self.label.setText(cor)
##                        global bulb_info_list
##                        global Cena
##                        global Controlador
##                       
####                        print(Cena, len(bulb_info_list), Controlador)
##                       
##                        ip = str(bulb_info_list[Controlador -1][1])                       
##                        
##                        cmd="flux_led -c " + cor +' '+ip
##                        self.thread = Thread(cmd,"")
##                        self.thread.start()
##                        time.sleep(.1)
##               
##                 
##
##
####
##            except Exception as e:
##                print(e)
##
##        picker = False
##        



#import images_rc



class Thread(QtCore.QThread):
##    tempSignal = QtCore.pyqtSignal(str)
    
    def __init__(self, cmd, cor,   parent=None):
        super(Thread, self).__init__(parent=parent)
        self.cmd = cmd
##        self.ip = ip
        
    def run(self):
     global bulb_info_list    
     p = subprocess.Popen(self.cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                 close_fds=False)
     print(p.stdout.read()) #show response in 'status




class PlaylistModel(QAbstractItemModel):

    Title, ColumnCount = range(2)

    def __init__(self, parent=None):
        super(PlaylistModel, self).__init__(parent)

        self.m_playlist = None

    def rowCount(self, parent=QModelIndex()):
        return self.m_playlist.mediaCount() if self.m_playlist is not None and not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        return self.ColumnCount if not parent.isValid() else 0

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column) if self.m_playlist is not None and not parent.isValid() and row >= 0 and row < self.m_playlist.mediaCount() and column >= 0 and column < self.ColumnCount else QModelIndex()

    def parent(self, child):
        return QModelIndex()

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            if index.column() == self.Title:
                location = self.m_playlist.media(index.row()).canonicalUrl()
                return QFileInfo(location.path()).fileName()

            return self.m_data[index]

        return None

    def playlist(self):
        return self.m_playlist

    def setPlaylist(self, playlist):
        if self.m_playlist is not None:
            self.m_playlist.mediaAboutToBeInserted.disconnect(
                    self.beginInsertItems)
            self.m_playlist.mediaInserted.disconnect(self.endInsertItems)
            self.m_playlist.mediaAboutToBeRemoved.disconnect(
                    self.beginRemoveItems)
            self.m_playlist.mediaRemoved.disconnect(self.endRemoveItems)
            self.m_playlist.mediaChanged.disconnect(self.changeItems)

        self.beginResetModel()
        self.m_playlist = playlist

        if self.m_playlist is not None:
            self.m_playlist.mediaAboutToBeInserted.connect(
                    self.beginInsertItems)
            self.m_playlist.mediaInserted.connect(self.endInsertItems)
            self.m_playlist.mediaAboutToBeRemoved.connect(
                    self.beginRemoveItems)
            self.m_playlist.mediaRemoved.connect(self.endRemoveItems)
            self.m_playlist.mediaChanged.connect(self.changeItems)

        self.endResetModel()

    def beginInsertItems(self, start, end):
       
        self.beginInsertRows(QModelIndex(), start, end)

    def endInsertItems(self):
      
        self.endInsertRows()

    def beginRemoveItems(self, start, end):
        self.beginRemoveRows(QModelIndex(), start, end)

    def endRemoveItems(self):
        self.endRemoveRows()

    def changeItems(self, start, end):
        self.dataChanged.emit(self.index(start, 0),
                self.index(end, self.ColumnCount))
        
class Player(QWidget):

    fullScreenChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(Player, self).__init__(parent)

        self.colorDialog = None
        self.trackInfo = ""
        self.statusInfo = ""
        self.duration = 0

        self.player = QMediaPlayer()
        self.player.setVolume(20)
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)      
        self.player.durationChanged.connect(self.durationChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.metaDataChanged.connect(self.metaDataChanged)
        self.playlist.currentIndexChanged.connect(self.playlistPositionChanged)
        self.player.mediaStatusChanged.connect(self.statusChanged)
        self.player.bufferStatusChanged.connect(self.bufferingProgress)
        self.player.videoAvailableChanged.connect(self.videoAvailableChanged)
        self.player.error.connect(self.displayErrorMessage)

##        self.videoWidget = VideoWidget()
##        self.player.setVideoOutput(self.videoWidget)

        self.playlistModel = PlaylistModel()
        self.playlistModel.setPlaylist(self.playlist)

        self.playlistView = QListView()
        self.playlistView.setSpacing(2)
        self.playlistView.setStyleSheet(''' 
			    
			    background-color: white;
			    font: 20px Arial ;
			    
			    color: blue;
			    selection-color: white;
			    selection-background-color: blue;
			}''')               
        self.playlistView.setModel(self.playlistModel)
        self.playlistView.setCurrentIndex(
                self.playlistModel.index(self.playlist.currentIndex(), 0))

        #~ self.playlistView.activated.connect(self.jump)
        self.playlistView.clicked.connect(self.jump)        
 

        self.slider = QSlider(Qt.Horizontal)
     
           
        self.slider.setRange(0, self.player.duration() / 1000)

        self.labelDuration = QLabel()
        #~ self.slider.sliderMoved.connect(self.seek) não alterar musica




        openButton = QPushButton("Abrir", clicked=self.open_file)

        controls = PlayerControls()
        controls.setState(self.player.state())
        controls.setVolume(self.player.volume())
        controls.setMuted(controls.isMuted())


        controls.play.connect(self.player.play)
        controls.pause.connect(self.player.pause)
        controls.stop.connect(self.player.stop)
        controls.next.connect(self.playlist.next)
        controls.previous.connect(self.previousClicked)
        controls.changeVolume.connect(self.player.setVolume)
        controls.changeMuting.connect(self.player.setMuted)
        controls.changeRate.connect(self.player.setPlaybackRate)
##        controls.stop.connect(self.videoWidget.update)

        self.player.stateChanged.connect(controls.setState)
        self.player.volumeChanged.connect(controls.setVolume)
        self.player.mutedChanged.connect(controls.setMuted)

##        self.fullScreenButton = QPushButton("FullScreen")
##        self.fullScreenButton.setCheckable(True)

##        self.colorButton = QPushButton("Color Options...")
##        self.colorButton.setEnabled(False)
##        self.colorButton.clicked.connect(self.showColorDialog)

        displayLayout = QHBoxLayout()
##        displayLayout.addWidget(self.videoWidget, 2)
        displayLayout.addWidget(self.playlistView)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        #~ controlLayout.addWidget(openButton)
        #~ controlLayout.addStretch(1) #adiciona um espaço vazio
        controlLayout.addWidget(controls)
        #~ controlLayout.addStretch(1) #adiciona um espaço vazio
##        controlLayout.addWidget(self.fullScreenButton)
##        controlLayout.addWidget(self.colorButton)

        layout = QVBoxLayout()
        layout.addLayout(displayLayout)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.slider)
        hLayout.addWidget(self.labelDuration)
        layout.addLayout(hLayout)
        layout.addLayout(controlLayout)
        #~ layout.addLayout(histogramLayout)

        self.setLayout(layout)

        if not self.player.isAvailable():
            QMessageBox.warning(self, "Service not available",
                    "The QMediaPlayer object does not have a valid service.\n"
                    "Please check the media service plugins are installed.")

            controls.setEnabled(False)
            self.playlistView.setEnabled(False)
##            openButton.setEnabled(False)
##            self.colorButton.setEnabled(False)
##            self.fullScreenButton.setEnabled(False)

        self.metaDataChanged()
               
        global play_list
                      
        #self.addToPlaylist(play_list)

    def open_file(self):
        fileNames, _ = QFileDialog.getOpenFileNames(self, "ESCOLHA O ÁLBUM","/media/pi")
    
        self.addToPlaylist(fileNames)

    def addToPlaylist(self, fileNames):
        global play_list 
        print(fileNames)          
        for name in fileNames:
            fileInfo = QFileInfo(name)
            if fileInfo.exists():
                				
                url = QUrl.fromLocalFile(fileInfo.absoluteFilePath())
                
                if fileInfo.suffix().lower() == 'mp3':
                    #~ print("passou 1")
                    self.playlist.addMedia(QMediaContent(url))
##                    self.playlist.load(url)
                else:
                    self.playlist.addMedia(QMediaContent(url))
                    print("passou 2")
            else:
                url = QUrl(name)
                if url.isValid():
                    print("passou 3")
                    self.playlist.addMedia(QMediaContent(url))

    def durationChanged(self, duration):
        duration /= 1000

        self.duration = duration
        self.slider.setMaximum(duration)

    def positionChanged(self, progress):
        progress /= 1000

        if not self.slider.isSliderDown():
            self.slider.setValue(progress)

        self.updateDurationInfo(progress)

    def metaDataChanged(self):
        pass
        #~ if self.player.isMetaDataAvailable():
            #~ self.setTrackInfo("%s - %s" % (
                    #~ self.player.metaData(QMediaMetaData.AlbumArtist),
                    #~ self.player.metaData(QMediaMetaData.Title)))

    def previousClicked(self):
        # Go to the previous track if we are within the first 5 seconds of
        # playback.  Otherwise, seek to the beginning.
        if self.player.position() <= 5000:
            self.playlist.previous()
        else:
            self.player.setPosition(0)
            self.player.play()
            self.player.play()            

    def jump(self, index):
        if index.isValid():
            self.playerState = QMediaPlayer.StoppedState	
            self.playlist.setCurrentIndex(index.row())
            self.player.play()
            self.player.play()            

    def playlistPositionChanged(self, position):
        self.playlistView.setCurrentIndex(
                self.playlistModel.index(position, 0))

    def seek(self, seconds):
        self.player.setPosition(seconds * 1000)

    def statusChanged(self, status):
        self.handleCursor(status)
        print(status)
        if status == QMediaPlayer.LoadingMedia:
            self.setStatusInfo("Loading...")
        elif status == QMediaPlayer.StalledMedia:
            self.setStatusInfo("Media Stalled")
        elif status == QMediaPlayer.EndOfMedia:
            QApplication.alert(self)
        elif status == QMediaPlayer.InvalidMedia:
            self.displayErrorMessage()
        else:
            self.setStatusInfo("")

    def handleCursor(self, status):
        if status in (QMediaPlayer.LoadingMedia, QMediaPlayer.BufferingMedia, QMediaPlayer.StalledMedia):
            self.setCursor(Qt.BusyCursor)
        else:
            self.unsetCursor()

    def bufferingProgress(self, progress):
        self.setStatusInfo("Buffering %d%" % progress)

    def videoAvailableChanged(self, available):
        
##        if available:
##            self.fullScreenButton.clicked.connect(
##                    self.videoWidget.setFullScreen)
##            self.videoWidget.fullScreenChanged.connect(
##                    self.fullScreenButton.setChecked)
##
##            if self.fullScreenButton.isChecked():
##                self.videoWidget.setFullScreen(True)
##        else:
##            self.fullScreenButton.clicked.disconnect(
##                    self.videoWidget.setFullScreen)
##            self.videoWidget.fullScreenChanged.disconnect(
##                    self.fullScreenButton.setChecked)
##
##            self.videoWidget.setFullScreen(False)
##
##        self.colorButton.setEnabled(available)
          pass

    def setTrackInfo(self, info):
        self.trackInfo = info

        #~ if self.statusInfo != "":
            #~ self.setWindowTitle("%s | %s" % (self.trackInfo, self.statusInfo))
        #~ else:
            #~ self.setWindowTitle(self.trackInfo)

    def setStatusInfo(self, info):
        self.statusInfo = info

        #~ if self.statusInfo != "":
            #~ self.setWindowTitle("%s | %s" % (self.trackInfo, self.statusInfo))
        #~ else:
            #~ self.setWindowTitle(self.trackInfo)

    def displayErrorMessage(self):
        self.setStatusInfo(self.player.errorString())

    def updateDurationInfo(self, currentInfo):
        duration = self.duration
        if currentInfo or duration:
            currentTime = QTime((currentInfo/3600)%60, (currentInfo/60)%60,
                    currentInfo%60, (currentInfo*1000)%1000)
            totalTime = QTime((duration/3600)%60, (duration/60)%60,
                    duration%60, (duration*1000)%1000);

            format = 'hh:mm:ss' if duration > 3600 else 'mm:ss'
            tStr = currentTime.toString(format) + " / " + totalTime.toString(format)
        else:
            tStr = ""

        self.labelDuration.setText(tStr)

 
class PlayerControls(QWidget):

    play = pyqtSignal()
    clear = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()
    next = pyqtSignal()
    previous = pyqtSignal()
    changeVolume = pyqtSignal(int)
    changeMuting = pyqtSignal(bool)
    changeRate = pyqtSignal(float)

    def __init__(self, parent=None):
        super(PlayerControls, self).__init__(parent)
        self.playerState = QMediaPlayer.StoppedState
        self.playerMuted = False
        self.playButton = QToolButton(clicked=self.playClicked)
        self.playButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/play.png"))
        self.playButton.setIconSize(QtCore.QSize(90, 35))
 

        self.stopButton = QToolButton(clicked=self.stop)
        #~ self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.setEnabled(False)
        self.stopButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/stop.png"))
        self.stopButton.setIconSize(QtCore.QSize(90, 35))  


        self.nextButton = QToolButton(clicked=self.next)
        self.nextButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/avancar.png"))
        self.nextButton.setIconSize(QtCore.QSize(90, 35))  
 

        self.previousButton = QToolButton(clicked=self.previous)                

        self.previousButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/retroceder.png"))
        self.previousButton.setIconSize(QtCore.QSize(90, 35)) 
        
        self.ejectButton = QToolButton()                
        self.ejectButton.clicked.connect(self.ejetar)

        self.ejectButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/ejetar.png"))
        self.ejectButton.setIconSize(QtCore.QSize(90, 35))                      

        self.muteButton = QToolButton(clicked=self.muteClicked) 
        self.muteButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/volume.png"))
        self.muteButton.setIconSize(QtCore.QSize(60, 20))                  

        self.volumeSlider = QSlider(Qt.Horizontal,
                valueChanged=self.changeVolume)
        self.volumeSlider.setMinimumSize(QtCore.QSize(180, 80))
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setProperty("value", 20)
        self.volumeSlider.setSliderPosition(20)
        self.volumeSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.volumeSlider.setTickInterval(25)        
        self.volumeSlider.setStyleSheet(''' QSlider::groove:horizontal {
			    border: 1px solid;
			    background-color: grey;
			    height: 15px;
			    margin: 10px;
			}
			
			QSlider::handle:horizontal {
			    background-color: blue;
			    border: 1px solid;
			    border-style: outset;
			    border-radius: 5px;
			    height: 10px;
			    width: 15px;
			    margin: -30px 0px;
			}''')
        self.rateBox = QComboBox(activated=self.updateRate)
        self.rateBox.addItem("0.5x", 0.5)
        self.rateBox.addItem("1.0x", 1.0)
        self.rateBox.addItem("2.0x", 2.0)
        self.rateBox.setCurrentIndex(1)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stopButton)
        layout.addWidget(self.previousButton)        
        layout.addWidget(self.playButton)
        layout.addWidget(self.nextButton)
        layout.addWidget(self.ejectButton)
        layout.addWidget(self.muteButton)
        layout.addWidget(self.volumeSlider)
        #~ layout.addWidget(self.rateBox)
        self.setLayout(layout)

    def state(self):
        return self.playerState

    def setState(self,state):
        if state != self.playerState:
            self.playerState = state

            if state == QMediaPlayer.StoppedState:
                self.stopButton.setEnabled(False)
                self.playButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/play.png"))
                #~ self.playButton.setIcon(
                        #~ self.style().standardIcon(QStyle.SP_MediaPlay))
            elif state == QMediaPlayer.PlayingState:
                self.stopButton.setEnabled(True)
                self.playButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/pause.png"))
                #~ self.playButton.setIcon(
                        #~ self.style().standardIcon(QStyle.SP_MediaPause))
            elif state == QMediaPlayer.PausedState:
                self.stopButton.setEnabled(True)
                self.playButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/play.png"))
                #~ self.playButton.setIcon(
                        #~ self.style().standardIcon(QStyle.SP_MediaPlay))
    def ejetar(self):
        global midia_usb
        global remove_midia             
        if midia_usb != "":						
	        msgBox = QMessageBox()
	        msgBox.setWindowTitle('Ejetar '+ str(midia_usb)+" ?")
	        msgBox.setText('''<h1><strong><span style="color: #0000ff;">\
	        Deseja ejetar a m&iacute;dia?</span></strong></h1>''')
	        
	        bt1   = QPushButton('Cancelar')
	        bt1.setStyleSheet(btnStyle.btn_style())
	        bt1.setMinimumWidth(180)
	        bt1.setMaximumWidth(180)
	        bt1.setMinimumHeight(80)
	        bt1.clicked.connect(self.abort_remove)
	        msgBox.addButton(bt1, QMessageBox.YesRole)
	        bt2   = QPushButton('Sim')
	        bt2.setStyleSheet(btnStyle.btn_style())
	        bt2.setMinimumWidth(180)
	        bt2.setMaximumWidth(180)
	        bt2.setMinimumHeight(80)
	        bt2.clicked.connect(self.remove_midia)
	        msgBox.addButton(bt2, QMessageBox.YesRole)
	        flags = Qt.WindowFlags()
	        flags |= Qt.SplashScreen
	        msgBox.setWindowFlags(flags)   
	        msg = msgBox.exec_()
    def abort_remove(self):
        global remove_midia     
        remove_midia = False
	        
    def remove_midia(self):
        global remove_midia     
        global midia_usb       
        midia = midia_usb 
               
        if midia != "":
	        remove_midia = True 
	        
    
    def volume(self):
        return self.volumeSlider.value()

    def setVolume(self, volume):
        self.volumeSlider.setValue(volume)

    def isMuted(self):
        return self.playerMuted

    def setMuted(self, muted):
        if muted != self.playerMuted:
            self.playerMuted = muted
            #~ self.muteButton.setStyleSheet(btnStyle.style_player("/usr/share/APP/btn/mute.png"))
            self.muteButton.setStyleSheet(btnStyle.style_player(\
            "/usr/share/APP/btn/mute.png")if muted else btnStyle.style_player("/usr/share/APP/btn/volume.png"))
           
        #~ else:
            

            #~ self.muteButton.setIcon(
                    #~ self.style().standardIcon(
                            #~ QStyle.SP_MediaVolumeMuted if muted else QStyle.SP_MediaVolume))

    def playClicked(self):
        if self.playerState in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState):
            self.play.emit()
        elif self.playerState == QMediaPlayer.PlayingState:
            self.pause.emit()

    def muteClicked(self):
        self.changeMuting.emit(not self.playerMuted)

    def playbackRate(self):
        return self.rateBox.itemData(self.rateBox.currentIndex())

    def setPlaybackRate(self, rate):
        for i in range(self.rateBox.count()):
            if qFuzzyCompare(rate, self.rateBox.itemData(i)):
                self.rateBox.setCurrentIndex(i)
                return

        self.rateBox.addItem("%dx" % rate, rate)
        self.rateBox.setCurrentIndex(self.rateBox.count() - 1)

    def updateRate(self):
        self.changeRate.emit(self.playbackRate())

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        #~ pygame.init()

##        self.ui = Ui_MainWindow()
        self.setupUi(self)


        self.timer = QTimer()
        self.timer.setInterval(1000)       
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        #~ vbox = QVBoxLayout()
        #~ self.setLayout(vbox)
        self.frameAudioLocal.hide()
        self.tabsWidget.setTabEnabled(2, False)
##        self.tabsWidget.removeTab(2)
##        self.tab_3.hide()
        self.showFullScreen()

        #~ self.show()
        
if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
       app = QtWidgets.QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))
        

w = MainWindow()
w.show()
sys.exit(app.exec_())
=======
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VilatecClientApp.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import random
import json
import sys
import os
import time
import re
import pygame
import paho.mqtt.client as paho
from flux_led import WifiLedBulb, BulbScanner, LedTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer,  QPoint, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap, qRgb, QColor, QImage, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget,\
     QAction, QTabWidget,QVBoxLayout, QLabel, QRadioButton, QHBoxLayout, QGroupBox, QMessageBox
from PIL import Image
from math import *
import subprocess

_excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
     _excepthook(exctype, value, traceback)
     sys.exit(1)
sys.excepthook = exception_hook

global picker
picker = True
global Cena
global Controlador
total_de_controladores = 4
Controlador = 1 # do index da cmbIDS

Cena = -1
#pub = paho.Client("ClientID")
#pub.connect("iotgate.me",1883)
cor = "(255, 255, 255, 255)"
im = "123"
rgb = "123"
imgIndex = 1
contador = 1
global BULB
BULB = []

global previousColor
bulb_info_list = []
previousColor = ""
def btn_style():
    styleBtn = str("""
    QPushButton
    {
    font: 15pt Arial;
    margin: 1px;
    border-color: #0c457e;
    border-style: outset;
    border-radius: 3px;
    border-width: 1px;
    color: white;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2198c0, stop: 1 #0d5ca6);
    }

    QPushButton:pressed
    {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0d5ca6, stop: 1 #2198c0);
    }
""")
    return styleBtn
    
    
def get_QTabBar_style():
    styleStr = str("""
        QTabBar {                                          
            background: None;                         
            color: #ff000000;                              
            font: 12pt Arial;
            min-height: 20px;
            position: west;
                                        
        }                                                  
        QTabBar::tab {                  
            background: #6574ff;                         
            color: #000000;                              
            border-width: 2px;                             
            border-style: solid;                           
            border-color: #0000ff;                             
            border-bottom-color: #00ffffff;                
            border-top-left-radius: 6px;                   
            border-top-right-radius: 18px;                  
            min-height: 10px;                              
            padding: 2px;                                  
        }                                                  
        QTabBar::tab:selected {
        margin-top: 2px;
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2198c0, stop: 1 #0d5ca6);
            border-color:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2198c0, stop: 1 #0d5ca6);                             
            border-bottom-color: #0800ff;
           
        }                                                  
        QTabBar::tab:!selected {                           
            margin-top: 8px;                               
        }                                                  
        QTabBar[colorToggle=true]::tab {                   
        background: #ff0000;                         
        }                                                  
    """)

    return styleStr


def findControllers():
    global bulb_info_list
    scanner = BulbScanner()
    scanner.scan(timeout=2)
    bulb_info_list = scanner.getBulbInfo()  # Scaneia todos na rede

    #print(scanner)

    print("=============================================")
    print("Bulb list")
    print("=============================================")
    for i in bulb_info_list:
        print(i)
    print("=============================================")

    return bulb_info_list

def find_from_prompt():
   global bulb_info_list
   cmd="flux_led -s"
   p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                 close_fds=False)
   bulbs = p.stdout.readlines()
   print(bulbs)
   del bulbs[0]
   LIST_OF_BULBS = []
   BULB = []        
   SERIAL_NUMBER = ''
   ER = ''
   IP = []
   ip = ''
   
   for elements in bulbs:             
        fim = False
        ocorreu = False
        for itens in str(elements):        
             if itens.isdigit() and not fim:
                  ocorreu = True
                  SERIAL_NUMBER = SERIAL_NUMBER + itens
             elif ocorreu and itens != " " and not fim:
                  SERIAL_NUMBER = SERIAL_NUMBER + itens                  
             else:
                  
                  if ocorreu and itens == " ":
                       BULB.append(SERIAL_NUMBER)
                       SERIAL_NUMBER = ''
                       fim = True
             if fim:
                  if itens != " " and itens != "\\"and itens != "n":
                       ip = ip + itens
        
        BULB.append(ip.replace("\r","").replace("'",""))
        bulb_info_list.append(BULB)
        BULB = []
        ip = ''
   return bulb_info_list

##def action(multiple, id, color, intensity):
##        global previousColor
##        global previousID
##        try:
##          print("\n==================================")
##          print(" DEBUG INFORMATION")
##          print("==================================")
##          print("Multiple: "   + str(multiple))
##          print("id: "         + id)
##          print("Color: "      + color)
##          print("intensity: "  + str(intensity))
##          print("==================================\n")
##
##          # Remove os caracteres ( ) e remove os espacos no texto
##          color = color.replace('(',"").replace(")","").replace(" ","")
##          # So altera a cor caso ela seja diferente
##          print(color)
##          if (color != previousColor or id != previousID):
##            previousColor = color
##            previousID    = id
##            colorList     = color.split(',')
##
##            print(colorList)
##
##            if(multiple == True):
##              print("Looking for bulbs...")
##              for bulb_info in bulb_info_list:
##                if bulb_info:
##                    bulb = WifiLedBulb(bulb_info['ipaddr'])
##                    bulb.refreshState()
##
##                    r = int(colorList[0])
##                    g = int(colorList[1])
##                    b = int(colorList[2])
##
##                    print(bulb_info['ipaddr'] + " (Red: " + str(r) + " ,Green: "+ str(g) +" ,Blue: "+ str(b) + ")")
##                    if(int(intensity) > 0):
##                      bulb.setRgb(r,g,b, persist=True, brightness=intensity)
##                    else:
##                      bulb.setRgb(r,g,b, persist=True)
##
##                else:
##                    print("Couldn't find the " + id + " bulb")
##            else:
##              print("Specific bulb...")
##
##              # Itera pelo lista de lampadas até encontrar uma com o ip específico.
##              if bulb_info_list:                
##                    for i in bulb_info_list:
##                        if(i['id'] == id):
##                          bulb_info = i
##                          print("bulb_info")
##                          print(bulb_info)
##                          break         
##
##                    
##                    #bulb_info = scanner.getBulbInfoByID(id)
##                    bulb = WifiLedBulb(bulb_info['ipaddr'])
##                    bulb.refreshState()
##                    print("bulb")
##                    print(bulb)
##                    if bulb:
##                        r = int(colorList[0])
##                        g = int(colorList[1])
##                        b = int(colorList[2])
##
##                        print(bulb_info['ipaddr'] + " (Red: " + str(r) + " ,Green: "+ str(g) +" ,Blue: "+ str(b) + ")")
##                        if(int(intensity) > 0):
##                            bulb.setRgb(r,g,b, persist=True, brightness=intensity)
##                        else:
##                            bulb.setRgb(r,g,b, persist=True)
##        except Exception as e:
##            print(e)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        sys._excepthook = sys.excepthook 
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1024, 600)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icones/logo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
##        MainWindow.setSizeGripEnabled(False)
        self.tabsWidget = QtWidgets.QTabWidget(MainWindow)        
        
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabsWidget.sizePolicy().hasHeightForWidth())
        self.tabsWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabsWidget.setFont(font)
        
        
        self.tabsWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabsWidget.setObjectName("tabsWidget")
        
##        self.tabsWidget.setTabBar(TabBar(self))
##        self.tabsWidget.setTabPosition(2)        
        self.tabsWidget.setStyleSheet(get_QTabBar_style())
        
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        
        
        self.conteiner_bnt_cenas = QtWidgets.QWidget(self.tab_1)
        
        self.conteiner_bnt_cenas.setObjectName("conteiner_bnt_cenas")
        self.conteiner_selectImg = QtWidgets.QHBoxLayout(self.conteiner_bnt_cenas)
        self.conteiner_selectImg.setContentsMargins(0, 0, 0, 0)
        self.conteiner_selectImg.setObjectName("conteiner_selectImg")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.conteiner_selectImg.addItem(spacerItem)
        self.btnArrowLeft_2 = QtWidgets.QPushButton(self.conteiner_bnt_cenas)
        self.btnArrowLeft_2.setMaximumSize(QtCore.QSize(300, 100))
        self.btnArrowLeft_2.setStyleSheet(btn_style())
        self.btnArrowLeft_2.setObjectName("btnArrowLeft_2")
        self.conteiner_selectImg.addWidget(self.btnArrowLeft_2)
        self.btnSelectImage = QtWidgets.QPushButton(self.conteiner_bnt_cenas)
        self.btnSelectImage.setMaximumSize(QtCore.QSize(300, 100))
        self.btnSelectImage.setStyleSheet(btn_style())
        self.btnSelectImage.setObjectName("btnSelectImage")
        self.conteiner_selectImg.addWidget(self.btnSelectImage)
        self.btnArrowRight = QtWidgets.QPushButton(self.conteiner_bnt_cenas)
        self.btnArrowRight.setMaximumSize(QtCore.QSize(300, 100))
        self.btnArrowRight.setStyleSheet(btn_style())
        self.btnArrowRight.setObjectName("btnArrowRight")
        self.conteiner_selectImg.addWidget(self.btnArrowRight)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, 900, 10)
        self.conteiner_selectImg.addItem(spacerItem1)        
        
        self.label_3 = QtWidgets.QLabel(self.tab_1)
        self.label_noImage = QtWidgets.QLabel(self.tab_1)
        self.label_noImage.setGeometry(QtCore.QRect(0, 0, 1005, 400))
        self.label_noImage.setAlignment(QtCore.Qt.AlignCenter)

        #label para mostrar a falta de imagem
        
        
        
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_noImage.setFont(font)
        
        self.label_3.setStyleSheet("background-color:rgb(200,200,200,200)")
        
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setObjectName("label_3")

        
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/colorPicker/wheel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabsWidget.addTab(self.tab_1, icon1, "")        
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.sliderVolume = QtWidgets.QSlider(self.tab_2)
        
        self.sliderVolume.setMinimumSize(QtCore.QSize(150, 80))
        
        self.sliderVolume.setStyleSheet("QSlider::groove:horizontal {\n"
"    border: 1px solid;\n"
"    background-color: grey;\n"
"    height: 15px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background-color: blue;\n"
"    border: 1px solid;\n"
"    border-style: outset;\n"
"    border-radius: 5px;\n"
"    height: 120px;\n"
"    width: 40px;\n"
"    margin: -30px 0px;\n"
"}")
        self.sliderVolume.setMaximum(100)
        self.sliderVolume.setProperty("value", 50)
        self.sliderVolume.setOrientation(QtCore.Qt.Horizontal)
        self.sliderVolume.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sliderVolume.setTickInterval(25)
        self.sliderVolume.setObjectName("sliderVolume")
        self.labelVolume = QtWidgets.QLabel(self.tab_2)
        
        
        self.labelVolume.setFont(font)
        self.labelVolume.setObjectName("labelVolume")
        self.lcdVolume = QtWidgets.QLCDNumber(self.tab_2)
        
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.lcdVolume.setFont(font)
        self.lcdVolume.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdVolume.setProperty("value", 50.0)
        self.lcdVolume.setObjectName("lcdVolume")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_2)
        
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btnMusica4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica4.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica4.setStyleSheet(btn_style())
        self.btnMusica4.setObjectName("btnMusica4")
        self.gridLayout.addWidget(self.btnMusica4, 0, 1, 1, 1)
        self.btnMusica1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica1.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica1.setStyleSheet(btn_style())
        self.btnMusica1.setObjectName("btnMusica1")
        self.gridLayout.addWidget(self.btnMusica1, 0, 0, 1, 1)
        self.btnMusica6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica6.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica6.setStyleSheet(btn_style())
        self.btnMusica6.setObjectName("btnMusica6")
        self.gridLayout.addWidget(self.btnMusica6, 1, 1, 1, 1)
        self.btnMusica5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica5.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica5.setStyleSheet(btn_style())
        self.btnMusica5.setObjectName("btnMusica5")
        self.gridLayout.addWidget(self.btnMusica5, 1, 0, 1, 1)
        self.btnMusica3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica3.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica3.setStyleSheet(btn_style())
        self.btnMusica3.setObjectName("btnMusica3")
        self.gridLayout.addWidget(self.btnMusica3, 2, 1, 1, 1)
        self.btnMusica2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnMusica2.setEnabled(False)
        self.btnMusica2.setMaximumSize(QtCore.QSize(300, 80))
        self.btnMusica2.setStyleSheet(btn_style())
        self.btnMusica2.setObjectName("btnMusica2")
        self.gridLayout.addWidget(self.btnMusica2, 2, 0, 1, 1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icones/musica.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabsWidget.addTab(self.tab_2, icon2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
       
        

        # Seta a color wheel
       
        #self.img = QImage("wheel.png").mirrored() #inverte a imagem
        self.img = QImage("/usr/share/imagens/wheel.png")
        
        self._img = QImage(1, 1, QImage.Format_ARGB32)
        self.img =self.img.scaled(400, 400, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)        
        pixmap = QtGui.QPixmap(QtGui.QPixmap.fromImage(self.img))       
        self.labelColorWheel = QtWidgets.QLabel(self.tab)
        self.labelColorWheel.setPixmap(pixmap)
        self.labelColorWheel.mouseMoveEvent = self.getPos

        
        self.labelColorWheel.resize(pixmap.width(),pixmap.height())

        #self.labelColorWheel.setObjectName("labelColorWheel")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioButton_6 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_6.setFont(font)
        self.radioButton_6.setObjectName("radioButton_6")
        self.gridLayout_2.addWidget(self.radioButton_6, 3, 2, 1, 1)
        self.radioButton_10 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_10.setFont(font)
        self.radioButton_10.setObjectName("radioButton_10")
        self.gridLayout_2.addWidget(self.radioButton_10, 5, 2, 1, 1)
        self.radioButton_7 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_7.setFont(font)
        self.radioButton_7.setObjectName("radioButton_7")
        self.gridLayout_2.addWidget(self.radioButton_7, 4, 1, 1, 1)
        self.radioButton_9 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_9.setFont(font)
        self.radioButton_9.setObjectName("radioButton_9")
        self.gridLayout_2.addWidget(self.radioButton_9, 5, 1, 1, 1)
        self.radioButton_5 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_5.setFont(font)
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout_2.addWidget(self.radioButton_5, 3, 1, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout_2.addWidget(self.radioButton, 1, 1, 1, 1)
        self.radioButton_8 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_8.setFont(font)
        self.radioButton_8.setObjectName("radioButton_8")
        self.gridLayout_2.addWidget(self.radioButton_8, 4, 2, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout_2.addWidget(self.radioButton_4, 2, 2, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout_2.addWidget(self.radioButton_3, 2, 1, 1, 1)
        self.btnSave = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btnSave.setMinimumSize(QtCore.QSize(0, 80))
        self.btnSave.setStyleSheet(btn_style())
        self.btnSave.setObjectName("btnSave")
        self.btnSave.clicked.connect(self.salvaCena)
        self.gridLayout_2.addWidget(self.btnSave, 6, 1, 1, 2)
        self.cmbIDS = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cmbIDS.setFont(font)
        self.cmbIDS.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.cmbIDS.setObjectName("cmbIDS")
        self.gridLayout_2.addWidget(self.cmbIDS, 0, 1, 1, 2)
        self.radioButton_2 = QtWidgets.QRadioButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout_2.addWidget(self.radioButton_2, 1, 2, 1, 1)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.horizontalLayoutWidget_2)
        self.graphicsView.setStyleSheet("background-color: rgb(85, 170, 127);")
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.graphicsView.setFixedSize(QtCore.QSize(100, 100))
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icones/gears.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabsWidget.addTab(self.tab, icon3, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        
        self.label_2.setObjectName("label_2")
        self.tabsWidget.addTab(self.tab_3, icon, "")

        self.retranslateUi(MainWindow)
        self.tabsWidget.setCurrentIndex(0)
        self.cmbIDS.setCurrentIndex(1)
        self.cmbIDS.highlighted[int].connect(self.mudouControlador)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ########
        self.sliderVolume.sliderMoved.connect(self.setVolume)
        self.sliderVolume.valueChanged.connect(self.changeValue)
        self.btnMusica1.clicked.connect(self.tocaMusicaMpb)
        self.btnMusica2.clicked.connect(self.tocaMusicaClass)
        self.btnMusica3.clicked.connect(self.popup)
        self.btnMusica4.clicked.connect(self.tocaMusicaGospel)
        self.btnMusica5.clicked.connect(self.tocaMusicaClass)
        self.btnMusica6.clicked.connect(self.tocaMusicaCatolica)

        self.setupCmbIDS()
        self.btnArrowLeft_2.clicked.connect(self.moveEsq)
        self.btnArrowRight.clicked.connect(self.moveDir)
        self.tabsWidget.setIconSize(QtCore.QSize(35, 35))
        ''' SET GEOMETRY'''
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 30, 941, 361))
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(630, 70, 281, 441))
        #COLOR PICKER
        self.labelColorWheel.setGeometry(QtCore.QRect(80, 30, 400, 400))
        
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(160, 450, 251, 73))
        #BOTÃO DE SELEÇÃO DAS CENAS
        self.conteiner_bnt_cenas.setGeometry(QtCore.QRect(24, 475, 941, 50))
        #LABEL COM IMAGEM DAS CENAS
        self.label_3.setGeometry(QtCore.QRect(0, 0, 1005, 472))
        self.label2_img = QImage("logo.jpg")

        label_pixmap = QtGui.QPixmap(QtGui.QPixmap.fromImage(self.label2_img))
##            pixmap = pixmap.scaled(900, 350, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        label_pixmap = label_pixmap.scaled(1100, 350)
        self.label_2.setPixmap(label_pixmap)
        
        self.label_2.setGeometry(QtCore.QRect(0, 0, 1005, 400))
        self.lcdVolume.setGeometry(QtCore.QRect(830, 420, 131, 101))
        self.labelVolume.setGeometry(QtCore.QRect(40, 440, 141, 61))
        self.sliderVolume.setGeometry(QtCore.QRect(200, 410, 400, 131))
        self.tabsWidget.setGeometry(QtCore.QRect(6, 9, 1010, 585))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("Vilatec app")
        self.tabsWidget.setWhatsThis("<html><head/><body><p>Aba &quot;sobre&quot; explicando o que é a empresa.</p></body></html>")
        self.btnArrowLeft_2.setText("<")
        self.btnSelectImage.setText("Selecionar")
        self.btnArrowRight.setText(">")
       
        self.label_noImage.setText("")
        self.im = QImage("/usr/share/imagem1.jpg")
        pixmap = QtGui.QPixmap(QtGui.QPixmap.fromImage(self.im))        
               
        if pixmap.width() < 1 and pixmap.height() < 1:
                
                self.label_noImage.setText('Scenário '+str(imgIndex))
                pixmap = pixmap.scaled(1, 1)
                self.label_3.setPixmap(pixmap)
            

        else:
            self.label_noImage.setText('')
            pixmap = pixmap.scaled(1005, 472)
            self.label_3.setPixmap(pixmap)
            
            

        self.tabsWidget.setTabText(self.tabsWidget.indexOf(self.tab_1), "Iluminação")
        self.labelVolume.setText("Volume:")
        self.btnMusica4.setText("GOSPEL")
        self.btnMusica1.setText("MPB")
        self.btnMusica6.setText("CATÓLICAS")
        self.btnMusica5.setText("CLÁSSICAS")
        self.btnMusica3.setText("NATUREZA")
        self.btnMusica2.setText("OUTRAS")        
        self.tabsWidget.setTabText(self.tabsWidget.indexOf(self.tab_2), "Músicas")
        self.radioButton_6.setText("Cena 6")
        self.radioButton_10.setText("Cena 10")
        self.radioButton_7.setText("Cena 7")
        self.radioButton_9.setText("Cena 9")
        self.radioButton_5.setText("Cena 5")
        self.radioButton.setText("Cena 1")
        self.radioButton_8.setText("Cena 8")
        self.radioButton_4.setText("Cena 4")
        self.radioButton_3.setText("Cena 3")
        self.btnSave.setText("Salvar")
        self.radioButton_2.setText("Cena 2")
        self.label.setText("(Red, Green, Blue)")
        self.tabsWidget.setTabText(self.tabsWidget.indexOf(self.tab), "Ajustes")
        
##        self.label_2.setText("<html><head/><body><p><img src=\":/icones/logo.jpg\"/></p></body></html>")
        self.tabsWidget.setTabText(self.tabsWidget.indexOf(self.tab_3), "Sobre")
        self.radioButton.toggled.connect(self.mudouCena)
        self.radioButton_2.toggled.connect(self.mudouCena)
        self.radioButton_3.toggled.connect(self.mudouCena)
        self.radioButton_4.toggled.connect(self.mudouCena)
        self.radioButton_5.toggled.connect(self.mudouCena)
        self.radioButton_6.toggled.connect(self.mudouCena)
        self.radioButton_7.toggled.connect(self.mudouCena)
        self.radioButton_8.toggled.connect(self.mudouCena)
        self.radioButton_9.toggled.connect(self.mudouCena)
        self.radioButton_10.toggled.connect(self.mudouCena)





    def mudouControlador(self, index):
        '''SETA O INDICE DO CONTROLADOR'''
        global Controlador
        Controlador = index + 1

    def moveDir(self):
        global imgIndex
        if(imgIndex < 10):
            imgIndex = imgIndex + 1
            self.mudaImagem()
            try:
                  with open('./CENAS/CENA'+str(imgIndex)+'.txt') as f:
                      line = f.readlines()
                      for self.itens in line:
                           p = subprocess.Popen(self.itens, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                close_fds=False)
                         
##                         self.thread = Thread(itens,"")
##                         self.thread.start()
            except FileNotFoundError:
               buttonReply = QMessageBox.question(self, "Cena "+str(imgIndex)+ ' está sem dados',\
               "Deseja Configurar?" , QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
               if buttonReply == QMessageBox.Yes:
                    self.tabsWidget.setCurrentIndex(2)
                    
                  

            
        print(imgIndex)
        
    def moveEsq(self):
        global imgIndex
        if(imgIndex > 1):
            imgIndex = imgIndex - 1
            self.mudaImagem()
            try:
                  with open('./CENAS/CENA'+str(imgIndex)+'.txt') as f:
                      line = f.readlines()
                      print(line)
                      for self.itens in line:
                         p = subprocess.Popen(self.itens, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           close_fds=False)
##                         self.thread = Thread(itens,"")
##                         self.thread.start()
                         
            except FileNotFoundError:
               buttonReply = QMessageBox.question(self, '  BD não encontrado',\
               "Cena"+str(imgIndex+1)+ ' está sem dados' , QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
               if buttonReply == QMessageBox.Yes:
                    pass
               
        print(imgIndex)

    def mudaImagem(self):
        _translate = QtCore.QCoreApplication.translate        
        try:
            self.im = QImage("/usr/share/imagem" + str(imgIndex) + ".jpg")           

            pixmap = QtGui.QPixmap(QtGui.QPixmap.fromImage(self.im))
            
            if pixmap.width() < 1 and pixmap.height() < 1:
                
                self.label_noImage.setText('Scenário '+str(imgIndex))
                pixmap = pixmap.scaled(1, 1)
                self.label_3.setPixmap(pixmap)            

            else:
                self.label_noImage.setText('')
                pixmap = pixmap.scaled(1005, 472)
                self.label_3.setPixmap(pixmap)
             
            
        except Exception as e:
            print(e)


    def mudouCena(self, param):
        global Cena
        Cena = -1        
        if(self.radioButton.isChecked()):
            Cena = 1
        elif(self.radioButton_2.isChecked()):
            Cena = 2
        elif(self.radioButton_3.isChecked()):
            Cena = 3
        elif(self.radioButton_4.isChecked()):
            Cena = 4
        elif(self.radioButton_5.isChecked()):
            Cena = 5
        elif(self.radioButton_6.isChecked()):
            Cena = 6
        elif(self.radioButton_7.isChecked()):
            Cena = 7
        elif(self.radioButton_8.isChecked()):
            Cena = 8
        elif(self.radioButton_9.isChecked()):
            Cena = 9
        elif(self.radioButton_10.isChecked()):
            Cena = 10
        else:
            Cena = -1
        
##        print("O RB marcado eh: " + str(Cena))

    def tocaMusicaClass(self):
        pygame.mixer.music.load('./musicas/clasicas.mp3')
        pygame.mixer.music.play(-1)  # 0 - toca uma vez, -1 - toca infinitamente em loop


    def tocaMusicaMpb(self):
        pygame.mixer.music.load('./musicas/mpb.mp3')
        pygame.mixer.music.play(-1)  # 0 - toca uma vez, -1 - toca infinitamente em loop

    def tocaMusicaGospel(self):
        pygame.mixer.music.load('./musicas/gospel.mp3')
        pygame.mixer.music.play(-1)  # 0 - toca uma vez, -1 - toca infinitamente em loop


    def tocaMusicaCatolica(self):
        pygame.mixer.music.load('./musicas/catolicas.mp3')
        pygame.mixer.music.play(-1)  # 0 - toca uma vez, -1 - toca infinitamente em loop

    def tocaSomChuva(self):
        pygame.mixer.music.load('./musicas/chuva.mp3')
        pygame.mixer.music.play(-1)

    def tocaSomCachoeira(self):
        pygame.mixer.music.load('./musicas/cachoeira.mp3')
        pygame.mixer.music.play(-1)

    def tocaSomPassaros(self):
        pygame.mixer.music.load('./musicas/passaros.mp3')
        pygame.mixer.music.play(-1)

    def tocaSomMar(self):
        pygame.mixer.music.load('./musicas/mar.mp3')
        pygame.mixer.music.play(-1)

    def setVolume(self):
        pygame.mixer.music.set_volume(self.sliderVolume.value() / 100)

    def changeValue(self):
        valor = self.sliderVolume.value()
        self.lcdVolume.setProperty("value", valor)

    def popup(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('Seletor - Sons de Natureza')
        msgBox.setIconPixmap(QPixmap('./img/bannerpopup2.png'))
        #msgBox.setText('<h3>Escolha abaixo o tipo de som que você gostaria de ouvir</h3>') ## SEM TEXTO, SE USAR IMAGEM
        bt1   = QPushButton('CACHOEIRA')
        bt1.setStyleSheet(btn_style())
        bt1.setMinimumWidth(180)
        bt1.setMaximumWidth(180)
        bt1.setMinimumHeight(80)
        bt1.clicked.connect(self.tocaSomCachoeira)
        msgBox.addButton(bt1, QMessageBox.YesRole)
        bt2   = QPushButton('PÁSSAROS')
        bt2.setStyleSheet(btn_style())
        bt2.setMinimumWidth(180)
        bt2.setMaximumWidth(180)
        bt2.setMinimumHeight(80)
        bt2.clicked.connect(self.tocaSomPassaros)
        msgBox.addButton(bt2, QMessageBox.YesRole)
        bt3   = QPushButton('CHUVA')
        bt3.setStyleSheet(btn_style())
        bt3.setMinimumWidth(180)
        bt3.setMaximumWidth(180)
        bt3.setMinimumHeight(80)
        bt3.clicked.connect(self.tocaSomChuva)
        msgBox.addButton(bt3, QMessageBox.YesRole)
        bt4   = QPushButton('MAR / PRAIA')
        bt4.setStyleSheet(btn_style())
        bt4.setMinimumWidth(180)
        bt4.setMaximumWidth(180)
        bt4.setMinimumHeight(80)
        bt4.clicked.connect(self.tocaSomMar)
        msgBox.addButton(bt4, QMessageBox.NoRole)
        # bt5   = QPushButton('SAIR')
        # bt5.setStyleSheet(btn_style())
        # msgBox.addButton(bt5, QMessageBox.NoRole)
        ret = msgBox.exec_()

    def recurring_timer(self):
        ''' SÓ PROCESSA O COLOR PICKER SE FOR VERDADEIRO '''
        
        global picker
        if picker:
            picker = False

        else:
            picker = True
            

    def setupCmbIDS(self):
        list = find_from_prompt()
        if list:
            for item in list:
                self.cmbIDS.addItem(item[0])
                
##            for item in list:
##                self.cmbIDS.addItem(item['id'])

        else:
            buttonReply = QMessageBox.question(self, 'Nenhum controlador encontrado',\
                "Tentar novamente", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                while not list:
                     list = find_from_prompt()
                     if list:
                        for item in list:
                           self.cmbIDS.addItem(item[0])
                     else:
                          buttonReply = QMessageBox.question(self, 'Nenhum controlador encontrado',\
                          "Tentar novamente", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                          if buttonReply == QMessageBox.Yes:
                                pass
            else:
               print('No clicked.')            
        
            

    def change_cmbIDS(self, ids):
         pass
##        ''' Função chamada pela thread na função: def setupCmbIDS(self): '''
##        cmd="flux_led -s"
##        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
##                      close_fds=False)
##        print(p.stdout.read()) #show response in 'status
##          
##        if ids !='a':
##            print("veio")
##            list = json.loads(ids) #converte a string ids em lista
##            self.cmbIDS.addItem(list['id'])
            
##
##        else:
##            buttonReply = QMessageBox.question(self, 'Erro',\
##                "Nenhum controlador encontrado\n       Tentar novamente?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
##            if buttonReply == QMessageBox.Yes:
##                '''Chama a thread novamente para buscar bulbs'''
##                self.thread = Thread("list","")          
##                self.thread.tempSignal.connect(self.change_cmbIDS)
##                self.thread.start()
##            else:
##                self.thread = Thread("list","")          
##                self.thread.tempSignal.connect(self.change_cmbIDS)
        
##            print(json.loads(cor))
##                self.graphicsView.setStyleSheet("background-color:rgb"+cor)
##                self.label.setText(str(cor))

    def responseThread(self,data):
        ''' Função chamada pela thread na função: a definir: def salvaCena(self):'''
        
        global cor
        print("desativar esse print")
##        try:
####            if contador == 1:                
##                ctrl = json.loads(data)# converte a string em dicionario
##                if ctrl != None:
##                    action(False,ctrl['id'],cor,255)
##                    #print("ctrl")
##                    #print(ctrl)
##                    
                    
##        except:
##            pass


        
##        ctrl = self.cmbIDS.currentText()
##        if ctrl != None:
##            action(False,ctrl,cor,255)
##            print(ctrl)        
        
##            print(json.loads(cor))
##                self.graphicsView.setStyleSheet("background-color:rgb"+cor)
##                self.label.setText(str(cor))
    def salvaCena(self):
        global bulb_info_list
        global Cena
        global cor
        global Controlador
        CONTROLADOR = Controlador -1
        
##        print(Cena, len(bulb_info_list), Controlador)
        
        ip = str(bulb_info_list[CONTROLADOR] [1])
        cmd="flux_led -c " + cor +' '+ip
        try:
             with open('./CENAS/CENA'+str(Cena)+'.txt') as f:
                 line = f.readlines()
                 line[Controlador] = line[CONTROLADOR].replace(line[CONTROLADOR], cmd +'\n')
                
                 
                 
             with open('./CENAS/CENA'+str(Cena)+'.txt', "w") as f:
                  f.writelines(line)
##                 f.write(line)
                     
        except FileNotFoundError:
             if os.path.exists('./CENAS') == False:
                  os.mkdir('./CENAS')
             time.sleep(1)
                  
             with open('./CENAS/CENA'+str(Cena)+'.txt', 'w') as f:
                 
                 for i in range(0, total_de_controladores +1):
                     '''se não tiver arquivo grava 5 x a mesma cor'''
                     f.write(cmd+'\n')
                     
##        self.thread = Thread(cmd,"")
##        self.thread.start()
        
##        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
##                             close_fds=False)

##        for value in range(100):
##             
##             cor = str(value)+',0,0'
##             print(value)
##             cmd="flux_led -c " + cor +' '+ip
##             self.thread = Thread(cmd,"")          
##     ##        self.thread.tempSignal.connect(self.change_cmbIDS)
##             self.thread.start()
        
        

        


            
    def getPos(self , event):        
            
        global picker
        global cor
        if picker:
            try:

                    centerX = 200
                    centerY = 200
                    radius = 200                    
                    x = event.pos().x()
                    y = event.pos().y()
                    position = sqrt((x - centerX)**2 + (y - centerY)**2)
                    c = self.img.pixel(x,y)  # color code (integer): 3235912
                    # depending on what kind of value you like (arbitary examples)
                    c_qobj = QColor(c)  # color object
                    c_rgb = str(QColor(c).getRgb())  # 8bit RGBA: (255, 23, 0, 255)
##                    print( x, y, c_rgb)
                    if (position < radius):
                        
                        cor = c_rgb
                        cor = cor.replace('(',"").replace(")","").replace(" ","")
                        cor = cor[:-4]
                        self.graphicsView.setStyleSheet("background-color:rgb"+c_rgb)
                        self.label.setText(cor)
                        global bulb_info_list
                        global Cena
                        global cor
                        global Controlador
                       
                        print(Cena, len(bulb_info_list), Controlador)
                       
                        ip = str(bulb_info_list[Controlador -1][1])
                        self.cmd="flux_led -c " + cor +' '+ip
                        p = subprocess.Popen(self.cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           close_fds=False)
               
                 


##
            except Exception as e:
                print(e)

        picker = False
        



import images_rc



class Thread(QtCore.QThread):
##    tempSignal = QtCore.pyqtSignal(str)
    
    def __init__(self, cmd, cor,   parent=None):
        super(Thread, self).__init__(parent=parent)
        self.cmd = cmd
##        self.ip = ip
        
    def run(self):
     global bulb_info_list    
     p = subprocess.Popen(self.cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                 close_fds=False)
##     print(p.stdout.read()) #show response in 'status

##class Thread(QtCore.QThread):
##    tempSignal = QtCore.pyqtSignal(str)
##    
##    def __init__(self, x, liga_bulbs, parent=None):
##        super(Thread, self).__init__(parent=parent)
##        self.x = x
##        self.liga_bulbs = liga_bulbs
##        
##    def run(self):
##        global bulb_info_list
##        try:           
##            if self.x == "list":
##                '''ATUALIZA O cmbIDS'''
##                self.list = findControllers()                
##                if self.list:
##                    
####                    data2 = [{'ipaddr': '192.168.43.102', 'model': 'AK001-ZJ200', 'id': '600194ACFBC4'},\
####                             {'ipaddr': '192.168.43.102', 'model': 'AK001-ZJ200', 'id': '600194ACsdas'},\
####                             {'ipaddr': '192.168.43.102', 'model': 'AK001-ZJ200', 'id': '608194ACsdas'},\
####                             {'ipaddr': '192.168.43.102', 'model': 'AK001-ZJ200', 'id': '208194ACsdas'},\
####                             {'ipaddr': '192.168.43.102', 'model': 'AK001-ZJ200', 'id': '638194ACsdas'},\
####                             {'ipaddr': '192.168.43.102', 'model': 'AK001-ZJ200', 'id': '600194Assdas'}]
####                    list = data2                    
##                    
##                    try:                        
##                         file = open('bulbs.txt', 'r')
##                         content = file.readlines()
##                         file.close()
##                        
##                        
##                        
##                         for line1 in content:
##                            line1 = line1.rstrip('\r\n')
##                            #print(line1)
##                            try:
##                                line1 = json.loads(line1)# converte a string em dicionario
##                            except:
##                                pass
##                            list_line = 0
##                            
##                            
##                            for line2 in self.list:
####                                line2 = json.dumps(line2)# converte a lista em string
##                                list_line = list_line + 1                                
##                                try:
##                                    if line1['id'] == line2['id']:
##                                        
##                                        del self.list[list_line -1]#se conter a id no arquivo, exclui da lista
##                                    
##                                except:
##                                    pass                            
##                                                           
##                         
##                         if len(self.list) > 0:
##                                 '''COPIA NOVOS BULBS SE EXISTIR'''
##                                 #print("list data")
##                                 with open('bulbs.txt', 'a') as f:                                
##                                     for itens in self.list:                                
##                                         a = itens
##                                         a = json.dumps(a)# converte a lista em string                                                                       
##                                         f.write(a +'\n')
##
##                         bulbs = ""
##                         with open('bulbs.txt', 'r') as f:
##                                 bulbs = f.readlines()
##                                 
##                         print(bulbs)       
##                         for itens in bulbs:                              
##                                a = itens
##                                
##                                a = a.rstrip('\r\n')                     
##                                
##                                self.tempSignal.emit(a)
####                                b = json.loads(b)# converte a string em lista 
####                                bulb_info_list.append(b)
####                                
####                                BULB.append(WifiLedBulb(b['ipaddr'])) #PARA SENTENCIAR O BULB APENAS UMA VEZ                                
####                                BULB[COUNTER].refreshState()                                
####                                COUNTER = COUNTER + 1
##                                
##                         COUNTER = 0
##                         for itens in bulbs:                              
##                                a = itens                                
##                                a = a.rstrip('\r\n')                     
##                                b = a                                
##                                b = json.loads(b)# converte a string em lista 
##                                bulb_info_list.append(b)                                
##                                BULB.append(WifiLedBulb(b['ipaddr'])) #PARA SENTENCIAR O BULB APENAS UMA VEZ                                
##                                BULB[COUNTER].refreshState()                                
##                                COUNTER = COUNTER + 1
##                                
##                                      
##
##                         
####                        
##                    except FileNotFoundError:
##                        with open('bulbs.txt', 'w') as f:                                
##                                for itens in self.list:                                
##                                    a = itens
##                                    a = json.dumps(a)# converte a lista em string                                                                       
##                                    f.write(a+'\n')
##
##                        with open('bulbs.txt', 'r') as f:
##                                bulbs = f.readlines()
##                                for itens in bulbs:                               
##                                    a = itens
##                                    a = a.rstrip('\r\n')
##        ##                            a = json.loads(a)# converte a lista em string
##                                    self.tempSignal.emit(a)
##                                    a = json.loads(a)# converte a lista em string                            
##                                    bulb_info_list.append(a)
##                                    
##                    
##                                  
##                        
##                        
####                else:
####                    self.tempSignal.emit("a")
##                    
##        
####            self.tempSignal.emit(self.x)
####            print("*************************************"+str(self.liga_bulbs))
##            if len(self.liga_bulbs) > 10:
##                '''Liga todos bulbos armazenados no arquivo'''
##                global cor
##                try:
##                    
##                    
##                    ctrl = json.loads(self.liga_bulbs)# converte a string em dicionario
##                    #print("*************************************"+str(ctrl))
##                    if len(ctrl) > 0:
####                        action(False,ctrl['id'],cor,255)
####                        action(multiple, id, color, intensity)
##                        color = cor
##                        multiple = False
##                        id = ctrl['id']
##                        intensity = 255
##                        
##                        
##                        global previousColor
##                        global previousID
##                        try:
##                          #print("\n==================================")
##                          #print(" DEBUG INFORMATION")
##                          #print("==================================")
##                          #print("Multiple: "   + str(multiple))
##                          #print("id: "         + id)
##                          #print("Color: "      + color)
##                          #print("intensity: "  + str(intensity))
##                          #print("==================================\n")
##
##                          # Remove os caracteres ( ) e remove os espacos no texto
##                          color = color.replace('(',"").replace(")","").replace(" ","")
##                          # So altera a cor caso ela seja diferente
##                          #print(color)
##                          if (color != previousColor or id != previousID):
##                            previousColor = color
##                            previousID    = id
##                            colorList     = color.split(',')
##
##                            #print(colorList)
##
##                            if(multiple == True):
##                              print("Looking for bulbs...")
##                              for bulb_info in bulb_info_list:
##                                if bulb_info:
##                                    bulb = WifiLedBulb(bulb_info['ipaddr'])
##                                    bulb.refreshState()
##
##                                    r = int(colorList[0])
##                                    g = int(colorList[1])
##                                    b = int(colorList[2])
##
##                                    print(bulb_info['ipaddr'] + " (Red: " + str(r) + " ,Green: "+ str(g) +" ,Blue: "+ str(b) + ")")
##                                    if(int(intensity) > 0):
##                                      bulb.setRgb(r,g,b, persist=True, brightness=intensity)
##                                    else:
##                                      bulb.setRgb(r,g,b, persist=True)
##
##                                else:
##                                    #print("Couldn't find the " + id + " bulb")
##                                    pass
##                            else:
##                                   #print("Specific bulb...")
##
##                                   # Itera pelo lista de lampadas até encontrar uma com o ip específico.
##                                   
##                                   COUNTER = 0
##                                   if bulb_info_list:                
##                                         for i in bulb_info_list:
##                                             if(i['id'] == id):
##                                               bulb = BULB[COUNTER]                                              
####                                               print("BULB ENCONTRADO")
####                                               print(bulb)
##                                               break
##                                             COUNTER = COUNTER +1
##                                         
##                                         #bulb_info = scanner.getBulbInfoByID(id)
##                                         #print("bulb")
##                                         #print(bulb)
##                                         if bulb:
##                                             r = int(colorList[0])
##                                             g = int(colorList[1])
##                                             b = int(colorList[2])
##
##                                             #print(bulb_info['ipaddr'] + " (Red: " + str(r) + " ,Green: "+ str(g) +" ,Blue: "+ str(b) + ")")
##                                             if(int(intensity) > 0):
##                                                 bulb.setRgb(r,g,b, persist=True, brightness=intensity)
##                                             else:
##                                                 bulb.setRgb(r,g,b, persist=True)
##
####                                           for i in bulb_info_list:
####                                             if(i['id'] == id):
####                                               bulb_info = i
####                                               print("bulb_info")
####                                               print(bulb_info)
####                                               break         
##                                                 
####                                         bulb = bulb_info['ipaddr']
####                                         print("bulb_info agora" + str(bulb))
####                                         if bulb:
####                                             r = int(colorList[0])
####                                             g = int(colorList[1])
####                                             b = int(colorList[2])
####
####                                             #print(bulb_info['ipaddr'] + " (Red: " + str(r) + " ,Green: "+ str(g) +" ,Blue: "+ str(b) + ")")
####                                             if(int(intensity) > 0):
####                                                 bulb.setRgb(r,g,b, persist=True, brightness=intensity)
####                                             else:
####                                                 bulb.setRgb(r,g,b, persist=True)
##                        except Exception as e:
##                            print(e)
##
##
##
##                        
##                        
##                except:
##                            pass
##
##           
##            
##        except Exception as e:
##            print(e)
##            


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        pygame.init()

##        self.ui = Ui_MainWindow()
        self.setupUi(self)

        self.timer = QTimer()
        self.timer.setInterval(50)       
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        vbox = QVBoxLayout()
        self.setLayout(vbox)
##        self.showFullScreen()
        
        self.show()
        
if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
       app = QtWidgets.QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))
        

w = MainWindow()
w.show()
sys.exit(app.exec_())
>>>>>>> 965d32fb01a8fb59d39c74783db5e79ec77f5465
