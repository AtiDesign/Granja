import pyfirmata

board = pyfirmata.Arduino('COM3')
print("Conectado ao Arduino na COM3")
board.digital[13].write(1)  # liga LED no pino 13
