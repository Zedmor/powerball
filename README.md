

# powerball

powerball is a prototype built for Greenphire company as a part of interview 
process for engineering position.

It
 is built with [Python][0] using the 
[Django Web Framework][1].

Project is in powerball app.

Users are able to register accounts, login, logout, enter their numbers and watch other users entries (as registered and unregistered users).

## User story

Powerball story as provided:

As a Greenphire employee I would like to add my favorite 6 numbers to consider for a Powerball entry ticket so that I can win 1 billion dollars.


* Capture the name of the employees entering the number.
* The first 5 favorite numbers will need to be in the range of 1 to 69 and unique. (remember that this is a drawing so there cannot be duplicates in this range of 5 numbers)
* 6th favorite number will need to be in the range of 1 to 26 and flagged as 
the 6th Powerball number.
* Keep count of each individual favorite number provided to determine which numbers to use in our final winning number. (i.e. count the duplicates).
* Retrieve the max count of each unique duplicate number and use them as the 
Powerball numbers.
* if there is a tie based on the max counts randomly select the tied number.
* Display all employees with their corresponding number entries.
* Display the final Powerball number based on the requirements above.

Sample output:
 
    Enter your first name: Wade
    Enter your last name: Wilson
    select 1st # (1 thru 69): 12
    select 2nd # (1 thru 69 excluding 12): 20
    select 3rd # (1 thru 69 excluding 12 and 20): 23
    select 4th # (1 thru 69 excluding 12, 20, and 23: 56
    select 5th # (1 thru 69 excluding 12, 20, 23, and 56: 30
    select Power Ball # (1 thru 26): 25
    
     
    Wade Wilson 15 26 33 60 34 Powerball: 16
    Frank Castle 15 26 34 56 61 Powerball: 16
     
    Powerball winning number:
    15 26 34 55 63 Powerball: 16

## Installation

### Quick start

To set up a development environment quickly, first install Python 3. It
comes with virtualenv built-in. So create a virtual env by:

    1. `$ python3 -m venv powerball`
    2. `$ . powerball/bin/activate`

Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate

### Detailed instructions

Take a look at the docs for more information.

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
