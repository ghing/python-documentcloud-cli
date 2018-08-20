"""
Utility functions to get JSON-serializeable versions of python-documentcloud
objects

"""

def format_date(d):
    return '{:%a, %d %b %Y %H:%m:%S %z}'.format(d)


def serialize_document(doc):
    """Get a Document as a JSON-serializeable object"""

    serialized = {
        'document': {},
    }

    props = [
        'id',
        'title',
        'access',
        'pages',
        'description',
        'source',
        'created_at',
        'updated_at',
        'canonical_url',
        'language',
        'file_hash',
        'contributor',
        'contributor_organization',
        'display_language',
        'data',
        'sections',
        'annotations',
    ]

    serializers = {
        'created_at': format_date,
        'updated_at': format_date,
        'sections': lambda x: [y.__dict__ for y in x],
        'annotations': lambda x: [y.__dict__ for y in x],
    }

    for prop in props:
        serializer = serializers.get(prop)

        val = getattr(doc, prop)
        if serializer is not None:
            val = serializer(val)

        serialized['document'][prop] = val

    return serialized


def serialize_entity(entity):
    """Get an Entity object as a JSON-serializeable object"""

    props = ['type', 'relevance', 'value']
    return {
        p: getattr(entity, p)
        for p in props
    }


def serialize_project(project):
    """Get a Project as a JSON-serializeable object"""

    serialized = {}

    serialized['id'] = project.id
    serialized['title'] = project.title
    serialized['document_ids'] = [
        document_id for document_id in project.document_ids
    ]

    return serialized
