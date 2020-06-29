from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, QThreadPool, QObject, QRunnable, pyqtSignal


import time
import sys
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from tester import Tester
from scrapper import Scrapper
from test_data_generator import generate_test_data
from bertTester import BertTester
from bert import Bert
from cnnModel import CnnModel
from dataProcessor import DataProcessor
import traceback, sys


##################################################### STATIC VARIABLES #####################################################
ASSETS_PATH = "./assets"
CLASS_NAMES_CNN=['food and drink', 'entertainment', 'business and industry', 'family and relationships', 'fitness and wellness', 'hobbies and activities', 'shopping and  fashion', 'sports and outdoors', 'technology']
CLASS_NAMES_BERT = ['shopping and  fashion', 'entertainment', 'food and drink', 'hobbies and activities', 'technology', 'business and industry', 'family and relationships', 'fitness and wellness', 'sports and outdoors']
MODEL_PATH_CNN="./models/last_model.h5"   #CHANGE_THIS
MODEL_PATH_BERT="./models/model_all_captions_hashtags_12k.h5" #CHANGE_THIS

##################################################### GLOBAL VARIABLES #####################################################
test_df = None
folder_path = None
dataLoaded = False
bert = None
cnnModelClass = None
cnnModel = None
predictions = [None, None]

##################################################### WORKERS-THREADS #####################################################

class ResultObj(QObject):
    def __init__(self, val):
        self.val = val

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

class Worker(QRunnable):
    def __init__(self, username, threshold):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.signals = WorkerSignals()
        self.username = username
        self.threshold = threshold

    def run(self):
      scrapper=Scrapper()
      global folder_path
      global test_df
      test_df = generate_test_data(self.username, self.threshold)
      folder_path = scrapper.dowload_data(self.username, self.threshold)
      #user_account="skyemcalpine"
      folder_path = folder_path.replace("\\","/")
      print(folder_path)
      self.signals.result.emit(True)

class BertWorker(QRunnable):
    def __init__(self, model_path, class_names):
        super(BertWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.signals = WorkerSignals()
        self.model_path = model_path
        self.class_names = class_names

    def run(self):
      global bert
      bert=Bert(self.model_path, self.class_names)
      bert.load_model()
      print("BERT LOADED")
      self.signals.result.emit(True)

class CnnWorker(QRunnable):
    def __init__(self):
        super(CnnWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.signals = WorkerSignals()

    def run(self):
      global cnnModelClass
      global cnnModel
      cnnModelClass =CnnModel(CLASS_NAMES_CNN, MODEL_PATH_CNN)
      #cnnModel.visualise_data()
      cnnModel = cnnModelClass.load_model()
      print("CNN LOADED")
      self.signals.result.emit(True)

class BertPredictionWorker(QRunnable):
    def __init__(self, username, threshold):
        super(BertPredictionWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.signals = WorkerSignals()
        self.username = username
        self.threshold = threshold

    def run(self):
      global bert
      global test_df
      global predictions
      bertTester=BertTester()
      predictions[0]=bertTester.test_bert(self.username, self.threshold, test_df, bert).flatten()
      self.signals.result.emit(ResultObj(predictions[0]))

class CnnPredictionWorker(QRunnable):
    def __init__(self):
        super(CnnPredictionWorker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.signals = WorkerSignals()

    def run(self):
      tester=Tester()
      predictions, classnames = tester.test(folder_path, cnnModelClass, cnnModel)
      print(predictions)
      print(classnames)
      self.signals.result.emit({'p':predictions, 'c':classnames})

##################################################### MAIN WINDOW #####################################################
class Window(QMainWindow):
    def createTable(self): ######################### CREATE THE TABLE
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Cell (1,2)"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        #self.tableWidget.move(0,0)

    def __init__(self):
        super().__init__()

        # set the title of main window
        self.setWindowTitle('Interest Classifier')

        # set the size of window
        self.Width = 1000
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
		
		    # add all widgets
        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("enter username")
        self.spinBox = QSpinBox(self)
        self.spinBox.setRange(0, 1000)
        self.scrap_btn = QPushButton('scrap data', self)
        self.load_bert_btn = QPushButton('Load Bert', self)
        self.load_cnn_btn = QPushButton('Load VGG16', self)
        self.username_label = QLabel("Username:", self)
        self.threshold_label = QLabel("Number of posts:", self)
        self.load_data_label = QLabel("DATA: NOT LOADED", self)
        self.load_bert_label = QLabel("BERT: NOT LOADED", self)
        self.load_cnn_label = QLabel("CNN: NOT LOADED",self)
        table = "<table>"
        for i in range(9):
          table += "<tr><td></td></tr>"
        table += "</table>"
        self.table = QLabel(table, self)
        self.cnn_btn = QPushButton('CNN Result', self)
        self.bert_btn = QPushButton('Bert Result', self)
        self.label_animation = QLabel(self)
        self.label_animation_cnn = QLabel(self)
        self.label_animation_bert = QLabel(self)

        self.bert_btn.setEnabled(False)
        self.cnn_btn.setEnabled(False)

        self.spinner = QMovie(ASSETS_PATH+'/Rolling-1s-200px_dark.gif')
        self.spinner_cnn = QMovie(ASSETS_PATH+'/Rolling-1s-200px_dark.gif')
        self.spinner_bert = QMovie(ASSETS_PATH+'/Rolling-1s-200px_dark.gif')
        self.label_animation.setMovie(self.spinner)
        self.label_animation_cnn.setMovie(self.spinner_cnn)
        self.label_animation_bert.setMovie(self.spinner_bert)
        self.spinner.setScaledSize(QSize(20, 20))
        self.spinner_cnn.setScaledSize(QSize(20, 20))
        self.spinner_bert.setScaledSize(QSize(20, 20))
        self.createTable()
        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        hbox = QHBoxLayout()
        bert_loader_box = QHBoxLayout()
        cnn_loader_box = QHBoxLayout()

        hbox.addWidget(self.scrap_btn)
        hbox.addWidget(self.load_data_label)
        hbox.addWidget(self.label_animation)
        self.spinner.start()
        #self.label_animation.setStyleSheet("font-size: 0")
        sp_retain = QSizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.label_animation.setSizePolicy(sp_retain)
        self.label_animation.setHidden(True)
        self.label_animation_bert.setSizePolicy(sp_retain)
        self.label_animation_bert.setHidden(True)
        self.label_animation_cnn.setSizePolicy(sp_retain)
        self.label_animation_cnn.setHidden(True)
        



        bert_loader_box = QHBoxLayout()
        bert_loader_box.addWidget(self.load_bert_btn)
        bert_loader_box.addWidget(self.load_bert_label)
        bert_loader_box.addWidget(self.label_animation_bert)
        

        cnn_loader_box = QHBoxLayout()
        cnn_loader_box.addWidget(self.load_cnn_btn)
        cnn_loader_box.addWidget(self.load_cnn_label)
        cnn_loader_box.addWidget(self.label_animation_cnn)
        
        
        left_layout.addWidget(self.username_label)
        left_layout.addWidget(self.textbox)
        left_layout.addWidget(self.threshold_label)
        left_layout.addWidget(self.spinBox)
        #left_layout.addWidget(self.scrap_btn)
        left_layout.addLayout(hbox)
        left_layout.addLayout(cnn_loader_box)
        left_layout.addLayout(bert_loader_box)
        left_layout.addWidget(self.cnn_btn)
        left_layout.addWidget(self.bert_btn)
        left_layout.addWidget(self.table)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.figure = plt.figure(figsize=(15,6))
        self.canvas = FigureCanvas(self.figure)
        #self.figure.set_facecolor((0.20703125, 0.20703125, 0.20703125))
        #self.canvas.setPalette(QPalette(QColor(255,255,255)))
        ax = plt.gca()
        #ax.set_facecolor((0.20703125, 0.20703125, 0.20703125))

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.canvas)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.cnn_data={'foods':20, 'family':15, 'entertainment':30,
        'business':35,'fitness':20, 'hobbies':15, 'shopping':30,
        'sports':35,"technology":75} 
        self.bert_data={'foods':50, 'family':15, 'entertainment':10,
        'business':35,'fitness':40, 'hobbies':15, 'shopping':30,
        'sports':150,"technology":75} 

        self.scrap_btn.clicked.connect(self.scrap_data)
        self.load_bert_btn.clicked.connect(self.load_bert)
        self.load_cnn_btn.clicked.connect(self.load_cnn)
        self.cnn_btn.clicked.connect(lambda:self.cnn_Result(self.cnn_data,"CNN_Classifier")) 
        self.bert_btn.clicked.connect(lambda:self.bert_Result(self.bert_data,"BERT_Classifier"))

    def load_bert(self):
      
      self.start_spinner(self.spinner_bert, self.label_animation_bert)
      worker = BertWorker(str(MODEL_PATH_BERT), CLASS_NAMES_BERT)
      self.threadpool.start(worker)
      worker.signals.result.connect(lambda : (self.load_bert_label.setText("BERT: <b style='color:green'>LOADED</b>"), self.enable_cnn_button("bert"), self.stop_spinner(self.spinner_bert, self.label_animation_bert)))
      print("bert test")

    def setDataLoaded(self):
      global dataLoaded
      dataLoaded = True
      self.load_data_label.setText("DATA: <b style='color:green'>LOADED</b>")

    def load_cnn(self):
      worker = CnnWorker()
      self.start_spinner(self.spinner_cnn, self.label_animation_cnn)
      self.threadpool.start(worker)
      worker.signals.result.connect(lambda : (self.load_cnn_label.setText("CNN: <b style='color:green'>LOADED</b>"), self.enable_cnn_button("cnn"), self.stop_spinner(self.spinner_cnn, self.label_animation_cnn)))

    def start_spinner(self, spinner, animation_label):
      spinner.start()
      animation_label.setHidden(False)
      

    def stop_spinner(self, spinner, animation_label):
      spinner.stop()
      animation_label.setHidden(True)


    def enable_cnn_button(self, type):
      global dataLoaded
      global bert
      if type == "cnn":
        if folder_path and cnnModel:
          self.cnn_btn.setEnabled(True)
      else:
        if (dataLoaded) and (bert!=None):
          self.bert_btn.setEnabled(True) 
      print(dataLoaded)
      print(bert!=None)     


    def scrap_data(self):
      #self.create_bar(self.cnn_data, "test")
      username = str(self.textbox.text())
      threshold = int(self.spinBox.value())
      worker = Worker(username, threshold)
      self.start_spinner(self.spinner, self.label_animation)
      self.threadpool.start(worker)
      worker.signals.result.connect(lambda: (self.stop_spinner(self.spinner, self.label_animation), self.setDataLoaded(), self.enable_cnn_button("cnn"), self.enable_cnn_button("bert")))
      
      """self.spinner.start()
      scrapper=Scrapper()
      username = str(self.textbox.text())
      threshold = 2
      global folder_path
      global test_df
      test_df = generate_test_data(username,threshold)
      folder_path = scrapper.dowload_data(username,threshold)
      #user_account="skyemcalpine"
      folder_path = folder_path.replace("\\","/")
      print(folder_path)
      self.stop_spinner()"""


    def cnn_Result(self, data, title):
      #tester=Tester()
      #predictions, classnames = tester.test(folder_path, cnnModelClass, cnnModel)
      worker = CnnPredictionWorker()
      self.threadpool.start(worker)
      worker.signals.result.connect(lambda x : self.showCnn_Result(x, title))

    def showCnn_Result(self, result, title):
      data={ classname: prediction for classname, prediction in zip(CLASS_NAMES_CNN, result['p'])}
      table = "<table>"
      for key, value in data.items():
        table += "<tr><td>" + str(key) + "</td><td>" + str(value) + "</td></tr>"
      table += "</table>"
      self.table.setText(table) 
      self.create_bar(data,title)


    def bert_Result(self,data,title):
      username = str(self.textbox.text())
      threshold = int(self.spinBox.value())
      #predictions=bertTester.test_bert(username, threshold, test_df, bert).flatten()
      worker = BertPredictionWorker(username, threshold)
      self.threadpool.start(worker)
      worker.signals.result.connect(lambda x : self.showBert_Result(x, title))

    def showBert_Result(self, predictionsObj, title):
      #if predictions[0]:
      #  predictions_bert = predictions[0]
      predictions = predictionsObj.val
      print(predictions)
      data={ classname: prediction for classname, prediction in zip(CLASS_NAMES_BERT, predictions)}
      table = "<table>"
      for key, value in data.items():
        table += "<tr><td>" + str(key) + "</td><td>" + str(value) + "</td></tr>"
      table += "</table>"
      self.table.setText(table) 
      print(data)
      self.create_bar(data,title)
    
    def create_bar(self,data,title):
        data=data 
        courses = list(data.keys()) 
        values = list(data.values()) 
        print(values)
        self.figure.clear()
        plt.xlabel('interests', fontsize=10)
        plt.ylabel('probabilities', fontsize=10)
        plt.bar(courses, values, color ='maroon',  width = 0.3) 
        plt.tick_params(axis='x', which='major', labelsize=7,rotation=20)
        plt.suptitle(title,fontsize=10, color='white')
        plt.tight_layout(70)
        self.canvas.draw()


##################################################### MAIN FUNCTION #####################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    ex = Window()
    ex.show()
    sys.exit(app.exec_())
