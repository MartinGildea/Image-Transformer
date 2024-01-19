class InvalidSampleDimensions(Exception):
    def __init__(self, message="Both the height and width of the Sample must be positive integers"):
        self.message = message
        super().__init__(self.message)


class SampleHeightExceedsImageHeight(Exception):
    def __init__(self, message="The sample height selected is larger than the image."
                               "Please ensure the sample height is smaller than the image."):
        self.message = message
        super().__init__(self.message)


class SampleWidthExceedsImageWidth(Exception):
    def __init__(self, message="The sample width selected is larger than the image."
                               "Please ensure the sample width is smaller than the image."):
        self.message = message
        super().__init__(self.message)


class SampleAreaExceedsImageArea(Exception):
    def __init__(self, message="The combined area of the samples would be greater than the area of the image."
                               "Please try select a smaller width and/or height for the samples."):
        self.message = message
        super().__init__(self.message)


class NoFreePositionError(Exception):
    def __init__(self, message="Exhausted every possible permutation of sample positions and could not find a "
                               "permutation that fit. Please try selecting smaller samples."):
        self.message = message
        super().__init__(self.message)
