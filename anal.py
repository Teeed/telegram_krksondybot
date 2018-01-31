#!/usr/bin/env python3

import numpy as np
import json

import urllib.request
import urllib.parse

from datetime import datetime
import time


import config

def linear_predict(curr, sonde_id):
	curr.execute('SELECT pp.lat, pp.lon, pp.alt FROM FALLING_SONDE_DATA(%s) AS pp', [sonde_id])


	data = curr.fetchall()
	data = np.array(data)

	try:
		x,y,z = data.T
	except ValueError:
		return None

	datamean = data.mean(axis=0)
	uu, dd, vv = np.linalg.svd(data - datamean)
	p = 1

	linepts = vv[0] * np.mgrid[-p:p:2j][:, np.newaxis]
	linepts += datamean

	# print(linepts)

	lx, ly, lz = linepts.T

	A_xz = np.vstack((lx, np.ones(len(lx)))).T
	m_xz, c_xz = np.linalg.lstsq(A_xz, lz)[0]

	A_yz = np.vstack((ly, np.ones(len(ly)))).T
	m_yz, c_yz = np.linalg.lstsq(A_yz, lz)[0]

	def lin(z):
		x = (z - c_xz)/m_xz
		y = (z - c_yz)/m_yz
		return x, y

	elevation_data = json.loads(urllib.request.urlopen('https://maps.googleapis.com/maps/api/elevation/json?%s' % urllib.parse.urlencode(
		{
		'locations': '%s,%s' % (x[0], y[0]),
		'key': config.GMAPS_API_KEY,
		}
	)).read().decode('utf8'))

	elevation = elevation_data['results'][0]['elevation']

	# sonde is >7km above the ground
	if z[0] - 7000 > elevation:
		return None

	predx, predy = lin(elevation)

	return predx, predy, elevation

	# sonde_name = sonde_name.upper()

	# print(sonde_name, predx, predy, elevation)



	# from mpl_toolkits.mplot3d import Axes3D
	# import matplotlib.pyplot as plt


	# fig = plt.figure()
	# ax = Axes3D(fig)
	# zz = [elevation, np.max(z)]
	# xx, yy = lin(zz)

	# plt.title(sonde_name)

	# ax.scatter(x, y, z)
	# # ax.plot3D(*linepts.T)
	# ax.plot(xx, yy, zz)


	# plt.show()

