# ===========
#  Libraries
# ===========
import tensorflow as tf
import random
import glob
import os

from .size import Size
from .kitti import Kitti
from .kittiraw import KittiRaw
from .nyudepth import NyuDepth

# ==================
#  Global Variables
# ==================
LOSS_LOG_INITIAL_VALUE = 0.1


# ===========
#  Functions
# ===========


# ===================
#  Class Declaration
# ===================
# TODO: Criar rotina que subdivide os dados disponívels em train/valid
class Dataloader:
    def __init__(self, args):
        # Detects which dataset was selected and creates the 'datasetObj'.
        self.selectedDataset = args.dataset
        # print(selectedDataset)

        if self.selectedDataset == 'kittiraw_residential_continuous':
            self.datasetObj = KittiRaw()  # TODO: Terminar
            pass

        elif self.selectedDataset == 'nyudepth':
            self.datasetObj = NyuDepth()  # TODO: Terminar
            pass

        else:
            print("[Dataloader] The typed dataset '%s' is invalid. Check the list of supported datasets." % self.selectedDataset)
            raise SystemExit

        # Collects Dataset Info
        self.dataset_name = self.datasetObj.name
        self.dataset_path = self.datasetObj.dataset_path
        self.image_size = self.datasetObj.image_size
        self.depth_size = self.datasetObj.depth_size

        print("[Dataloader] dataloader object created.")

    # TODO: Ler outros Datasets
    def getTrainInputs(self, args):
        if args.machine == 'olorin':
            # KittiRaw Residential Continuous
            # Image: (375, 1242, 3) uint8
            # Depth: (375, 1242)    uint8
            if args.dataset == 'kittiraw_residential_continuous':
                search_image_files_str = "../../mestrado_code/monodeep/data/residential_continuous/training/imgs/*.png"
                search_depth_files_str = "../../mestrado_code/monodeep/data/residential_continuous/training/dispc/*.png"

                tf_image_filenames = tf.train.match_filenames_once(search_image_files_str)
                tf_depth_filenames = tf.train.match_filenames_once(search_depth_files_str)

        elif args.machine == 'xps':
            image_filenames, depth_filenames = self.datasetObj.getFilenamesLists()
            tf_image_filenames, tf_depth_filenames = self.datasetObj.getFilenamesTensors()


        try:
            print("\nSummary - Dataset Inputs")
            print("image_filenames: ", len(image_filenames))
            print("depth_filenames: ", len(depth_filenames))
        except TypeError:
            print("[TypeError] 'image_filenames' and 'depth_filenames' are None.")

        return image_filenames, depth_filenames, tf_image_filenames, tf_depth_filenames

    def readData(self, tf_image_filenames, tf_depth_filenames):
        # Creates Inputs Queue.
        # ATTENTION! Since these tensors operate on a FifoQueue, using .eval() may misalign the pair (image, depth)!!!
        seed = random.randint(0, 2 ** 31 - 1)
        tf_train_image_filename_queue = tf.train.string_input_producer(tf_image_filenames, shuffle=False,
                                                                       seed=seed)
        tf_train_depth_filename_queue = tf.train.string_input_producer(tf_depth_filenames, shuffle=False,
                                                                       seed=seed)

        # Reads images
        image_reader = tf.WholeFileReader()
        tf_image_key, image_file = image_reader.read(tf_train_image_filename_queue)
        tf_depth_key, depth_file = image_reader.read(tf_train_depth_filename_queue)

        # FIXME: Kitti Original as imagens de disparidade são do tipo int32, no caso do kittiraw_residential_continous são uint8
        tf_image = tf.image.decode_image(image_file, channels=3)  # uint8
        tf_depth = tf.image.decode_image(depth_file, channels=1)  # uint8

        # Restores images structure (size, type)
        tf_image.set_shape([self.image_size.height, self.image_size.width, self.image_size.nchannels])
        tf_depth.set_shape([self.depth_size.height, self.depth_size.width, self.depth_size.nchannels])

        return tf_image, tf_depth

    # TODO: Terminar
    def splitData(self, ratio=0.8):


        print("Terminar")

    def checkIntegrity(self, sess, tf_image_filenames, tf_depth_filenames):
        try:
            image_filenames, depth_filenames = sess.run([tf_image_filenames, tf_depth_filenames])

            image_filenames_aux = [item.replace(self.datasetObj.image_replace[0], self.datasetObj.image_replace[1]) for item in image_filenames]
            depth_filenames_aux = [item.replace(self.datasetObj.depth_replace[0], self.datasetObj.depth_replace[1]) for item in depth_filenames]

            # print(image_filenames)
            # input("oi1")
            # print(depth_filenames)
            # input("oi2")
            #
            # print(image_filenames_aux)
            # input("oi3")
            # print(depth_filenames_aux)
            # input("oi4")

            numSamples = len(image_filenames_aux)

            print("[Dataloader] Checking if RGB and Depth images are paired... ")
            if image_filenames_aux == depth_filenames_aux:
                print("[Dataloader] Check Integrity: Pass")
            else:
                raise ValueError

            return numSamples

        except ValueError:
            print("[Dataloader] Check Integrity: Failed")
            raise SystemExit