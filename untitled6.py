# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hkMD6Bi1J-lAE0d5Zvjk61TdsRwLlKv2
"""

# Required Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("Fixed_Columns_Medicine_Details.csv")
df.info()

# Data Cleaning
df_cleaned = df.dropna(subset=['side_effects'])

for col in ['excellent_review_%', 'average_review_%', 'poor_review_%']:
    df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)

# Extract primary side effect
df_cleaned['primary_side_effect'] = df_cleaned['side_effects'].apply(
    lambda x: x.split()[0] if isinstance(x, str) else 'Unknown'
)

# Focus on top 10 frequent side effects
top_10 = df_cleaned['primary_side_effect'].value_counts().nlargest(10).index
df_filtered = df_cleaned[df_cleaned['primary_side_effect'].isin(top_10)].copy()

# Encode target
label_encoder = LabelEncoder()
df_filtered['side_effect_encoded'] = label_encoder.fit_transform(df_filtered['primary_side_effect'])

# Features and target
X = df_filtered[['excellent_review_%', 'average_review_%', 'poor_review_%']]
y = df_filtered['side_effect_encoded']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
conf_matrix = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
print("Classification Report:\n", report)

sns.set(style="whitegrid")

# 1. Review Score Distributions
fig, axs = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(df_filtered['excellent_review_%'], bins=30, ax=axs[0], color="green")
axs[0].set_title("Excellent Review %")
sns.histplot(df_filtered['average_review_%'], bins=30, ax=axs[1], color="blue")
axs[1].set_title("Average Review %")
sns.histplot(df_filtered['poor_review_%'], bins=30, ax=axs[2], color="red")
axs[2].set_title("Poor Review %")
plt.tight_layout()
plt.show()

# 2. Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df_filtered[['excellent_review_%', 'average_review_%', 'poor_review_%']].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Between Review Scores")
plt.show()

# 3. Count of Side Effects
plt.figure(figsize=(10, 6))
sns.countplot(data=df_filtered, y='primary_side_effect',
              order=df_filtered['primary_side_effect'].value_counts().index,
              palette="Set2")
plt.title("Top 10 Side Effects")
plt.xlabel("Count")
plt.ylabel("Side Effect")
plt.show()

# 4. Boxplot: Excellent Review % by Side Effect
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_filtered, x='primary_side_effect', y='excellent_review_%', palette='pastel')
plt.xticks(rotation=45)
plt.title("Excellent Review % by Side Effect")
plt.show()

# 5. Confusion Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='YlGnBu',
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(df_filtered['excellent_review_%'], df_filtered['poor_review_%'], alpha=0.5)
plt.title('Scatter Plot: Excellent Review % vs Poor Review %')
plt.xlabel('Excellent Review %')
plt.ylabel('Poor Review %')
plt.grid(True)
plt.show()

side_effect_counts = df_filtered['primary_side_effect'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(side_effect_counts, labels=side_effect_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Top 10 Side Effects')
plt.show()

sns.pairplot(df_filtered[['excellent_review_%', 'average_review_%', 'poor_review_%']])
plt.suptitle('Pair Plot of Review Scores', y=1.02)
plt.show()

plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
sns.violinplot(x='primary_side_effect', y='excellent_review_%', data=df_filtered, palette='Set3')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.title('Distribution of Excellent Review % by Primary Side Effect')
plt.xlabel('Primary Side Effect')
plt.ylabel('Excellent Review %')
plt.tight_layout()  # Adjust layout to prevent overlapping elements
plt.show()