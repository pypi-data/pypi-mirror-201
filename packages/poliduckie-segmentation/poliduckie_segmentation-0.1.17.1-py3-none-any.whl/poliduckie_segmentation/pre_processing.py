import cv2
import pickle
import os

'''
BirdEyeView HOW TO USE

- Set the FILE_NAME to the pickle file containing the transformation matrix
- Instance an object
- Compute the transformation by calling obj.computeBirdEye(desired image)

'''


class BirdEyeView():

    def __init__(self, path=None):
        pkg_path = os.path.abspath(__file__)
        model_path = path if path != None else os.path.join(
            os.path.dirname(pkg_path), 'BirdEyeCalibration', 'BirdEyeMatrix.pkl')
        file = open(model_path, 'rb')
        self.Matrix = pickle.load(file)
        pass

    def computeBirdEye(self, img):
        return cv2.warpPerspective(img, self.Matrix, img.shape[:2][::-1])

    def comuteInverseBirdEye(self, img):
        return cv2.warpPerspective(img, self.Matrix, img.shape[:2][::-1], flags=cv2.WARP_INVERSE_MAP)
