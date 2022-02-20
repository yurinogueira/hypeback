# HypeBack Project

Backend de transação automatica de [Utility Tokens](#utility-tokens), pelo protocolo [Ethereum](#ethereum), para [holders](#holder) de algum [Contrato](#contrato) de protocolo [Ethereum](#ethereum) especifico.

*Read this in [English](README.md)*

## Rodando

Para rodar o projeto e realizar testes é necessário seguir os seguintes passos.

- Criar o arquivo .env dentro da pasta `config` seguindo como base o [.env.sample](config/env.sample).
- Alterar os arquivos `abi.json` e `bytecode.txt` dentro da pasta `/src/api/token` adequando-o a sua própria [Utility Tokens](#utility-tokens).
- Alterar o arquivo `nft_abi.json` dentro da pasta `/src/api` adequando-o ao seu próprio [Contrato](#contract).

Finalizando esses passos basta seguir executar os seguintes comandos:

```bash
make build              # Builda o projeto
make migrate            # Realiza as migrações necessárias
make createsuperuser    # Cria o usuário com acesso ao admin
make development        # Inicia o servidor em modo de desenvolvimento
```

Para rodar o servidor em modo produção executar os seguintes comandos,
observação: esses comandos precisam ser executados paralelamente, são serviços
diferentes que continuaram em execução.

```bash
make production-prerun  # Builda o projeto
make production         # Inicia o servidor em modo de produção
make production-woker   # Inicia o Celery Worker
make production-beat    # Inicia o Celery Beat
```


## Contribuindo

Contribuições são sempre bem-vindas!

Veja [CONTRIBUTING.md](CONTRIBUTING.pt-br.md) para saber como começar.


## Dependências

Segue abaixo algumas dependências.

- [Django 4](https://github.com/django/django)
- [Web3.py](https://github.com/ethereum/web3.py)
- [Celery](https://github.com/celery/celery)
- ...

Veja a [lista completa](requirements.txt).

## Autores

- [@Thiago Mozart](https://github.com/ThiagoMozart)
- [@Yuri Nogueira](https://github.com/yurinogueira)


## FAQ
Segue abaixo alguns links que podem ser úteis.

#### Ethereum

- [Wikipédia](https://pt.wikipedia.org/wiki/Ethereum)
- [Ethereum](https://ethereum.org/pt-br/)

#### Utility Tokens

- [Wikipédia](https://pt.wikipedia.org/wiki/Token_n%C3%A3o_fung%C3%ADvel)
- [CoinNext](https://coinext.com.br/blog/utility-security-token)

#### Contrato

- [Wikipédia](https://pt.wikipedia.org/wiki/Contrato_inteligente)
- [Iberdrola](https://www.iberdrola.com/inovacao/smart-contracts)

#### Holder

Uma pessoa detendora de um token não-fungível.
