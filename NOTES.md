Here, some useful notes for the work in progress

# **EMOJIS' MEANING**
👉 <font color='green'>**Take good note of this**</font>

☝️ <font color='orange'>**Interesting unsolved question**</font>

⚠️ <font color='orangered'>**TO DO**</font>

# **Adzuna API Rate Limit**
Default API access limits: [**Source: terms of service**](https://developer.adzuna.com/docs/terms_of_service)
- 25 hits / min
- 250 hits / day
- 1 000 hits / week
- 2 500 hits / month

👉 <font color='green'>**THIS SEEMS AWFULLY LOW! And hence will need to design some sort of scheduler in order not to be bottlenecked.**</font>

# **TheMuse API Rate Limit**
The limit seems a little higher, especially if **the app is registered**.
This will allow up to **3 600 requests by hour**. [**Source: Api-V2 Doc**](https://www.themuse.com/developers/api/v2)

 👉 <font color='green'>**To know where you are relative to the limit, these HTTP headers will be returned with every response:**</font>

- `X-RateLimit-Remaining`: How many requests you can still make at this time
- `X-RateLimit-Limit`: The total number of requests you're allowed to make
- `X-RateLimit-Reset`: Seconds remaining before the rate limit resets

# **TheMuse API Endpoints**
## **Jobs: `https://www.themuse.com/api/public/jobs`**
Parameters:
- `page` (required): the page number to load
- `category` the job category to get, interesting ones for our problematic:
    - <font color='cyan'>Computer and IT</font>
    - <font color='violet'>Data and analytics</font>
    - <font color='cyan'>IT</font>
    - <font color='orange'>Software Engineer</font>
    - <font color='violet'>Data Science</font>
    - <font color='limegreen'>Design and UX</font>
    - <font color='orange'>Software Engineering</font>
    - <font color='limegreen'>UX</font>

👉 <font color='green'>**You should obviously notice the close categories, which may generate duplicates**.</font>

- `level`: the experience level required for the job (5 levels)
- `location`: the job location you get

For this parameter, what seems to be quite a burden is that it's too granular. You have indeed to specify **towns**... In alphabetical order.

☝️ <font color='orange'>**It's mentioned you can ask for remote jobs but haven't yet found how.**</font>

⚠️ <font color='red'>**You should investigate if it would be possible to specify 
countries (seems not)**</font>

### **IMPORTANT FOR THIS ENDPOINT**
👉 <font color='green'>**Each response of the API provides, in its body, a `"page_count"` key specifying the total number of pages containing results fitting to the query**.</font>


## **Job: `https://www.themuse.com/api/public/jobs/:id`**
Gets an individual job, specifying the id of the corresponding ad (obviously returned by the previous endpoint)

⚠️ <font color='red'>**This endpoint's output and the subset from the previous one should be compared to tell if they're identical or not.**</font>
