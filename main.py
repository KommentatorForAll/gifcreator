import numpy as np
from PIL import Image
import glob


def main():
    stamp = Image.open(input("Stamped_image: "))
    bg_img_folder = input("Folder with background images: ")
    bg_duration = int(input("Duration of each background (frames): "))
    transition_duration = int(input("Duration of the transitions (frames): "))
    full_duration_ms = int(input("Duration of the whole gif (ms): "))

    backgrounds = []
    for file_path in glob.glob(f"{bg_img_folder}/*.png"):
        backgrounds.append(Image.open(file_path))

    background_amount = len(backgrounds)
    full_duration_frames = background_amount * bg_duration + background_amount * transition_duration

    empty_image = Image.new("RGBA", stamp.size, 0)
    frames = []
    in_transition = False
    frame_index = -1
    bg_index = 0
    movement_speed = empty_image.size[0]/transition_duration
    for i in range(full_duration_frames):
        frame_index += 1
        img = empty_image.copy()
        current_bg = backgrounds[bg_index]
        if not in_transition:
            img.paste(current_bg, (0, 0), current_bg)

            if frame_index >= bg_duration:
                in_transition = True
                frame_index = 0
            pass
        else:
            next_bg = backgrounds[(bg_index+1) % background_amount]
            img.paste(current_bg, (0-round(movement_speed * frame_index), 0), current_bg)
            img.paste(next_bg, (empty_image.size[0]-round(movement_speed * frame_index), 0), next_bg)
            if frame_index >= transition_duration:
                in_transition = False
                bg_index += 1
                frame_index = 0
            pass

        to_stamp = get_stamp(stamp, i)
        img.paste(to_stamp, (0, 0), to_stamp.convert("RGBA"))
        frames.append(img)
        pass

    frames[0].save("myGif2.gif", format="GIF", append_images=frames, save_all=True, duration=full_duration_ms/full_duration_frames, loop=0)


def get_stamp(stamp, i):
    if stamp.is_animated:
        stamp.seek(i % stamp.n_frames)
    return stamp


if __name__ == '__main__':
    main()
