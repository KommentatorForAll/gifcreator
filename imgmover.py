import math

from PIL import Image
import matplotlib.pyplot as plt

yes_options = ["yes", "y", "true", "t", "1"]


def main():
    original_image = Image.open(input("input image: "))
    duration_frames = int(input("Duration (frames): "))
    duration_ms = int(input("Duration (ms): "))
    duration_ms_p_frame = duration_ms / duration_frames
    px_upshift = int(input("shift up by px: "))
    bool_sincurve = input("sincurve? ").lower() in yes_options
    adjust_function = (sin_curve if bool_sincurve else triangle)(duration_frames, px_upshift)

    plt.plot(list([adjust_function(x) for x in range(duration_frames)]))
    # plt.show()
    empty_img = Image.new("RGBA", original_image.size, 0)
    frames = []
    for i in range(duration_frames):
        img = empty_img.copy()
        img.paste(original_image, (0, 0-round(adjust_function(i))), original_image)
        frames.append(img)
    frames[0].save("myGif.gif", format="GIF", append_images=frames, save_all=True, duration=duration_ms_p_frame, loop=0, disposal=2)


def sin_curve(duration: int, px_upshift: int) -> callable(int):
    """
    returns a function to determin the new y position on a given frame
    :param duration: how long it takes for the image to cycle back to its starting position
    :param px_upshift: how high the highest point is in relation to the original position
    :return:
    """
    sinbase = lambda x: math.sin(x - (math.pi / 2))
    sin_hightadjusted = lambda x: (sinbase(x)/2 + 0.5) * px_upshift
    sin_lengthadjusted = lambda x: sin_hightadjusted((x/duration) * 2 * math.pi)
    return sin_lengthadjusted


def triangle(duration: int, px_upshift: int) -> callable(int):
    """
    returns a function to determin the new y position on a given frame
    :param duration: how long it takes for the image to cycle back to its starting position
    :param px_upshift: how high the highest point is in relation to the original position
    :return:
    """
    delta = 2*px_upshift / duration

    def fun(x):
        if x > duration / 2:
            return delta * (duration - x)
        else:
            return delta * x

    return fun


if __name__ == '__main__':
    main()
