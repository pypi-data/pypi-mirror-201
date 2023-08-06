from pydantic import BaseModel, conlist
from typing import List
from glsm.features import Feature
import math

class NonPredictive(BaseModel):
    '''
    A non predictive lead scoring model.
    '''
    features: conlist(Feature) = []
    round_decimals: int = 2

    def add_features(self, features: List[Feature]):
        '''
        Adds a list of features to the model.

        All items must be of type Feature otherwise raises a TypeError.
        '''
        for feature in features:
            if not isinstance(feature, Feature):
                raise TypeError("All element of the list must be of type Feature")

        self.features.extend(features)

    def remove_features(self, features: List[str]):
        '''
        Removes a list of features from the model given their names.
        '''

        for i in range(len(features)):
            for feature in self.features:
                if feature.name == features[i]:
                    self.features.remove(feature)


    def compute_lambda(self, lead: dict) -> float:
        '''
        Computes Lead score of a given lead.
        '''

        self.compute_normalized_weights()

        lambda_value = sum(
            [
                (feature.normalized_weight**2) * feature.get_points(lead[feature.name])
                for feature in self.features
            ]
        )

        return round(lambda_value, self.round_decimals)

    def compute_normalized_weights(self):
        '''
        Computes the normalized weights of the model features.

        The normalized weight of a feature is the weight of the feature divided by the magnitude of the weights of all the features.
        '''

        magnitude = math.sqrt(
            sum([feature.weight**2 for feature in self.features])
        )

        for feature in self.features:
            feature.normalized_weight = feature.weight / magnitude

    def describe_features(self,):
        '''
        '''

        description = {}

        for feature in self.features:
            description[feature.name] = {
                "weight": feature.weight,
                "normalized_weight": round(
                    feature.normalized_weight,
                    self.round_decimals
                )
            }

        print(description)

        return description





