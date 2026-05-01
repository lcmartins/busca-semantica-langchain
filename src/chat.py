from search import Search

class Chat:
    _searchInstance = Search.instance()
    def __init__(self):
        while True:
            query = input("Digite sua pergunta (ou 'sair' para encerrar): ")
            print("pensando para responder a sua pergunta...")
            if query.lower() == 'sair':
                print("Encerrando o programa.")
                break

            resposta = self._searchInstance.search(query)
            print(f"Resposta:\n {resposta}\n")

if __name__ == "__main__":
    Chat()