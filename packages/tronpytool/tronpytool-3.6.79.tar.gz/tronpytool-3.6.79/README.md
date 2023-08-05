# 🏗👷🏾 TronPyTool
### Library API for Python on TRX or Tron

[![moodyeth](https://img.shields.io/pypi/v/moodyeth?style=plastic)](https://pypi.org/project/moodyeth/)
[![moodyeth](https://img.shields.io/pypi/pyversions/moodyeth.svg)](https://pypi.org/project/moodyeth/)
[![moodyeth](https://api.travis-ci.com/tokenchain/moodyeth.svg?branch=master)](https://pypi.org/project/moodyeth/)
[![moodyeth](https://img.shields.io/github/issues/tokenchain/moodyeth.svg)](https://pypi.org/project/moodyeth/)


Ethereum based all tool chain for smart contract development kit [documentation](https://htmlpreview.github.io/?https://github.com/tokenchain/tronpytool/blob/master/docs/tronpytool/index.html).

### Why do we use python
Using it because it is fast and easy. More importantly it runs directly by its own and no more dependencies.

Its much faster to building modules and calling functions on python.
Also it can be wrapped into an executable binary on wasm or cpython that runs on natively any platforms.

If you are using PyCharm or similar IDE, all type are ready to show at your finger tips.

### Get Started

`pip3 install tronpytool`

or upgrade using

`sudo pip3 install tronpytool --upgrade`

The development of tronpytool contract deployment tools:

Setup (for the early version, we are going to setup the workspace manually. )

Setup the folders:
 /vault
 /artifact
 /deploy_history
 /deploy_results
 /factoryabi

### Why use tron-py-tool

It is a all-in-one package with zero setup and configurations that works for multiple architectures. It is lightweight and simple. Build-in ERC20 support and bulk token sending support. Out of the box that comes with solc-compile automation and web3 executions.

### Features
- support most of the evm compatible chains
- golang module compile support
- python module compile support
- typescript module compile support
- tron payment usdt support with simple operation

### Examples:

##### Deployment of the new contract:

```
# !/usr/bin/env python
# coding: utf-8
import os


```

#### Show the amount of your wallet

```
#!/usr/bin/env python
# coding: utf-8
from tronpytool import Tron
from tronpytool import HttpProvider

tron = Tron().setNetwork('nile')


tron.toSun(1)
# result: 1000000

tron.fromSun(1000000)
# result: 1



```

#### Mint Coins
The example for minting coins with 18 decimal

```
# !/usr/bin/env python
# coding: utf-8
import os


```

#### Code compile
Integration of forge that can work perfectly with latest version with ONE LINE code.
```

# !/usr/bin/env python
# coding: utf-8
import os

from tronpytool import TronBrew, Evm

solidity_files = [
    "vault/token/RaceToken.sol",
]

ROOT = '.../Documents/b95/devtron'
FACTORY = '$HOME/Documents/piplines/factoryabi'

print("-----> job from here")
print(ROOT)
print("-----> now its ready to go")

TronBrew(ROOT, FACTORY).setClassSolNames(solidity_files).setEvm(Evm.ISTANBUL).useForge().localTranspile()

```




Documentation is ready [here](https://htmlpreview.github.io/?https://github.com/tokenchain/tronpytool/blob/master/docs/tronpytool/index.html)

Also there is a brother library for those who works with [EVM](https://github.com/tokenchain/moodyeth) network.

# 📦 Showcase your project with this SDK
PR your link or your github repo here.




### Donations

Welcome for donation for the good works!