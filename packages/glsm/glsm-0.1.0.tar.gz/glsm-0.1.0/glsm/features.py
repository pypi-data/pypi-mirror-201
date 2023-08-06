from pydantic import BaseModel, validator
from typing import List, Tuple

class Feature(BaseModel):
    '''
    A feature of a model.
    '''

    name: str
    points_map: List[Tuple[str, float]] # (label, points)
    weight: float
    normalized_weight: float = None

    def get_points(self, label: str) -> float:
        '''
        Returns the points assigned to the label of a feature.
        '''
        for item in self.points_map:
            if item[0] == label:
                return item[1]
        return None







