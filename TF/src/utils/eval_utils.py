import tensorflow as tf
import numpy as np

def eval_keras_model(
        model: tf.keras.Model,
        val_ds,
):
    model.compile(
        optimizer=tf.keras.optimizers.SGD(),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=['accuracy']
    )
    loss, accuracy = model.evaluate(val_ds, verbose=0)
    return accuracy



def eval_tflite_model(
        model_path: str,
        val_ds,
):
    interpreter = tf.lite.Interpreter(
        model_path=model_path,
        num_threads=20,
    )
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    ds = val_ds.unbatch().batch(1)

    accuracy = 0
    size = 0

    for batch in ds:
        interpreter.set_tensor(input_details[0]['index'], batch[0].numpy())
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]['index'])
        accuracy += np.sum(np.argmax(output, axis=1) == batch[1].numpy())
        size += 1
    return accuracy / float(size)
