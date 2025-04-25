import os
import shutil
import zipfile
from pathlib import Path

import cv2
import numpy as np
import requests
import tensorflow as tf
from mtcnn import MTCNN
from PIL import Image
from tensorflow.keras import Model, layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator


class FaceRecognitionSystem:
    def __init__(self, input_shape=(160, 160, 3), embedding_size=128):
        self.input_shape = input_shape
        self.embedding_size = embedding_size
        self.detector = MTCNN()
        self.model = self._build_model()
        
    def _build_model(self):
        """Build the face recognition model using MobileNetV2 as backbone"""
        base_model = MobileNetV2(
            input_shape=self.input_shape,
            include_top=False,
            weights='imagenet'
        )
        
        x = base_model.output
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(1024, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        embeddings = layers.Dense(self.embedding_size)(x)
        
        model = Model(inputs=base_model.input, outputs=embeddings)
        return model
    
    def _download_lfw_dataset(self, url="http://vis-www.cs.umass.edu/lfw/lfw.tgz"):
        """Download and extract LFW dataset"""
        dataset_dir = Path("dataset/lfw")
        if not dataset_dir.exists():
            dataset_dir.mkdir(parents=True)
            
            # Download dataset
            print("Downloading LFW dataset...")
            response = requests.get(url, stream=True)
            with open("lfw.tgz", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract dataset
            print("Extracting dataset...")
            shutil.unpack_archive("lfw.tgz", "dataset")
            os.remove("lfw.tgz")
    
    def _preprocess_face(self, image_path):
        """Detect and preprocess face using MTCNN"""
        image = cv2.imread(str(image_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect face
        faces = self.detector.detect_faces(image)
        if not faces:
            return None
            
        # Get the first face
        x, y, w, h = faces[0]['box']
        face = image[y:y+h, x:x+w]
        
        # Resize to input shape
        face = cv2.resize(face, (self.input_shape[0], self.input_shape[1]))
        face = face.astype(np.float32) / 255.0
        
        return face
    
    def _create_triplets(self, dataset_path, num_triplets=1000):
        """Create triplets for training"""
        triplets = []
        people = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
        
        for _ in range(num_triplets):
            # Select anchor person
            anchor_person = np.random.choice(people)
            anchor_images = [f for f in os.listdir(os.path.join(dataset_path, anchor_person)) 
                           if f.endswith(('.jpg', '.png'))]
            
            if len(anchor_images) < 2:
                continue
                
            # Select anchor and positive images
            anchor_img, positive_img = np.random.choice(anchor_images, 2, replace=False)
            
            # Select negative person and image
            negative_person = np.random.choice([p for p in people if p != anchor_person])
            negative_images = [f for f in os.listdir(os.path.join(dataset_path, negative_person))
                             if f.endswith(('.jpg', '.png'))]
            negative_img = np.random.choice(negative_images)
            
            triplets.append((
                os.path.join(dataset_path, anchor_person, anchor_img),
                os.path.join(dataset_path, anchor_person, positive_img),
                os.path.join(dataset_path, negative_person, negative_img)
            ))
            
        return triplets
    
    def triplet_loss(self, y_true, y_pred, alpha=0.2):
        """Triplet loss function"""
        anchor, positive, negative = y_pred[:, 0], y_pred[:, 1], y_pred[:, 2]
        
        pos_dist = tf.reduce_sum(tf.square(anchor - positive), axis=1)
        neg_dist = tf.reduce_sum(tf.square(anchor - negative), axis=1)
        
        basic_loss = pos_dist - neg_dist + alpha
        loss = tf.maximum(basic_loss, 0.0)
        
        return tf.reduce_mean(loss)
    
    def train(self, dataset_path, epochs=10, batch_size=32):
        """Train the face recognition model"""
        # Download dataset if not exists
        self._download_lfw_dataset()
        
        # Create triplets
        triplets = self._create_triplets(dataset_path)
        
        # Prepare data generator
        def triplet_generator():
            while True:
                batch_triplets = np.random.choice(triplets, batch_size)
                batch_anchor = []
                batch_positive = []
                batch_negative = []
                
                for anchor_path, positive_path, negative_path in batch_triplets:
                    anchor = self._preprocess_face(anchor_path)
                    positive = self._preprocess_face(positive_path)
                    negative = self._preprocess_face(negative_path)
                    
                    if anchor is not None and positive is not None and negative is not None:
                        batch_anchor.append(anchor)
                        batch_positive.append(positive)
                        batch_negative.append(negative)
                
                if batch_anchor:
                    yield [np.array(batch_anchor), np.array(batch_positive), np.array(batch_negative)], np.zeros(len(batch_anchor))
        
        # Compile model
        self.model.compile(optimizer='adam', loss=self.triplet_loss)
        
        # Train model
        self.model.fit(
            triplet_generator(),
            steps_per_epoch=len(triplets) // batch_size,
            epochs=epochs
        )
    
    def save_model(self, path):
        """Save the trained model"""
        self.model.save(path)
    
    def load_model(self, path):
        """Load a trained model"""
        self.model = tf.keras.models.load_model(path, custom_objects={'triplet_loss': self.triplet_loss})

if __name__ == "__main__":
    # Initialize and train the face recognition system
    face_recognition = FaceRecognitionSystem()
    face_recognition.train("dataset/lfw")
    face_recognition.save_model("models/face_recognition_model.h5") 