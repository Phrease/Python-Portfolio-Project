# Import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
iris = load_iris()
X = iris.data # The flower measurement (features)
y = iris.target # The flower species (labels)

# Split the data into training and testing sets
# We'll 'train' the model on 80% of the data and 'test' it on the remaining 20%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# We're using a Decision Tree, which learns a set of if/else rules from the data
model = DecisionTreeClassifier()
model.fit(X_train, y_train) # This is the training step

# Now we ask the trained model to predict the species for the test set measurements
predictions = model.predict(X_test)

# We compare the model's predictions to the actual correct species
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy:.2f}") # Formats the output to two decimal places

# Let's ay we found a flower with these specific measurements:
# sepal length=5.1cm, sepal width=3.5cm, petal length=1.4cm, petal width=0.2cm
new_flower = [[5.1, 3.5, 1.4, 0.2]]
predicted_species = model.predict(new_flower)
predict_species_name = iris.target_names[predicted_species[0]]
print(f"Predicted Species for new flower: {predict_species_name}")

# Next we'll visualize this data.
# We'll convert the data to a pandas DataFrame for easier plotting with seaborn
import pandas as pd
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['species'] = iris.target_names[iris.target]

# Create a pair plot colored by species
sns.pairplot(df, hue='species')
plt.suptitle('Iris Dataset Pair Plot', y=1.02) # Add a title above the plot
plt.show()