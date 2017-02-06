# LineReader

Tool works under python3
Help people read charts

Usage Example:


```sh
$ python LineReader.py 60000 100 0 0 0001.jpg output.csv
```

Parameters are respectively:
* Maximum X Value tat Will be clicked.
* Maximum Y Value tat Will be clicked.
* Anything (TODO)
* Anything (TODO)
* Input file
* Output file

In program choosing is by mouse pointer + spacebar, 
because click is used for zoom and navigation.

Program opens window where one chooses (0,0) point than 
X Max point (XMAX,0) , as specified in commmand line,
Y Max point (0,YMAX), as specified in commmand line, 
every other point selected will be decoded in this coordinates and 
saved (appended!) to output (CSV format) 
