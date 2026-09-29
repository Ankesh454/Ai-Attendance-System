import dlib
import numpy as np
import face_recognition_models
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

    return detector, shapePredictor, faceRecog


def get_face_embeddings(image_np):

    detector, shapePredictor, faceRecog = load_dlib_models()

    faces = detector(image_np, 1)

    encodings = []

    for face in faces:

        shape = shapePredictor(image_np, face)

        face_descriptor = faceRecog.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        encodings.append(
            np.array(face_descriptor, dtype=np.float32)
        )

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

        if embedding is not None:

            embedding = np.array(
                embedding,
                dtype=np.float32
            )

            X.append(embedding)
            y.append(student.get("student_id"))

    if len(X) == 0:
        return None

    return {
        "X": X,
        "y": y
    }


def train_classifier():

    st.cache_resource.clear()

    model_data = get_trained_model()

    return model_data is not None


def predict_attendance(class_image_np):

    class_image_np = np.asarray(
        class_image_np,
        dtype=np.uint8
    )

    encodings = get_face_embeddings(class_image_np)

    detected_students = {}

    model_data = get_trained_model()

    if model_data is None:

        return detected_students, [], len(encodings)

    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(
        list(set(y_train))
    )

    # Strict face matching
    resemblance_threshold = 0.45

    # Required difference between best and second-best match
    minimum_gap = 0.08

    for encoding in encodings:

        distances = []

        for student_embedding, student_id in zip(
            X_train,
            y_train
        ):

            distance = np.linalg.norm(
                student_embedding - encoding
            )

            distances.append(
                (distance, student_id)
            )

        if not distances:
            continue

        distances.sort(
            key=lambda x: x[0]
        )

        best_distance, best_student_id = distances[0]

        # First check absolute similarity
        if best_distance > resemblance_threshold:
            continue

        # If there is only one registered student,
        # absolute threshold is enough.
        if len(distances) == 1:
            detected_students[int(best_student_id)] = True
            continue

        second_best_distance = distances[1][0]

        # Best match should clearly beat second-best match
        if (second_best_distance - best_distance) < minimum_gap:
            continue

        detected_students[int(best_student_id)] = True

    return (
        detected_students,
        all_students,
        len(encodings)
    )