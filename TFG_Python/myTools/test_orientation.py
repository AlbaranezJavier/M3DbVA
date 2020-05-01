import numpy as np
from math import atan, degrees
from matplotlib import pyplot as plt
from sklearn import linear_model

'''
Script, realiza una regresión linear con el algoritmo RANSAC. Representando los resultados obtenidos en una gráfica.
'''
def get_orientation(X, y):
    ransac = linear_model.RANSACRegressor()
    ransac.fit(X, y)

    line_X = np.array([X.min(), X.max()])[:, np.newaxis]
    line_y_ransac = ransac.predict(line_X)
    a = X.item(4) - X.item(0)
    b = line_y_ransac[1] - line_y_ransac[0]
    if b == 0:
        return 0
    else:
        return degrees(atan(a / b))

if __name__ == '__main__':
    n_samples = 4
    n_outliers = 1

    X = np.array([[541], [560], [579], [598], [617], [637], [656], [675], [694], [713], [550], [569], [589], [608], [627], [646], [665], [685], [704], [723]])
    y = np.array([183, 183, 182, 177, 175, 173, 178, 180, 184, 188, 192, 183, 180, 177, 176, 179, 180, 183, 184, 186])

    # Robustly fit linear model with RANSAC algorithm
    ransac = linear_model.RANSACRegressor()
    ransac.fit(X, y)
    inlier_mask = ransac.inlier_mask_
    outlier_mask = np.logical_not(inlier_mask)

    # Predict data of estimated models
    line_X = np.array([X.min(), X.max()])[:, np.newaxis]
    line_y_ransac = ransac.predict(line_X)
    a = abs(line_y_ransac[1] - line_y_ransac[0])
    b = X.item(len(X) - 1) - X.item(0)
    if b == 0:
        print(0)
    else:
        diff = -1 if X.min() < X.max() else 1
        print(int(degrees(atan(a / b)))*diff)

    lw = 2
    plt.scatter(X[inlier_mask], y[inlier_mask], color='yellowgreen', marker='.',
                label='Inliers')
    plt.scatter(X[outlier_mask], y[outlier_mask], color='gold', marker='.',
                label='Outliers')
    plt.plot(line_X, line_y_ransac, color='cornflowerblue', linewidth=lw,
             label='RANSAC regressor')
    plt.legend(loc='lower right')
    plt.xlabel("Input")
    plt.ylabel("Response")
    plt.show()