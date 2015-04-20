import json
import python_jsonschema_objects as pjs


investigationSchema = json.load(open("schemas/investigation_schema.json"))
investigationBuilder = pjs.ObjectBuilder(investigationSchema)
ns = investigationBuilder.build_classes()






