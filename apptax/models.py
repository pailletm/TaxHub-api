#coding: utf8
from taxhubapi import db

class BibTaxons(db.Model):
    __tablename__ = 'bib_taxons'
    __table_args__ = {'schema':'taxonomie'}
    id_taxon = db.Column(db.Integer, primary_key=True)
    cd_nom = db.Column(db.Integer)
    nom_latin = db.Column(db.Unicode)
    nom_francais = db.Column(db.Unicode)
    auteur = db.Column(db.Unicode)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<BibTaxons %r>'% self.nom_latin
