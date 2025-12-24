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

POKEMAX = 386


'''
first, requests.get(urlString) is synchronous and blocks
thus, we need async wrapper on it.
asyncio.to_thread(func,*args) will parse all args and pass into the func
in our case the function is just lambda function to get the json from GET 
request
'''
# async def asyncHttpGetJson(urlStr):
#     return await asyncio.to_thread(lambda arg: requests.get(arg, timeout = 10).json(), urlStr)
#
# async def getPokemonJson():
#     from random import randint
#     pokemonId = randint(1,POKEMAX) #I personally only acknowledge the 386, my childhood...
#     pokemonUrl = f"https://pokeapi.co/api/v2/pokemon/{pokemonId}"
#     pokemonJson = await asyncHttpGetJson(pokemonUrl)
#     return pokemonId, pokemonJson

'''
now, let's add caching
we have some important lessons:
1. now we cannot rely on a lambda call to the synchronous requests.get() anymore:
    IMPORTANT: caching async is pointless, you will be caching a coroutine (also called awaitable)
                while you actually want to store concrete data! always cache the synchronous func result!
2. general design guide line: when we have a cache decorator, the func should:
    - take in simple data as key, consider: 
        using pokemonId (int) 
            versus 
        entire resolved url (api call, base url + pokemonId)
        
        we have 2 concerns: 1. simpler key makes cache structure simpler
                            2. pokemonId -- name mapping is INVARIANT (we can also say idiomatic),
                            ideally pokemon id is always ties to the same pokemon, which the url is not:
                            we already have "v2" in the url route; this can become "v3", "v4", etc
                            and that will cause artificial cache miss and WE WONT SEE ANYTHING WRONF on client
                            side because, we are still getting correct names (assuming we update our base url
                            diligently) but the cache miss will spike ---  everything will miss once.
    
    - return complex data we desire to cache. Ideally we should use cache to save the effort of all IO bound
        chores in the future. This is intuitive: you want to cache whatever the server serves you as final product, 
        not some intermediate product that requires more server round trip; that just doesn't help.
    
'''

from functools import lru_cache

@lru_cache(maxsize=POKEMAX) # we only need at most this number of pokemon ids
def getJsonCached(pokemonId):
    pokemonUrl = f"https://pokeapi.co/api/v2/pokemon/{pokemonId}"
    return requests.get(pokemonUrl, timeout=10).json()

async def getPokemonJson():
    from random import randint
    pokemonId = randint(1, POKEMAX)
    pokemonJson =  await asyncio.to_thread(getJsonCached, pokemonId)
    return pokemonId, pokemonJson   # btw we can also not bother with this and return id, await ... on one line

def getPokemonName(jsonObj):    #given a json obj to handle, doesn't need to be async any more
    return jsonObj["name"]

async def driver(amount, verbose = True):
    from time import perf_counter
    start = perf_counter()
    calls = [getPokemonJson() for _ in range(amount)]   # a list of async function call instances
    pokemonJsonLst = await asyncio.gather(*calls, return_exceptions=True)   # allow the server to throw exceptions
    end = perf_counter()
    if verbose: print(f"gathered and completed {amount} calls in {end-start:.2f} seconds")  # 0.01 sec precision
    for item in pokemonJsonLst:
        if isinstance(item,Exception):
            if verbose: print(f"request failed: {item}")
        else:
            eachId, eachJson = item
            if verbose: print(f"pokedex {eachId}: {getPokemonName(eachJson)}")

    print(f"cache stats: {getJsonCached.cache_info()}")
    return round(end-start,2)   #round to 0.01 precision

async def runSequential(n,amount, verbose = True):
    performances = []
    for __ in range(n):
        performances.append(await driver(amount, verbose))
    return performances


'''
now, another IMPORTANT lesson:
now we want to test cache behavior, but I am using non-persistent cache 
that is destroyed after execution of code file (intended, else I will
literally blow up my computer cache space soon -- I kinda already do that)

so, to test cache, we should ideally run driver func multiple times.

But "await" keyword is illegal at top level a.k.a not legal in if name == main,
because await means , IMPORTANT! "suspend this corotine and yielf control back to event loop"
so it does not even make sense to be used in name==main: there is no event loop and it is not coroutine

AND, we also cannot just do what I commented out: 
add multiple calls to driver func in a coroutine manner is WRONG, because they
will all fire at the same time when we do asyncio.gather; all the driver calls are
"in flight" at basically the same time (assuming the IO delay is really high)
and we won't have anything in the cache when they are all busy; and even
if they hit the same pokemonIds, they all come back to us at similar times and
we will have a lot of miss! You always want to populate the cache in a good stream
and must avoid one-shot large amount of calls! 

'''

if __name__ == '__main__':
    # multipleRuns = [driver(20) for __ in range(10)]
    # asyncio.run(asyncio.gather(*multipleRuns, return_exceptions=True))

    performances = asyncio.run(runSequential(10,20, verbose=False))
    print(f"across multiple runs, we get performances {performances}")


    def print_trendline(data, width=40):
        if not data:
            print("(empty)")
            return

        lo, hi = min(data), max(data)
        span = hi - lo if hi != lo else 1.0

        for i, x in enumerate(data):
            # Normalize to [0, width]
            pos = int((x - lo) / span * width)
            line = " " * pos + "*"
            print(f"{i:02d} | {line} {x:.2f}")
    print_trendline(performances)

