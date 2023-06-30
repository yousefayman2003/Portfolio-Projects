from tensorflow.keras.models import load_model
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2

def predict_images(model, directory, shape):
    """
    Predict the digit in each PNG image in the input directory using a trained TensorFlow neural network model.

    Parameters:
    model (tensorflow.python.keras.engine.sequential.Sequential): The trained neural network model.
    directory (str): The directory containing the PNG images to be predicted.

    Returns:
    None
    """
    for filename in os.listdir(directory):

        # Check if the file is a PNG image
        if filename.endswith('.png'):

            filepath = os.path.join(directory, filename)
            try:
                # Open the image file 
                img = cv2.imread(filepath)[:,:,0]
                # Invert the pixel values and Scale it
                img = np.invert(np.array([img]))/255

                # Flattening the img pixels
                img = img.reshape(shape)

                # Predicting the img
                prediction = model.predict(img, verbose=0)
                digit = np.argmax(prediction)

                # Plotting the img
                plt.imshow(img.reshape(28,28), cmap='gray')
                plt.title(f'This Digit is {digit} with accuracy {round(np.max(prediction)*100,2)}', fontweight='bold', fontsize=20)
                plt.show(block=False)
                plt.pause(2)
                plt.close()
            except Exception as e:
                print(f'Error processing image {filename}: {e}')

def main():
    """If you want to compare between `CNN` and `ANN` prediction
      you can can change the model_file variable to `ann_model.h5` for ann model
     and `cnn_model.h5` for cnn model
     """
    model_file = 'cnn_model.h5'
    model = load_model(model_file)
    directory = './digits'
    if model_file == 'cnn_model.h5':
        shape = (-1, 28, 28, 1)
    else:
        shape = (-1,784)

    predict_images(model, directory, shape)

if __name__ == '__main__':
    main()
        
