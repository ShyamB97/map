"""
Created on: 10/05/2025 17:37

Author: Shyam Bhuller

Description: Visualise gpx files on a map in your browser.
#? add smoothing to the paths?
#? customization options for the map?
#? add custom markers for personal POIs?
"""

import argparse
import glob
import time

from rich import print

import render

def timer(func):
    """ Decorator which times a function.

    Args:
        func (function): function to time
    """
    def wrapper_function(*args, **kwargs) -> object:
        """ Times funcions, returns outputs
        Returns:
            any: func output
        """
        s = time.time()
        out = func(*args,  **kwargs)
        print(f'{func.__name__!r} executed in {(time.time()-s):.4f}s')
        return out
    return wrapper_function

@timer
def main(args : argparse.Namespace):
    gpxs = glob.glob(f"{args.file_path}/*.gpx")

    print(gpxs)
    m = render.render_map(gpxs)
    if args.export_html:
        m.write_html("map.html")
        print("map saved as map.html")
    else:
        m.show()

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Visualise gpx files on a map in your browser.")
    parser.add_argument(dest = "file_path", help = "File path where the gpx files are located.")
    parser.add_argument("--export_html", action = "store_true", help = "Save the rendered map to a html file.")
    args = parser.parse_args()
    print(args)
    main(args)