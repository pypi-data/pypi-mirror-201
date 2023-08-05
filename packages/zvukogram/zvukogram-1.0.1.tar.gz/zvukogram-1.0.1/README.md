<div align="left">
    <h1>ZvukoGram API <img src="https://zvukogram.com/design/img/dispic/zvuklogo.png" width=30 height=30></h1>
    <p align="left" >
        <a href="https://pypi.org/project/zvukogram/">
            <img src="https://img.shields.io/pypi/v/zvukogram?style=flat-square" alt="PyPI">
        </a>
        <a href="https://pypi.org/project/zvukogram/">
            <img src="https://img.shields.io/pypi/dm/zvukogram?style=flat-square" alt="PyPI">
        </a>
    </p>
</div>

A simple, yet powerful library for [ZvukoGram API](https://zvukogram.com/node/api/)


## Usage

With ``ZvukoGram API`` you can fully access the ZvukoGram API.

## Documentation

Official docs can be found on the [API's webpage](https://zvukogram.com/node/api/)

## Installation

```bash
pip install zvukogram
```

## Requirements

 - ``Python 3.7+``
 - ``aiohttp``
 - ``pydantic``

## Features

 - ``Asynchronous``
 - ``Exception handling``
 - ``Pydantic return model``
 - ``LightWeight``

## Basic example

```python
import asyncio

from zvukogram import ZvukoGram, ZvukoGramError


api = ZvukoGram('token', 'email') 


async def main():

    try:

        voices = await api.get_voices()
        print(voices['Русский'].pop().voice)

    except ZvukoGramError as exc:

        print(exc)

    generation = await api.tts(
        voice='Бот Максим',
        text='Привет!',
    )

    print(generation.file)
    audio = await generation.download()


    generation = await api.tts_long(
        voice='Бот Максим',
        text='Более длинный текст!',
    )
    while not generation.file:

        await asyncio.sleep(1)
        generation = await api.check_progress(generation.id)

    print(generation.file)

asyncio.run(main())
```

Developed by Nikita Minaev (c) 2023
