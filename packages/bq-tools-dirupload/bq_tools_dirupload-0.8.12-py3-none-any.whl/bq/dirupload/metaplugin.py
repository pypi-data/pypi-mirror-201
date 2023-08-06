

from .metatable import MetaTable
def path_metadata_plugin(import_request):
    r"""Import a directory and parse metadata form the path components
       based on bq-dirupload

       <request>
            <dry_run>True<dry_run>
            <must_map>True</must_map>
            <path>store://home/d1/plate-10/</path>
            <path_tags>service/datetime/site</path_tags>
            <re)tags>(?P<photo_site_code>\w+)_(?P<target_assemblage>\D+)(?P<plot>\d+)_(?P<season>\D+)(?P<year>\d+).+\.JPG</re_tags>
            <dataset> some_dataset </dataset>
            <tag>site:AA<tag>
            <tag_map>season:fa=fall</
            <tag_map>site_code:@00-TABLERESOURCE</tag_map>
            <fixed_tags>photo_site_code:@00-TABLERESOURCE</fixed_tags>
        </request>
    """
    return "GOT PATH METAPLUGIN"
