from bottle import *
from json import *


@route('/add/<entier1:int>/<entier2:int>', method='GET')
def add(entier1, entier2):
	return dumps(entier1 + entier2)


@route('/sub/<entier1:int>/<entier2:int>', method='GET')
def sub(entier1, entier2):
	return dumps(entier1 - entier2)


@route('/mul/<entier1:int>/<entier2:int>', method='GET')
def mul(entier1, entier2):
	return dumps(entier1 * entier2)


@route('/div/<entier1:int>/<entier2:int>', method='GET')
def div(entier1, entier2):
	return dumps(entier1 // entier2)


@route('/mod/<entier1:int>/<entier2:int>', method='GET')
def mod(entier1, entier2):
	return dumps(entier1 % entier2)


run(host='localhost', port=8080)
