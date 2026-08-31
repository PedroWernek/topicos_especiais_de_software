from marshmallow import Schema, fields, validate

class ProdutoSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1))
    preco = fields.Float(required=True, validate=validate.Range(min = 0.0))
    categoria_id = fields.Int(required=True) 

produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)
