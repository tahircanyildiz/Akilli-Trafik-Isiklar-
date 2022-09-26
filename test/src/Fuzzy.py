# NumPy (Numerical Python) - matematik kütüphanesidir 
import numpy as np
# numpy dizilerle çalışan bulanık bir mantık Python paketidir 
import skfuzzy as fuzz
# 'src' klasorunde 'Config.py' dosyasına erişmek 
from src.Config import Config


class Fuzzy:

    def __init__(self):
        # ayarla - 'Config.py' dosyasından 
        setting = Config['fuzzy']['range']
        # burdaki kırmızı ışığın arkasında, 'Config.py' dosyasındaki gibi ayarla
        self.x_behind_red_light = setting['behind_red_light']
        # gelen yeşil ışık, 'Config.py' dosyasındaki gibi ayarla
        self.x_arriving_green_light = setting['arriving_green_light']
        # uzantı, 'Config.py' dosyasındaki gibi ayarla
        self.x_extension = setting['extension']

        # ayarla - 'Config.py' dosyasından 
        setting = Config['fuzzy']['membership_function']['arriving_green_light']
        # fuzz.trimf( x , abc ) hazır fonksiyon - Üçgen üyelik işlevi oluşturucu.
        # Parametreler:
        # x: 1d dizisi(Bağımsız değişken), 
        # abc : 1d dizisi, uzunluk 3(Üçgen fonksiyonun şeklini kontrol eden üç elemanlı vektör. A <= b <= c gerektirir)
        # return:
        # y : 1d dizisi(Üçgen üyelik işlevi)
        self.arriving_green_light_few = fuzz.trimf(self.x_arriving_green_light, setting['few'])
        self.arriving_green_light_small = fuzz.trimf(self.x_arriving_green_light, setting['small'])
        self.arriving_green_light_medium = fuzz.trimf(self.x_arriving_green_light, setting['medium'])
        self.arriving_green_light_many = fuzz.trimf(self.x_arriving_green_light, setting['many'])

        # ayarla - 'Config.py' dosyasından 
        setting = Config['fuzzy']['membership_function']['behind_red_light']
        self.behind_red_light_few = fuzz.trimf(self.x_behind_red_light, setting['few'])
        self.behind_red_light_small = fuzz.trimf(self.x_behind_red_light, setting['small'])
        self.behind_red_light_medium = fuzz.trimf(self.x_behind_red_light, setting['medium'])
        self.behind_red_light_many = fuzz.trimf(self.x_behind_red_light, setting['many'])
        
       # ayarla - 'Config.py' dosyasından 
        setting = Config['fuzzy']['membership_function']['extension']
        self.extension_zero = fuzz.trimf(self.x_extension, setting['zero'])
        self.extension_short = fuzz.trimf(self.x_extension, setting['short'])
        self.extension_medium = fuzz.trimf(self.x_extension, setting['medium'])
        self.extension_long = fuzz.trimf(self.x_extension, setting['long'])

    # Fonksiyon - uzantı al
    # parametreler: kullandığımız self, yeşil ışığa gelen araba, kırmızı ışığının arkasında olan araba, uzantı sayısı
    def get_extension(self, arriving_green_light_car, behind_red_light_car, extension_count):
        # fuzz.interp_membership( x , xmf , xx ) hazır fonksiyon - Belirli bir değer için üyelik derecesini bulun
        # Parametreler: 
        # x: 1d dizisi(Bağımsız ayrık değişken vektör), 
        # xmf : 1d dizisi(İçin bulanık üyelik işlevi x. İle aynı uzunlukta x)
        # xx : float(Evrende ayrık tekil değer x)
        # return: 
        # xxmf : float(En Üyelik fonksiyon değeri xx, u(xx))
        # kırmızı ışığının arkasında (seviye = 1, cok az)
        behind_red_light_level_few = fuzz.interp_membership(self.x_behind_red_light, self.behind_red_light_few, behind_red_light_car)
        # kırmızı ışığının arkasında (seviye = 2, az)
        behind_red_light_level_small = fuzz.interp_membership(self.x_behind_red_light, self.behind_red_light_small, behind_red_light_car)
        # kırmızı ışığının arkasında (seviye = 3, orta)
        behind_red_light_level_medium = fuzz.interp_membership(self.x_behind_red_light, self.behind_red_light_medium, behind_red_light_car)
        # kırmızı ışığının arkasında (seviye = 4, cok)
        behind_red_light_level_many = fuzz.interp_membership(self.x_behind_red_light, self.behind_red_light_many, behind_red_light_car)

        arriving_green_light_level_few = fuzz.interp_membership(self.x_arriving_green_light, self.arriving_green_light_few, arriving_green_light_car)
        arriving_green_light_level_small = fuzz.interp_membership(self.x_arriving_green_light, self.arriving_green_light_small, arriving_green_light_car)
        arriving_green_light_level_medium = fuzz.interp_membership(self.x_arriving_green_light, self.arriving_green_light_medium, arriving_green_light_car)
        arriving_green_light_level_many = fuzz.interp_membership(self.x_arriving_green_light, self.arriving_green_light_many, arriving_green_light_car)


        # Kural 1: Varış az ise Uzantı(Extension) sıfırdır(0).
        rule1 = arriving_green_light_level_few
        # Kural 2: Varış küçükse VE Kuyruk Sıra (az VEYA küçükse) Uzantı(Extension) kısadır.
        rule2 = np.fmin(arriving_green_light_level_small,
                        np.fmax(behind_red_light_level_few, behind_red_light_level_small))
        # Kural 3: Varış küçükse VE Kuyruk (orta VEYA çok) ise, Uzantı(Extension) sıfırdır(0).
        rule3 = np.fmin(arriving_green_light_level_small,
                        np.fmax(behind_red_light_level_medium, behind_red_light_level_many))
        # Kural 4: Varış orta ise VE Kuyruk (az VEYA küçük) ise, Uzantı(Extension) orta düzeydedir.
        rule4 = np.fmin(arriving_green_light_level_medium,
                        np.fmax(behind_red_light_level_few, behind_red_light_level_small))
        # Kural 5: Varış orta ise VE Kuyruk (orta VEYA çok) ise Uzantı(Extension) kısadır.
        rule5 = np.fmin(arriving_green_light_level_medium,
                        np.fmax(behind_red_light_level_medium, behind_red_light_level_many))
        # Kural 6: Varış çoksa VE Kuyruk az ise, Uzantı(Extension) uzundur.
        rule6 = np.fmin(arriving_green_light_level_many, behind_red_light_level_few)
        # Kural 7: Varış çoksa VE Kuyruk (küçük VEYA orta) ise, Uzantı(Extension) orta düzeydedir.
        rule7 = np.fmin(arriving_green_light_level_many,
                        np.fmax(behind_red_light_level_small, behind_red_light_level_medium))
        # Kural 8: Varış az isa VE Kuyruk çoksa, Uzantı(Extension) kısadır.
        rule8 = np.fmin(arriving_green_light_level_many, behind_red_light_level_many)

        # eğer uzantı sayısı = 0 ise
        if extension_count == 0:
            # np.fmin - hazır fonksiyon
            # İki diziyi karşılaştırın ve eleman bazında minimumları içeren yeni bir dizi döndürür. 
            # np.fmax - hazır fonksiyon
            # İki diziyi karşılaştırın ve eleman bazında maximumları içeren yeni bir dizi döndürür. 
            extension_activation_zero = np.fmin(np.fmax(rule1, rule3), self.extension_zero)
            extension_activation_short = np.fmin(np.fmax(rule2, np.fmax(rule5, rule8)), self.extension_short)
            extension_activation_medium = np.fmin(np.fmax(rule4, rule7), self.extension_medium)
            extension_activation_long = np.fmin(rule6, self.extension_long)

        # eğer uzantı sayısı = 0 değilse
        else:
            extension_activation_zero = np.fmin(
                np.fmax(rule1, np.fmax(rule2, np.fmax(rule3, np.fmax(rule5, rule8)))), self.extension_zero)
            extension_activation_short = np.fmin(np.fmax(rule4, rule7), self.extension_short)
            extension_activation_medium = np.fmin(rule6, self.extension_medium)
            extension_activation_long = np.fmin(0, self.extension_long)

        # toplu
        aggregated = np.fmax(extension_activation_zero, np.fmax(extension_activation_short,
                                                                np.fmax(extension_activation_medium,
                                                                        extension_activation_long)))
       
        # sonucu döndürüyor
        return fuzz.defuzz(self.x_extension, aggregated, 'centroid')
