import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import tensorflow as tf

def display_images(X,y,):
    """
    Display a grid of randomly selected images from the input dataset with their corresponding labels.

    Parameters:
    X (DataFrame): The input dataset of images, where each row represents an image.
    y (DataFrame): The labels corresponding to the input dataset, where each row represents a label.

    Returns:
    None
    """
    m = X.shape[0]

    fig, axes = plt.subplots(6,6, figsize=(16,5))
    fig.tight_layout(pad=0.13,rect=[0, 0.03, 1, 0.91]) #[left, bottom, right, top]
    for i,ax in enumerate(axes.flat):
        # Select random indices
        random_index = np.random.randint(m)

        # Select rows corresponding to the random indices and
        # reshape the image
        X_random_reshaped = X[random_index].reshape(28,28)

        # Display the image
        ax.imshow(X_random_reshaped, cmap='gray')
        
        # Display the label above the image
        ax.set_title(y[random_index,0])
        ax.set_axis_off()
        fig.suptitle("Label, Image", fontsize=14)
    plt.show()

def display_images_true_and_predication(model, X, y, shape):
    """
    Display a grid of randomly selected images from the input dataset with their corresponding true labels and model predictions.

    Parameters:
    model (tensorflow.python.keras.engine.sequential.Sequential): The trained neural network model.
    X (DataFrame): The input dataset of images, where each row represents an image.
    y (DataFrame): The labels corresponding to the input dataset, where each row represents a label.
    shape (tuple): Contains the shape of input image

    Returns:
    None
    """

    m = X.shape[0]

    fig, axes = plt.subplots(6,6, figsize=(16,5))
    fig.tight_layout(pad=0.13,rect=[0, 0.03, 1, 0.91]) #[left, bottom, right, top]

    for i,ax in enumerate(axes.flat):
        # Select random indices
        random_index = np.random.randint(m)

        # Select rows corresponding to the random indices and
        # reshape the image
        X_random_reshaped = X[random_index].reshape(28,28)

        # Display the image
        ax.imshow(X_random_reshaped, cmap='gray')

        # Predict using the Neural Network
        prediction = model.predict(X[random_index].reshape(shape), verbose=0)
        yhat = np.argmax(prediction)

            # Display the label above the image
        ax.set_title(f"{y[random_index,0]},{yhat}",fontsize=10)
        ax.set_axis_off()
        fig.suptitle("Label, yhat", fontsize=14)
        
    plt.show()


def plot_loss_tf(history):
    """
    Plots the loss for training and validation per epochs for a TensorFlow neural network model.

    Parameters:
    history (tensorflow.python.keras.callbacks.History): The history object returned by the `fit()` method of a TensorFlow model.

    Returns:
    None
    """
    fig, ax = plt.subplots(1,1, figsize = (15,6))
    ax.plot(history.history['loss'], label='Training Loss', color='green')
    ax.plot(history.history['val_loss'], label='Validation Loss', color='red')
    ax.set_ylim([0, max(*history.history['loss'], *history.history['val_loss'] )+0.01])
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss (cost)')
    plt.title('Loss per Epoch')
    ax.legend()
    ax.grid(True)
    plt.show()

def plot_accuracy_tf(history):
    """
    Plots the accuracy for training and validation per epochs for a TensorFlow neural network model.

    Parameters:
    history (tensorflow.python.keras.callbacks.History): The history object returned by the `fit()` method of a TensorFlow model.

    Returns:
    None
    """

    fig, ax = plt.subplots(1,1, figsize = (15,6))
    ax.plot(history.history['accuracy'], label='Training Accuracy', color='green')
    ax.plot(history.history['val_accuracy'], label='Validation Accuracy', color='red')
    ax.set_ylim([min(history.history['accuracy'])-0.01, max(*history.history['accuracy'], *history.history['val_accuracy'] )+0.01])
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Accuracy')
    plt.title('Accuracy per Epoch')
    ax.legend()
    ax.grid(True)
    plt.show()

def display_errors(model, X ,y ,shape):
    """
    Display a grid of images that were misclassified by the input model, along with their true labels and predicted labels.

    Parameters:
    model (tensorflow.python.keras.engine.sequential.Sequential): The trained neural network model.
    X (DataFrame): The input dataset of images, where each row represents an image.
    y (DataFrame): The labels corresponding to the input dataset, where each row represents a label.
    shape (tuple): Contains the shape of input image

    Returns:
    None
    """
    p = model.predict(X, verbose=0)
    yhat= [np.argmax(item) for item in p]
    idxs = np.where(yhat != y[:,0])[0]
    if len(idxs) == 0:
        print("no errors found")
    else:
        cnt = min(10, len(idxs))
        fig, ax = plt.subplots(1,cnt, figsize=(16,5))
        fig.tight_layout(pad=0.13,rect=[0, 0.03, 1, 0.91]) #[left, bottom, right, top]
        for i in range(cnt):
            j = idxs[i]
            X_reshaped = X[j].reshape(28,28)

            # Display the image
            ax[i].imshow(X_reshaped, cmap='gray')

            # Predict using the Neural Network
            prediction = model.predict(X[j].reshape(shape), verbose=0)
            yhat = np.argmax(prediction)

            # Display the label above the image
            ax[i].set_title(f"{y[j,0]},{yhat}",fontsize=10)
            ax[i].set_axis_off()
            fig.suptitle("Label, yhat", fontsize=12)
    print(f"{len(idxs)} errors out of {len(X)} images")

def plot_confusion_matrix(model, X_test, y_test, yhat_labels, title):
    """
    Display a grid of images that were misclassified by the input model, along with their true labels and predicted labels.

    Parameters:
    model (tensorflow.python.keras.engine.sequential.Sequential): The trained neural network model.
    X_test (DataFrame): The input dataset of images, where each row represents an image.
    y_test (DataFrame): The labels corresponding to the input dataset, where each row represents a label.
    title (str): the title of the plot

    Returns:
    None
    """
    yhat_labels = [np.argmax(item) for item in model.predict(X_test, verbose=0)]
    conf_matrix = tf.math.confusion_matrix(labels=y_test, predictions=yhat_labels)
    plt.figure(figsize=(15,6))
    sns.heatmap(conf_matrix, annot=True, fmt='d')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(title)
    plt.show()