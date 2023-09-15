Here, some useful notes for the work in progress

# **On Adzuna API rate limit**
Default API access limits: [**Source: terms of service**](https://developer.adzuna.com/docs/terms_of_service)
- 25 hits / min
- 250 hits / day
- 1 000 hits / week
- 2 500 hits / month

which will need to design some sort of scheduler in order not to be bottlenecked.

# **On TheMuse API rate limit**
The limit seems a little higher, especially if **the app is registered**.
This will allow up to **3 600 requests by hour**. [**Source: Api-V2 Doc**](https://www.themuse.com/developers/api/v2)

 To know where you are relative to the limit, these HTTP headers will be returned with every response:

- `X-RateLimit-Remaining`: How many requests you can still make at this time
- `X-RateLimit-Limit`: The total number of requests you're allowed to make
- `X-RateLimit-Reset`: Seconds remaining before the rate limit resets
