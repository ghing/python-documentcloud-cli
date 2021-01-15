# DocumentCloud Command Line Interface

UPDATE: The old [python-documentcloud](https://github.com/datadesk/python-documentcloud) has been deprecated, breaking the functionality of this project. I am working on using the [current version](https://github.com/MuckRock/python-documentcloud/) of the library to get this tool working again.

A command line interface to the [DocumentCloud](https://www.documentcloud.org/) service, written in Python.

I started this project because I needed a way to bulk upload a directory of documents where I had already uploaded some of the documents. I needed a more flexible client that let me use common Unix command line tools like `find`, `ls`, `grep` and `xargs` to provide input to the program. Similarly, I imagine the output of this program being piped to tools like [csvkit](https://csvkit.readthedocs.io/en/1.0.3/) or [ndjson-cli](https://github.com/mbostock/ndjson-cli).

This project serves a need for me when I need programatic interaction with the DocumentCloud API, but don't want to have to write the same boilerplate code, or bootstrap a coding project to upload some documents or extract a list of entities.

## Supported functionality

I'm adding features as I need them for my work. Currently this utility supports the following:

- Uploading documents
- Retrieving project metadata
- Retriveving document metadata
- Retrieving document entities

## Installation

Use pip:

```
pip install git+git://github.com/ghing/python-documentcloud-cli.git#egg=python-documentcloud-cli
```

## Credentials

You can specify username and password with the `--username` and `--password` command-line arguments, or with the `DOCUMENTCLOUD_USERNAME` and `DOCUMENTCLOUD_PASSWORD` environment variables. The latter are preferred because then passwords won't accidently be stored in your shell history.

## Examples

### Load a list of URLs into a project

```
cat urls.txt | \
xargs -I % sh -c "documentcloud upload --project 'Test Project' %"
```

### Display a list of document IDs for documents in a project

```
documentcloud projects get "Test Project" | ndjson-split d.projects[0].document_ids
```

### Get CSV of organization entities in a document

```
documentcloud documents entities 12345-test-slug | \
ndjson-split d.entities | \
ndjson-filter 'd.type == "organization"' | \
in2csv -f ndjson
```

### Get CSV of all entities for all documents in a project

```
documentcloud projects get "Test Project" | \
ndjson-split d.projects[0].document_ids | \
xargs -I % documentcloud documents entities % | \
ndjson-split d.entities | \
in2csv -f ndjson
```

## Prior art

* [dcupload](https://github.com/onyxfish/dcupload) - A quick and dirty command line tool for bulk uploading documents to DocumentCloud.
