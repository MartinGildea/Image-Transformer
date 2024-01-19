import os

from ImageSampler import ImageSampler


class UserConsole:
    """
    A simple user console class that has major scope for improvement. Requests the user places an image in the input
    folder, then asks them to specify the filename of the image and the dimensions of their sample.

    Enforces the requested 3 samples and performs validation on all input.
    """
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    def __init__(self, input_path="SampleInput"):
        self.input_path = input_path
        self.output_path = "SampleOutput"

    def _handle_input_file(self) -> None:
        while True:
            file_name = input("Image file name: ")
            file_extension = os.path.splitext(file_name)[1].lower()

            if not os.path.exists(os.path.join(self.input_path, file_name)):
                print("File does not exist. Please try again.")
            elif file_extension not in self.SUPPORTED_FORMATS:
                print("This file is not in a supported image format."
                      "Please try again with a supported image format (jpg, jpeg, png, bmp, gif).")
            else:
                break
        self.image_sampler = ImageSampler(file_name, self.input_path)

    def _validate_sample_dimension(self, dimension_name: str, dimension: int) -> bool:
        if dimension > self.image_sampler.get_image_dimensions()[0]:
            print(f"The {dimension_name} of the sample must be smaller than the {dimension_name} of the image.")
            return False
        elif dimension <= 0:
            print(f"The {dimension_name} of the sample must be a positive integer greater than 0.")
            return False
        return True

    def _handle_sample_dimensions_input(self) -> (int, int):
        while True:
            while True:
                width = int(input("Please enter the width of the samples:"))
                if self._validate_sample_dimension("width", width):
                    break

            while True:
                height = int(input("Please enter the height of the samples:"))
                if self._validate_sample_dimension("height", height):
                    break

            if height * width * 3 > \
                    self.image_sampler.get_image_dimensions()[0] * self.image_sampler.get_image_dimensions()[1]:
                print("The combined area of the three samples must be smaller than the area of the image.\n")
            else:
                break
        return width, height

    def generate_samples(self, width: int, height: int) -> None:
        try:
            self.image_sampler.generate_samples((width, height))
            print("Samples successfully generated!")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def run_console(self) -> None:
        print("Please place the image you wish you sample in the SampleInput folder")
        print("Enter the file name with its extension (e.g., image.jpg).\n")
        self._handle_input_file()
        width, height = self._handle_sample_dimensions_input()
        self.generate_samples(width, height)


if __name__ == "__main__":
    console = UserConsole()
    console.run_console()
