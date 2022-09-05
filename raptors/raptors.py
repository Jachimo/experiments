#!/usr/bin/env python

# An attempt to solve xkcd's "Raptor Problem" using Python 2.x.
# See http://xkcd.com/135/ for more information on the setup.

import sys
import math

# Global variables

TRIDIST = 20.0  # Distance raptors are from each other in triangle
STARTRANGE = (TRIDIST / math.sqrt(3))  # Distance raptors are from human in center
KILLRADIUS = 0.5  # How close (in meters) a raptor needs to get to kill the man
TICKLENGTH = 0.025  # How long in seconds for each "tick" or turn of the simulation


# Utility functions to make life easier

def rad(deg):
	"""Quick function to convert degrees to radians"""
	return deg*(math.pi / 180)

def deg(rad):
	"""Quick function to convert radians to degrees"""
	return rad*(180 / math.pi)

def polarDistance( r1, theta1, r2, theta2 ):  # Theta1 and Theta2 should be in degrees
	"""Calculate distance between two polar coords"""
	return math.sqrt( (r1)**2 + (r2)**2 - (2*(r1)*(r2)*math.cos( rad(theta1 - theta2) )))


# Class definitions

class Actor:
	"""An actor in the system.  Actors have a position, direction, and speed."""
	def __init__(self, x=0.0, y=0.0, heading=0.0, speed=0.0, maxSpeed=0.0 ):
		""" Kinda/sorta the class constructor """
		self.position = ( x, y )
		self.heading = heading
		self.speed = speed
		self.maxSpeed = maxSpeed
	
	def updatePosition(self, interval):
		"""Update the position of the actor, using a specified time interval in seconds."""
		# Starting position
		startX = self.position[0]
		startY = self.position[1]
		# Calculate distance traveled in the time interval (neglect accel.)
		dist = self.speed * interval
		moveX = dist * math.cos( rad(self.heading) )
		moveY = dist * math.sin( rad(self.heading) )
		# Update Actor.position
		self.position = ( (startX+moveX), (startY+moveY) )

class World:
	"""The whole system, which contains several Actors."""
	def __init__(self):
		"""Populate the world with the four actors; the man and three raptors, and a timestamp"""
		# The man, at the origin, standing still at the very beginning
		self.man = Actor(x=0.0, y=0.0, heading=0.0, speed=0.0, maxSpeed=6.0)
		
		# The first raptor, along the Y axis, which is injured/slow
		self.injuredRaptor = Actor()
		self.injuredRaptor.position = ( 0, (20 / math.sqrt(3)) )
		self.injuredRaptor.speed = 0.0
		self.injuredRaptor.maxSpeed = 10.0
		self.injuredRaptor.distance = (20/math.sqrt(3))
		
		# The second raptor, healthy/fast
		self.secondRaptor = Actor()
		self.secondRaptor.position = ( (20/math.sqrt(3))*math.cos(rad(210)), (20/math.sqrt(3))*math.sin(rad(210)) )
		self.secondRaptor.speed = 0.0
		self.secondRaptor.maxSpeed = 25.0
		self.secondRaptor.distance = (20/math.sqrt(3))
		
		# The third raptor, also healthy/fast
		self.thirdRaptor = Actor()
		self.thirdRaptor.position = ( (20/math.sqrt(3))*math.cos(rad(330)), (20/math.sqrt(3))*math.sin(rad(330)) )
		self.thirdRaptor.speed = 0.0
		self.thirdRaptor.maxSpeed = 25.0
		self.thirdRaptor.distance = (20/math.sqrt(3))
		
		# Shortest distance
		self.shortestDist = (20/math.sqrt(3))
		
		# Timestamp, for tracking everything
		self.timeStamp = 0.0
	
	def setRunDirection(self, manHeading):
		"""Set the direction that the man runs in, in degrees where x-axis is zero."""
		self.man.speed = 6.0  # If we assume he starts moving quickly at max speed
		self.man.heading = float(manHeading)
	
	def updateRaptorHeading(self, raptor):
		"""Calculate the heading for a raptor so that it is looking right at the man."""
		# First break the man's position into x and y components
		manX = self.man.position[0]
		manY = self.man.position[1]
		
		# And do the same for the raptor that we pass in
		raptorX = raptor.position[0]
		raptorY = raptor.position[1]
		
		# Calculate the heading in radians
		if (manX - raptorX) == 0:  # vertical line, special case
			if manY >= raptorY:  # man above raptor
				raptor.heading = 90.0
			else:  # raptor above man
				raptor.heading = 270.0
		else: # general case
			raptor.heading = deg( math.atan( (manY - raptorY)/(manX - raptorX) ) )
	
	def updateRaptorSpeed(self, raptor, interval):
		"""Update the raptor's speed given a time increment."""
		if raptor.speed < raptor.maxSpeed :
			# If the raptor hasn't reached top speed yet, it accels at 4 m/s^2
			curspd = raptor.speed + (4 * interval)
			if curspd < raptor.maxSpeed: # Don't want to let it exceed max speed
				raptor.speed = curspd
			else:
				raptor.speed = raptor.maxSpeed
		else:
			raptor.speed = raptor.maxSpeed
	
	def calcRaptorDistance(self, raptor):
		"""Calculate the distance between a raptor and the man"""
		manX = self.man.position[0]
		manY = self.man.position[1]
		raptorX = raptor.position[0]
		raptorY = raptor.position[1]
		raptor.distance = math.fabs( math.sqrt( (raptorX - manX)**2 + (raptorY - manY)**2 ) )
	
	def calcShortestDist(self):
		"""Return the shortest distance between the man and any of the raptors."""
		return min(self.injuredRaptor.distance, self.secondRaptor.distance, self.thirdRaptor.distance)
	def updateShortestDist(self):
		"""Update World.shortestDist"""
		self.shortestDist = self.calcShortestDist()
	
	def tick(self, interval):
		"""Move forward in time by some interval (seconds), update positions, headings, speeds."""
		self.timeStamp = self.timeStamp + interval
		
		# Update raptor headings (man's heading is const.)
		self.updateRaptorHeading(self.injuredRaptor)
		self.updateRaptorHeading(self.secondRaptor)
		self.updateRaptorHeading(self.thirdRaptor)
		
		# Update raptor speeds (man's speed is const.)
		self.updateRaptorSpeed(self.injuredRaptor, interval)
		self.updateRaptorSpeed(self.secondRaptor, interval)
		self.updateRaptorSpeed(self.thirdRaptor, interval)
		
		# Update raptor and man positions
		self.man.updatePosition(interval)  # move man first
		self.injuredRaptor.updatePosition(interval)
		self.secondRaptor.updatePosition(interval)
		self.thirdRaptor.updatePosition(interval)
		
		# Calulate and update raptor distances
		self.calcRaptorDistance(self.injuredRaptor)
		self.calcRaptorDistance(self.secondRaptor)
		self.calcRaptorDistance(self.thirdRaptor)
		
		# Update overall shortest distance
		self.updateShortestDist()

def simulateVerbose(dir):
	print "You have decided to run at a heading of " + str(dir) + " degrees."
	print "Using kill radius of " + str(KILLRADIUS) + " meters."
	print "Simulating using " + str(TICKLENGTH) + " second clock ticks."
	
	w = World()  # instantiate a new world for the simulation
	w.setRunDirection(dir)  # set the direction to run in
	
	while (w.shortestDist > KILLRADIUS):
		w.tick(TICKLENGTH)
		print "Time: " + str(w.timeStamp) + "   Distance: " + str(w.shortestDist)
	else:
		print "You were eaten by a raptor."
		print "Final time was " + str(w.timeStamp) + " seconds."


def simulate(dir):
	w = World()  # instantiate a new world for the simulation
	w.setRunDirection(dir)  # set the direction to run in
	
	while (w.shortestDist > KILLRADIUS):
		w.tick(TICKLENGTH)
		if w.timeStamp > 100.0:
			return "ERROR"
	else:
		return w.timeStamp

def fullSim():
	for i in range(0,359):
		print "Angle: " + str(i) + "   Lifespan: " + str(simulate(i))

