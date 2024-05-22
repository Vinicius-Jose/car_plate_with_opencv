from array import array
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr

DEFAULT_PATH = "./app/image/"


def read_image(img_path: str) -> cv2.typing.MatLike:
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img, gray


def apply_filter(img: cv2.typing.MatLike) -> cv2.typing.MatLike:
    bfilter = cv2.bilateralFilter(img, 11, 17, 17)
    edged = cv2.Canny(bfilter, 30, 200)
    return edged


def find_countours(img: cv2.typing.MatLike) -> array:
    keypoints = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    return location


def apply_mask(
    img: cv2.typing.MatLike, gray_img: cv2.typing.MatLike, location_countours: array
):
    mask = np.zeros(gray_img.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location_countours], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    return new_image, mask


def cropp_image(gray_img: cv2.typing.MatLike, mask: np.array) -> np.array:
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray_img[x1 : x2 + 1, y1 : y2 + 1]
    return cropped_image


def read_text_from_img(cropped_img: np.array) -> array:
    reader = easyocr.Reader(["pt"])
    result = reader.readtext(cropped_img)
    return result


def save_result(
    text: str, img: cv2.typing.MatLike, countours: array, file_name: str
) -> str:
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(
        img,
        text=text,
        org=(countours[0][0][0], countours[1][0][1] + 60),
        fontFace=font,
        fontScale=1,
        color=(0, 255, 0),
        thickness=2,
        lineType=cv2.LINE_AA,
    )
    res = cv2.rectangle(
        img, tuple(countours[0][0]), tuple(countours[2][0]), (0, 255, 0), 3
    )
    file_path = save_img("result_" + file_name, res)
    return file_path


def save_img(file_name: str, img: cv2.typing.MatLike) -> None:
    file_path = DEFAULT_PATH + file_name
    plt.imsave(file_path, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return file_path


def main():

    while True:
        img_path = input("Input the image path: ")
        if not img_path:
            break
        file_name = img_path.split("/")[-1]

        img, gray_image = read_image(img_path)
        save_img("001_" + file_name, gray_image)

        img_filter = apply_filter(gray_image)
        save_img("002_" + file_name, img_filter)

        countours = find_countours(img_filter)
        new_img, mask = apply_mask(img, gray_image, countours)
        save_img("003_" + file_name, new_img)

        cropped_image = cropp_image(gray_image, mask)
        save_img("004_" + file_name, cropped_image)

        result = read_text_from_img(cropped_image)
        text = [item[-2] for item in result]
        text = " ".join(text)
        result_path = save_result(text, img, countours, file_name)
        print("CAR LICENSE PLATE: ", text)
        print("Result save : ", result_path)


if __name__ == "__main__":
    main()
