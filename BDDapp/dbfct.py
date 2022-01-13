import sqlite3
conn = sqlite3.connect("data.db")
c = conn.cursor()


def creer_table():
	c.execute('CREATE TABLE IF NOT EXISTS tabletexte(texte TEXT, etat TEXT, date_etat DATE)')


def ajout_data(texte, etat, date_etat):
	c.execute('INSERT INTO tabletexte(texte, etat, date_etat) VALUES (?,?,?)',(texte, etat, date_etat))
	conn.commit()

def voir_data():
	c.execute('SELECT * FROM tabletexte')
	data = c.fetchall()
	return data


def voir_unique_texte():
	c.execute('SELECT DISTINCT texte FROM tabletexte')
	data = c.fetchall()
	return data

def get_texte(texte):
	c.execute('SELECT * FROM tabletexte WHERE texte="{}"'.format(texte))
	data = c.fetchall()
	return data

def edit_texte_data(new_texte, new_etat, new_date_etat, texte, etat, date_etat):
	c.execute("UPDATE tabletexte SET texte=?, etat=?, date_etat=? WHERE texte=? and etat=?and date_etat=?", (new_texte, new_etat, new_date_etat))
	conn.commit()
	data=c.fetchall()
	return data
