# Arabic Handwritten Digits with Neural Networks
This project uses Artificial Neural Networks (ANN) and Convolutional Neural Networks (CNN) to recognize handwritten digits. The models are trained and evaluated on the Arabic Handwritten Digits dataset, which contains 70,000 images of handwritten digits (60,000 for training and 10,000 for testing) with their corresponding labels you can check the dataset from kaggle from this [link](https://www.kaggle.com/datasets/mloey1/ahdd1). The goal is to train models that can accurately classify new images of handwritten digits.
## Requirements
To run this project, you will need:
-	Python 3.6 or higher
-	Jupyter Notebook
-	TensorFlow 2.0 or higher
-	Pandas
-	NumPy
-	Matplotlib
-	Seaborn
-	scikit-learn
## Installation
To install the required libraries, you can use pip:
`pip install tensorflow pandas numpy matplotlib seaborn scikit-learn`
## Usage
To run the project, you can open the Jupyter Notebook file Notebook.ipynb and run each cell in order. The notebook contains all the code to train and evaluate the ANN and CNN models, as well as some utility functions to visualize the data and the models' performance.
Alternatively, you can run the Python script predict.py to use a trained model to predict the digit in each PNG image in a given directory you can make such images by opening your paint application on your device and making the width of the canvas to be 28 x 28 and then drawing the number then saving it to given directory. You will need to provide the path to the trained model and the directory containing the PNG images to be predicted. You can run the script in the terminal by navigating to the directory containing the script and running the command:
python predict.py
## Files
-	notebook.ipynb: Jupyter Notebook containing the code to train and evaluate the ANN and CNN models.
-	predict.py: Python script to predict the digit in each PNG image in a given directory using a trained model.
-	utils.py: Python module containing utility functions used in the notebook.
- data.zip: Compressed file containing the training and testing datasets in CSV format.
- ann_model.h5: Trained ANN model saved in HDF5 format.
- digits: Directory contains the test images i drawed in paint
- ann_model.h5: Trained ANN model saved in HDF5 format.
- cnn_model.h5: Trained CNN model saved in HDF5 format.
- presentation.pptx: Presentation Of The Project.

## Results
The ANN model achieved an accuracy of 98% on the test dataset, while the CNN model achieved an accuracy of 99%. The CNN model outperformed the ANN model in both accuracy and generalizing well to new examples, indicating that the use of convolutional layers is beneficial for image classification tasks. The models can be used to predict the digit in new images of handwritten digits.
