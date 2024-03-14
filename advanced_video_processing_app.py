import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSlider, QFileDialog, QAction, QMenuBar, QToolBar, QSizePolicy, QComboBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize video capture and timer
        self.video_capture = cv2.VideoCapture(0)  # Open default camera
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Set up main window layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Image label to display the video feed
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet("background-color: black;")

        # Buttons for controlling video stream
        self.start_button = QPushButton('Start')
        self.start_button.setFont(QFont("Arial", 12))
        self.start_button.clicked.connect(self.start_video)

        self.stop_button = QPushButton('Stop')
        self.stop_button.setFont(QFont("Arial", 12))
        self.stop_button.clicked.connect(self.stop_video)

        self.save_button = QPushButton('Save')
        self.save_button.setFont(QFont("Arial", 12))
        self.save_button.clicked.connect(self.save_frame)

        # Combo box for selecting image processing methods
        self.processing_combo_box = QComboBox()
        self.processing_combo_box.setFont(QFont("Arial", 12))
        self.processing_combo_box.addItem("None")
        self.processing_combo_box.addItem("Grayscale")
        self.processing_combo_box.addItem("Edge Detection")

        # Slider for adjusting processing parameters
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(100)
        self.threshold_slider.valueChanged.connect(self.update_threshold_label)

        # Label to display current threshold value
        self.threshold_label = QLabel("Threshold: 100")
        self.threshold_label.setFont(QFont("Arial", 12))

        # Set up main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.stop_button)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.processing_combo_box)
        buttons_layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(buttons_layout)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.threshold_label)
        slider_layout.addWidget(self.threshold_slider)
        slider_layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(slider_layout)

        self.central_widget.setLayout(self.layout)

        # Flag to indicate if processing is enabled
        self.is_processing = False

        # Create menu and toolbar
        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        # Create a menu bar with a "File" menu
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')

        # Add a "Save" action to the "File" menu
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_frame)
        file_menu.addAction(save_action)

    def create_toolbar(self):
        # Create a toolbar with "Start" and "Stop" actions
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        start_action = QAction('Start', self)
        start_action.triggered.connect(self.start_video)
        toolbar.addAction(start_action)

        stop_action = QAction('Stop', self)
        stop_action.triggered.connect(self.stop_video)
        toolbar.addAction(stop_action)

    def start_video(self):
        # Start the video stream when the "Start" button is clicked
        if not self.timer.isActive():
            self.timer.start(1000 // 30)  # 30 FPS
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

    def stop_video(self):
        # Stop the video stream when the "Stop" button is clicked
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def save_frame(self):
        # Save the current frame as an image when the "Save" button is clicked
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'JPEG Image (*.jpg);;PNG Image (*.png)')
        if file_path:
            if self.video_capture:
                ret, frame = self.video_capture.read()
                if ret:
                    if self.is_processing:
                        frame = self.process_frame(frame)
                    cv2.imwrite(file_path, frame)

    def update_frame(self):
        # Update the displayed frame from the video stream
        if self.video_capture:
            ret, frame = self.video_capture.read()
            if ret:
                if self.is_processing:
                    frame = self.process_frame(frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap)

    def process_frame(self, frame):
        # Apply selected image processing methods to the frame
        processing_method = self.processing_combo_box.currentText()
        if processing_method == "Grayscale":
            process_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return process_image
        elif processing_method == "Edge Detection":
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            process_image = cv2.Canny(frame_gray, self.threshold_slider.value(), self.threshold_slider.value() * 2)
            return process_image

    def update_threshold_label(self):
        # Update the threshold label when the slider value changes
        self.threshold_label.setText("Threshold: " + str(self.threshold_slider.value()))

    def closeEvent(self, event):
        # Release the video capture when the application is closed
        if self.video_capture and self.video_capture.isOpened():
            self.video_capture.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowTitle('Video Stream with Qt and OpenCV')
    main_window.show()
    sys.exit(app.exec_())
