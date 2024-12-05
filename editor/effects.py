from PIL import Image, ImageFilter, ImageEnhance
import os


def make_linear_ramp(white):
    """Create a linear ramp for sepia effect."""
    r, g, b = white
    return [(r * i // 255, g * i // 255, b * i // 255) for i in range(256)]


class ApplyEffects:
    """Apply various image effects to an image."""

    EFFECTS_MAP = {
        'brightness': 'apply_brightness',
        'grayscale': 'apply_grayscale',
        'blackwhite': 'apply_black_white',
        'sepia': 'apply_sepia',
        'contrast': 'apply_contrast',
        'blur': 'apply_blur',
        'findedges': 'apply_find_edges',
        'bigenhance': 'apply_edge_enhance_more',
        'enhance': 'apply_edge_enhance',
        'smooth': 'apply_smooth_more',
        'emboss': 'apply_emboss',
        'contour': 'apply_contour',
        'sharpen': 'apply_sharpen',
    }

    @staticmethod
    def get_effect_names():
        """Return a list of available effect names."""
        return list(ApplyEffects.EFFECTS_MAP.keys())

    @staticmethod
    def apply_effect(edited_image, effect):
        """Apply the specified effect to the image."""
        if effect not in ApplyEffects.EFFECTS_MAP:
            return f"{effect} is not a supported effect."

        filepath, ext = os.path.splitext(edited_image)
        edit_path = f"{filepath}_edited{ext}"

        img = Image.open(edited_image)
        method = getattr(ApplyEffects, ApplyEffects.EFFECTS_MAP[effect])
        img = method(img)
        img.save(edit_path, format='PNG', quality=100)
        return f"Effect '{effect}' applied successfully."

    @staticmethod
    def apply_brightness(img):
        """Apply brightness effect."""
        return ImageEnhance.Brightness(img).enhance(1.8)

    @staticmethod
    def apply_grayscale(img):
        """Apply grayscale effect."""
        return img.convert('L')

    @staticmethod
    def apply_black_white(img):
        """Apply black and white effect."""
        return img.convert('1')

    @staticmethod
    def apply_sepia(img):
        """Apply sepia effect."""
        sepia_palette = make_linear_ramp((255, 240, 192))
        img = img.convert('L')
        img.putpalette([value for rgb in sepia_palette for value in rgb])
        return img.convert('RGB')

    @staticmethod
    def apply_contrast(img):
        """Apply contrast effect."""
        return ImageEnhance.Contrast(img).enhance(2.0)

    @staticmethod
    def apply_blur(img):
        """Apply blur effect."""
        return img.filter(ImageFilter.BLUR)

    @staticmethod
    def apply_find_edges(img):
        """Apply find edges effect."""
        return img.filter(ImageFilter.FIND_EDGES)

    @staticmethod
    def apply_edge_enhance_more(img):
        """Apply edge enhancement effect."""
        return img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    @staticmethod
    def apply_edge_enhance(img):
        """Apply edge enhancement effect."""
        return img.filter(ImageFilter.EDGE_ENHANCE)

    @staticmethod
    def apply_smooth_more(img):
        """Apply smooth more effect."""
        return img.filter(ImageFilter.SMOOTH_MORE)

    @staticmethod
    def apply_emboss(img):
        """Apply emboss effect."""
        return img.filter(ImageFilter.EMBOSS)

    @staticmethod
    def apply_contour(img):
        """Apply contour effect."""
        return img.filter(ImageFilter.CONTOUR)

    @staticmethod
    def apply_sharpen(img):
        """Apply sharpen effect."""
        return img.filter(ImageFilter.SHARPEN)
