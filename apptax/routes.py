#coding: utf8
from flask import jsonify, Blueprint
from . import models

from taxhubapi import init_app
from taxhubapi import db

from sqlalchemy import create_engine, MetaData, select, Table

#For debug
import pprint

adresses = Blueprint('bib_taxons', __name__)

@adresses.route('/', methods=['GET'])
def get_bibtaxons():
    results = models.BibTaxons.query.all()
    # return jsonify({'bibtaxons': results})
    return jsonify(data=[c.as_dict() for c in results])


#Test mix reflection/mapping db sur une table
@adresses.route('/bib_taxons_taxref', methods=['GET'])
def get_bibtaxonsXtaxref():
    #connexion DB
    engine = create_engine(init_app().config['SQLALCHEMY_DATABASE_URI'])
    meta = MetaData(bind=engine)

    meta.reflect(schema='taxonomie', views=True)

    tableBibTaxon = meta.tables['taxonomie.bib_taxons']
    tableTaxref = meta.tables['taxonomie.taxref']

    results = db.session.query(tableBibTaxon, tableTaxref)\
        .join(tableTaxref, tableBibTaxon.columns.cd_nom==tableTaxref.columns.cd_nom)\
        .all()

    columns = [column.name for column in tableTaxref.columns] + [column.name for column in tableBibTaxon.columns]
    rows = [
        {
            c: getattr(row, c)
                for c in columns
        }
        for row in results
    ]

    return jsonify(rows)

#Test reflecting db sur une table
@adresses.route('/taxref', methods=['GET'])
def get_taxref():
    #connexion DB
    engine = create_engine(init_app().config['SQLALCHEMY_DATABASE_URI'])
    meta = MetaData(bind=engine)

    meta.reflect(schema='taxonomie', views=True)

    tableTaxref = Table('taxonomie.taxref', meta, autoload=True)
    results = select([tableTaxref])\
                .where(tableTaxref.columns.nom_complet.like('%Faga%'))\
                .limit(5)\
                .execute()

    rows = [
        {c.name: getattr(row, c.name)
            for c in [column for column in tableTaxref.columns]
            } for row in results
        ]

    return jsonify(rows)

#Test reflecting db sur une vue
@adresses.route('/plantae', methods=['GET'])
def get_taxonPlantae():
    #connexion DB
    engine = create_engine(init_app().config['SQLALCHEMY_DATABASE_URI'])
    meta = MetaData(bind=engine)

    meta.reflect(schema='taxonomie', views=True)
    print(meta.tables)
    tableTaxref = meta.tables['taxonomie.v_bibtaxon_attributs_plantae']
    # .where(tableTaxref.columns.nom_complet == 'Animalia')\
    results = select([tableTaxref])\
                .limit(5)\
                .execute()

    rows = [
        {c.name: getattr(row, c.name)
            for c in [column for column in tableTaxref.columns]
            } for row in results
        ]

    return jsonify(rows)
