'''
inspired by: https://github.com/ArjanCodes/2022-asyncio
This is a simple workflow to demonstrate using
asyncio to speed up i0 intensive tasks in the context
of making http requests

we are using Pokemon api, https://pokeapi.co/
as our test case server. It is free and nice and cozy.
'''
import asyncio
import requests

'''
first, requests.get(urlString) is synchronous and blocks
thus, we need async wrapper on it.
asyncio.to_thread(func,*args) will parse all args and pass into the func
in our case the function is just lambda function to get the json from GET 
request
'''
async def asyncHttpGetJson(urlStr):
    return await asyncio.to_thread(lambda arg: requests.get(arg, timeout = 10).json(), urlStr)

async def getPokemonJson():
    from random import randint
    pokemonId = randint(1,386) #I personally only acknowledge the 386, my childhood...
    pokemonUrl = f"https://pokeapi.co/api/v2/pokemon/{pokemonId}"
    pokemonJson = await asyncHttpGetJson(pokemonUrl)
    return pokemonId, pokemonJson

def getPokemonName(jsonObj):    #given a json obj to handle, doesn't need to be async any more
    return jsonObj["name"]

async def driver(amount):
    from time import perf_counter
    start = perf_counter()
    calls = [getPokemonJson() for _ in range(amount)]   # a list of async function call instances
    pokemonJsonLst = await asyncio.gather(*calls, return_exceptions=True)   # allow the server to throw exceptions
    end = perf_counter()
    print(f"gathered and completed {amount} calls in {end-start:.2f} seconds")  # 0.01 sec precision
    for item in pokemonJsonLst:
        if isinstance(item,Exception):
            print(f"request failed: {item}")
        else:
            eachId, eachJson = item
            print(f"pokedex {eachId}: {getPokemonName(eachJson)}")


if __name__ == '__main__':
    asyncio.run(driver(20))