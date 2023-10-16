import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define your model architecture
model = tf.keras.Sequential([
    # Define your convolutional layers and other layers here
])

# Compile the model with an appropriate loss function and optimizer
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Set up data augmentation and load your dataset using ImageDataGenerator
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    validation_split=0.2  # Split your dataset into training and validation
)

train_generator = train_datagen.flow_from_directory(
    'path/to/training/dataset',
    target_size=(224, 224),  # Adjust to your image size
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    'path/to/training/dataset',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Train the model
model.fit(
    train_generator,
    epochs=10,  # Adjust as needed
    validation_data=validation_generator
)

# Save the trained model for future use
model.save('strawberry_health_model.h5')
