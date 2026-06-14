import tensorflow as tf
import json

def main():
    print("TensorFlow Version:", tf.__version__)
    
    # 1. Load Training Dataset
    print("Loading training dataset...")
    training_set = tf.keras.utils.image_dataset_from_directory(
        'train',
        labels="inferred",
        label_mode="categorical",
        class_names=None,
        color_mode="rgb",
        batch_size=32,
        image_size=(128, 128),
        shuffle=True,
        seed=None,
        validation_split=None,
        subset=None,
        interpolation="bilinear",
        follow_links=False,
        crop_to_aspect_ratio=False
    )
    
    # 2. Load Validation Dataset
    print("Loading validation dataset...")
    validation_set = tf.keras.utils.image_dataset_from_directory(
        'valid',
        labels="inferred",
        label_mode="categorical",
        class_names=None,
        color_mode="rgb",
        batch_size=32,
        image_size=(128, 128),
        shuffle=True,
        seed=None,
        validation_split=None,
        subset=None,
        interpolation="bilinear",
        follow_links=False,
        crop_to_aspect_ratio=False
    )
    
    # 3. Build the CNN Model
    print("Building model architecture...")
    cnn = tf.keras.models.Sequential()
    
    # Block 1
    cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu', input_shape=[128, 128, 3]))
    cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
    
    # Block 2
    cnn.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
    cnn.add(tf.keras.layers.Conv2D(filters=64, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
    
    # Block 3
    cnn.add(tf.keras.layers.Conv2D(filters=128, kernel_size=3, padding='same', activation='relu'))
    cnn.add(tf.keras.layers.Conv2D(filters=128, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
    
    # Block 4
    cnn.add(tf.keras.layers.Conv2D(filters=256, kernel_size=3, padding='same', activation='relu'))
    cnn.add(tf.keras.layers.Conv2D(filters=256, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
    
    # Block 5
    cnn.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, padding='same', activation='relu'))
    cnn.add(tf.keras.layers.Conv2D(filters=512, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
    
    # Classifier Head
    cnn.add(tf.keras.layers.Dropout(0.25))
    cnn.add(tf.keras.layers.Flatten())
    cnn.add(tf.keras.layers.Dense(units=1500, activation='relu'))
    cnn.add(tf.keras.layers.Dropout(0.4))
    cnn.add(tf.keras.layers.Dense(units=38, activation='softmax'))
    
    # 4. Compile Model
    print("Compiling model...")
    # Using the legacy Adam optimizer for consistency with notebook
    optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=0.0001)
    cnn.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    
    cnn.summary()
    
    # 5. Train Model
    print("Starting training (10 epochs)...")
    training_history = cnn.fit(x=training_set, validation_data=validation_set, epochs=10)
    
    # 6. Evaluate Model
    print("Evaluating model on training set...")
    train_loss, train_acc = cnn.evaluate(training_set)
    print(f"Training accuracy: {train_acc:.4f}, Training loss: {train_loss:.4f}")
    
    print("Evaluating model on validation set...")
    val_loss, val_acc = cnn.evaluate(validation_set)
    print(f"Validation accuracy: {val_acc:.4f}, Validation loss: {val_loss:.4f}")
    
    # 7. Save Model and History
    print("Saving model to 'trained_plant_disease_model.keras'...")
    cnn.save('trained_plant_disease_model.keras')
    
    print("Saving training history to 'training_hist.json'...")
    with open('training_hist.json', 'w') as f:
        json.dump(training_history.history, f)
        
    print("Training process completed successfully!")

if __name__ == '__main__':
    main()
