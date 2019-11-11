from app import *

from flask import render_template, request, redirect, url_for, flash


@server.route('/', methods=["GET","POST"])
def landingpage():
	return render_template('landingpage.html', title="Welcome!")