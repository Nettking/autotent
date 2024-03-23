import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Load the image
image = cv2.imread('input.png')

# Reshape the image to a 2D array of pixels
pixels = image.reshape(-1, 3)

# Prepare data
X = pixels.astype(np.float32)  # Convert to float32
y = np.arange(len(X))          # Each pixel is assigned a unique label

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the KNN model
k = 5  # Number of neighbors
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)

# Classify pixels
predicted_labels = knn.predict(X)

# Reshape the predicted labels back to the shape of the original image
classified_image = predicted_labels.reshape(image.shape[0], image.shape[1])

# Visualize the classified image
cv2.imshow('Classified Image', classified_image.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
