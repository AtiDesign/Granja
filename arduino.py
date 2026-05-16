import pyfirmata

class Arduino:
    def __init__(self, port="COM3"):
        self.board = pyfirmata.Arduino(port)

        # Pinos digitais para atuadores
        self.fan_pin = self.board.digital[9]
        self.exh_pin = self.board.digital[10]
        self.heat_pin = self.board.digital[11]
        self.light_pin = self.board.digital[13]

        # Pinos analógicos para sensores
        self.temp_pin = self.board.analog[0]   # Exemplo: LM35 ou outro sensor analógico
        self.hum_pin  = self.board.analog[1]   # Exemplo: sensor de umidade analógico
        self.lux_pin  = self.board.analog[2]   # LDR
        self.nh3_pin  = self.board.analog[3]   # MQ-135

        # Configura como entrada
        for pin in [self.temp_pin, self.hum_pin, self.lux_pin, self.nh3_pin]:
            pin.enable_reporting()

    # Métodos de controle
    def set_fan(self, on: bool):
        self.fan_pin.write(1 if on else 0)

    def set_exhaust(self, on: bool):
        self.exh_pin.write(1 if on else 0)

    def set_heat(self, on: bool):
        self.heat_pin.write(1 if on else 0)

    def set_light(self, on: bool):
        self.light_pin.write(1 if on else 0)

    # Métodos de leitura
    def read_temp(self):
        return self.temp_pin.read()

    def read_hum(self):
        return self.hum_pin.read()

    def read_lux(self):
        return self.lux_pin.read()

    def read_nh3(self):
        return self.nh3_pin.read()
