from Classes import Animal

class Voar(Animal):
    def voar(self):
        pass

class Nadar(Animal):
    def nadar(self):
        pass

class Pato(Voar, Nadar):
    def __init__(self, nome, som):
        super().__init__(nome, "Pato", som)
        self.nome = nome

    def voar(self):
        print(f'O pato {self.nome} está voando')

    def nadar(self):
        print(f'O pato {self.nome} está nadando')

pato = Pato('Patolino', 'Quack')
pato.nadar()
pato.voar()
pato.emitir_som()
pato.apresentar()
pato.matar()
pato.emitir_som()
pato.apresentar()