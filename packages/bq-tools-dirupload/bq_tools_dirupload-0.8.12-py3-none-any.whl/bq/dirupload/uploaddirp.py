
#!/usr/bin/env python
# from __future__ import unicode_literals
# from __future__ import print_function
# from builtins import input
# from builtins import range
# from future import standard_library
# standard_library.install_aliases()

import os
import sys
import csv
import fnmatch
import argparse
import logging
import json
import random
import requests
import string
import time
import types
import traceback
import posixpath
import copy
import concurrent
import threading
from itertools import zip_longest
from collections import OrderedDict

import regex as re  # substitute RE with branches
from lxml import etree

import bqapi
import vqapi
from bq.metadoc.formats import Metadoc
from .metatable import MetaTable
from .watchdirs import watch_directories

import queue

file_queue = queue.Queue()


log = logging.getLogger(__name__)

thread_local = threading.local()

def upload(image_path, meta):
    """ Upload a single file with meta """
    session = thread_local.session
    args    = thread_local.args

    meta = dict(meta)
    filename = os.path.basename(image_path)
    original_image_path = image_path
    image_path = meta.pop("path").replace('\\', '/') # dima: ensure unix paths
    data_service = session.service("data_service")
    #import_service = session.service("import")
    # print ("HELLO", session.transfer)
    destination_path = image_path
    if args.destination_dir:
        destination_path = posixpath.join(args.destination_dir, image_path)
        # print ("destination_path: ", destination_path)

    uri = None
    if args.skip_loaded or args.replace_uploaded:
        response = data_service.get(params={"name": filename}, render=session.render)
        response = session.metadoc(response)
        if len(response) and response[0].get("name") == filename:
            if args.skip_loaded:
                args.log.warning("skipping %s: previously uploaded ", filename)
                return response  # we return the resource for the dataset registration if applicable
            if args.replace_uploaded:
                uri = response[0].get("uri")
    ######################
    #  move tags to xml
    if meta and not args.transfer_only:
        tags = Metadoc(tag="resource", name=meta.pop("name"))
        for tag, value in meta.items():
            if tag and value:
                #etree.SubElement(tags, tag).text=value
                tags.add_tag(tag, value=value)

        if args.register_only:
            tags.tag = "image"  # Check extension (load extension from image service etc)
            tags.attrib["name"] = filename
            tags.attrib["value"] = posixpath.join(args.register_only, image_path)
            destination_path = ""

        xml = session.to_xml(tags)
    else:
        xml = None

    if args.dry_run:
        response = tags
        response.tag = "image"
        response.attrib["name"] = filename
        response.attrib["resource_uniq"] = "00-XX"

    if args.replace_uploaded and uri is not None:
        args.log.info("replacing meatdata for %s", image_path)
        if not args.dry_run:
            response = data_service.put(path=uri, data=xml, render=session.render)
            response = session.metadoc(response)
    elif args.register_only:
        args.log.info("Registering meatdata for %s", image_path)
        if not args.dry_run:
            response = data_service.post("image", data=xml, render=session.render)
            response = session.metadoc(response)
    else:
        try:
            with open(original_image_path, "rb") as fileobj:
                if os.fstat(fileobj.fileno()).st_size == 0:
                    if not args.empty:
                        args.log.warning("Skipping %s: Empty file", original_image_path)
                        return None
                if not args.dry_run:
                    #response = import_service.transfer_fileobj(
                    response = session.transfer(
                        fileobj=fileobj, xml=xml, dstpath=destination_path, protocol=args.protocol)

        except OSError as exc:
            args.log.error("Skipping %s:  system error %s", original_image_path, exc)
            return None
    if response is None:
        return destination_path
    uri = response.get("uri")
    if not args.quiet:
        log.info("Uploaded %s to %s with %s", image_path, uri, xml)
    return response

def xml_bq05(xml):
    " convert to tagxml str "
    return xml.to_tagxml()
def metadoc_bq05(response):
    if isinstance(response, requests.Response):
        return Metadoc.from_tagxml_etree(response.xml())
    else:
        return Metadoc.from_tagxml_etree(response)

def transfer_bq05(self, fileobj, xml, dstpath, protocol):
    """Transfer a resource and register

       self is a bqapi session object

    Returns:
      Metadoc of resource
    """
    import_service = self.service("import")
    filename = dstpath
    response = import_service.transfer(filename=filename, fileobj=fileobj, xml=xml)
    #print ("RESPONSE ", response, etree.tostring(response.xml()))
    # <upload> <resource name=... /> </upload>
    return Metadoc.from_tagxml_etree(response.xml()[0])

def metadoc_viqi1(response):
    return response
def xml_viqi1(xml):
    return xml
def transfer_viqi1(self, fileobj, xml, dstpath, protocol):
    """Transfer a resource and register

       self is a bqapi session object
    Returns:
      Metadoc of resourc
    """
    import_service = self.service("import")
    #xml.set("name", dstpath) # setup the location on the server

    return import_service.transfer_fileobj(fileobj=fileobj, xml=xml, dstpath=dstpath, protocol=protocol)


def read_csv_table(filename, start_col=1):
    """
    Read a csv table into a dict keyed by 1st column
    head1 head2 head3
    K1    V1    V2
    K2    V1    V2
    { K1 , {  head1:K1, head2:V1, head3:V2 } }
    { K2,  { head1:K1, head2:v3, head3:v4 } }
    """
    fixedtags = {}
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        fieldnames = next(reader)
        keyfield = fieldnames[0]
        fieldnames = fieldnames[start_col:]
        for row in reader:
            # grab value of first columner and use as key for the rest of the values.
            fixedtags[row[0]] = OrderedDict(zip_longest(fieldnames, row[start_col:]))
    return fixedtags




DOC_EPILOG = r"""
bq-dirupload -n  --threads 1 --re-tags "(?P<photo_site_code>\w+)_(?P<target_assemblage>\D+)(?P<plot>\d+)_(?P<season>\D+)(?P<year>\d+).+\.JPG" --dataset upload --tagmap target_assemblage:@speciesmap.csv --tagmap photo_site_code:@locationmap.csv --tagmap season:fa=fall --tagmap year:15=2015 --fixedtags photo_site_code:@photo_code_reference_2019_0912.csv TopLevelDir

 Magic decoder ring:
    -n : dry run
    --threads 1: one thread for debugging
    --retags :   use filename to create tags: photo_site_code, target_assemblage, season and year.
    --dataset : create a dataset "upload"
    --tagmap target_assemblage:@speciesmap.csv: use value ins speciesmap.csv to rename tag/values for target_assemblage
    --tagmap photo_site_code:@locationmap: Use location map to rename tag/value from photo_site_code
    --tagmap season:fa=fall : rename season 'fa' to 'fall'
    --tagmap year:15=2015 : remame year from '15' to 2015
    --fixedtags photo_site_code:@photo_code_reference_2019_0912.csv  :  use photo_site_code to read a set of fixed tags to be applied to the resource

   A map is consists of [context_tag:]oldval=newval or [context_tag:]@map.csv where csv is a two column table of old value, new value

Other interesting Arguments

    --debug-file somefile :  write actions to somefile
    --path-tags   map components of the file path  to metadata tags i.e.   on the path ghostcrabs/manua/winter/somefile.jpg
                  --path-tags=project/site/season  ->  { project:ghostcrabs, site:manua, season:winter} as tags on somefile.jpg
                  --path-tags=/site//              ->  {site:manua }   skipping root and season elements


"""
def build_parser():
    parser = vqapi.cmd.bisque_argument_parser(
        "Upload files to bisque",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=DOC_EPILOG,
    )
    parser.add_argument(
        "--tag",
        help="Add name:value pair, can be templated with other values mycode:$site$season",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--path-tags",
        help="tag names for a parsable path i.e. /root/project/date//subject/ or \\root\\project\\data\\subject",
        default="",
    )
    parser.add_argument(
        "--re-tags", help=r"re expressions for tags i.e. (?P<location>\w+)--(?P<date>[\d-]+)"
    )
    parser.add_argument(
        "--re-only", help=r"Accept files only if match re-tags", default=False, action="store_true"
    )
    parser.add_argument(
        "--mustmap",
        help=r"Contextual tag  must have a value in a tagmap",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--include",
        help="shell expression for files to include. Can be repeated",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--exclude",
        help="shell expression for files to exclude. Can be repeated",
        action="append",
        default=[],
    )
    parser.add_argument("--dataset", help="create dataset and add files to it", default=None)
    parser.add_argument("--threads", help="set number of uploader threads", default=8)
    parser.add_argument(
        "--empty", help="Allow empty files to be uploaded", action="store_true", default=False
    )
    parser.add_argument(
        "-s",
        "--skip-loaded",
        help="Skip upload if there is file with the same name already present on the server",
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--replace-uploaded",
        help="Force upload of metadata even if file exists on server",
        action="store_true",
    )
    parser.add_argument(
        "--tagmap",
        action="append",
        default=[],
        help="Supply a map tag/value -> tag/value found in tag path and re decoder.  [context_key:]carp=carpenteria or [context_key:]@tagmap.csv",
    )
    parser.add_argument(
        "--fixedtags",
        action="append",
        default=[],
        help="key:tag=value or key:@fileoftags fixed tags to add to resource: First column is key: including filename or image_path",
    )
    parser.add_argument(
        "--json-args",
        type = open,
        action = LoadFromJson,
        help="Load default arguments from json file i.e { \"--path-tags\" : \"project/date\" }"
    )
    # DEBUG
    parser.add_argument(
        "--protocol",
        default = None,
        choices=("binary", "fsxlustre", "multipart"),
        help="Set the upload protocol or let tyhe system choose"
    )
    parser.add_argument(
        "--destination-dir",
        default = None,
        help="Upload to destination-dir on server .. must be valid mount i.e /home/my-uploads"
    )

    parser.add_argument("--transfer-only", default=False, action="store_true",
                        help="Upload files only without registration")
    parser.add_argument("--register-only", default=False,
                        help="register files without actually uploading them use argument as prefix path for ")
    parser.add_argument("--archive-type", default=None,
                        choices=["zip-bisque", "zip-multi-file", "zip-time-series", "zip-z-stack", "zip-dicom"],
                        help="zip archive will be given a type: bisque, z-stack, t-stack")
    parser.add_argument("--watch", default=False, action="store_true",
                        help="Watch directories listed for new files and transfer")
    parser.add_argument("directories", help="director(ies) to upload", default=[], nargs="*")
    return parser



class LoadFromJson(argparse.Action):
    """ Load arguments from a json file
    """
    def __call__ (self, parser, namespace, values, option_string = None):
        #print ("GOT NAMESPACE ", namespace)
        with values as f:
            contents = f.read()
            contents = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(contents)
            args = [item for sb in contents.items() for item in sb]
            data = parser.parse_args(args, namespace=None)
            for k, v in vars(data).items():
                #print("K", k, "v", v)
                if k == "directories":
                    namespace.directories += v[1]
                    continue
                if getattr(namespace, k, None) is not None:
                    setattr(namespace, k, v)
        #print ("EXIT NAMESPACE ", namespace)


def build_tagtables(args):
    """ Build fixed tags and tag map tables from inputs

    Tag tables are structure as follow
    { <contenxt tga> :  { 'tag' : 'value " ... }  }
    <context tga> is a tag name or '' meaning all contexts

    Fixed tags are applied to all records where a context is found
    Tag maps are map of <old tag name> ->  <new tag name>


    """
    def fail(*msg):
        args.log.error(*msg)
        sys.exit(1)

    fixedtags = {}
    for tagtable in args.fixedtags:
        context, tagtable = tagtable.split(":")
        if "=" in tagtable:
            fixedtags.setdefault(context, {}).update(dict([tagtable.split("=")]))
            continue
        if tagtable[0] == "@":
            if not tagtable.endswith(".csv"):
                fail("fixed tag %s table must be .csv file", tagtable)
            if not os.path.exists(tagtable[1:]):
                fail("File %s does not exist", tagtable[1:])
        else:
            fail("%s Must be in form of tag=val or @tableofvalue", tagtable)
        #
        with open(tagtable[1:], "r") as csvfile:
            reader = csv.reader(csvfile)
            fieldnames = next(reader)
            keyfield = fieldnames[0]
            fieldnames = fieldnames[1:]
            for row in reader:
                # grab value of first columner and use as key for the rest of the values.
                fixedtags.setdefault(context, {})[row[0]] = OrderedDict(
                    zip_longest(fieldnames, row[1:])
                )

    # load tag map items (mapping certain values from filename/path to full values)
    tagitems = {"": {}}
    for entry in args.tagmap:
        context = ""
        if ":" in entry:
            context, entry = entry.split(":")
        if entry.startswith("@"):
            if not entry.endswith(".csv"):
                fail("tagmap %s table must be .csv file", entry[1:])
            if not os.path.exists(entry[1:]):
                fail("tagmap file %s does not exist", entry[1:])
                continue

            with open(entry[1:], "r") as csvfile:
                tagitems.setdefault(context, {}).update(
                    (row[0].strip(), row[1].strip()) for row in csv.reader(csvfile)
                )
        else:
            tagitems.setdefault(context, {}).update([entry.split("=")])
    return fixedtags, tagitems


def process_environment():
    """Check environment for arguments

       We define an environment variable called OEMTransfer which is a path to the OEMTransfer.json file.
       the OEMTransfer.json contents would look be like so:
       {  "ExportPath": "D:\\Experiments\\Confluence\\Confluence_001\\Export"  }

    """
    tpath = os.environ.get('BQ_TRANSFER_JSON') or os.environ.get("OEM_TRANSFER")
    if tpath and os.path.exists(tpath):
        sys.argv.append ("--json-args=%s" % tpath)


def get_server_version(parser=None):
    """ Get the server version of bisque/viqi server
    Args:
      an initialized bisque parser
    Returns:
      Parsed argument list with server_versions set
    """
    pargs = vqapi.cmd.bisque_config(parser=parser)
    pargs.server_verion = None
    try:
        # Check version of server
        resp = requests.get(os.path.join(pargs.host, "web/about"),
                            headers={'Accept':"application/xml"})
        if resp.status_code == 200:
            pargs.server_version =  "viqi1"
            return pargs
        resp = requests.get(os.path.join(pargs.host, "client_service/about"),
                            headers={'Accept' : "application/xml"})
        if resp.status_code == 200:
            pargs.server_version =  "bisque05"
            return pargs
    except requests.exceptions.RequestException:
        logging.exception ("During initial connect")
    pargs.server_version = None
    return pargs


def transfer_directories(metatable, directories, includes=None, excludes=None):
    """find and tag local files for upload using a parallel uploader
    """
    # Start workers with default arguments
    #manager = ProcessManager(
    #    limit=int(args.threads),
    #    workfun=send_image_to_bisque,
    #    is_success=check_success,
    #    on_success=append_result_list,
    #    on_fail=append_error_list,
    #)

    # helper function to add a list of paths
    def add_files(files, root):
        root = os.path.join(root, "")
        for f1 in files:
            if includes and not any(fnmatch.fnmatch(f1, include) for include in includes):
                log.info("Skipping %s: not included", f1)
                continue
            if excludes and any(fnmatch.fnmatch(f1, exclude) for exclude in excludes):
                log.info("Skipping %s: excluded", f1)
                continue
            #manager.schedule(args=(session, args, root, f1, tagitems, fixedtags))
            log.info("appending %s with %s", f1, root)
            metatable.append(f1, root)
            file_queue.put(f1)

    # Add files to work queue
    try:
        for directory in directories:
            if directory[0] == '@':
                root = os.path.abspath(os.path.expanduser(directory[1:]))
                with open(root, 'r', encoding='utf8') as filelist:
                    #add_files([os.path.join(root, afile.strip()) for afile in filelist], root=root)
                    add_files([afile.strip() for afile in filelist], root="")
                continue

            full_root = os.path.abspath(os.path.expanduser(directory))
            # /home/kgk/clients/bears/Hallo/CRIT
            # relative_root  Hallo/Crit = Hallo/Crit , ~/work/data => work/data , ~jojo/work/data => work/data
            #print (f"{full_root} -> {relative_root} -> {parent}")
            # /home/kgk/clients/bears
            #  Walk the full root
            #      /home/kgk/clients/bears/Hallo/CRIT
            #  Set parent = /home/kgk/clients/bears/
            if os.path.isdir(full_root):
                relative_root = directory[2:] if directory.startswith("~/") else directory
                parent = full_root.replace(relative_root, "").replace("\\", "/")
                for root, _, files in os.walk(full_root):
                    #print ("In ", root, _, files, " Prefix DIR ", directory)
                    add_files(
                        (os.path.join(root, f1).replace("\\", "/") for f1 in files), root=parent
                    )
            elif os.path.isfile(full_root):
                parent = os.path.dirname(full_root)
                print ("ADDING FILE ", full_root, " parent:", parent)
                add_files([full_root.replace("\\", "/")], root=parent)
            else:
                log.error("argument %s was neither directory or file", full_root)
        return metatable
        # wait for all workers to stop
        #while manager.isbusy():  # wait while queue has work
        #    time.sleep(1)
        #manager.stop()  # wait for worker to finish

    except (KeyboardInterrupt, SystemExit) :
        print("TRANSFER INTERRUPT")
        #manager.kill()
        # manager.stop()


LEVELS = {"debug": logging.DEBUG,
          "info": logging.INFO,
          "warn": logging.WARN,
          "error": logging.ERROR,
          }


def thread_session_initialize(session):
    if session.server_version == "viqi1":
        #session = vqapi.cmd.bisque_session(parser=parser, args=args)
        session = session.copy()
        session.transfer = types.MethodType(transfer_viqi1,session)
        session.to_xml = xml_viqi1
        session.metadoc = metadoc_viqi1
        session.render  = "doc"
        thread_local.session = session
        thread_local.args    = session.parse_args
    elif session.server_version == "bisque05":
        #session = bqapi.cmd.bisque_session(parser=parser, args=args)
        session = session.copy()
        session.transfer = types.MethodType(transfer_bq05, session)
        session.to_xml = xml_bq05
        session.metadoc = metadoc_bq05
        session.render  = "xml"
        thread_local.session = session
        thread_local.args    = session.parse_args

def main():
    parser = build_parser()

    process_environment()

    args = get_server_version(parser)
    if args.server_version == "viqi1":
        session = vqapi.cmd.bisque_session(parser=parser, args=args)
        if session is None:
            sys.exit(1)
        session.transfer = types.MethodType(transfer_viqi1,session)
        session.to_xml = xml_viqi1
        session.metadoc = metadoc_viqi1
        session.render  = "doc"
        import_svc = session.service("import")
        import_svc.transfer_protocol_info("/home/somdir")
    elif args.server_version == "bisque05":
        session = bqapi.cmd.bisque_session(parser=parser, args=args)
        if session is None:
            sys.exit(1)
        session.transfer = types.MethodType(transfer_bq05, session)
        session.to_xml = xml_bq05
        session.metadoc = metadoc_bq05
        session.render  = "xml"
    if args.server_version is None or session is None:
        print(f"Could not reach/determine {args.server_version} at {args.host}")
        sys.exit(1)
    session.service_version = args.server_version

    args.log = logging.getLogger("bq")
    args.log.info("Arguments %s", " ".join(sys.argv[1:]))
    args.log.info("Arguments from parser %s", args)
    if args.debug:
        args.log.setLevel(LEVELS.get(args.debug.lower(), logging.DEBUG))

    if session is None:
        print("Failed to create session.. check credentials")
        sys.exit(0)


    #args.path_tags = args.path_tags.split(os.sep)
    #if args.re_tags:
    #    args.re_tags = re.compile(args.re_tags, flags=re.IGNORECASE)

    fixedtags, tagitems = build_tagtables(args)

    metatable = MetaTable(tags = args.tag,
                          re_tags=args.re_tags,
                          path_tags=args.path_tags,
                          fixedtags=fixedtags,
                          tagmaps=tagitems,
                          re_only=args.re_only,
                          mustmap=args.mustmap,
                          archive_type=args.archive_type,
                          progress = not args.quiet)

    #if args.watch:
    #    pass
    #else:
    #    transfer_directories(metatable, args.directories, includes=args.include, excludes=args.exclude)
    # print(f"{metatable.as_dict()}")

    start_time = time.time()
    SKIPPED = metatable.skipped
    UNIQS = []
    SUCCESS = []
    ERROR = []
    DONE_TOKEN = "DONE"  #nosec
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(args.threads),
                                               initializer=thread_session_initialize,
                                               initargs=(session, )) as executor:

        # Start loading the file_queue with parsed path object

        future_to_path = {
            executor.submit(transfer_directories,
                            metatable, args.directories, includes=args.include, excludes=args.exclude): DONE_TOKEN
        }

        while future_to_path:
            done, not_done = concurrent.futures.wait(future_to_path,
                                                     timeout=1,
                                                     return_when=concurrent.futures.FIRST_COMPLETED)
            while not file_queue.empty():
                file_path = file_queue.get()
                meta = metatable.as_dict()[file_path] # dima: if needed
                future_to_path[executor.submit(upload, file_path, meta)] = file_path

            # process any completed futures
            for future in done:
                file_path = future_to_path[future]
                try:
                    data = future.result()
                except Exception as exc:
                    log.exception("%s generated an exception: %s", file_path, exc)
                    ERROR.append((file_path, exc) )
                    print(f'FAILED to Upload {file_path}')
                else:
                    if file_path == DONE_TOKEN:
                        print("PROCESSED", len(data.as_dict()))
                    elif data is None:
                        # either a skip and error (prevously logged)
                        pass
                    elif isinstance(data, str):
                        SUCCESS.append(data)
                    else:
                        UNIQS.append(data.get("resource_uniq"))
                        SUCCESS.append(future)
                        print(f'{file_path} ->  {data}')
                del future_to_path[future]

        # future_uploads = {executor.submit(upload, session, args, path, meta): path
        #                   for path, meta  in metatable.as_dict().items()}
        # for future in concurrent.futures.as_completed(future_uploads):
        #     path = future_uploads[future]
        #     try:
        #         data = future.result()
        #         UNIQS.append(data.get("resource_uniq"))
        #         SUCCESS.append(future)
        #     except Exception as exc:
        #         log.exception("%s generated an exception: %s", path, exc)
        #         ERROR.append((path, exc) )
        #     else:
        #         print('%r path ->  %s' % (path, data))

    end_time = time.time()

    # if args.watch:
    #     print("NOT IMPLEMENTED yet")
    #     sys.exit(1)
    #     watch_directories(session, args, fixedtags, tagitems)
    # else:
    #     if not args.directories:
    #         parser.print_help()
    #         sys.exit(0)
    #     transfer_directories(session, args, fixedtags, tagitems)



    # Store output dataset
    if args.dataset and UNIQS:
        if args.debug:
            args.log.debug("create/append dataset %s with %s", args.dataset, UNIQS)
        data = session.service("data_service")
        dataset = data.get("dataset", params={"name": args.dataset}, render="doc")
        dataset = session.metadoc(dataset)
        dataset_uniq = len(dataset) and dataset[0].get("resource_uniq")  # fetch uri of fist child
        datasets = session.service("dataset_service")
        if not args.dry_run:
            if dataset_uniq:
                response = datasets.append_member(dataset_uniq, UNIQS)
            else:
                response = datasets.create(args.dataset, UNIQS)
            if args.debug:
                dataset_doc = session.metadoc(response)
                args.log.debug("created dataset %s", str(dataset_doc))
        else:
            args.log.info ("created dataset with %s", UNIQS)
    if args.debug:
        for S in SUCCESS:
            args.log.debug("success %s", S)
        for E in ERROR:
            args.log.debug("failed %s", E)
            #if "with_exception" in E:
            #    traceback.print_exception(E["with_exc_type"], E["with_exc_val"], E["with_exc_tb"])
    if not args.quiet:
        print("Total upload time: {:.2f}s".format(end_time-start_time))
        print("Successful uploads: ", len(SUCCESS))
        print("Failed uploads:", len(ERROR))
        print("Skipped uploads:", len(SKIPPED))


if __name__ == "__main__":
    main()


#
#
#
# U:\Shared\Personal_or_Sampling_Group_Folders\UCLA\UCLA MARINe Archives for UCSB\Digital Image Archive\1 Monitoring Imagery and Datasheets\1999b Fall Images\1 Alegria\Photoplots\A1.jpg
# U:\Shared\Personal_or_Sampling_Group_Folders\UCLA\UCLA MARINe Archives for UCSB\Digital Image Archive\1 Monitoring Imagery and Datasheets\2002a Spring Images\4 Carpinteria
# 1999b Fall Images\ fa99
# 1 Alegria\ aleg
# Photoplots\
# A1.jpg ant1

# aleg_ant1_fa99a.JPG


# bq-dirupload  -n -d INFO --threads 4  --profile marine-testing --exclude "*Thumbs.db" --exclude "*ZbThumbnail.info" --exclude "*.info" --exclude "*.tmp" --exclude "*picasa*" --exclude "*.xls" --exclude "*.pdf" --exclude "*.psd" --exclude "*.DS_Store" --exclude "*.ppt" --exclude "*.txt" --exclude "*.docx" --tag photo_type:plot --re-only --mustmap --re-tags "(?P<photo_site_code>[a-zA-Z0-9]+)_(?P<target_assemblage>\D+)(?P<plot>\d+)?_(?|((?P<photo_type>(ul|ur|ll|lr))_)?(?P<season>(sp|fa|wi|su))(?P<year>\d+)|(?P<season>(sp|fa|wi|su))(?P<year>\d+)(?P<photo_type>_(ul|ur|ll|lr)_)?)(\((?P<rep>\d+)\))?.*\.JPG" --dataset UCSC20210503 --tagmap target_assemblage:@speciesmap.csv --tagmap photo_site_code:@locationmap.csv --fixedtags season:@seasonmap.csv --tagmap year:@yearmap.csv --tagmap photo_type:@phototypemap.csv --tag 'season_code:$season$year' --fixedtags photo_site_code:@photo_code_reference.csv --debug-file uploadedMOL.txt Z:\Intertidal_Photos_All\mms-images\"Andrew Molera"
