import sys
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pydub import AudioSegment
import librosa
import soundfile as sf
import noisereduce as nr

class NoiseReducerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Noise Removal & Audio Enhancement")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.uploadButton = QtWidgets.QPushButton("Upload Audio File")
        self.uploadButton.clicked.connect(self.uploadFile)
        layout.addWidget(self.uploadButton)

        self.processButton = QtWidgets.QPushButton("Process Audio")
        self.processButton.clicked.connect(self.processAudio)
        layout.addWidget(self.processButton)

        self.statusLabel = QtWidgets.QLabel("Status: Waiting for file...")
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    def uploadFile(self):
        file_filter = "Audio Files (*.mp3 *.wav *.ogg *.flac)"
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", file_filter)
        if file_name:
            self.audio_path = file_name
            self.statusLabel.setText(f"Selected File: {os.path.basename(file_name)}")

    def processAudio(self):
        if not hasattr(self, 'audio_path'):
            QMessageBox.warning(self, "Error", "Please upload an audio file first!")
            return
        
        self.statusLabel.setText("Processing...")

        y, sr = librosa.load(self.audio_path, sr=None)

        reduced_noise = nr.reduce_noise(y=y, sr=sr)

        output_folder = os.path.join(os.getcwd(), "Enhanced Sounds")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_file = os.path.join(output_folder, "enhanced_audio.wav")
        sf.write(output_file, reduced_noise, sr)

        self.statusLabel.setText("Processing Complete!")
        QMessageBox.information(self, "Success", f"Audio processed and saved in 'Enhanced Sounds' as enhanced_audio.wav")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = NoiseReducerApp()
    window.show()
    sys.exit(app.exec_())
