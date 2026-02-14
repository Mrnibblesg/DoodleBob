import cv2 as cv
import sys
import matplotlib.pyplot as plt

if (len(sys.argv) < 2):
    raise ValueError(f"Expected at least one command line argument, got {len(sys.argv) - 1}")


def main():
    # Take input image, convert to black and white with thresholding
    fig, ax = plt.subplots(1, 2)

    img = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)

    img_color = cv.imread(sys.argv[1])
    img_color = cv.cvtColor(img_color, cv.COLOR_BGR2RGB)

    ax[0].imshow(img, cmap='gray')
    ax[1].imshow(img_color)
    plt.show()


if __name__ == "__main__":
    main()
