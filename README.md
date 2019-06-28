An API wrapper to post and parse poll tapes to the STAR-Vote append-only bulletin. This package also includes the append-only-bulletin board from STAR-Vote.

**Installation**  
***API Server***  
Use Python3/pip3.  
run ```pip3 install -r requirements.txt``` to install packages.  
for ocr: ```brew install tesseract```  
  
***Append-only Bulletin Server***  
From inside the STAR-Vote directory, run:  
```cabal update```  
```cabal sandbox init```  
```cabal install -j ./append-only-bb```  
  
**Running**
***API Server***  
To start the api server, simply sun ```python app.py```.  
A simple api endpoint example exists at ```localhost:8080/api/hello```.  

***Append-only Bulletin Server***  
To run the server, you need to find the executable in the sanbox folder.  
Mine was located at:  
```./dist/dist-sandbox-12b8a418/build/bbserver/bbserver```
If you dont have a ```dist``` folder, try looking under ```./.cabal-sandbox/bin/```
