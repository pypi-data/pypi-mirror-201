from jsonschema import Draft7Validator, validators


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for prop, sub_schema in properties.items():
            if "default" in sub_schema:
                instance.setdefault(prop, sub_schema["default"])

            if "$ref" in sub_schema:
                scope, resolved = validator.resolver.resolve(sub_schema["$ref"])
                if isinstance(sub_schema, dict):
                    sub_schema.update(resolved)
                    del sub_schema["$ref"]

        for error in validate_properties(validator, properties, instance, schema,):
            yield error

    return validators.extend(validator_class, {"properties": set_defaults},)


DefaultValidatingDraft7Validator = extend_with_default(Draft7Validator)
