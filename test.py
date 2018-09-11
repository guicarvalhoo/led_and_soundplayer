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
