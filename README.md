# Hack-the-Build-Dreamers-
An initiative to measure crowd and ensure safety at various places (restaurants, stores, hospitals, events, etc.) before visiting them.

## Problem it solves
PROBLEM IT SOLVES:
Health being our first priority,this project aims to solve the problem of frequent human contact at heavily crowded places in the wake of the Corona Virus Pandemic and help minimize social contanct.
#### Current Scenario
1. If we wish to visit a restaurant/ grocery store/salon, we would want to select a place where there are very few people at real-time so as to avoid crowds and waiting and hence to avoid viral exposure. 
2. Alternatively, if there is a particular hour of the day when there are very few people at the store/salon/restaurant, we would select that hour to visit the place. 
3. Right now, there is no solution for this problem, that is, there is no way we can find out which place has how much customer-density at real time as well as any live updates about the place regarding sanitary measures followed there.

## Key Highlights
Close-o-meter is an interactive web platform, where users can get to know live updates about crowds as well people’s reviews about the sanitary conditions at different places like restaurants, events, stores, malls etc and hence choose the place safest to them.
1. Users can track people at different locations by visualising it in maps having clusters of crowd marking them with red, if number of people/area density is high, yellow for moderate density and green for safest density at different locations.
2. Users can explore different restaurants and dining places and check-in by scanning qr code at the restaurant, other users will be able to see the number of people currently present at the restaurant.
3. After authenticating through Google oauth and checking in, users can now see live updates about the sanitary conditions of the restaurant, people’s reviews and ratings, and number of people checking in at regular intervals providing better user experience.
4. For checking out, users can provide feedback and ratings to the place to help others track the safety at different places. 


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Requires Python3 to run locally. See instructions to setup [Python3](https://www.python.org/downloads/).

### Installation
* Clone the repository in a folder and write the following commands
```
1.git clone https://github.com/kbindra/Hack-the-build-Dreamers.git

```
#### Backend(Flask)
* Setup virtual environment
```
1.pip install virtualenv
2.virtualenv venv 
3.env/Scripts/activate
```
* Install all dependencies
```
pip install -r requirements.txt
```
* Run Server
```
python app.py
Open localhost:5000 on your browser
```
![Screenshot of home page](https://github.com/kbindra/Hack-the-build-Dreamers/blob/master/screenshots/frontpage.jpg)
