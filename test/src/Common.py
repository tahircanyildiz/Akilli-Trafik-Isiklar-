# Enum, benzersiz, sabit değerlere bağlı bir dizi
# sembolik ad (üyeler) olan numaralandırmalar oluşturmak için python'da bir sınıftır. 
from enum import Enum


class Lane(Enum):
    left_to_right = 1
    right_to_left = 2
    bottom_to_top = 3
    top_to_bottom = 4

#Trafik Durumu
class TrafficStatus(Enum):
    red = 1
    green = 2
    yellow = 3


class DoubleLane(Enum):
    Horizontal = 1
    Vertical = 2
