from flask import jsonify

from taxhubapi import init_app
from taxhubapi import db

from sqlalchemy import create_engine, MetaData, Table

class GenericTable:
    def __init__(self, tableName, schemaName):
        engine = create_engine(init_app().config['SQLALCHEMY_DATABASE_URI'])
        meta = MetaData(bind=engine)
        meta.reflect(schema=schemaName, views=True)
        self.tableDef = meta.tables[tableName]
        self.columns = [column.name for column in self.tableDef.columns]

    def serialize(self, data):
        return serializeQuery(data, self.columns)

def serializeQuery( data, columnDef):
    rows = [
        {c['name'] : getattr(row, c['name']) for c in columnDef if getattr(row, c['name']) != None } for row in data
    ]
    return rows


def serializeQueryOneResult( row, columnDef):
    row = {c['name'] : getattr(row, c['name']) for c in columnDef if getattr(row, c['name']) != None }
    return row
