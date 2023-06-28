from PIL import Image
import random


# cite: https://blog.csdn.net/s000da/article/details/90242740
def random_crop(image, crop_shape, padding=None):
    oshape = image.size

    if padding:
        oshape_pad = (oshape[0] + 2 * padding, oshape[1] + 2 * padding)
        img_pad = Image.new("RGB", (oshape_pad[0], oshape_pad[1]))
        img_pad.paste(image, (padding, padding))

        nh = random.randint(0, oshape_pad[0] - crop_shape[0])
        nw = random.randint(0, oshape_pad[1] - crop_shape[1])
        image_crop = img_pad.crop((nh, nw, nh + crop_shape[0], nw + crop_shape[1]))

        return image_crop
    else:
        print("WARNING!!! nothing to do!!!")
        return image
