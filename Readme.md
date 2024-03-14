# Video Stream Application with PyQt5 and OpenCV

This application provides a simple interface for capturing, processing, and saving video streams from a webcam using PyQt5 and OpenCV.

## Usage Instructions

1. Ensure you have Python installed on your system.
2. Install the required dependencies:

pip install PyQt5 opencv-python

3. Run the application:

## Functionality

### Start and Stop Buttons

- Click the **Start** button to begin capturing the video stream from the webcam.
- Click the **Stop** button to pause the video stream.

### Save Button

- Click the **Save** button to save the current frame as an image. You will be prompted to choose the file format (JPEG or PNG) and the location to save the image.

### Image Processing

- Choose from the available image processing methods in the dropdown menu:
- **None**: No processing applied.
- **Grayscale**: Convert the frame to grayscale.
- **Edge Detection**: Detect edges in the frame using the Canny edge detector.
- Adjust the processing parameters using the slider:
- **Threshold**: Adjust the threshold value for edge detection.

### Menu Bar and Toolbar

- The **File** menu in the menu bar provides a **Save** option to save the current frame.
- The toolbar offers quick access to **Start** and **Stop** actions.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
