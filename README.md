# **Job Market Project Homework**

Here's a file to help team-mates understand how the project works.
There's also the `NOTES.md` file, for further information, especially about the APIs.

# **General Links from DataScientest and the APIs**
- [**Docs**](https://docs.google.com/document/d/1R2yEuvZT49VSL96ciWjyp8NSZWBUD7fr/edit)
- [**API Adzuna**](https://developer.adzuna.com/)
- [**API The Muse**](https://www.themuse.com/developers/api/v2)

# **Install**
You can opt for a use of basic tools to manage the project (i.e. `venv` and `pip`.)
## **Virtual Environment**
It's of course best practise to create a virtual environment. This can be performed, inside a folder dedicated to the project, with the following command:

`python -m venv .venv` (on some Linux distributions, it's possible you'll have to switch `python` to `python3`)

Then, your virtual environment will be called `.venv`, and will be a hidden folder. As you obviously don't have to commit it, it's added in `.gitignore`.

## **Packages Installing**
All needed packages are listed in `requirements.txt`. Therefore, all can be installed via:

`pip install -r requirements.txt`

Especially, this includes a full `jupyterlab` environment, allowing you to fully develop within as an IDE.

## **Packages Small Description/Purpose**
### `python-dotenv`
As you will have to use credentials for each API, this library will allow you to load them as environment variables, preventing them to be hardcoded and visible inside the code.

All your credentials have to be stored in a `.env` file. A template is provided in the repository with the `.env_template` file to show you how you can manage it.

For further information, [**this tutorial**](https://www.youtube.com/watch?v=c42T5wKSztQ) sums-up the fundamentals.

### `httpx`
This package is an alternative to `requests` which has been considered as it allows to perform asynchronous requests if necessary.
Envisioning the rate limit of Adzuna's API for example, this may seem a bit overkill or useless, but you have also to consider that webscraping could be part of the job. Again, it's well understand that the main issue isn't performance, anyway, this package is consistent and its interface is quite alike `requests`' one.

### `bs4`
This has been chosen as the parser provider.

### `rich`
This is essentially there for "enriching terminal outputs", allowing to define colors for logging purposes, as this will be often noticed within the code.

🚸 **TO BE CONTINUED**

# **Content**
## **Special Subfolders**
### **`notebooks`**
Obviously intended for **exploratory purposes**:
- tests for data mining
- EDA later
This will surely be erased/gitignored later

### **`data`** (gitignored)
This folder contains the different dumps from
- **APIs requesting**
- **Webscraping**

It has been **added to `.gitignore` not to overflow storage**.

Hence, dump files have to be stored somewhere else.

### **`config_data`**
For the moment, this contains, as a JSON file, the list of French towns involved with The Muse API.

## **Main Files**
### `adzuna.py`
This module contains functions devoted to extract dumps from different endpoints from Adzuna API:
#### 🛠️ `get_adzuna_ads`
##### **OVERVIEW**

This function allows to call the API in order to **find relevant information about ads**, the endpoint used being `GET jobs/{country}/search/{page}`
It can be seen as a daily tool which will try to fetch as many ads as possible:
- calling for **1 related page, containing 50 results**,
- playing around the rate-limit of 25 calls per min,
- **theorically** proceeding to **up to 250 calls** (daily rate limit),
- **evaluating if the aggregated response contains too many duplicates** (checked on the **`id`** field, which a threshold ratio set inside the function via the **`THRESHOLD`** constant) and then **stopping the fetching whenever it occurs**.

🔎 *Experiments lead to notice that duplicates tend to often appear after featching 100 pages, meaning you're still far from the theorical limit*.

##### **PARAMETERS**

Both being optional, they allow to narrow the scope of search
- `what`: the keywords to search for (multiple items may be space separated)
- `cat_tag`: the category tag, as returned by the `category` endpoint (read below)

##### **RETURN VALUES**

It returns a `tuple` containing:
- A list of `AdzunaJob` objects, as defined in `data_models.py`
- The number of remaining calls for the day.

##### **EXAMPLES OF USE**
> ❌ **TO DO**

#### 🛠️ `get_adzuna_cats`

This function requests the API to get a list of existing categories, the used endpoint being `GET jobs/{country}/categories`.
> ❌ **DEVELOP**

#### 🛠️ `get_adzuna_locs`

This function requests the API to get salary data for locations inside an area, the used endpoint being `GET jobs/{country}/geodata`
> ❌ **DEVELOP**

#### 🛠️ `dump_adzuna_jobs`

This function allows to dump ads transformed data from the API to be stored in JSON format in the `data` folder.

### `the_muse.py`
Same as previously, but for The Muse API.

### `utils.py`
Sums up utility functions or constants used in the whole project, essentially to refactor the code and externalize specific purposes (like authenticating to the APIs and creating a client.)

### `adzuna_urls`
Module devoted to forge/scraped URLs involved with Adzuna API, meaning:
- Adzuna's own pages
- HelloWork pages

corresponding to a job ad.

### `data_models`
This module contains logic devoted to **transform** extracted data.
