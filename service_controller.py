#!/usr/bin/env python3
import subprocess

def check_service_status(name):
	# p = subprocess.Popen(['service', name, 'status'], stdout=subprocess.PIPE)
	# status = p.stdout.readlines()[3].split()[1] == b'active'
	output = subprocess.check_output("service " + name + " status | grep Active", shell=True)
	status = output.split()[1] == b'active'

	# True = active, otherwise -> False
	return status

def start_service(name):
	ret = subprocess.check_call(['service', name, 'start'])
	# returns bool indicator of success
	return ret == 0

def stop_service(name):
	ret = subprocess.check_call(['service', name, 'stop'])
	return ret == 0

def restart_service(name):
	ret = subprocess.check_call(['service', name, 'restart'])
	return ret == 0