#coding: utf8
from flask import jsonify, Blueprint
from flask import request

from taxhubapi import init_app
from taxhubapi import db
from ..utils import sqlalchemy as sqlautils
from .models import BibTaxons, Taxref
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
        if param in bibTaxonColumns:
            col = getattr(bibTaxonColumns,param)
            q = q.filter(col == parameters[param])
        elif param == 'ilikelatin':
            q = q.filter(taxrefColumns.lb_nom.ilike(parameters[param]+'%'))
    count= q.count()
    results = q.limit(limit).all()
    taxonsList = []
    for r in results :
        obj = r.as_dict()
        obj['is_doublon'] = False

        #Ajout des synonymes
        #!! Deux façons d'écrire la requête avec des perfs très différentes mais alors vraiment
        # q = select([BibTaxons.id_taxon])\
        #     .where(func.taxonomie.find_cdref(BibTaxons.cd_nom) == func.taxonomie.find_cdref(obj['cd_nom']))\
        #     .where(BibTaxons.id_taxon != obj['id_taxon'])
        #@TODO réécrire la requête en mode subquery
        q= "SELECT id_taxon \
            FROM taxonomie.bib_taxons t \
            JOIN taxonomie.taxref tx ON tx.cd_nom = t.cd_nom\
            WHERE tx.cd_ref IN (\
                SELECT  tx.cd_ref FROM taxonomie.taxref tx \
                WHERE  tx.cd_nom = %d \
            ) AND NOT t.id_taxon = %d" % (obj['cd_nom'],obj['id_taxon'])
        results =db.session.connection().execute(q)


        if results.rowcount > 0 :
            print(results.rowcount)
            print([i.id_taxon for i in results])
            obj['is_doublon'] = True
            obj['synonymes'] = [i.id_taxon for i in results]
        taxonsList.append(obj)

    return taxonsList
