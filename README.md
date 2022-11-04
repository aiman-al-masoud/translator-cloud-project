# API Documentation

## Translate API

```typescript
{

"from" : string // source language 
"to" : string, // target language
"from_text" : string, // text to be translated
"id" : int // request id
}
```

Response
```typescript
{
"to_text" : string, // translated text
"id" : int // request id
}
```

## Set-Up
### Virtual Enviroment set-up

#### 1) Clone this repo
```
$ git clone https://github.com/aiman-al-masoud/translator-cloud-project.git
```
and navigate to its root directory.

  
#### 2) Create a python virtual environment 
Use this name necessarily, because of the *.gitignore*
```
$ python3 -m venv .venv
```

(You'll be prompted to install the 'venv' module if you don't have it yet).

  
#### 3) Activate the virtual environment

```
$ source .venv/bin/activate
```

(You should notice that the console starts displaying the virtual environment's name before your username and the dollar-sign).

To exit from the virtual environment
```
$ deactivate
```

  
#### 4) Install this app's dependencies 
Inside the virtual environment you just created:
  
```
(venv)$ pip install -r requirements.txt
```

#### 5) Get the models
Move to the *test* directory and execute
```sh
python3 install-packages.py -f en -t it -txt "Hello World"
# en -> it 
```

```sh
python3 install-packages.py -f it -t en -txt "Ciao Mondo"
# it -> en 
```

If there are any problems with downloading language packages:
```
$ python3
>>> import argostranslate.package
>>> argostranslate.package.update_package_index()
>>> exit()
```

And then run the two commands above.
## Testing
### 1) Launch the server
Move to the *src* directory and execute
```
$ python3 -m flask run
```
and navigate to its root directory.

Open the browser on `http://127.0.0.1:5000`