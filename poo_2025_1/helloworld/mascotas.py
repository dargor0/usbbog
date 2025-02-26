#!/usr/bin/env python3

"""
Ejemplo de objetos: Mascotas

Ejemplo de uso de clases y objetos

Autor: Oscar Diaz <odiaz@ieee.org>
Fecha: 2025-02-25
"""


class Mascota:
    """Clase para manejar mascotas"""
    nombre = ""
    especie = ""
    raza = ""
    edad = 0

    def __init__(self, nombre, especie="perro", raza="doberman", edad=1):
        """Constructor de la clase Mascota"""
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad

    def habla(self):
        """Muestra mensaje de mascota"""
        print(f"Soy '{self.nombre}' de la especie '{self.especie}'")
        print(f" de raza '{self.raza}' y edad '{self.edad}' años")
        if self.especie.lower() == "perro":
            print(" hago 'Guau!'")
        elif self.especie.lower() == "gato":
            print(" hago 'Miau!'")
        else:
            print(" hago '?????'")


def run():
    """script entrypoint"""

    # **** Poner el código ejecutable de su ejercicio aquí

    m1 = Mascota("Firulais", edad=8)
    m1.habla()
    m2 = Mascota("Michi", "gato", "siames", edad=4)
    m2.habla()
    m3 = Mascota("Motas", "hamster", "rata", edad=0.5)
    m3.habla()

    # ****


# **** Conserve este condicional para ejecutar el programa directamente
if __name__ == "__main__":
    run()
