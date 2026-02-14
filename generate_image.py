import cv2 as cv
import sys
if (len(sys.argv) < 2):
    raise ValueError(f"Expected at least one command line argument, got {len(sys.argv) - 1}")


def main():
    print(sys.argv)
    # Take input image, convert to black and white with thresholding
    try:

        img = cv.imread()
    except:



if __name__ == "__main__":
    main()
