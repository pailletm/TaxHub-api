#coding: utf8
from flask import jsonify, json, Blueprint
from flask import request

from taxhubapi import init_app
from taxhubapi import db
from ..utils import sqlalchemy as sqlautils
from .models import BibTaxons, Taxref,CorTaxonAttribut
from sqlalchemy import create_engine, MetaData, select, Table, func

adresses = Blueprint('bib_taxons', __name__)

@adresses.route('/', methods=['GET'])
@sqlautils.json_resp
def get_bibtaxons():
    bibTaxonColumns = BibTaxons.__table__.columns
    taxrefColumns = Taxref.__table__.columns
    parameters = request.args

    q = db.session.query(BibTaxons)\
        .join(BibTaxons.taxref)

    #Traitement des parametres
    limit = parameters.get('limit') if parameters.get('limit') else 100
    offset = parameters.get('page') if parameters.get('page') else 0

    for param in parameters:
        if param in taxrefColumns:
            col = getattr(taxrefColumns,param)
            q = q.filter(col == parameters[param])
        elif param in bibTaxonColumns:
            col = getattr(bibTaxonColumns,param)
            q = q.filter(col == parameters[param])
        elif param == 'ilikelatin':
            q = q.filter(bibTaxonColumns.nom_latin.ilike(parameters[param]+'%'))
        elif param == 'ilikelfr':
            q = q.filter(bibTaxonColumns.nom_francais.ilike(parameters[param]+'%'))
    count= q.count()
    results = q.limit(limit).all()
    taxonsList = []
    for r in results :
        obj = r.as_dict()
        obj['is_doublon'] = False

        #Ajout des synonymes
        q = db.session.query(BibTaxons.id_taxon)\
            .join(BibTaxons.taxref)\
            .filter(Taxref.cd_ref== func.taxonomie.find_cdref(obj['cd_nom']))\
            .filter(BibTaxons.id_taxon != obj['id_taxon'])
        results =q.all()

        if q.count() > 0 :
            obj['is_doublon'] = True
            obj['synonymes'] = [i.id_taxon for i in results]
        taxonsList.append(obj)

    return taxonsList


@adresses.route('/', methods=['POST', 'PUT'])
@adresses.route('/<id_taxon>', methods=['POST', 'PUT'])
@sqlautils.json_resp
def insertUpdate_bibtaxons(id_taxon=None):

    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json(silent=True)
    else:
        return "415 Unsupported Media Type ;)"

    if id_taxon:
        bibTaxon =db.session.query(BibTaxons).filter_by(id_taxon=id_taxon).first()
    else :
        bibTaxon = BibTaxons(
            cd_nom = data['cd_nom'],
            nom_latin =  data['nom_latin'],
            nom_francais =  data['nom_francais'],
            auteur =data['auteur'] if 'auteur' in data else None
        )
    db.session.add(bibTaxon)
    db.session.commit()

    #Traitement des attibuts
    id_taxon = bibTaxon.id_taxon

    #Suppression des attributs exisitants
    bibTaxonAtts = bibTaxon.attributs
    for bibTaxonAtt in bibTaxon.attributs:
         db.session.delete(bibTaxonAtt)
    db.session.commit()

    for att in data['attributs_values']:
        attVal = CorTaxonAttribut(
            id_attribut = att,
            id_taxon = id_taxon,
            valeur_attribut =data['attributs_values'][att]
        )
        db.session.add(attVal)
    db.session.commit()

    return bibTaxon.as_dict()
