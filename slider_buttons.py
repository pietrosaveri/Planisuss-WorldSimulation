import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont

#inizitialize a class for the slider and for the buttons window
class SliderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #set title for main window
        self.setWindowTitle("Edit variables")

        #set size of main window
        self.setGeometry(100, 100, 220, 800)
        
        #set max and min variables of the slider
        min_value_slider = 0
        max_value_slider = 400

        #create a central widget for the window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        #create a layout for the central widget
        layout = QVBoxLayout()

        #create a vertical slider
        self.slider = QSlider(2, self) #2 means vertical

        #set the initial value of the slider to 0
        initial_value = 0
        
        #these are the initial values of the variables in the buttons (the best values that we found to give a balanced simulation)
        self.starting_value_predator = 9
        self.starting_value_herd = 125
        self.starting_value_pride = 287
        self.starting_value_boredom = 4
        self.satrting_value_aging_erb = 10
        self.starting_value_aging_car = 1
        self.starting_value_max_herd = 20
        self.starting_value_max_pride = 50
        
        #set a variable for each button to check if it has been clicked
        self.button1_clicked = False
        self.button2_clicked = False
        self.button3_clicked = False
        self.button4_clicked = False
        self.button5_clicked = False
        self.button6_clicked = False
        self.button7_clicked = False
        self.button8_clicked = False
        
        #setting a minimum and maximum range for the slider 
        self.slider.setMinimum(min_value_slider)
        self.slider.setMaximum(max_value_slider)

        #set the slider to the initial_value variable
        self.slider.setValue(initial_value)

        # when the value of the slider changes, the fucntion update_variable will update self.variable and the text  of the slider
        self.slider.valueChanged.connect(self.update_variable)

        # setup the self.variable to the initial value and create a label object
        self.variable, self.label = initial_value, QLabel(self)
        
        #setup the initial text of the label
        self.text = "insert variable"
        self.label.setText(f"{self.text}: {self.variable}")

        #create a font for the label
        font = QFont()
        font.setPointSize(16) #font size

        #set the font
        self.label.setFont(font)

        #add the slider and label to the layout
        layout.addWidget(self.slider)
        layout.addWidget(self.label)

        #create buttons each with its own name
        self.button1_text = "Predator Advantage"
        self.button2_text = "Max energy erbast"
        self.button3_text = "Max energy carviz"
        self.button4_text = "Boredom"
        self.button5_text = "Aging erbast"
        self.button6_text = "Aging carviz"
        self.button7_text = "Max herd components"
        self.button8_text = "Max pride components"

        #create a button box
        button_box = QVBoxLayout()

        #Create buttons
        self.button1 = QPushButton(self.button1_text, self)
        self.button1.clicked.connect(self.on_button1_click)

        self.button2 = QPushButton(self.button2_text, self)
        self.button2.clicked.connect(self.on_button2_click)

        self.button3 = QPushButton(self.button3_text, self)
        self.button3.clicked.connect(self.on_button3_click)

        self.button4 = QPushButton(self.button4_text, self)
        self.button4.clicked.connect(self.on_button4_click)

        self.button5 = QPushButton(self.button5_text, self)
        self.button5.clicked.connect(self.on_button5_click)

        self.button6 = QPushButton(self.button6_text, self)
        self.button6.clicked.connect(self.on_button6_click)

        self.button7 = QPushButton(self.button7_text, self)
        self.button7.clicked.connect(self.on_button7_click)

        self.button8 = QPushButton(self.button8_text, self)
        self.button8.clicked.connect(self.on_button8_click)

        #add buttons to the button box that is displayed when the program run
        button_box.addWidget(self.button1)
        button_box.addWidget(self.button2)
        button_box.addWidget(self.button3)
        button_box.addWidget(self.button4)
        button_box.addWidget(self.button5)
        button_box.addWidget(self.button6)
        button_box.addWidget(self.button7)
        button_box.addWidget(self.button8)

        #add the button box to the layout
        layout.addLayout(button_box)

        #set the layout for the central widget
        central_widget.setLayout(layout)


    def update_variable(self):
        #function used to update not only the text but also the self.variable as the slider is changing
        self.variable = self.slider.value()
        self.label.setText(f"{self.text}: {self.variable}")

    def on_button1_click(self):
        #button for the PREDATOR_ADVANTAGE variable

        if not self.button1_clicked:
            #the first time the button is clicked, it automatically sets to our suggeted value
            self.text = self.button1_text
            self.label.setText(f"{self.text}: {self.starting_value_predator}")
            self.slider.setValue(self.starting_value_predator)
            self.button1_clicked = True  # Set the flag to True after the first click
        else:
            #from the second time the button is clicked, the value is not set automatically
            self.text = self.button1_text
            self.label.setText(f"{self.text}: {self.variable}")

    def on_button2_click(self):
        #button for the MAX_EN_HERD variable

        if not self.button2_clicked:
            #the first time the button is clicked, it automatically sets to our suggeted value
            
            self.text = self.button2_text
            self.label.setText(f"{self.text}: {self.starting_value_herd}")
            self.slider.setValue(self.starting_value_herd)
            self.button2_clicked = True
        else:
            #from the second time the button is clicked, the value is not set automatically
            self.text = self.button2_text
            self.label.setText(f"{self.text}: {self.variable}")

    def on_button3_click(self):
        #button for the MAX_EN_PRIDE variable

        if not self.button3_clicked:
            #the first time the button is clicked, it automatically sets to our suggeted value
            self.text = self.button3_text
            self.label.setText(f"{self.text}: {self.starting_value_pride}")
            self.slider.setValue(self.starting_value_pride)
            self.button3_clicked = True
        else:
            #from the second time the button is clicked, the value is not set automatically
            self.text = self.button3_text
            self.label.setText(f"{self.text}: {self.variable}")

    def on_button4_click(self):
        #button for the BOREDOM variable

        if not self.button4_clicked:
            # the first time the button is clicked, it automatically sets to our suggeted value
            self.text = self.button4_text
            self.label.setText(f"{self.text}: {self.starting_value_boredom}")
            self.slider.setValue(self.starting_value_boredom)
            self.button4_clicked = True
        else:
            #from the second time the button is clicked, the value is not set automatically
            self.text = self.button4_text
            self.label.setText(f"{self.text}: {self.variable}")

    def on_button5_click(self):
        #button for the AGING_ERB variable
        
        if not self.button5_clicked:
            #the first time the button is clicked, it automatically sets to our suggeted value
            self.text = self.button5_text
            self.label.setText(f"{self.text}: {self.satrting_value_aging_erb}")
            self.slider.setValue(self.satrting_value_aging_erb)
            self.button5_clicked = True
        else:
            #from the second time the button is clicked, the value is not set automatically
            self.text = self.button5_text
            self.label.setText(f"{self.text}: {self.variable}")

    def on_button6_click(self):
        #button for the AGING_CAR variable
        if not self.button6_clicked:
            #the first time the button is clicked, it automatically sets to our suggeted value
            self.text = self.button6_text
            self.label.setText(f"{self.text}: {self.starting_value_aging_car}")
            self.slider.setValue(self.starting_value_aging_car)
            self.button6_clicked = True
        else:
            # from the second time the button is clicked, the value is not set automatically
            self.text = self.button6_text
            self.label.setText(f"{self.text}: {self.variable}")

    def on_button7_click(self):
        #button for the MAX_HERD variable
        if not self.button7_clicked:
            #the first time the button is clicked, it automatically sets to our suggeted value
            self.text = self.button7_text
            self.label.setText(f"{self.text}: {self.starting_value_max_herd}")
            self.slider.setValue(self.starting_value_max_herd)
            self.button7_clicked = True
        else:
            #from the second time the button is clicked, the value is not set automatically
            self.text = self.button7_text
            self.label.setText(f"{self.text}: {self.variable}")

    def on_button8_click(self):
        #button for the MAX_PRIDE variable

        if not self.button8_clicked:
            #the first time the button is clicked, it automatically sets to our suggeted value
            self.text = self.button8_text
            self.label.setText(f"{self.text}: {self.starting_value_max_pride}")
            self.slider.setValue(self.starting_value_max_pride)
            self.button8_clicked = True
        else:
            #from the second time the button is clicked, the value is not set automatically
            self.text = self.button8_text
            self.label.setText(f"{self.text}: {self.variable}")

    def run(self):
        #funciton to show the main window
        self.show()

    def get_slider_value(self):

        #function used in main_code.py to get the value of the slider
        return self.variable
    
    def get_slider_text(self):

        #function used in main_code.py to get the text of the slider
        return self.text

#start the application to be able to run the window on graphic_portion.py
app = QApplication(sys.argv)

#set the main window
slider_window = SliderWindow()

#uncomment this lines to run the code here, without running the other two files
#slider_window.run()
#sys.exit(app.exec_())
