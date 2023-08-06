import cv2
import usb

import time
import numpy as np

from rich.progress import Progress
from rich.console import Console
import click

from pathlib import Path

console = Console()

def print_info(message):
    console.log(f":information_source: {message}")

def print_success(message):
    console.log(f":heavy_check_mark: {message}")

def print_error(message):
    console.log(f":x: {message}")

def reset_usb(vendor, product, sleep_s=1):
    vendor_int = int(vendor, 16)
    vendor_hex = hex(vendor_int)
    product_int = int(product, 16)
    product_hex = hex(product_int)
    print_info(f'Resetting USB device with vendor ID {vendor_hex} and product ID {product_hex}')
    dev = usb.core.find(idVendor=vendor_int, idProduct=product_int)
    dev.reset()

    time.sleep(sleep_s)
    print_success(f'USB device reset successfull')

def get_time_in_ms():
    curr_time = round(time.time()*1000)
    return curr_time

@click.command()
@click.option('--width', default=1280, help='Height of the resolution')
@click.option('--height', default=720, help='Width of the resolution')
@click.option('--base_output_path', default="./recording", help='The target base path to store the recording files')
@click.option('--folder_name', help='The name of the folder to store the current recording at', required=True)
@click.option('--fps', default=30, help='The fps for the recording')
@click.option('--time_in_seconds', default=10, help='The time in seconds to record for')
@click.option('--fourcc', default="GREY", help="The fourcc to be used for the recording")
@click.option('--device', default=0, help="The device to use for the recording")
@click.option('--vendor_id', help="The ID of the vendor to reset", required=True)
@click.option('--product_id', help="The ID of the product to reset", required=True)
@click.option('--exposure', help="The exposure value", default=255)
def main(width, height, base_output_path, folder_name, fps, time_in_seconds, fourcc, device, vendor_id, product_id, exposure):
    reset_usb(vendor_id, product_id)

    final_path = base_output_path + "/" + folder_name
    if (Path(final_path).exists()):
        print_error(f"{final_path} already exists and can't be reused")
        return

    Path(final_path).mkdir(parents=True, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*fourcc)
    cap = cv2.VideoCapture(device)

    cap.set(cv2.CAP_PROP_FOURCC, fourcc)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)

    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

    print_info("Starting recording:")

    start = get_time_in_ms()
    frame_count = 0
    with Progress() as progress:

        task1 = progress.add_task("[red]Recording: ", total=time_in_seconds)
        previous = start

        try:
            while not progress.finished:
                ret, frame = cap.read()
                if ret:
                    frame_count+=1
                    cv2.imwrite(final_path + "/" + str(frame_count) + ".jpg", frame)
                now = get_time_in_ms()
                progress.update(task1, advance=(now - previous) / 1000)
                previous = now
        finally:
            cap.release()

    print_success(f"Recording Finished > {frame_count/time_in_seconds} FPS")

def run():
    main()


if __name__ == "__main__":
    run()