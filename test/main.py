# 'src' klasorunde 'Simulator.py' dosyasına erişmek 
from src.Simulator import Simulator


#---------------------MAIN--------------------------
# çalıştırmak
if __name__ == "__main__":
    simulator = Simulator('Bulanık Trafik Sistemi')
    # başla
    simulator.start()