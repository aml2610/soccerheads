import cv2
import numpy as np


BLACK_PATCH_COLOUR_HSV = np.uint8([[[0, 100, 0]]])
BLACK_PATCH_N_SIDES = 5
BLACK_PATCH_AREA_LOWER_LIMIT = 50
BLACK_PATCH_AREA_LOWER_HIGHER_LIMIT = 100


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
        return centroids_found[0]
    else:
        return None
