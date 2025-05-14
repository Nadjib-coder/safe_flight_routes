import tensorflow as tf
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt   # <-- new

# 1. point to the directory that was saved with model.save(...)
saved_path = Path("models/eruption_small_model.h5")      # adjust as needed

# 2. re-load the full Keras model graph & weights
model = tf.keras.models.load_model(saved_path)

# 3. rebuild the validation dataset exactly as during training
VAL_DIR  = Path("data_reviewed/validation")
IMG_SIZE = (128, 128)
BATCH_SZ = 32

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SZ,
    label_mode="binary",
    shuffle=False)                               # keep file order stable

# 4. predict
val_prob = model.predict(val_ds, verbose=0).ravel()   # sigmoid outputs ∈ [0,1]
val_bin  = (val_prob > 0.5).astype(int)               # hard 0/1 at threshold 0.5

# 4b. grab the ground-truth labels in the same order
val_true = np.concatenate([y for _, y in val_ds], axis=0).astype(int).ravel()

# 4c. keep the file paths (TF ≥ 2.4; older TF fallback shown below)
try:
    file_paths = val_ds.file_paths
except AttributeError:
    from glob import glob
    file_paths = sorted(glob(str(VAL_DIR / "*" / "*")))

# 4d. numeric id → class name   (['eruption', 'no_eruption'])
class_names = val_ds.class_names

# ────────────────────────────────────────────────────────────────
# 5. DISPLAY EACH IMAGE WITH TRUE + PREDICTED LABELS
# ────────────────────────────────────────────────────────────────
for fp, gt, pr in zip(file_paths, val_true, val_prob):
    img = tf.keras.utils.load_img(fp, target_size=IMG_SIZE)

    plt.figure(figsize=(4, 4))
    plt.imshow(img)
    plt.axis("off")

    pred_lbl  = class_names[int(pr > 0.5)]
    true_lbl  = class_names[int(gt)]
    plt.title(f"True: {true_lbl}   •   Pred: {pr:.2f} → {pred_lbl}",
              fontsize=10, pad=8)

    plt.show(block=False)
    plt.pause(0.001)          # make sure the window shows up
    input("to continue,  Ctrl-C to stop")
    plt.close()
