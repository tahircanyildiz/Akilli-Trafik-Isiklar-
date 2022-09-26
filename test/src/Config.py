# NumPy (Numerical Python) - matematik kütüphanesidir 
# bilimsel hesaplamaları hızlı bir şekilde yapmamızı sağlıyor
# Numpy’ın temelini numpy dizileri oluşturur.
# python listelerinden daha hızlı
import numpy as np

Config = {
    # araba ayarla
    'vehicle': {
        # hizi = 5 veriyoruz
        'speed': 5,
        # Güvenli mesafe = 5 veriyoruz 
        'safe_distance': 5,
        # arabanın uzunluğu
        'body_length': 25,
        # arabanın genişliği
        'body_width': 15,
        # faktörü
        'safe_spawn_factor': 1.1
    },

    # simülatör ayarla
    'simulator': {
        # ekranın genişliği
        'screen_width': 600,
        # ekranın yüksekliği
        'screen_height': 600,
        # arabanın tamponu
        'bumper_distance': 5,
        # sınıfı
        'spawn_rate': {
            # hızlı
            'fast': 400,  # millisecond
            # orta
            'medium': 1500,  # millisecond
            # yavaş
            'slow': 3500,  # millisecond
        },

        'frame_rate': 30,
        'gap_between_traffic_switch': 2,  # second
        'moving_averages_period': 1,  # second
        'static_duration': 1,  # second
        'seconds_before_extension': 1,  # second
        'fuzzy_notification_duration': 5  #second
    },
    # renkleri ayarla
    'colors': {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'dark_gray': (169, 169, 169),
        'traffic_yellow': (250, 210, 1),
        'traffic_green': (34, 139, 94),
        'traffic_red': (184, 29, 19),
        'red': (255, 0, 0),
        'yellow': (255, 255, 0),
        'green': (0, 255, 0)
    },

    # trafik ışığı ayarla
    'traffic_light': {
        # kırmızı ışığında 10 sn dur
        'red_light_duration': 10,  # second
        # sarı ışığında 1.5 sn dur
        'yellow_light_duration': 1.5,  # second
        # yeşil ışığında 10 sn dur
        'green_light_duration': 10,  # second
        # merkezden uzaklık
        'distance_from_center': (40, 10),
        # trafik lambaların yüksekliği
        'body_height': 30,
        # trafik lambaların genişliği
        'body_width': 20
    },

    # arka ayarla
    'background': {
        'road_marking_width': 2,
        'road_marking_alternate_lengths': (20, 10),
        'road_marking_gap_from_yellow_box': 10,
        'yellow_box_junction': (50, 50, 50, 50),  # top, right, bottom, left
    },

    # bulanık
    'fuzzy': {
        'range': {
            # kırmızı ışığın arkasında
            # np.arange bir array geri veriyor 
            # np.arange(start=1, stop=10, step=3) --> array([1, 4, 7]) verecektir 
            'behind_red_light': np.arange(-4, 17, 1),
            # array([-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 , 14, 15, 16])

            #gelen yeşil ışık
            'arriving_green_light': np.arange(-4, 17, 1),

            #uzantı
            'extension': np.arange(0, 21, 1)
            # array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        },
        'membership_function': {
            # kırmızı ışığın arkasında
            'behind_red_light': {
                # çok az
                'few': [0, 0, 3],
                # az
                'small': [0, 3, 6], 
                # orta
                'medium': [3, 6, 9],
                # çok
                'many': [6, 9, 12]
            },

            # gelen yeşil ışık
            'arriving_green_light': {
                # çok az
                'few': [0, 0, 3],
                # az
                'small': [0, 3, 6],
                # orta
                'medium': [3, 6, 9],
                # çok
                'many': [6, 9, 12]
            },

            # uzantı
            'extension': {
                # sıfır
                'zero': [0, 0, 0],
                # kısa
                'short': [0, 2, 4],
                # orta düzeyde
                'medium': [2, 4, 6],
                # uzun
                'long': [4, 6, 8]
            }
        }
    }
}
