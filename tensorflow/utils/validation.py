# ===========
#  Libraries
# ===========
import tensorflow as tf
import utils.loss as loss

# ==================
#  Global Variables
# ==================
LOG_INITIAL_VALUE = 1


# ===================
#  Class Declaration
# ===================
class Validation:
    def __init__(self, image_size, depth_size, input_size, output_size):
        # Raw Input/Output
        self.tf_image = tf.placeholder(tf.float32, shape=(None, image_size.height, image_size.width, image_size.nchannels))
        self.tf_depth = tf.placeholder(tf.float32, shape=(None, depth_size.height, depth_size.width, depth_size.nchannels))

        # Network Input/Output
        self.tf_image_resized = tf.image.resize_images(self.tf_image, [input_size.height, input_size.width])
        self.tf_depth_resized = tf.image.resize_images(self.tf_depth, [output_size.height, output_size.width])
        self.tf_log_depth_resized = tf.log(self.tf_depth_resized + tf.constant(LOG_INITIAL_VALUE, dtype=tf.float32))

        # TODO: Implementar validacao por batches
        # batch_size = 2 # TODO: Move variable
        #
        # self.tf_image_resized_uint8 = tf.cast(self.tf_image_resized, tf.uint8)  # Visual purpose
        #
        # # Creates Training Batch Tensors
        # self.tf_batch_data_resized, self.tf_batch_data, self.tf_batch_labels = tf.train.shuffle_batch(
        #     # [tf_image_key, tf_depth_key],           # Enable for Debugging the filename strings.
        #     [self.tf_image_resized_uint8, self.tf_image_resized, self.tf_depth_resized],  # Enable for debugging images
        #     batch_size=batch_size,
        #     num_threads=1,
        #     capacity=16,
        #     min_after_dequeue=0)

        self.tf_loss = None
        self.loss = -1

        print("\n[Network/Validation] Validation Tensors Created.")
        print(self.tf_image)
        print(self.tf_depth)
        print(self.tf_image_resized)
        print(self.tf_depth_resized)
        print(self.tf_log_depth_resized)
