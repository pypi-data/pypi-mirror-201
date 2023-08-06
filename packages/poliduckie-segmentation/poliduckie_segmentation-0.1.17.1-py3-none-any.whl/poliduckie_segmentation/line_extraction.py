'''
HOW TO USE:
This class takes care of extracting the lines from a binary image.
It uses K-means clustering to find the centroids of the lines. Then it uses PCA to rotate the centroids so that they are sorted by their x coordinate.
The class also provides a method to fit a bezier curve to the centroids, as well as a method to get a spline representation of the curve.

The class can be used as follows:
    lineExtraction = LineExtraction()
    x, y, pca = lineExtraction.extract_centroids(img)
    bezier_points = lineExtraction.fit_bezier(x, y, degree=3, n_points=100)
    spline_points = lineExtraction.fit_spline(x, y, n_points=100)
'''

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.special import comb
from scipy.interpolate import splrep, splev
import cv2


class LineExtraction:
    N_CLUSTERS = 15
    MIN_ENTRIES = 8
    MAX_DISTANCE = 80

    def __init__(self):
        pass

    def getCentroids(points):
        # K means clustering
        kmeans = KMeans(n_clusters=LineExtraction.N_CLUSTERS,
                        n_init=10).fit(points)
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_

        # remove centroids with too few points
        newCentroids = []
        for i in range(centroids.shape[0]):
            if np.sum(labels == i) >= LineExtraction.MIN_ENTRIES:
                newCentroids.append(centroids[i])
        centroids = np.array(newCentroids)

        return centroids

    def PCAreduce(self, centroids):
        pca = PCA(n_components=2)
        pca.fit(centroids)
        return pca.transform(centroids), pca

    def filter_centroids(centroids):
        # remove centroids that are too distant from each other
        newCentroids = []
        for i in range(centroids.shape[0]):
            if i == 0:
                newCentroids.append(centroids[i])
            else:
                if np.linalg.norm(centroids[i] - centroids[i-1]) < LineExtraction.MAX_DISTANCE:
                    newCentroids.append(centroids[i])

        return np.array(newCentroids)

    def extract_centroids(self, img, usePCA=True):
        # Extract non zero points
        points = np.argwhere(img > 0)
        points = np.fliplr(points)

        # If there are no points, return None
        if len(points) == 0:
            return None

        # Get centroids
        centroids = LineExtraction.getCentroids(points)

        if usePCA:
            # Rotate the centroids
            pcaCentroids, pca = self.PCAreduce(centroids)

            # sort the centroids by their x coordinate
            pcaCentroids = pcaCentroids[np.argsort(pcaCentroids[:, 0])]

            # filter centroids
            pcaCentroids = LineExtraction.filter_centroids(pcaCentroids)

            # Get the x and y coordinates
            x, y = pcaCentroids[:, 0], pcaCentroids[:, 1]

        else:
            # sort the centroids by their y coordinate
            centroids = centroids[np.argsort(centroids[:, 1])]

            # filter centroids
            centroids = LineExtraction.filter_centroids(centroids)

            # If PCA is not used, return the original centroids
            x, y = centroids[:, 0], centroids[:, 1]

        return x, y, pca if usePCA else None

    def get_bezier_parameters(X, Y, degree=3):
        """ Least square qbezier fit using penrose pseudoinverse.

        Parameters:

        X: array of x data.
        Y: array of y data. Y[0] is the y point for X[0].
        degree: degree of the Bézier curve. 2 for quadratic, 3 for cubic.

        Based on https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy
        and probably on the 1998 thesis by Tim Andrew Pastva, "Bézier Curve Fitting".
        """
        if degree < 1:
            raise ValueError('degree must be 1 or greater.')

        if len(X) != len(Y):
            raise ValueError('X and Y must be of the same length.')

        if len(X) < degree + 1:
            raise ValueError(f'There must be at least {degree + 1} points to '
                             f'determine the parameters of a degree {degree} curve. '
                             f'Got only {len(X)} points.')

        def bpoly(n, t, k):
            """ Bernstein polynomial when a = 0 and b = 1. """
            return t ** k * (1 - t) ** (n - k) * comb(n, k)
            # return comb(n, i) * ( t**(n-i) ) * (1 - t)**i

        def bmatrix(T):
            """ Bernstein matrix for Bézier curves. """
            return np.matrix([[bpoly(degree, t, k) for k in range(degree + 1)] for t in T])

        def least_square_fit(points, M):
            M_ = np.linalg.pinv(M)
            return M_ * points

        T = np.linspace(0, 1, len(X))
        M = bmatrix(T)
        points = np.array(list(zip(X, Y)))

        final = least_square_fit(points, M).tolist()
        final[0] = [X[0], Y[0]]
        final[len(final)-1] = [X[len(X)-1], Y[len(Y)-1]]
        return np.array(final)

    def bernstein_poly(i, n, t):
        """
        The Bernstein polynomial of n, i as a function of t
        """
        return (t**(n-i)) * (1 - t)**i * comb(n, i)

    def bezier_curve(points, nTimes=50):
        """
        Given a set of control points, return the
        bezier curve defined by the control points.

        points should be a list of lists, or list of tuples
        such as [ [1,1],
                    [2,3],
                    [4,5], ..[Xn, Yn] ]
            nTimes is the number of time steps, defaults to 1000

            See http://processingjs.nihongoresources.com/bezierinfo/
        """

        nPoints = len(points)
        xPoints = np.array([p[0] for p in points])
        yPoints = np.array([p[1] for p in points])

        t = np.linspace(0.0, 1.0, nTimes)

        polynomial_array = np.array(
            [LineExtraction.bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)])

        xvals = np.dot(xPoints, polynomial_array)
        yvals = np.dot(yPoints, polynomial_array)
        return np.array([xvals, yvals])

    def bezier_fit(self, img, degree=5, nPoints=100, usePCA=False):
        x, y, pca = self.extract_centroids(img, usePCA=usePCA)

        controls = LineExtraction.get_bezier_parameters(x, y, degree=degree)

        if usePCA:
            controls = pca.inverse_transform(np.array(controls))

        bpoints = LineExtraction.bezier_curve(controls, nTimes=nPoints)

        return bpoints

    def spline_interpolation(self, img, nPoints=100, usePCA=False):
        y, x, pca = self.extract_centroids(img, usePCA)

        if usePCA:
            x, y = y, x

        tck = splrep(x, y)
        xnew = np.linspace(min(x), max(x), nPoints)
        ynew = splev(xnew, tck)

        if usePCA:
            ynew, xnew = pca.inverse_transform(np.array([xnew, ynew]).T).T
        return np.array([ynew, xnew])


if __name__ == '__main__':
    from matplotlib import pyplot as plt

    # Load image
    img = cv2.imread('a.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.inRange(img, (254, 254, 0), (256, 256, 0))

    # Extract lines
    lineExtraction = LineExtraction()
    bezier_lines = lineExtraction.bezier_fit(img, usePCA=False)
    spline_lines = lineExtraction.spline_interpolation(img, usePCA=False)

    plt.imshow(img, cmap='gray')
    plt.plot(bezier_lines[0], bezier_lines[1],
             linewidth=5, color='red', label='bezier', alpha=0.8)
    plt.plot(spline_lines[0], spline_lines[1],
             linewidth=5, color='blue', label='spline', alpha=0.8)
    plt.legend()

    plt.show()
