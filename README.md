# Parrot
    ______                    _   
    | ___ \                  | |  
    | |_/ /_ _ _ __ _ __ ___ | |_ 
    |  __/ _` | '__| '__/ _ \| __|
    | | | (_| | |  | | | (_) | |_ 
    \_|  \__,_|_|  |_|  \___/ \__|
	                              
	                              
A fun server that repeats what you tell him to repeat.
An original idea from Guillaume Chelfi and Yannick Méheut.

Fork us on [GitHub](https://github.com/the-useless-one/parrot)

## History

How can someone win an argument? By repeating one's point
of view over, and over, and over, and over, [...], and over.

Let's look at an example:

>"- Dude, this movie totally rocks!
- Meh, I think it's pretty boring...
- Is not.
- Is too.
- Is not!
- Is too!
- Is not!
- Fine, you win..."

The original idea behind Parrot was this simple craving
from Chelfi and me to win every argument. The first version
of this script was written by Chelfi to tell me to shut
up. 

We made improvement when we came to the point where
we were out of ideas to implement. Obviously, the next
step was to make it "networked", and Chelfi had this
amazing idea of enabling everyone to connect to a server
to see the general trend of words.

## REQUIREMENTS

All you need is Python! At the moment, we use Python2,
but a port to Python3 is definitely on our TODO list.

## USAGE

### `parrot_server`
Just go to the `parrot_server` directory and type
the following command:

    ./parrot_server.py <port>

where port is the port the server will listen on.

Don't forget to make the script executable by with:

    chmod +x parrot_server.py

### `parrot_client`
Whoops! Nothing to see here at the moment!

## COPYRIGHT

Parrot - A fun server that repeats what you tell him to repeat.
Guillaume Chelfi and Yannick Méheut
Copyright © 2013

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation, either version 3 of the License, or (at your 
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
Public License for more details.

You should have received a copy of the GNU General Public License along 
with this program. If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
