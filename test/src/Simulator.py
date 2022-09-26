import pygame #multimedya uygulamalarının geliştirilmesi için kütüphane
import time

from src.Common import Lane, DoubleLane
from src.Config import Config
from src.Controller.VehicleController import VehicleController
from src.Controller.TrafficController import TrafficController
from src.Controller.BackgroundController import BackgroundController

class Simulator:
    #nesne oluşturmak
    def __init__(self, caption):
        self.caption = caption
        #Görüntülemek için bir pencere veya ekran başlatmak
        self.surface = pygame.display.set_mode((Config['simulator']['screen_width'],
                                                Config['simulator']['screen_height']))   

        """
        VehicleController:
        self.screen_height = Config['simulator']['screen_height']
        self.screen_width = Config['simulator']['screen_width']
        self.vehicle_body_width = Config['vehicle']['body_width']
        self.vehicle_body_length = Config['vehicle']['body_length']
        self.bumper_distance = Config['simulator']['bumper_distance']
        self.safe_distance = Config['vehicle']['safe_distance']

        TrafficController:
        self.surface = surface
        self.screen_height = Config['simulator']['screen_height']
        self.screen_width = Config['simulator']['screen_width']
        self.traffic_light_body_height = Config['traffic_light']['body_height']
        self.traffic_light_body_width = Config['traffic_light']['body_width']
        self.traffic_light_distance_from_center = Config['traffic_light']['distance_from_center']
        """

        self.vehicle_ctrl = VehicleController(self.surface)
        self.traffic_ctrl = TrafficController(self.surface)
        # BackgroundController siniftan nesne olusturma
        self.background_ctrl = BackgroundController(self.surface,
                                                    self.traffic_ctrl.get_traffic_lights(DoubleLane.Horizontal) +
                                                    self.traffic_ctrl.get_traffic_lights(DoubleLane.Vertical))
                                                    
        self.clock = pygame.time.Clock() #zamanı takip etmeye yardımcı olacak bir nesne oluşturun
        self.gap_between_switch = Config['simulator']['gap_between_traffic_switch']
         
        self.HORIZONTAL_SPAWN_EVENT = pygame.USEREVENT + 1 #create update timer
        self.VERTICAL_SPAWN_EVENT = pygame.USEREVENT + 2

        self.switching_traffic = False
        self.switching_traffic_start_time = None
        self.start_time = time.time()
        self.moving_averages = self.vehicle_ctrl.get_moving_averages_num_vehicles_behind_traffic()

        self.is_extended = False
        self.green_light_remaining_time = Config['traffic_light']['green_light_duration']
        self.extension_notification_start_time = time.time() - 10
       #Araç oluşturmak ve  yönlendirmek
       #dikey'deki arabalar soldan saga ve sagdan sola
       #yatay'deki arabaler aşağıdan yukarıya ve Yukarıdan aşağıya
    def spawn(self, double_lane: DoubleLane):
        if double_lane == DoubleLane.Horizontal:
            self.spawn_single_vehicle(Lane.left_to_right)
            self.spawn_single_vehicle(Lane.right_to_left)

        elif double_lane == DoubleLane.Vertical:
            self.spawn_single_vehicle(Lane.bottom_to_top)
            self.spawn_single_vehicle(Lane.top_to_bottom)
    #Araç oluştur
    def spawn_single_vehicle(self, lane: Lane):
        self.vehicle_ctrl.create_vehicle(lane, self.traffic_ctrl.traffic_lights[lane])

    #ana oyun döngüsü
    def main_loop(self):
        
        game_over = False
          #olay kuyruğunda tekrar tekrar bir olay oluşturun      
          #  güncelleme zamanlayıcısı oluştur
        pygame.time.set_timer(self.HORIZONTAL_SPAWN_EVENT, Config['simulator']['spawn_rate']['slow'])
        pygame.time.set_timer(self.VERTICAL_SPAWN_EVENT, Config['simulator']['spawn_rate']['slow'])

        while not game_over:

            for event in pygame.event.get():#kuyruktan olayları al
                if event.type == self.HORIZONTAL_SPAWN_EVENT: #
                    rate = self.background_ctrl.get_spawn_rate(DoubleLane.Horizontal)
                    pygame.time.set_timer(self.HORIZONTAL_SPAWN_EVENT, Config['simulator']['spawn_rate'][rate])
                    self.spawn(DoubleLane.Horizontal)

                if event.type == self.VERTICAL_SPAWN_EVENT:
                    rate = self.background_ctrl.get_spawn_rate(DoubleLane.Vertical)
                    pygame.time.set_timer(self.VERTICAL_SPAWN_EVENT, Config['simulator']['spawn_rate'][rate])
                    self.spawn(DoubleLane.Vertical)

                if event.type == pygame.QUIT:
                    game_over = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for double_lane in [DoubleLane.Horizontal, DoubleLane.Vertical]:
                        for rate in ['slow', 'medium', 'fast']:
                            if self.background_ctrl.spawn_rate_buttons[double_lane][rate].collidepoint(event.pos):
                                self.background_ctrl.set_spawn_rate(double_lane, rate)
                    # if self.background_ctrl.fuzzy_button.collidepoint(event.pos):
                    #     moving_averages = self.vehicle_ctrl.get_moving_averages_num_vehicles_behind_traffic()
                    #     print(self.calculate_fuzzy_score(moving_averages))

            self.background_ctrl.refresh_screen()#ekranı yenile
            self.background_ctrl.draw_road_markings()#yol işaretlerini çiz
            self.background_ctrl.draw_vehicle_count(self.vehicle_ctrl.counter)#Araç sayısını çiz
            self.background_ctrl.draw_spawn_rate_buttons()#varis oranı düğmelerini çiz
            self.background_ctrl.draw_light_durations(self.traffic_ctrl.get_green_light_extension())#Işık sürelerini çiz

            # print(self.traffic_ctrl.get_green_light_remaining())

            self.traffic_ctrl.update_and_draw_traffic_lights() #güncelleme ve trafik ışıkları çizme
            self.vehicle_ctrl.destroy_vehicles_outside_canvas() #tabl dışındaki araçları imha etmek
            self.vehicle_ctrl.update_and_draw_vehicles() #araçları güncelle ve çiz
            self.vehicle_ctrl.update_num_vehicles_behind_traffic()#trafiğin arkasındaki araç sayısını güncelle

            if round((time.time() - self.start_time), 1) % Config['simulator']['static_duration'] == 0:
                self.moving_averages = self.vehicle_ctrl.get_moving_averages_num_vehicles_behind_traffic()#hareketli ortalamalar trafiğin gerisinde kalan araç sayısı
            self.background_ctrl.draw_moving_averages(self.moving_averages) #Hareketli ortalamaları çiz

            current_green_light_remaining_time = self.traffic_ctrl.get_green_light_remaining()#Mevcut yeşil ışık kalan süresi
            direction_changed = current_green_light_remaining_time > self.green_light_remaining_time #Yön değişti
            self.green_light_remaining_time = current_green_light_remaining_time #yeşil ışık kalan süresi

            if not self.is_extended:
                if current_green_light_remaining_time <= Config['simulator']['seconds_before_extension']:
                    fuzzy_score = self.calculate_fuzzy_score(self.moving_averages)
                    self.horizontal = self.moving_averages[Lane.left_to_right]
                    self.vertical = self.moving_averages[Lane.top_to_bottom]
                    self.background_ctrl.draw_fuzzy_score(fuzzy_score, self.traffic_ctrl.get_current_active_lane())
                    self.traffic_ctrl.set_green_light_extension(fuzzy_score)
                    self.is_extended = True
                    self.extension_notification_start_time = time.time()
                    self.green_light_remaining_time = self.traffic_ctrl.get_green_light_remaining()
            else:
                if direction_changed:
                    self.traffic_ctrl.clear_all_green_light_extension()
                    self.is_extended = False

            if time.time() - self.extension_notification_start_time < Config['simulator']['fuzzy_notification_duration']:
                self.background_ctrl.draw_extension_notification(self.traffic_ctrl.get_green_light_extension(), self.horizontal, self.vertical)

            pygame.display.update()
            self.clock.tick(Config['simulator']['frame_rate'])
          #bulanık puanı hesapla
    def calculate_fuzzy_score(self, moving_averages):
        traffic_state = self.traffic_ctrl.get_current_active_lane()
        if self.is_extended :
            ext_count = 1
        else:
            ext_count =0
            
        if traffic_state == DoubleLane.Vertical:
            return self.traffic_ctrl.calculate_fuzzy_score(moving_averages[Lane.top_to_bottom], moving_averages[Lane.left_to_right], ext_count)
        elif traffic_state == DoubleLane.Horizontal:
            return self.traffic_ctrl.calculate_fuzzy_score(moving_averages[Lane.left_to_right], moving_averages[Lane.top_to_bottom], ext_count)
          #(deger atma)
    def initialize(self):
        self.spawn(DoubleLane.Horizontal)
        self.spawn(DoubleLane.Vertical)
        # self.toggle_traffic()
       #baslamak
    def start(self):
        pygame.init()
        pygame.display.set_caption(self.caption)

        self.initialize()
        self.main_loop()

        pygame.quit()
        quit()
