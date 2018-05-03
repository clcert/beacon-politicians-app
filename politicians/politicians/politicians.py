import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
		SECRET_KEY='development key',
		USERNAME='admin',
		PASSWORD='default'
	))
app.config.from_envvar('POLITICIANTS_SETTINGS', silent=True)