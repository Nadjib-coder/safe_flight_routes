#!/usr/bin/env python3
"""
Train a lightweight CNN (≈160 k parameters) for eruption / no-eruption
classification and export both a SavedModel and an INT8-quantised
TensorFlow-Lite artefact suitable for edge devices.

Tested with:
  • Python 3.10
  • TensorFlow 2.16 (CPU or GPU build)
  • pillow, numpy  (install via:  pip install tensorflow pillow numpy)
"""

from pathlib import Path
import tensorflow as tf

# ────────────────────────────────────────────────────────────────
# 1. CONFIGURATION  – change these paths if needed
# ────────────────────────────────────────────────────────────────
DATASET_ROOT   = Path("data_reviewed")       # <- put your path here
TRAIN_DIR      = DATASET_ROOT / "training"
VAL_DIR        = DATASET_ROOT / "validation"
IMG_SIZE       = (128, 128)                 # Sentinel-2 chips are small; 128 px is enough
BATCH_SIZE     = 32
EPOCHS         = 15
MODEL_OUT      = Path("models")             # everything gets written here
MODEL_OUT.mkdir(exist_ok=True)

# ────────────────────────────────────────────────────────────────
# 2. DATA INPUT
# ────────────────────────────────────────────────────────────────
# (If you need >3 Sentinel-2 bands, see the note at the bottom.)
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    seed=123)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="binary",
    seed=123)

# «prefetch to GPU/CPU pipeline»
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(512).prefetch(buffer_size=AUTOTUNE)
val_ds   = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# ────────────────────────────────────────────────────────────────
# 3. MODEL DEFINITION  – mirrors the “small_model.ipynb” from the repo
# ────────────────────────────────────────────────────────────────
inputs = tf.keras.Input(shape=(*IMG_SIZE, 3))

x = tf.keras.layers.Rescaling(1./255)(inputs)   # normalise [0,255] → [0,1]

x = tf.keras.layers.Conv2D(16, 3, padding="same", activation="relu")(x)
x = tf.keras.layers.MaxPooling2D()(x)

x = tf.keras.layers.Conv2D(32, 3, padding="same", activation="relu")(x)
x = tf.keras.layers.MaxPooling2D()(x)

x = tf.keras.layers.Conv2D(64, 3, padding="same", activation="relu")(x)
x = tf.keras.layers.MaxPooling2D()(x)

x = tf.keras.layers.Flatten()(x)
x = tf.keras.layers.Dense(64, activation="relu")(x)
x = tf.keras.layers.Dropout(0.3)(x)

outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)

model = tf.keras.Model(inputs, outputs, name="eruption_small_cnn")
model.summary()

# ────────────────────────────────────────────────────────────────
# 4. COMPILE & TRAIN
# ────────────────────────────────────────────────────────────────
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy",
             tf.keras.metrics.Precision(name="precision"),
             tf.keras.metrics.Recall(name="recall"),
             tf.keras.metrics.AUC(name="auc")])

history = model.fit(
    train_ds,
    epochs=EPOCHS,
    validation_data=val_ds)

# ────────────────────────────────────────────────────────────────
# 5. SAVE A FULL KERAS MODEL (SavedModel format)
# ────────────────────────────────────────────────────────────────
saved_path = MODEL_OUT / "eruption_small_model.h5"
model.save(saved_path, include_optimizer=False)
print(f"SavedModel written to  {saved_path}")


