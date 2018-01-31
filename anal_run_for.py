#!/usr/bin/env python3

import psycopg2 

import config

import anal

import sys



def run_anal(name):
	conn = psycopg2.connect(host=config.PGHOST, user=config.PGUSER, password=config.PGPASSWD, database=config.PGDB)
	curr = conn.cursor()

	curr.execute('SELECT id FROM sondes WHERE name = %s', (name,))

	sonde = curr.fetchone()

	# print(sonde)

	if sonde == None:
		return 'notfound'


	sonde_id = sonde[0]


	pred = anal.linear_predict(conn.cursor(), sonde_id)


	if pred is None:
		return 'toohigh'

	predx, predy, elevation = pred

	return(predx, predy, elevation)
