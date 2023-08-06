# Generic Lead Scoring Model
## About
`glsm` is a user-friendly Python package that simplifies the process of building lead scoring models. It supports both predictive and non-predictive models, providing flexibility and ease of use.

The goal of the lead score is to provide a qualification metric for comparison between leads. It is based on product interest and company interaction data.

### Predictive Model
Soon!
### Non-predictive Model

| Name | Description | Variable |
|------------ |------------|------------|
Weight| Feature weight   that represents the relative importance of each feature | $$w$$
Points| Assigned points of each feature | $$p$$
Normalized weight | Weights unit vector normalization | $${\hat{w}} = \frac{w_n}{\sqrt{\sum\limits^{n}_{i=0}w_i^2}}$$
Lead score | A weighted sum of assigned points for each feature, where the feature weights are normalized to form a unit vector. | $$\lambda = \sum_{i=1}^n {\hat{w}_i^2}{p_i}$$

***

## Index
1. [About](#about)
    1. [Predictive Model](#predictive-model)
    2. [Non-predictive Model](#non-predictive-model)
2. [Disclaimer](#disclaimer)
3. [Installation](#installation)
4. [Theory](#understanding-the-models)
    1. [Predictive Model](#predictive-model-1)
    2. [Non-predictive Model](#non-predictive-model-1)
        1. [Weight (${w}$):](#weight-w)
        2. [Normalized Weight (${\hat{w}}$):](#normalized-weight-hatw)
            1. [Unit vector nomalization:](#unit-vector-nomalization)
            2. [Feature vector magnitude:](#feature-vector-magnitude)
            3. [Normalized weight vector:](#normalized-weight-vector)
        3. [Points (${p}$):](#points-p)
        4. [Lead Score ($\lambda$):](#lead-score-lambda)
        5. [Features ($f_n$)](#features-f1f2f3--fn)
5. [Usage](#usage)
    1. [Predictive Model](#predictive-model-2)
    2. [Non-predictive Model](#non-predictive-model-2)
        1. [Importing the library](#importing-the-library)
        2. [Instantiating the model and adding features](#instantiating-the-model-and-adding-features)
        3. [Importing lead data](#importing-lead-data)
            1. [From a dictionary](#from-a-dictionary)
            2. [From a csv](#from-a-csv)
        4. [Calculating the lead score](#calculating-the-lead-score)


## Disclaimer
This library is in active development. Suggestions and contributions are welcome.
## Installation
### Requirements
- pydantic

Can be installed using pip:
```bash
pip install glsm
```
***
# Theory
There are two ways for you to understand the proposed models:

1. Through the [Google Sheets simulator](https://docs.google.com/spreadsheets/d/1ESEtcjno36ZLW5XMEoHqLKHjiZMkrZeIECcrcgFxHzA/edit?usp=sharing) (Non-predictive only)
2. Reading the following sections
## Predictive Model
Soon!

***
## Non-predictive Model

This model and the following set of rules are a suggestion to get you started. You can use them as a starting point and adapt them to your business needs.
The library is flexible enough to allow you to use your own assumptions and  rules.


The non-predictive model has the following characteristics:
1. It avoids the use of predictive algorithms, which can be data-intensive and require significant computational power and technical expertise to operate effectively.
2. It uses relative feature weights, meaning that the inclusion of a new feature won't change the weights of the existing ones. This can simplify the implementation and interpretation of the model.
3. It provides a score that ranges from 0 to 100 points, with 50 being the minimum threshold for lead qualification. The score reflects the current objectives and scenarios of the company, allowing for comparisons of lead performance over time.

###  Weight (${w}$):
Feature weight is a value that multiplies the points assigned to each feature. It is used to differentiate the importance of each feature.

You can make it easier to understand by thinking of it as a multiplier. The higher the weight, the more important the feature is. You can use any range of values (due to the unit vector normalization), but it is easier to interpret if the weights are between 0 and 1.

Suppose you choose to use values from 0 to 1. Your most important feature will have a weight of 1. Other features should have a weight less than 1.


### Normalized Weight (${\hat{w}}$):
The model needs to be flexible and adaptable to accommodate changes in the business environment. Sometime after the model is built, the company may change its focus or process. In this case, features may need to be added or removed.

The normalized weight is a unit vector that is used to scale data in a way that preserves the relative relationships between the features when new features are added.

The basic idea is to transform the data such that the magnitude of the vector formed by the features is equal to 1. This ensures that each feature is scaled proportionally to the others, so the relative relationships between them is preserved when new features are added.

You may be asking yourself, why not just recalculate the weights after adding or removing a feature?
Well, this may work if you have the original data and just want to make a report out of it, but once you calculate the lead score and send the conversion events to plaftorms such as Google Analytics, Facebook Ads, etc, the scores registered in those platforms can't be changed. Later on you may want to create audiences based on the lead score, but you won't be able to do that if the scoring model has changed. The normalized weight vector solves this problem.

<!-- #TODO rewrite this section -->

#### Unit vector nomalization:
$$
\hat{w_n} = \frac{w_n}{|w|}
$$
#### Feature weights vector magnitude:
$$
|w| = \sqrt{\sum\limits^{n}_{i=0}w_i^2}
$$

#### Normalized weight vector:

$$
\hat{w_n} = \frac{w_n}{\sqrt{\sum\limits^{n}_{i=0}w_i^2}}
$$

In this way the sum of the squares of the normalized weights is equal to 1:

$$
\sum\limits^{n}_{i=0}{\hat{w}_i^2} = 1
$$


### Points ($p$):
Assigned points per feature.The score assigned to each option of a feature. 50 shloud  assigned to the option that represents your ICP.



These numbers are only a suggestion. You can use any range of values, but it is easier to interpret if the points are $0  \leq p \geq 100$ and 50 is the ICP.

### Lead Score ($\lambda$):
Lead score is the sum of squares the normalized weights of each feature multiplied by the points assined to each feature.


$$
\lambda = \sum_{i=1}^n {\hat{w}_i^2}{p_i} = ({\hat{w}_1^2}{p_1})+({\hat{w}_2^2}{p_2})+({\hat{w}_3^2}{p_3})...({\hat{w}_n^2}{p_n})
$$

### Features ($f_n$)
Features are a set of characteristics assigned to each lead. If you have difficulties finding out which features to add, start by adding relevant lead form or CRM fields as features.

Each feature has points associated with it, which are assigned to each option of the feature. The points assigned to each option are relative to the minimum viable option for the lead to be considered qualified (50 points).

You should first define the features and their options, then assign 50 points to the minimum viable option for the lead to be considered qualified. The remaining points should be distributed among the other options in a way that reflects the relative importance of each option.

In this way if $\lambda \geq 50$ the lead is considered qualified.

Remember that this is a suggestion, you can assign the points as you see fit and as your business requires. You may want to use negative points to penalize leads that do not meet certain criteria for example. It is generally easier to work with positive points, but it is up to you.

#### Example:
| Monthly Website Users | Points|
|------------ | ------------|
Up to 50k | 30
50k - 100k | 50 (ICP)
100k - 200k | 80
More than 200k | 100

***


# Usage
## Predictive Model
Soon!
## Non-predictive Model
In the examples folder you can find a Jupyter Notebook with a step-by-step guide on how to use the library.
You may also want to check the [Google Sheets simulator](https://docs.google.com/spreadsheets/d/1ESEtcjno36ZLW5XMEoHqLKHjiZMkrZeIECcrcgFxHzA/edit?usp=sharing) (Non-predictive only)
### Importing the library
```python
from glsm.non_predictive import NonPredictive
from glsm.features import Feature
```
### Instantiating the model and adding features
```python
model = NonPredictive()

feature_a = Feature(
    name="Monthly Users",
    weight=0.5,
    points_map=[
        ("Up to 50K",00),
        ("50K - 100K",50),
        ("100K - 200K",70),
        ("More than 200K",100),
    ]
)

feature_b = Feature(
    name="Industry",
    weight=0.25,
    points_map=[
        ("Technology",70),
        ("Real State",20),
        ("Retail",50),
        ("Education",50),
        ("Health",100),
    ]
)

model.add_features([feature_a, feature_b])
```

### Importing lead data
#### From a dictionary
```python
lead = { # lambda = 81.43
        "Monthly Users": "50K - 100K",
        "Industry": "Technology",
        "Mkt Investment": "$300K - $400K",
    }
```
#### From a csv
```python
import csv

with open('leads.csv', 'r') as file:
    if file.read(3) == b'\xef\xbb\xbf':
        file.seek(3)
    csv_reader = csv.reader(file)
    headers = next(csv_reader)

    # New csv file adding lambda values
    with open('leads_with_lambda.csv', 'w', newline='') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(headers + ['lambda'])

        for row in csv_reader:
            lead = dict(zip(headers, row))
            lambda_value = model.compute_lambda(lead)
            csv_writer.writerow(row + [lambda_value])

```

### Calculating the lead score
```python
lambda_value = model.compute_lambda(lead)
```



