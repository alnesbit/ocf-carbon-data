#   OCF coding challenge

Pull multiple years of data about Carbon Intensity of the UK and write
it to a file.


##  Installation and system requirements

This utility consists of a single file `pull_carbon_data.py`.  Copy
this file to any directory you want to run it from.

Ensure that `python3` is in your `$PATH`.

The only external dependency is the Requests library ("an elegant and
simple HTTP library for Python, built for human beings").  Install
Requests the usual way, perhaps in a virtualenv in which you are doing
your development and testing:

```
python -m pip install requests
```


### Development and testing environment

-   Debian GNU/Linux 11.5
-   Python 3.9.2
    -   pip 20.3.4
    -   requests 2.28.1


##  Executing the utility

Running the utility will output progress data to standard output and
save the carbon intensity data to the specified filename:

```
$ ./pull_carbon_data.py carbon_data.out
Pulling data for 2017-09-12
Pulling data for 2017-09-13
...
Pulling data for 2022-11-04

$ cat carbon_data.out
2017-09-11T23:00Z       2017-09-11T23:30Z       134     140
2017-09-11T23:30Z       2017-09-12T00:00Z       143     144
2017-09-12T00:00Z       2017-09-12T00:30Z       137     142
2017-09-12T00:30Z       2017-09-12T01:00Z       134     140
2017-09-12T01:00Z       2017-09-12T01:30Z       133     139
2017-09-12T01:30Z       2017-09-12T02:00Z       122     137
...
```

The data fields are separated by tabs, with one line per each
30-minute time period.  The four fields are as follows:

```
From	To		Forecast	Actual
```


##  Improvements

Although this script satisfies the requirements of the challenge
without overengineering, there is much opportunity to discuss
optimization:
-   user interface, argument parsing
-   verbose output, debug output
-   output formats (pluggable?)
    -   CSV
    -   SQLite
    -   JSON
    -   etc
-   what to do with missing data?
-   creating a module
-   restarting a failed connection
-   checking for error codes
-   better API throttling
-   would a cluster of VPS'es in the cloud picking API request off a
    queue potentially speed up the collection of data?
-   optimization of data structures during data collection
