from marshmallow import Schema, fields, validate

#verificador de json
class CategoriaSchema(Schema):
    id = fields.Int(dump_only=True)#somente leitura
    nome = fields.Str(required=True, validate=validate.Length(min=1))

categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True) #para listas
