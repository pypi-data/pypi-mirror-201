import os

import tensorflow as tf
# try:
#     import importlib.resources as pkg_resources
# except ImportError:
#     import importlib_resources as pkg_resources

IMG_WIDTH = 320
IMG_HEIGHT = 240
IMG_CHANNELS = 3
N_CLASSES = 3 # [white, yellow, other]
BATCH_SIZE = 5

class Segmentation:
    def __init__(self, model=None, verbose=0):
        # can be done better with importlib.resources
        if model == None:
            pkg_path = os.path.abspath(__file__)
            model_path = os.path.join(os.path.dirname(pkg_path), 'models', 'multiclass_segmentation_model')
            model = tf.keras.models.load_model(model_path)
        self.model = model
        self.model.summary()
        self.verbose = verbose

    def predict(self, image):
        return self.model.predict(image.reshape((1,IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)), verbose=self.verbose)

    def predict_batch(self, images):
        return self.model.predict(images.reshape((1,IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)), verbose=self.verbose)

    def get_model(self):
        return self.model

    def get_model_summary(self):
        return self.model.summary()

    def train(self, x_train, y_train):
        callbacks=[
            tf.keras.callbacks.EarlyStopping(patience=100, monitor='val_loss'),
            tf.keras.callbacks.TensorBoard(log_dir='logs')]
        results = self.model.fit(x_train,y_train, validation_split=0.1, batch_size = BATCH_SIZE, epochs=100, callbacks=callbacks)

    @staticmethod
    def define_model():
        inputs = tf.keras.layers.Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))
        s = tf.keras.layers.Lambda(lambda x:x /255)(inputs)
        
        c1 = tf.keras.layers.Conv2D(16, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(s)
        c1 = tf.keras.layers.Dropout(0.1)(c1)
        c1 = tf.keras.layers.Conv2D(16, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(c1)
        p1 = tf.keras.layers.MaxPooling2D((2,2))(c1)

        c2 = tf.keras.layers.Conv2D(32, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(p1)
        c2 = tf.keras.layers.Dropout(0.1)(c2)
        c2 = tf.keras.layers.Conv2D(32, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(c2)
        p2 = tf.keras.layers.MaxPooling2D((2,2))(c2)

        c3 = tf.keras.layers.Conv2D(64, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(p2)
        c3 = tf.keras.layers.Dropout(0.1)(c3)
        c3 = tf.keras.layers.Conv2D(64, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(c3)
        p3 = tf.keras.layers.MaxPooling2D((2,2))(c3)

        c4 = tf.keras.layers.Conv2D(128, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(p3)
        c4 = tf.keras.layers.Dropout(0.1)(c4)
        c4 = tf.keras.layers.Conv2D(128, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(c4)
        p4 = tf.keras.layers.MaxPooling2D((2,2))(c4)

        c5 = tf.keras.layers.Conv2D(256, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(p4)
        c5 = tf.keras.layers.Dropout(0.1)(c5)
        c5 = tf.keras.layers.Conv2D(256, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(c5)

        u6 = tf.keras.layers.Convolution2DTranspose(128, (2,2), strides=(2,2), padding='same')(c5)
        u6 = tf.keras.layers.concatenate([u6, c4]) #merge with old layer
        c6 = tf.keras.layers.Conv2D(128, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(u6)
        c6 = tf.keras.layers.Dropout(0.1)(c6)
        c6 = tf.keras.layers.Conv2D(128, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(c6)

        u7 = tf.keras.layers.Convolution2DTranspose(64, (2,2), strides=(2,2), padding='same')(c6)
        u7 = tf.keras.layers.concatenate([u7, c3])  #merge with old layer
        c7 = tf.keras.layers.Conv2D(64, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(u7)
        c7 = tf.keras.layers.Dropout(0.1)(c7)
        c7 = tf.keras.layers.Conv2D(64, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(c7)

        u8 = tf.keras.layers.Convolution2DTranspose(32, (2,2), strides=(2,2), padding='same')(c7)
        u8 = tf.keras.layers.concatenate([u8, c2])  #merge with old layer
        c8 = tf.keras.layers.Conv2D(32, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(u8)
        c8 = tf.keras.layers.Dropout(0.1)(c8)
        c8 = tf.keras.layers.Conv2D(32, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(c8)

        u9 = tf.keras.layers.Convolution2DTranspose(16, (2,2), strides=(2,2), padding='same')(c8)
        u9 = tf.keras.layers.concatenate([u9, c1])  #merge with old layer
        c9 = tf.keras.layers.Conv2D(16, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(u9)
        c9 = tf.keras.layers.Dropout(0.1)(c9)
        c9 = tf.keras.layers.Conv2D(16, (3,3), activation="relu", kernel_initializer='he_normal', padding='same')(c9)

        outputs = tf.keras.layers.Conv2D(N_CLASSES, (1,1), activation = 'softmax')(c9)  #[white line, yellow line, other]

        model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
        model.compile(optimizer='adam', loss='binary_crossentropy')
        model.summary()

        return model
