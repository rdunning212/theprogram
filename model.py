import tensorflow as tf
from tensorflow.python.keras import layers
import pandas as pd
from sklearn.model_selection import train_test_split

game_stats = pd.read_csv('team_stats_by_game.csv')

game_features = game_stats.copy()
game_labels = game_features.pop('Result')
normalize = tf.keras.layers.Normalization()

X_train, X_test, y_train, y_test = train_test_split(game_features, game_labels, test_size=0.25, random_state=20)

game_model = tf.keras.Sequential([
    normalize,
    layers.Dense(256),
    tf.keras.layers.Dropout(0.2),
    layers.Dense(128),
    tf.keras.layers.Dropout(0.2),
    layers.Dense(64),
    tf.keras.layers.Dropout(0.2),
    layers.Dense(1)
])

game_model.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=tf.optimizers.Adam(), metrics=['accuracy'])

game_model.fit(X_train, y_train, epochs=1000)

game_model.evaluate(X_test, y_test, verbose=2)
