import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

# Define the CNN model
def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(3, activation='softmax')  # Assuming 10 different food types
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Load and preprocess the data
def load_data():
    train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1./255)

    training_set = train_datagen.flow_from_directory('dataset/training_set', target_size=(64, 64), batch_size=32, class_mode='categorical')
    test_set = train_datagen.flow_from_directory('dataset/training_set', target_size=(64, 64), batch_size=32, class_mode='categorical')
    
    return training_set, test_set

# Train the model
def train_model(model, training_set, test_set):
    model.fit(training_set, steps_per_epoch=8000//32, epochs=25, validation_data=test_set, validation_steps=2000//32)

# Predict salt content (placeholder function)
def predict_salt_content(food_type):
    salt_content = {
        'food_type_1': 0.5,
        'food_type_2': 1.0,
        # Add salt content for each food type
    }
    return salt_content.get(food_type, 0.0)

# Adjust electrical stimulation based on salt content (placeholder function)
def adjust_stimulation(salt_content):
    if salt_content > 1.0:
        print("High salt content detected. Adjusting stimulation accordingly.")
    else:
        print("Salt content within acceptable range.")

# Main function
if __name__ == "__main__":
    model = create_model()
    training_set, test_set = load_data()
    train_model(model, training_set, test_set)

    # Example prediction
    test_image = tf.keras.preprocessing.image.load_img(r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\dataset\single_prediction\test_image.jpg.jpg", target_size=(64, 64))
    test_image = tf.keras.preprocessing.image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    try:
        result = model.predict(test_image)
        food_type = np.argmax(result)

        # Predict salt content and adjust stimulation
        salt_content = predict_salt_content(food_type)
        adjust_stimulation(salt_content)
    except PermissionError as e:
        print(f"PermissionError: {e}")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")