import coreapi


def get_inequality_schema_fields(name, location, required, schema, description=''):
    return [
        coreapi.Field(name, required=required, location=location, schema=schema(description=description)),
        coreapi.Field(f'{name}__gt', description=f'{description} ',required=required, location=location, schema=schema(description=f'{description} (greater than)')),
        coreapi.Field(f'{name}__gte', description=f'{description} ',required=required, location=location, schema=schema(description=f'{description} (greater than or equal)')),
        coreapi.Field(f'{name}__lt', description=f'{description} ',required=required, location=location, schema=schema(description=f'{description} (lesser than)')),
        coreapi.Field(f'{name}__lte', description=f'{description} ',required=required, location=location, schema=schema(description=f'{description} (lesser than or equal)')),
    ]
