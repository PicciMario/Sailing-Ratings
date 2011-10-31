# Sailing rating calculator.
by PicciMario <mario.piccinelli@gmail.com>

Used to check delta arrival times for boats with different ratings
in a compensated time race.

If you are running a race and know your arrival time (even approximate)
and your rating, you can check how much time the different rated boats
have to arrive before or after you to have the same arrival time after
compensation.

For example, if you are racing a 1h race on a Mousse 99 (rating 0.75), 
using the provided ratings file (iseo.dat), you can type:

<blockquote>
./rating.py -f iseo.dat -r 0.75 -t 1
</blockquote>

and see:

<blockquote>
[...]<br>
Melges 24        -0:10:00    (+0:50:00 * 0.90 = +0:45:00)  <br>
Mousse 99        --------    (+1:00:00 * 0.75 = +0:45:00)  <---- ref. boat<br>
[...]
</blockquote>

So, you know that, if your race is 1h long and you arrive no more than 
10 minutes after the Melges 24, you win!

## Usage: 

<blockquote>
./rating.py -f rating_file
</blockquote>

Options:

* -h          this help
* -f file     file containing the rating table
* -r value    reference rating (default: 0.75)

Race length in real time for the reference boat
(if more than one are present they are added):

* -s value    seconds
* -m value    minutes
* -t value    hours

Default: 1h

The rating table must be a CSV file in the form:
boat class, rating coefficient