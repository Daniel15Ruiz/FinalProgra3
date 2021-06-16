from flask import Flask, render_template, request, url_for, redirect, flash, url_for
from flask import Flask, session
import json
import networkx as nx
from networkx.algorithms.clique import node_clique_number
from networkx.algorithms.operators.product import _init_product_graph
from networkx.classes.function import nodes
from networkx.drawing import nx_agraph
from networkx.generators.degree_seq import expected_degree_graph
from networkx.generators.trees import prefix_tree
from networkx.readwrite import json_graph
import os
from networkx.utils.decorators import nodes_or_number
from werkzeug import security
from werkzeug.utils import secure_filename

H = nx.DiGraph()

listaprin = []
listasecun = []
listaTercera=[]
Columnas=[]
Columnas2=[]

def Matris():
	Columnas2.clear()
	Filas=[]
	lista=[]
	lista2=[]
	for i in H.nodes:
		Columnas2.append(i)
		Filas.append(i)
        
	p = len(Columnas2)+1
	for i in range (p):
		lista.append(0)
		lista2.append(0)
	listaFinal=[]
	m=1
	for i in Filas:
		lista=lista2.copy()
		lista[0]=i
		for edge in H.edges:
			m=1
			for j in Columnas2:
				if ((i==edge[0] and j == edge[1]) or (i==edge[1] and j == edge[0])):
					lista[m]=1
				m+=1
		
		listaFinal.append(lista)

    

	return listaFinal

proyecto = Flask(__name__)

proyecto.secret_key= 'AyudemeInge'

proyecto.config['UPLOAD_FOLDER'] = 'static/img'

@proyecto.route('/')
def inicio():
    col=[]
    
    x=Matris()
    col=Columnas2.copy()
    
    return render_template("Inicio.html",matris=x,grupo2=listasecun,grupo1=listaprin, columnas=col,grupo3=listaTercera)

@proyecto.route('/home')
def inicio2():
    x=Matris()
    col=Columnas2.copy()

    
    return render_template("Inicio.html",matris=x,grupo2=listasecun,grupo1=listaprin, columnas=col,grupo3=listaTercera)

@proyecto.route('/agregar', methods=["POST"])
def agregado():

    

    
    if request.method == 'POST':
        
	    nombre = request.form['nombre']
	    H.add_node(nombre)
	    listaTercera.append(nombre)
	    listaprin.append(nombre)
	    listasecun.append(nombre)
        
	    H.nodes[nombre]["Titulo"] = ""
	    H.nodes[nombre]["Texto"] = ""
    x=Matris()
    col=Columnas2.copy()
    return render_template("Inicio.html",matris=x,grupo2=listasecun,grupo1=listaprin,columnas=col,grupo3=listaTercera)

@proyecto.route('/unir', methods=["POST"])
def unir():
    if request.method == 'POST':
        nodo1= request.form['a']
        nodo2= request.form['b']
        H.add_edge(nodo1,nodo2)
        print(H.edges)  
        listaprin.remove(nodo1)
        listasecun.remove(nodo2)
        x=Matris()
        col=Columnas2.copy()

        
        return render_template("Inicio.html",matris=x,grupo2=listasecun,grupo1=listaprin,columnas=col,grupo3=listaTercera)

@proyecto.route('/info', methods=["POST"])
def info():
    if request.method=='POST':
        name= request.form['nodo']
           
        #H.nodes[name]["Titulo"]=request.form['titulo']
        #H.nodes[name]["Texto"]= request.form['Parrafo']

        text= str(H.nodes[name]["Titulo"])
        tittle= str(H.nodes[name]["Texto"])

        return render_template("Editar.html",text=text,tittle=tittle,name=name)

@proyecto.route('/guardar', methods=["POST"])
def Ginfo():
    if request.method=='POST':
        name= request.form['nodo']
           
        H.nodes[name]["Titulo"]=request.form['tittle']
        H.nodes[name]["Texto"]= request.form['text']

        text= str(H.nodes[name]["Texto"])
        tittle= str(H.nodes[name]["Titulo"])

        return render_template("Editar.html",text=text,tittle=tittle,name=name)

@proyecto.route('/Inicio')
def ver():
    for n in H.nodes:
        nodiInicio = n
        break
    try:
        text=str(H.nodes[nodiInicio]["Texto"])
    except:
        text=""
    try:
        tittle=str(H.nodes[nodiInicio]["Titulo"])
    except:
        tittle=""
    
    try:
        if list(H.successors(nodiInicio)):
            sigue= list(H.successors(nodiInicio))[0]
        else:
            sigue=0
    except:
        sigue=0
    try:
        if list(H.predecessors(nodiInicio))[0]:
            antes=list(H.predecessors(nodiInicio))[0]
        else:
            antes=0
    except:
        antes=0
    
    return render_template("Ver.html", tittle= tittle, text= text, sigue=sigue, antes=antes)

@proyecto.route('/sigue/<sigue>')
def sigue(sigue):
    name=sigue
    try:
        text=str(H.nodes[name]["Texto"])
    except:
        text=""
    try:
        tittle=str(H.nodes[name]["Titulo"])
    except:
        tittle=""
    try:
        if list(H.successors(name)):
            sigue= list(H.successors(name))[0]
        else:
            sigue=0
    except:
        sigue=0
    try:
        if list(H.predecessors(name))[0]:
            antes=list(H.predecessors(name))[0]
        else:
            antes=0
    except:
        antes=0
    return render_template("Ver.html", tittle= tittle, text= text, sigue=sigue, antes=antes)
    
@proyecto.route('/atras/<atras>')
def atras(atras):
    name=atras
    try:
        text=str(H.nodes[name]["Texto"])
    except:
        text=""
    try:
        tittle=str(H.nodes[name]["Titulo"])
    except:
        tittle=""
    try:
        if list(H.successors(name)):
            sigue= list(H.successors(name))[0]
        else:
            sigue=0
    except:
        sigue=0
    try:
        if list(H.predecessors(name))[0]:
            antes=list(H.predecessors(name))[0]
        else:
            antes=0
    except:
        antes=0
    return render_template("Ver.html",tittle= tittle, text= text, sigue=sigue, antes=antes)

@proyecto.route('/Estructura')
def Vis():
	d = json_graph.node_link_data(H)  
	j=str(d)
	x = j.replace("'", "\"")
	x= x[53:]
	x="{"+x
	return render_template("grafo.html", json=x)



if __name__=="__main__":
	proyecto.run(port=8000,debug=True)