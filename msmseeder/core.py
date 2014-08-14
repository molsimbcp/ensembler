# ========
# Global package variables
# ========

import os
src_toplevel_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

datestamp_format_string = '%Y-%m-%d %H:%M:%S UTC'

project_metadata_filename = 'project-data.yaml'
manual_specifications_filename = 'manual-specifications.yaml'

template_acceptable_ratio_observed_residues = 0.7

# ========
# Definitions
# ========

def get_utcnow_formatted():
    import datetime
    now = datetime.datetime.utcnow()
    datestamp = now.strftime(datestamp_format_string)
    return datestamp

def check_project_toplevel_dir():
    import os
    for dirpath in ['structures', 'templates', 'targets', 'models']:
        if not os.path.exists(dirpath):
            raise Exception, 'Current directory not recognized as the top-level directory of a project.'

def get_src_git_commit_hash():
    import os
    import subprocess
    import msmseeder
    git_metadata_path = os.path.join(msmseeder.core.src_toplevel_dir, '.git')
    try:
        commit_hash = subprocess.check_output(['git', '--git-dir', git_metadata_path, 'rev-parse', 'HEAD'])
        commit_hash = commit_hash.strip()
    except subprocess.CalledProcessError:
        raise Exception('Failed to find source code git commit hash')
    return commit_hash

class ProjectMetadata:
    def __init__(self, data):
        # Listed in desired document order
        self.project_metadata_categories = ['init', 'gather_targets', 'gather_templates', 'build_models', 'sort_by_sequence_identity', 'cluster_models', 'refine_implicit_md', 'solvate_models', 'refine_explicit_md', 'package_for_fah']
        self.data = data

    def write(self, ofilepath):
        import yaml
        with open(ofilepath, 'w') as ofile:
            for category in self.project_metadata_categories:
                if category in self.data.keys():
                    subdict = {category: self.data[category]}
                    yaml.dump(subdict, ofile, default_flow_style=False)

# XXX Deprecated
class DeprecatedProjectMetadata:
    '''Container class for project metadata'''
    def __init__(self):
        # Listed in document order.
        self.project_metadata_categories = ['init', 'target-selection', 'template-selection', 'modelling', 'model-refinement', 'packaging']
        self.data = {}

    def load(self, filepath):
        '''Load project metadata from YAML file.
        Overwrites any existing data already contained in the data attribute.'''
        import yaml
        self.filepath = filepath
        try:
            with open(self.filepath, 'r') as ifile:
                yaml_data = yaml.load(ifile)
        except IOError as e:
            if e.errno == 2:
                print 'ERROR: Project metadata file "%s" not found. Perhaps you are not in the project top-level directory?' % filepath
            raise

        if type(yaml_data) != dict:
            raise Exception, 'Something wrong with the project metadata file. Contained data was not loaded as a dict.'
        self.data = yaml_data

    def write(self, ofilepath=None):
        '''Write project metadata to YAML file'''
        import os, yaml
        if ofilepath == None:
            try:
                ofilepath = self.filepath
            except:
                raise

        ofile_preexisted = False
        if os.path.exists(ofilepath):
            ofile_preexisted = True

        with open(ofilepath, 'w') as ofile:
            for category in self.project_metadata_categories:
                if category in self.data.keys():
                    subdict = {category: self.data[category]}
                    yaml.dump(subdict, ofile, default_flow_style=False)

        if ofile_preexisted:
            print 'Updated project metadata file "%s"' % ofilepath
        else:
            print 'Created project metadata file "%s"' % ofilepath

    def add_metadata(self, new_metadata):
        for key in new_metadata.keys():
            self.data[key] = new_metadata[key]

    def get(self, attribs_to_get):
        ''' Pass an attribute with which to query the project metadata, or a tuple of such attributes.
        Returns None if data not found.
        '''
        if type(attribs_to_get) == str:
            attribs_to_get = (attribs_to_get,)

        # query against first attrib
        try:
            retrieved_data = self.data[attribs_to_get[0]]
        except KeyError:
            retrieved_data = None

        # if more than one attrib to query against
        if len(attribs_to_get) > 1 and retrieved_data != None:
            for attrib in attribs_to_get[1:]:
                try:
                    retrieved_data = retrieved_data[attrib]
                except KeyError:
                    retrieved_data = None
                    break

        return retrieved_data


def xpath_match_regex_case_sensitive(context, attrib_values, xpath_argument):
    ''' To be used as an lxml XPath extension, for regex searches of attrib values.
    '''
    import re
    # If no attrib found
    if len(attrib_values) == 0:
        return False
    # If attrib found, then run match against regex
    else:
        regex = re.compile(xpath_argument)
        return bool( re.search(regex, attrib_values[0]) )

def xpath_match_regex_case_insensitive(context, attrib_values, xpath_argument):
    ''' To be used as an lxml XPath extension, for regex searches of attrib values.
    '''
    import re
    # If no attrib found
    if len(attrib_values) == 0:
        return False
    # If attrib found, then run match against regex
    else:
        regex = re.compile(xpath_argument, re.IGNORECASE)
        return bool( re.search(regex, attrib_values[0]) )
