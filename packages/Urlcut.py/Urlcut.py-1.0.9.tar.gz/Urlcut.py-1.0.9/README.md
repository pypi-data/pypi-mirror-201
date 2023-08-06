<h1 align="center">Urlcut.py</h1>

<h3 align="center">This is the official Urlcut Python package.</h3>



### Install


```sh

pip install Urlcut.py

```



### Usage



```py

import urlcutpy as Urlcut
Urlcut.Authenticate("API-Key")

```


### How to shortend a link


```py

Response = Urlcut.Create("https://www.example.com")
print(Response)

```



> Output



```json

{

  "success": true,

  "shortened": "CxTYCb",

  "domain": "example.com",

  "credits": 0.4
}

```



### How to delete an existing short link



```js

Response = Urlcut.Delete("Example-Short")
print(Response)

```



> Output



```json

{

  "success": true

}

```



### How to get the analytics of a short link



```js

Response = Urlcut.Analytics("Example-Short")
print(Response)

```



> Output



```json

{

  "success": true,

  "countriesOfTheUsers": [ { "DE": 1 } ],

  "usersDeviceType": { "PC": 1, "PHONE": 0 }

}

```