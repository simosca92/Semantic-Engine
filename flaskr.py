# -*- coding: utf-8 -*
from gensim.corpora.wikicorpus import WikiCorpus, tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from pprint import pprint
from gensim import models
import multiprocessing
import time
from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
import sys
import gensim
import threading
from gensim.models.fastsent import FastSent
import codecs
from gensim import utils, matutils 
import smart_open

reload(sys)

def getAllSentence(loc):
	allSentence=[]
	file = utils.smart_open(loc)
	title=""
	phrase=""
	row=0
	vect=[]
	for line in file:
		#If I am in a id row
		if("###" in line):
			s=line
			if(title != ""):
				phrase = utils.to_unicode(phrase)
				# each file line is a single sentence in the Brown corpus
				# each token is WORD/POS_TAG
				token_tags = [t for t in phrase.split()]
				# ignore words with non-alphabetic tags like ",", "!" etc (punctuation, weird stuff)
				words = [token for token in token_tags]

				if len(words)<=3:  # don't bother sending out empty sentences
				    continue
				allSentence.append((phrase,utils.to_unicode(title)))
			phrase = ""
			title=s
		else:
			phrase+=utils.to_unicode(line).lower()#MINUSCOLO
		row=row+1
	file.close()

	return allSentence

def loadModel(ID,t=0):
	global sent
	global allDoc
	result=None
	if(ID==1):
		print "Loading DBOW + DMConc model..."
		result= models.Doc2Vec.load('models/DBOWw/my_modelDBOWw.doc2vec')
		print "Done"
	elif(ID==2):
		print "Loading DBOW model..."
		result= models.Doc2Vec.load('models/DBOW/CinLettInf/my_modelDBOW.doc2vec')
		print "Done"
	elif(ID==3):
		print "Loading FASTSENT model..."
		result = FastSent.load('models/dim200/w5/FastSent1_no_autoencoding_200_10_1e-10')
		del sent
		del allDoc
		sent=getAllSentence('corpus/corpus/mergLett.txt')
		allDoc=result.getSentenceVect('models/obj/lettDoc/Vect.npy')
		print "Done"
	return result

sys.setdefaultencoding("utf-8")
app = Flask(__name__)


model=None
#to load how many models you want

model=loadModel(1)
actual=1
topic=1
sent=[]
allDoc=[]

pg=["a", "ad", "affinché", "agl", "agli", "ai", "al", "i", "all", "alla", "alle","allo", "anche", "anziché", "anzichè", "bensì", "che", "chi", "ci", "cioè","coi","col","come", "comunque", "con", "contro", "cosa",
		"cui", "da", "daché", "dachè", "dacché", "dacchè", "dagl", "dagli", "dai", "dal", "dall", "dalla", "dalle", "dallo", "degl", "degli", "dei",
		"del", "dell", "della", "delle", "dello", "di", "dopo", "dov", "dove", "dunque", "durante", "e", "ed", "egli", "eppure", "essi", "finché", "fino", 
		"fra", "giacché", "giacchè", "gl", "gli", "il", "in", "inoltre", "io", "l", "la", "le", "lei", "li", "lo", "loro", "lui", "ma", "mentre", "mi",
		"mia", "mie", "miei", "mio", "ne", "neanche", "negl", "negli", "nei", "nel", "nell", "nella", "nelle", "nello", "nemmeno", "neppure",
		"noi", "non", "nonché", "nondimeno", "nostra", "nostre", "nostri", "nostro", "o", "onde", "oppure", "ossia", "ovvero",
		"per", "perchè", "perciò", "però", "più", "poiché", "prima", "purché", "quale", "quandanche",
		"quando", "quanta", "quante", "quanti", "quanto", "quantunque", "quasi", "quella", "quelle", "quelli", "quello", "questa",
		"queste", "questi", "questo", "quindi", "se", "sebbene", "sennonché", "sennonchè", "senza", "seppure", "si", "siccome",
		"sopra", "sotto", "su", "sua", "subito", "sue", "sugl", "sugli", "sui", "sul", "sull", "sulla", "sulle", "sullo", "suo", "suoi", "talché",
		"ti", "tra", "tu", "tua", "tue", "tuo", "tuoi", "tuttavia", "tutti", "tutto", "un", "una", "uno", "vi", "voi", "vostra", "vostre", "vostri", "vostro"]
app.config.from_object(__name__)
@app.route('/')
#def index():
#	if 'username' in session:
#		return 'Logged in as %s' % escape(session['username'])
#	return 'You are not logged in'
@app.route('/engine', methods=['GET', 'POST'])
#@app.route('/login/<name>',methods=['GET', 'POST'])
def login(result=None):
	#url_for('static', filename='style.css')
	global model
	global actual
	global topic
	global sent
	global allDoc
	session['model']="1"
	session['topic']='t1'
	if request.method == 'POST':
		session['value'] = request.form['value']
		session['model'] = request.form['model']
		session['topic'] = request.form['topic']
		#carico il modello allenato in base alla scelta
		if(str(request.form['model'])=="1"):
			if(actual!=1):
				actual=1
				del model
				model=loadModel(1)
		elif(str(request.form['model'])=="2"):
			if(actual!=2):
				actual=2
				del model
				model=loadModel(2)
		else:
			if(actual!=3):
				actual=3
				del model
				model=loadModel(3,topic)
				session['topic']='t1'
				topic=1
		
		if((session['value']!=" ") and (session['value']!="")): 
			#calcolo i "most_similar"
			#tagg = TaggedDocument(tokens1, ["QUERY"])
			#dv = model.infer_vector(tokens1,alpha=0.5, min_alpha=0.0001, steps=20)
			token=list(gensim.utils.tokenize(str(session['value']).lower()))
			for w in pg:
				try:
					token.remove(w)
					print w
				except ValueError:
					token=token
			if((actual==1) or (actual==2)):
				#PARAGRAPH VECTOR
				model.random.seed(0)
				dv=model.infer_vector(token)
				res=[]
				try:
					sim1=model.docvecs.most_similar(positive=[str(session['value'])], topn=20)
				except:
					sim1="No match found in the dictionary"
				
				#model.random.seed(0)
				sim2=model.docvecs.most_similar([dv], topn=20)
				res.append(sim1)
				#res.append(sim2)
				final=""
				for i in range(0,len(sim2)-1):
					sim = sim2[i]
					st=sim[0].split("***")
					print sim[0]
					#final=final+st[0]
					partial=st[0].replace("###","")
					resString = ''.join([i for i in partial if not i.isdigit()])
					final=final+resString
					final=final+'<br>'
					filename=st[1]
					f = open("corpus/allWikiTrain/"+filename, "r")
					searchlines = f.readlines()
					f.close()
					for k, line in enumerate(searchlines):
						if(st[0] in line):
							for l in searchlines[k:k+3]: 
								final=final+l
							final=final+'<br>'
							break
				#print final
				res.append(final.split('<br>'))		
				return render_template('index.html',result=res)
			
			else:
				#FASTSENT
				query=''
				res=[]
				for t in token:
					query=query + t + ' '
				print query
				if session['topic'] == 't1':
					if(topic!=1):
						del sent
						del allDoc
						sent=getAllSentence('corpus/corpus/mergLett.txt')
						allDoc=model.getSentenceVect('models/obj/lettDoc/Vect.npy')
						topic=1
				elif session['topic'] == 't2':
					if(topic!=2):
						del sent
						del allDoc
						sent=getAllSentence('corpus/corpus/mergInf.txt')
						allDoc=model.getSentenceVect('models/obj/infDoc/Vect.npy')
						topic=2
				else:
					if(topic!=3):
						del sent
						del allDoc
						sent=getAllSentence('corpus/corpus/mergCin.txt')
						allDoc=model.getSentenceVect('models/obj/cinDoc/Vect.npy')
						topic=3
				final=''
				sim=model.mostSimilarSent(sent,query,allDoc,40)
				res.append("No match found in the dictionary")
				for p,t in sim:
					partial=t.replace("###","")
					resString = ''.join([i for i in partial if not i.isdigit()])
					final=final+resString
					final=final+'<br>'
					final=final+" "+p
					final=final+'<br>'
				print sim
				res.append(final.split('<br>'))		
				return render_template('index.html',result=res)
	return render_template('index.html')
@app.route('/logout')
def logout():
	
	session.pop('value', None)
	return redirect(url_for('index'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
