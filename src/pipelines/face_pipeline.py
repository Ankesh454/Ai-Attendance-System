import dlib
import numpy as np
import face_recognition_models
import streamlit as st
from sklearn.svm import SVC

from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():

    detector = dlib.get_frontal_face_detector()

    shapePredictor = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    faceRecog = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, shapePredictor, faceRecog


def get_face_embeddings(image_np):

    detector, shapePredictor, faceRecog = load_dlib_models()
    faces = detector(image_np, 3)

    encodings = []

    for face in faces:
        shape = shapePredictor(image_np, face)

        face_descriptor = faceRecog.compute_face_descriptor(
            image_np,
            shape,
            3
        )

        encodings.append(np.array(face_descriptor, dtype=np.float32))

    return encodings


@st.cache_resource
def get_trained_model():

    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")

        if embedding:
            X.append(embedding)
            y.append(student.get("student_id"))

    if len(X) == 0:
        return None

    clf = SVC(kernel='linear',probability=True,class_weight="balanced")

    try:
        clf.fit(X,y)
    except ValueError:
        pass

    return {"clf":clf, "X": X, "y": y}


def train_classifier():
    st.cache_resource.clear()

    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):

    encodings = get_face_embeddings(class_image_np)

    detected_students = {}

    model_data = get_trained_model()

    if model_data is None:
        return detected_students, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    resemblance_threshold = 0.5

    for encoding in encodings:
        if len(all_students) >=2:
            probabilities = clf.predict_proba([encoding])[0]
            best_index = np.argmax(probabilities)
            predicted_id = int(clf.classes_[best_index])
            best_probability = probabilities[best_index]
        else:
            predicted_id = int(all_students[0])
            best_probability = 1.0

        student_embedding = X_train[y_train.index(predicted_id)]

        best_match_score = np.linalg.norm(student_embedding - encoding)

        if(best_probability >= 0.80 and best_match_score <= resemblance_threshold):
            detected_students[predicted_id] = True
    
    return detected_students,all_students,len(encodings)
        