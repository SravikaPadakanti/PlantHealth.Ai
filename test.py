import numpy as np
import tensorflow as tf
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python test.py <path_to_test_image>")
        print("Example: python test.py test/test/AppleCedarRust1.JPG")
        return
        
    image_path = sys.argv[1]
    
    # 1. Load the labels from the validation folder
    print("Loading class names from validation folder...")
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
    class_names = validation_set.class_names
    
    # 2. Load the trained model
    print("Loading trained model...")
    try:
        model = tf.keras.models.load_model('trained_plant_disease_model.keras')
    except Exception as e:
        print("Error loading model. Make sure you have trained the model first!")
        print(e)
        return
        
    # 3. Preprocess and predict
    print(f"Predicting for image: {image_path}...")
    try:
        image = tf.keras.preprocessing.image.load_img(image_path, target_size=(128, 128))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])  # convert single image to batch
        
        predictions = model.predict(input_arr)
        result_index = np.argmax(predictions)
        
        print("\n=== Prediction Result ===")
        print(f"Predicted Class Index: {result_index}")
        print(f"Predicted Class Label: {class_names[result_index]}")
        print(f"Confidence score: {predictions[0][result_index]:.4f}")
    except Exception as e:
        print("Error reading or processing the image file.")
        print(e)

if __name__ == '__main__':
    main()
