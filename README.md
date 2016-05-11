Currently a work in progress. Source code is python3 compatible.

You will need an API key of your own from http://en.ilmatieteenlaitos.fi/.

#### To try out:
```
$ pip install -r requirements.txt  
$ export FMI_API_KEY=<your API key from Ilmatieteen laitos>
$ python main.py
```

In the browser open the address `http://localhost:5000/forecast?location=hels`

It should show the location data for Helsinki Central Railway Station.
