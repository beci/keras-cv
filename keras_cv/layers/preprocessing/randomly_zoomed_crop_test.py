# Copyright 2022 The KerasCV Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import tensorflow as tf
from absl.testing import parameterized

from keras_cv.layers import preprocessing


class RandomlyZoomedCropTest(tf.test.TestCase, parameterized.TestCase):
    height, width = 300, 300
    batch_size = 4
    target_size = (224, 224)
    seed = 42

    def test_train_augments_image(self):
        # Checks if original and augmented images are different

        input_image_shape = (self.batch_size, self.height, self.width, 3)
        image = tf.random.uniform(shape=input_image_shape, seed=self.seed)

        layer = preprocessing.RandomlyZoomedCrop(
            height=self.target_size[0],
            width=self.target_size[1],
            aspect_ratio_factor=(3 / 4, 4 / 3),
            zoom_factor=(0.8, 1.0),
            seed=self.seed,
        )
        output = layer(image, training=True)

        input_image_resized = tf.image.resize(image, self.target_size)

        self.assertNotAllClose(output, input_image_resized)

    def test_grayscale(self):
        input_image_shape = (self.batch_size, self.height, self.width, 1)
        image = tf.random.uniform(shape=input_image_shape)

        layer = preprocessing.RandomlyZoomedCrop(
            height=self.target_size[0],
            width=self.target_size[1],
            aspect_ratio_factor=(3 / 4, 4 / 3),
            zoom_factor=(0.8, 1.0),
        )
        output = layer(image, training=True)

        input_image_resized = tf.image.resize(image, self.target_size)

        self.assertAllEqual(output.shape, (4, 224, 224, 1))
        self.assertNotAllClose(output, input_image_resized)

    def test_preserves_image(self):
        image_shape = (self.batch_size, self.height, self.width, 3)
        image = tf.random.uniform(shape=image_shape)

        layer = preprocessing.RandomlyZoomedCrop(
            height=self.target_size[0],
            width=self.target_size[1],
            aspect_ratio_factor=(3 / 4, 4 / 3),
            zoom_factor=(0.8, 1.0),
        )

        input_resized = tf.image.resize(image, self.target_size)
        output = layer(image, training=False)

        self.assertAllClose(output, input_resized)

    @parameterized.named_parameters(
        ("Not tuple or list", dict()),
        ("Length not equal to 2", [1, 2, 3]),
        ("Members not int", (2.3, 4.5)),
        ("Single float", 1.5),
    )
    def test_height_errors(self, height):
        with self.assertRaisesRegex(
            ValueError,
            "`height` must be an integer. Received height=(.*)",
        ):
            _ = preprocessing.RandomlyZoomedCrop(
                height=height,
                width=100,
                aspect_ratio_factor=(3 / 4, 4 / 3),
                zoom_factor=(0.8, 1.0),
            )

    @parameterized.named_parameters(
        ("Not tuple or list", dict()),
        ("Length not equal to 2", [1, 2, 3]),
        ("Members not int", (2.3, 4.5)),
        ("Single float", 1.5),
    )
    def test_width_errors(self, width):
        with self.assertRaisesRegex(
            ValueError,
            "`width` must be an integer. Received width=(.*)",
        ):
            _ = preprocessing.RandomlyZoomedCrop(
                height=100,
                width=width,
                aspect_ratio_factor=(3 / 4, 4 / 3),
                zoom_factor=(0.8, 1.0),
            )

    @parameterized.named_parameters(
        ("Single integer", 5),
        ("Single float", 5.0),
    )
    def test_aspect_ratio_factor_errors(self, aspect_ratio_factor):
        with self.assertRaisesRegex(
            ValueError,
            "`aspect_ratio_factor` must be tuple of two positive floats or "
            "keras_cv.core.FactorSampler instance. Received aspect_ratio_factor=(.*)",
        ):
            _ = preprocessing.RandomlyZoomedCrop(
                height=self.target_size[0],
                width=self.target_size[1],
                aspect_ratio_factor=aspect_ratio_factor,
                zoom_factor=(0.8, 1.0),
            )

    @parameterized.named_parameters(
        ("Single integer", 5),
        ("Single float", 5.0),
    )
    def test_zoom_factor_errors(self, zoom_factor):
        with self.assertRaisesRegex(
            ValueError,
            "`zoom_factor` must be tuple of two positive floats"
            " or keras_cv.core.FactorSampler instance. Received "
            "zoom_factor=(.*)",
        ):
            _ = preprocessing.RandomlyZoomedCrop(
                height=self.target_size[0],
                width=self.target_size[1],
                aspect_ratio_factor=(3 / 4, 4 / 3),
                zoom_factor=zoom_factor,
            )
