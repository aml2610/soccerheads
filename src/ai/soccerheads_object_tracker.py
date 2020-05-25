import cv2
import numpy as np


# Ball detection params
BLACK_PATCH_COLOUR_HSV = np.uint8([[[0, 100, 0]]])
BLACK_PATCH_N_SIDES = 5
BLACK_PATCH_AREA_LOWER_LIMIT = 50
BLACK_PATCH_AREA_LOWER_HIGHER_LIMIT = 100

# My player detection params
MY_PLAYER_TEMPLATE = cv2.imread("resources/my_player_template.png", 0)
MY_PLAYER_TEMPLATE_W, MY_PLAYER_TEMPLATE_H = MY_PLAYER_TEMPLATE.shape[::-1]


def get_contour_n_sides(contour):
    peri = cv2.arcLength(contour, True)
    return len(cv2.approxPolyDP(contour, 0.04 * peri, True))


def get_current_ball_position(frame):
    bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
    hsv_frame_only_black_objects = cv2.inRange(
        hsv_frame,
        BLACK_PATCH_COLOUR_HSV,
        BLACK_PATCH_COLOUR_HSV
    )
    edged = cv2.Canny(hsv_frame_only_black_objects, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    centroids_found = []

    for contour in contours:
        n_sides = get_contour_n_sides(contour)
        area = cv2.contourArea(contour)
        if n_sides is BLACK_PATCH_N_SIDES and BLACK_PATCH_AREA_LOWER_LIMIT < area < BLACK_PATCH_AREA_LOWER_HIGHER_LIMIT:
            M = cv2.moments(contour)
            if M["m00"]:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centroids_found.append((cX, cY))
    if len(centroids_found):
        # cv2.circle(frame, centroids_found[0], 10, (0, 255, 0), -1)
        # cv2.imwrite("image1.png", frame)
        return centroids_found[0]
    else:
        return None


def get_current_my_player_position(frame):
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(grayscale_frame, MY_PLAYER_TEMPLATE, cv2.TM_SQDIFF)
    _, _, min_loc, _ = cv2.minMaxLoc(res)
    if min_loc is not None:
        centroid = (min_loc[0] + int(MY_PLAYER_TEMPLATE_W / 2), min_loc[1] + int(MY_PLAYER_TEMPLATE_H / 2))
        # cv2.circle(frame, centroid, 10, (255, 255, 0), -1)
        # cv2.imwrite("image2.png", frame)
        return centroid
    else:
        return None
