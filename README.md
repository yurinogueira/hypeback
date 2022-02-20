# HypeBack Project

[Utility Tokens](#utility-tokens) automatic transaction backend, by the ethereum
[Ethereum](#ethereum) protocol, for [holders](#holder) of a specific 
[Ethereum](#ethereum) protocol [Contract](#contract).

*Leia isso em [Português](README.pt-br.md)*

## Running

To run the project, follow the following steps.

- Create the .env file inside the `config` folder, following the [.env.sample](config/env.sample) file.
- Change the `abi.json` and `bytecode.txt` files inside the `/src/api/token` folder, adapting it to your own [Utility Tokens](#utility-tokens).
- Change the `nft_abi.json` file inside the `/src/api` folder, adapting it to your own [Contract](#contract).

At the end of these steps, just run the following commands:

```bash
make build              # Build the project
make migrate            # Run the migrations
make createsuperuser    # Create a user with admin access
make development        # Start development server
```

To run the server in production mode, just run the following commands,
note: these commands need to be run in parallel, they are different
continue services.

```bash
make production-prerun  # Build the project
make production         # Run production server
make production-woker   # Start the Celery Worker
make production-beat    # Start the Celery Beat
```


## Contributing

Contributions are always welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) to learn how to get started.

## Dependencies

See below some dependencies.

- [Django 4](https://github.com/django/django)
- [Web3.py](https://github.com/ethereum/web3.py)
- [Celery](https://github.com/celery/celery)
- ...

See the [full list](requirements.txt).

## Authors

- [@Thiago Mozart](https://github.com/ThiagoMozart)
- [@Yuri Nogueira](https://github.com/yurinogueira)


## FAQ
See below some links that may be useful.

#### Ethereum

- [Wikipedia](https://en.wikipedia.org/wiki/Ethereum)
- [Ethereum](https://ethereum.org/en/)

#### Utility Tokens

- [Wikipedia](https://en.wikipedia.org/wiki/Non-fungible_token)
- [InvestoPedia](https://www.investopedia.com/non-fungible-tokens-nft-5115211)

#### Contract

- [Wikipedia](https://en.wikipedia.org/wiki/Smart_contract)

#### Holder

A person holding a NFT.
