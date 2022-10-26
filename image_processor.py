from PIL import Image, ImageChops


class ImageProcessor:

    def __init__(self, filename_path, quality=90, scale=60, blending_opacity=0.5):
        self.original_filename = filename_path
        self.resaved_filename = filename_path.split('.')[0] + '.resaved.jpg'
        self.ELA_filename = filename_path.split('.')[0] + '.ela.png'
        self.overlayed_filename = filename_path.split('.')[0] + '.overlayed.png'

        original_image = Image.open(self.original_filename).convert('RGB')
        original_image.save(self.resaved_filename, 'JPEG', quality=quality)
        resaved_image = Image.open(self.resaved_filename)

        ELA_image = self.convert_to_ela(original_image, resaved_image, scale)
        ELA_image.save(self.ELA_filename)

        overlayed_image = Image.blend(original_image, ELA_image, blending_opacity)
        overlayed_image.save(self.overlayed_filename)

    def convert_to_ela(self, original_image, resaved_image, scale):
        """
        Takes original and resaved with compression image and return ELA image,
        which is a difference between these two images.
        """

        ela_image = ImageChops.difference(original_image, resaved_image)
        width, height = ela_image.size
        ela_pixel_image = ela_image.load()
        for x in range(width):
            for y in range(height):
                ela_pixel_image[x, y] = tuple(k * scale for k in ela_pixel_image[x, y])
        return ela_image

    def compress_image(self):
        """
        Implement in future
        Compress image until it's size will be less than threshold
        """

        pass
