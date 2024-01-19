import os
from PIL import Image, ImageDraw

from SampleSelector import SampleSelector


class ImageSampler:
    """
    The ImageSampler class directly handles the image file while the randomization selection is abstracted to the
    SampleSelector class.

    It will take in a specified input file, then generate n samples (defaulting to 3). As well as an image
    that highlights where each of those samples was taken from in the original image.

    The sample output is overwritten each time the program is run.
    """

    def __init__(self, image_name, input_path="SampleInput", output_path="SampleOutput"):
        self.input_path = input_path
        self.output_path = output_path
        self.image = Image.open(os.path.join(self.input_path, image_name))
        self.image_width, self.image_height = self.image.size
        self.sample_positions = []

    def get_image_dimensions(self) -> (int, int):
        return self.image_width, self.image_height

    def _get_random_samples(self, sample_size: (int, int), number_of_samples: int = 3) -> None:
        sample_selector = SampleSelector(self.image_width, self.image_height, sample_size[0], sample_size[1])
        self.sample_positions = sample_selector.generate_random_samples(number_of_samples)

    def _generate_original_image_with_samples_highlighted(self, sample_size: (int, int)) -> None:
        draw = ImageDraw.Draw(self.image)
        for sample_position in self.sample_positions:
            draw.rectangle((sample_position[0], sample_position[1],
                            sample_position[0] + sample_size[0], sample_position[1] + sample_size[1]),
                           outline='red', width=2)
        self.image.save(os.path.join(self.output_path, "OriginalImageWithHighlightedSamples.png"))

    def _generate_samples_as_separate_images(self, sample_size: (int, int)) -> None:
        i = 1
        for sample_position in self.sample_positions:
            x, y = sample_position
            sample = self.image.crop((x, y, x + sample_size[0], y + sample_size[1]))
            sample.save(os.path.join(self.output_path, f"Sample{i}.png"))
            i = i + 1

    def generate_samples(self, sample_size: (int, int)) -> None:
        self._get_random_samples(sample_size)
        self._generate_samples_as_separate_images(sample_size)
        self._generate_original_image_with_samples_highlighted(sample_size)
