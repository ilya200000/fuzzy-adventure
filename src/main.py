import ctypes
import os

# Загружаем нашу C++ библиотеку
lib_path = os.path.abspath("physics.dll") # или .so
physics = ctypes.CDLL(lib_path)

# Настраиваем типы данных для C++
physics.check_collision.argtypes = [ctypes.c_float] * 6
physics.check_collision.restype = ctypes.c_bool

# Пример использования в цикле игры:
# if physics.check_collision(bullet.x, bullet.y, 5, enemy.x, enemy.y, 20):
#     print("Попадание, просчитанное на C++!")
