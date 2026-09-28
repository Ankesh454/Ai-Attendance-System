import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC 
import streamlit as st

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

    return detector,shapePredictor,faceRecog

def get_face_embeddings(image_np):
    detector,shapePredictor,faceRecog = load_dlib_models()
    faces = detector(image_np,1)

    encodings = []

    for face in faces:
        shape = shapePredictor(image_np,face)
        face_descriptor = faceRecog.compute_face_descriptor(image_np,shape,1) #128 embedding

        encodings.append(np.array(face_descriptor))
    return encodings


@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) == 0:
        return 0

    clf = SVC(kernel='linear',probability=True,class_weight='balanced')

    try:
        clf.fit(X,y)
    except ValueError:
        pass

    return {"clf":clf,"X":X,"y":y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):

    encodings = get_face_embeddings(class_image_np)

    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_students, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    resemblance_threshold = 0.6

    for encoding in encodings:

        predicted_student_id = clf.predict([encoding])[0]

        best_distance = float("inf")

        for student_embedding, student_id in zip(X_train, y_train):

            if student_id == predicted_student_id:

                distance = np.linalg.norm(
                    np.array(student_embedding) -
                    np.array(encoding)
                )

                if distance < best_distance:
                    best_distance = distance

        if best_distance <= resemblance_threshold:
            detected_students[int(predicted_student_id)] = True

    return detected_students, all_students, len(encodings)