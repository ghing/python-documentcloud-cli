import argparse
import json
import os
import re
import sys

from documentcloud import DocumentCloud, DoesNotExistError

from .serialize import (
    serialize_document,
    serialize_entity,
    serialize_project,
)


def get_document(args):
    """Retrieve document metadata"""

    client = DocumentCloud(args.username, args.password)

    try:
        doc = client.documents.get(args.id)
        print(json.dumps(serialize_document(doc)))

    except DoesNotExistError:
        sys.stderr.write("Document with id '{}' does not exist\n".format(
            args.id))
        sys.exit(1)




def get_document_entities(args):
    """Retrieve document entities"""

    client = DocumentCloud(args.username, args.password)

    try:
        doc = client.documents.get(args.id)

        print(json.dumps({
            'entities': [serialize_entity(e) for e in doc.entities],
        }))

    except DoesNotExistError:
        sys.stderr.write("Document with id '{}' does not exist\n".format(
            args.id))
        sys.exit(1)


def get_project(args):
    """Retrieve project metadata"""
    client = DocumentCloud(args.username, args.password)

    if args.id_or_title is None:
        # Get all projects
        projects = client.projects.all()
        print(json.dumps({
            'projects': [serialize_project(p) for p in projects],
        }))


    match_order = ['title', 'id']

    if re.match(r'^\d+$', args.id_or_title):
        match_order = ['id', 'title']

    for match_term in match_order:
        kwargs = {}
        kwargs[match_term] = args.id_or_title

        try:
            project = client.projects.get(**kwargs)
            print(json.dumps({
                'projects': [serialize_project(project)],
            }))
            break

        except DoesNotExistError:
            pass

    else:
        sys.stderr.write("Project with id or title '{}' does not exist\n".format(
            args.id_or_title))
        sys.exit(1)


def upload(args):
    """Upload a document"""

    client = DocumentCloud(args.username, args.password)
    project = None

    if args.project:
        project = client.projects.get(title=args.project)

        # TODO: Handle error if this project doesn't exist
        project = client.projects.get(title=args.project)

    # HACK: The API docs seem to indicate that I should just be able to pass the
    # project ID here. I think things break with newer versions of python.
    for file_or_url in args.file_or_url:
        document_id = client.documents.upload(file_or_url,
            project=str(project.id))


def add_credential_arguments(parser):
    """Add arguments for username and password to an argparse parser"""
    parser.add_argument(
        '-u', '--username',
        help="DocumentCloud username",
        default=os.environ.get('DOCUMENTCLOUD_USERNAME')
    )
    parser.add_argument(
        '-p', '--password',
        help="DocumentCloud password",
        default=os.environ.get('DOCUMENTCLOUD_PASSWORD')
    )


def main():
    parser = argparse.ArgumentParser(
        description="Command line interface to the DocumentCloud API")

    subparsers = parser.add_subparsers()

    parser_document = subparsers.add_parser(
        'documents',
        description="Create or retrieve documents"
    )
    subparsers_document = parser_document.add_subparsers()
    parser_document_get = subparsers_document.add_parser(
        'get',
        description="Get document metadata"
    )
    parser_document_get.add_argument(
        'id',
        help="Document id"
    )
    add_credential_arguments(parser_document_get)
    parser_document_get.set_defaults(func=get_document)
    parser_document_entities = subparsers_document.add_parser(
        'entities',
        description="Get document entities (from Open Calais)"
    )
    parser_document_entities.add_argument(
        'id',
        help="Document id"
    )
    add_credential_arguments(parser_document_entities)
    parser_document_entities.set_defaults(func=get_document_entities)

    parser_project = subparsers.add_parser(
        'projects',
        description="Create or retrieve projects"
    )
    subparsers_project = parser_project.add_subparsers()
    parser_project_get = subparsers_project.add_parser(
        'get',
        description="Get project metadata"
    )
    parser_project_get.add_argument(
         'id_or_title',
         nargs='?',
         help="Project id or title"
    )
    add_credential_arguments(parser_project_get)
    parser_project_get.set_defaults(func=get_project)

    parser_upload = subparsers.add_parser(
            'upload',
            description="Upload a file to DocumentCloud"
    )
    parser_upload.add_argument(
        'file_or_url',
        nargs='+',
        help="Path to local file or remote URL to upload"
    )
    add_credential_arguments(parser_upload)
    parser_upload.add_argument(
        '--project',
        help="Project title",
    )
    parser_upload.set_defaults(func=upload)

    args = parser.parse_args()

    args.func(args)
