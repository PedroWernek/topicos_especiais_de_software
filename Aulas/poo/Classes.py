class Animal:
    def __init__(self, nome, tipo, som):
        self.nome = nome
        self.tipo = tipo
        self.esta_vivo = True
        self.som = som

    def emitir_som(self):
        if self.esta_vivo:
            print(self.som)
        else :
            print("...")

    def apresentar(self):
        pass

    def matar(self):
        print('Barulho de tiro...')
        self.esta_vivo = False

class Cachorro(Animal):
    def __init__(self, nome, som):
        Animal.__init__(self, nome,"Cachorro", som)

    def apresentar(self):
        if self.esta_vivo:
            print(f'{self.tipo} ->'
                  f'\nNome: {self.nome}'
                  f'\nEsta vivo: {'Sim' if self.esta_vivo else 'Não'}'
                  '\nSom:', end=" ")
            self.emitir_som()
        else :
            print(f'Para que apresentar alguém que está morto...'
            )


cachorro = Cachorro("cachorro", "AuAu")
cachorro.emitir_som()
cachorro.apresentar()

cachorro.matar()
cachorro.emitir_som()
cachorro.apresentar()

