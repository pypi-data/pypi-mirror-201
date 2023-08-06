#
import os
import copy
from datetime import datetime
from collections import OrderedDict
import string
from itertools import zip_longest
import logging

import re

log = logging = logging.getLogger(__name__)


class MetaTable:
    """Create a table of metadata
    Args:
      session (session): A rrequests  session to the destination
      args (Namespace):  an argparse argument object (for flags)
      image_path (str): The abs path of the file to be uploaded
      root (str)      : The abs path of root dir
      tagmap (dict)   :   map for replacing values
                       { 'context-key' : { 'value':  'mapped value1' , ... }   # map for specific context
                         ''            : { 'value': 'mapped value' , ... }   # every context
                       }
     fixtags (dict)   :  a list of fixed tags to be added based on a key fields
                      { context-ley : { 'tag': 'value', ... }
    Returns:
      None on skipped or failed file or an XML resource
    """
    def __init__(self, tags = None, re_tags:str=None, path_tags:str=None, fixedtags=None, tagmaps=None,
                 re_only: bool = False, mustmap: bool = False, archive_type:str=None, progress: bool = False):
        if re_tags:
            self.re_tags = re.compile(re_tags, flags=re.IGNORECASE)
        else:
            self.re_tags = False
        self.path_tags = path_tags
        self.fixedtags = fixedtags or {}
        self.tags = tags or {}
        self.tagmaps  = tagmaps or {}
        if "" not in self.tagmaps:
            self.tagmaps[""] = {}
        self.re_only = re_only
        self.mustmap = mustmap
        self.archive_type = archive_type
        self.progress = progress
        self.metatable = None
        self.clear()
        self.skipped = []

    def as_dict(self):
        return self.metatable
    def clear(self, key=None):
        if key is not None:
            del self.metatable[key]
        self.metatable = OrderedDict()

    def append(self, image_path, root=""):
        #  args.log.debug ("preping tags %s %s %s %s", root, image_path,   tagmap.keys(), fixedtags.keys())
        #   Strip off top level dirs .. except user given root
        filename = os.path.basename(image_path)
        original_image_path = image_path
        image_path = image_path[len(root):]
        log.debug("APPEND %s %s ", root, image_path)

        # ############################################################################
        # # Skip pre-existing resources with same filename
        # if args.skip_loaded or args.replace_uploaded:
        #     response = data_service.get(params={"name": filename}, render="etree")
        #     if len(response) and response[0].get("name") == filename:
        #         if args.skip_loaded:
        #             args.log.warn("skipping %s: previously uploaded ", filename)
        #             return None
        #         elif args.replace_uploaded:
        #             tags = response[0]

        ############################################################################
        # Build argument tags into upload xml
        #if tags is None:
        #    tags = etree.Element("resource", name=image_path)
        resource_tags = {"path": image_path, "name": filename}
        # add any fixed (default) arguments  (maybe be overridden)
        static_tags = dict([x.split(":") for x in self.tags if "$" not in x])
        for tag, value in static_tags.items():
            resource_tags[tag] = value

        #######################
        # Date time
        # datetime processing (read from metadata or image)
        if any(tag in static_tags for tag in ('datetime', 'date', 'time')):
            if original_image_path.lower().endswith(".jpg") or original_image_path.lower().endswith(".jpeg"):
                from exif import Image
                with open(original_image_path, 'rb') as img_file:
                    img = Image(img_file)
                    image_meta = { k:img.get(k) for k in sorted(img.list_all()) }
                    date_time = image_meta.get("datetime", image_meta.get("datetime_original", datetime.today().strftime('%Y:%m:%d %H:%M:%S')))

            for tagkey in ('datetime', 'date', 'time'):
                # if the value has been set then skip
                if resource_tags.get(tagkey):
                    continue
                if tagkey=="datetime" and "datetime" in resource_tags:
                    # Read datetime from image
                    resource_tags[tagkey] = date_time
                    continue
                if tagkey=="date" and "date"  in resource_tags:
                    resource_tags[tagkey] = date_time.split(" ")[0].replace(":", "-")
                    continue
                elif tagkey=="time" and "time"  in resource_tags:
                    resource_tags[tagkey] = date_time.split(" ")[1]
                    continue
        ####################
        # common tags
        if any(tag in static_tags for tag in ('filename', 'original_path', 'upload_datetime')):
            for tagkey in ('filename', 'original_path', 'upload_datetime'):
                if resource_tags.get(tagkey):
                    # if the value has been set then skip
                    continue
                if tagkey == "filename" and "filename" in resource_tags:
                    resource_tags[tagkey] = filename
                if tagkey == "original_path" and "original_path" in resource_tags:
                    resource_tags[tagkey] = image_path
                if tagkey == "upload_datetime" and "upload_datetime" in resource_tags:
                    resource_tags[tagkey] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")

        ########
        # path elements can be made tags (only match directory portion) path_tags is presplit by os.sep
        if self.path_tags:
            for tag, value in zip_longest(self.path_tags.split("/"), image_path.split("/")[:-1]):
                if tag and value:
                    # etree.SubElement (tags, 'tag', name=tagmap.get(tag, tag), value = tagmap.get(value, value))
                    resource_tags[tag] = value
                    # resource_tags [tagmap.get(tag, tag)] =  tagmap.get(value, value)
        ############################################################################
        # RE over the filename
        if self.re_tags:
            matches = self.re_tags.match(filename)
            if matches:
                for tag, value in matches.groupdict().items():
                    if tag and value:
                        # etree.SubElement (tags, 'tag', name=tagmap.get (tag, tag), value = tagmap.get (value, value))
                        # resource_tags [tagmap.get(tag, tag)] =  tagmap.get(value, value)
                        resource_tags[tag] = value
            elif self.re_only:
                log.warn("Skipping %s: does not match re_tags", filename)
                self.skipped.append(image_path)
                return None
            else:
                log.warn("RE did not match %s", filename)
                self.skipped.append(image_path)
        #####################
        # resource_tags now contains all elements from the path and filename.
        # We now process these to find encoded entries for expansion
        ######################
        # Add fixed tags based on associated tagtable
        for tagkey, tagtable in self.fixedtags.items():
            key = None
            if tagkey == "filename":
                key = filename
            elif tagkey == "image_path":
                key = image_path
            else:
                key = resource_tags.get(tagkey)
            if key is None:
                log.warn("Lookup in fixed table: key %s  was not found", tagkey)
                continue
            if key not in tagtable:
                log.warn("Key %s : %s was not present in fixedtable", tagkey, key)
                continue
            for tag, value in tagtable[key].items():
                resource_tags[tag] = value

        #####################
        # Special geotag processing
        geo = {}
        new_resource_tags = copy.deepcopy(resource_tags)
        for tag, value in resource_tags.items():
            if tag in ("lat", "latitude"):
                geo["geo.coordinates.center.latitude"] = value
                del new_resource_tags[tag]
            if tag in ("alt", "altitude"):
                geo["geo.coordinates.center.altitude"] = value
                del new_resource_tags[tag]
            if tag in ("long", "longitude"):
                geo["geo.coordinate.center.longitude"] = value
                del new_resource_tags[tag]
        new_resource_tags.update(geo)
        resource_tags = new_resource_tags

        # if geo:
        #     geotags = etree.SubElement(tags, "tag", name="Geo")
        #     coords = etree.SubElement(geotags, "tag", name="Coordinates")
        #     center = etree.SubElement(coords, "tag", name="center")
        #     for tag, val in geo.items():
        #         etree.SubElement(center, "tag", name=tag, value=val)

        # add any templated tag (maybe be overridden)
        for tag, value in [
            string.Template(x).safe_substitute(resource_tags).split(":") for x in self.tags if "$" in x
        ]:
            # etree.SubElement (tags, 'tag', name=tag, value = value)
            resource_tags[tag] = value

        #####################
        # fold duplicates and de-reference items
        # mappers are one to one tables of oldtag[oldvalue] -> newtag[newvalue]
        new_tags = {}
        for tag, value in resource_tags.items():
            if (
                tag in self.tagmaps
            ):  # We have contextual map for this element  i.e. this tag's value is mapped
                mapper = self.tagmaps[tag]
                if self.mustmap:
                    if mapper.get(value) is None:
                        log.warn(
                            "Skipping %s:  %s does not match mapper in context:%s", filename, value, tag
                        )
                        self.skipped.append(image_path)
                        return None
            else:
                mapper = self.tagmaps[""]
            newtag = mapper.get(tag, tag)
            newvalue = mapper.get(value, value)
            new_tags[newtag] = newvalue
        resource_tags = new_tags
        ############################
        # Reapply fixed tags
        new_resource_tags = copy.deepcopy(resource_tags)
        for tag, value in resource_tags.items():
            if tag in self.fixedtags:
                fixedtable = self.fixedtags[tag][value]
                for ftag, fvalue in fixedtable.items():
                    new_resource_tags[ftag] = fvalue
        # new_resource_tags = apply_fixed_tags(args, filename, image_path, resource_tags, fixedtags)
        if resource_tags != new_resource_tags:
            log.debug("Found new fixed tags after mapping %s", new_resource_tags)
            resource_tags = new_resource_tags

        # change resource for register only
        #if args.register_only:
        #    tags.tag = "image"  # Check extension (load extension from image service etc)
        #    tags.attrib["name"] = filename
        #     tags.attrib["value"] = posixpath.join(args.register_only, image_path)



        ######################
        #  check if archive
        if (filename.endswith(".zip")
            or filename.endswith(".tar")
            or filename.endswith(".tar.gz")) and self.archive_type is not None:
            #ingest = etree.SubElement(tags, "tag", name="ingest")
            #etree.SubElement(ingest, "tag", name="type", value=args.archive_type)
            resource_tags["ingest"] = self.archive_type

        ######################
        #  move tags to xml
        # for tag, value in resource_tags.items():
        #     if tag and value:
        #         etree.SubElement(tags, "tag", name=tag, value=value)
        # xml = etree.tostring(tags, encoding="unicode")
        self.metatable[original_image_path] = resource_tags
        if self.progress:
            log.info("%s => %s", original_image_path, resource_tags)
