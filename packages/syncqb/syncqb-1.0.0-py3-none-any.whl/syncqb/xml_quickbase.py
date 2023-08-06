import base64
from .quickbase import QuickbaseClient
from .qb_errors import *

import requests
import time
import chardet
from lxml import etree, html

class XmlQuickbaseClient(QuickbaseClient):

    def __init__(self, credentials=None, timeout=90, database=None,  
                 authenticate=True, apptoken=None, hours=12, ticket=None, **kwargs):
        self.apptoken = apptoken
        self.hours = hours
        self.ticket = None

        if not credentials:
            credentials = kwargs
        if not credentials.get('username'):
            raise QBAuthError('In order to use this SDK, you must provide a Quickbase username and password, missing username.')
        if not credentials.get('password'):
            raise QBAuthError('In order to use this SDK, you must provide a Quickbase username and password, missing password.')
        super().__init__(credentials, timeout, database)

        if authenticate:
            self.authenticate()
        elif ticket is not None:
            self.ticket = ticket

    def _request(self, url, data, action, type):
        if action == 'files':
            headers = {'cookie': f'ticket={self.ticket}'}
        else:
            headers = {
                'content-type': 'application/xml',
                'QUICKBASE-ACTION': f'API_{action}',
            }
        while True:
            try:
                response = self._make_request(url, data, headers, type)
                break
            except requests.exceptions.Timeout:
                print('Timeout error, retrying...')
                time.sleep(1)

        if response.status_code == 401 or response.status_code == 403:
            raise QBAuthError('Invalid credentials')
        elif response.status_code == 404:
            raise QBConnectionError('Connection Error: Invalid URL')
        elif response.status_code == 400:
            raise QBResponseError('Response Error: Invalid request', response)
        elif response.status_code == 429:
            raise QBResponseError('Response Error: Too many requests', response)
        elif response.status_code == 500:
            raise QBResponseError('Response Error: Internal Quickbase Server Error', response)
        
        return response.content

    def _make_request(self, url, data, headers, type):
        if type == 'POST':
            return requests.post(url, data=data, headers=headers, timeout=self.timeout)
        elif type == 'GET':
            return requests.get(url, headers=headers, timeout=self.timeout)

    def _build_xml(self, data):
        if self.ticket:
            data['ticket'] = self.ticket
        if self.apptoken:
            data['apptoken'] = self.apptoken

        request = etree.Element('qdbapi')
        doc = etree.ElementTree(request)

        def add_sub_element(field, value):
            if isinstance(value, tuple):
                attrib, value = value
                attrib = dict((k, str(v)) for k, v in attrib.items())
            else:
                attrib = {}
            sub_element = etree.SubElement(request, field, **attrib)
            if not isinstance(value, str):
                value = str(value)
            sub_element.text = value

        for field, values in data.items():
            if not isinstance(values, list):
                values = [values]
            for value in values:
                add_sub_element(field, value)

        return etree.tostring(doc, xml_declaration=True, encoding="utf-8")

    def _parse_xml(self, response, required_fields=None, qid_headers=False, return_as_dict=True):
        encoding = chardet.detect(response)['encoding']

        if encoding != 'utf-8':
            response = response.decode(encoding, 'replace').encode('utf-8')

        if qid_headers:
            return response

        parsed = etree.fromstring(response)

        error_code = parsed.findtext('errcode')

        if error_code != '0':
            raise QuickbaseError(parsed.findtext('errtext'))

        if required_fields:
            values = {}
            for field in required_fields:
                if parsed.find(field) is None:
                    raise QuickbaseError(f'Missing required field: {field}')
                values[field] = parsed.find(field).text or ''

            return values
        elif return_as_dict:
            return self._format_etree_as_dict(parsed)
        else:
            return parsed

    def _parse_record_data(self, record_data, return_metadata=False, headers=None):

        records = []
        records_returned = record_data.xpath('.//record')
        for record in records_returned:
            record_data = {}
            for fields in record:
                fid = fields.get('id', fields.tag)
                is_file = False
                for child in fields:
                    if child.tag == 'url':
                        record_data[fid] = child.text
                        is_file = True
                    elif child.tail is not None:
                        record_data[fid] += child.tail
                if fid != 'update_id' and not is_file:
                    record_data[fid] = self._format_field_data(fields.text or '')

            records.append(record_data)
        if return_metadata:
            fields_returned = record_data.xpath('.//field')
            fields = {}

            for index, field in enumerate(fields_returned):
                id = field.get('id')
                field_data = {
                    'id': id,
                    'type': field.get('type'),
                    'base_type': field.get('base_type'),
                    'currency_symbol': field.get('currency_symbol'),
                    'label': field.xpath('label')[0].text,
                }

                if headers:
                    field_data['label_override'] = headers[index]

                fields[id] = field_data

            return records, fields
        
        return records

    def _parse_schema(self, response):
        tables = response.xpath('.//chdbid')
        fields = response.xpath('.//field')
        rows = []
        if tables:
            for t in tables:
                table = {
                    'name': t.get('name'),
                    'dbid': t.text
                }
                rows.append(table)
        elif fields:
            for f in fields:
                field = {x[0]: x[1] for x in f.items()}
                for child in f.iterchildren():
                    tag = child.tag
                    if tag == 'choices':
                        choices = tuple(c.text for c in child.iterchildren())
                        field['choices'] = choices
                    else:
                        field[child.tag] = child.text
                rows.append(field)
        return rows

    def _get_qid_headers(self, qid=None, database=None):
        request = {'qid': qid}

        response = self._request(
            f'{self.base_url}/db/{database or self.database}',
            self._build_xml(request),
            'GenResultsTable',
            'POST'
        )
        response = self._parse_xml(response, qid_headers=True)
        dom = html.fromstring(response)

        header_nodes = dom.xpath("//tr[1]/td")[1:-1]

        header_list = []
        for this_node in header_nodes:
            header_list.append(this_node.text_content().strip())

        return header_list

    def _format_field_data(self, data):
        try:
            value = float(data)
            if value.is_integer():
                value = int(value)
        except ValueError:
            value = data

        return value

    def _format_etree_as_dict(self, etree):
        main_tag = etree.tag

        if len(etree):
            main_dict = {main_tag: {}}
            for sub_element in etree:
                main_dict[main_tag].update(self._format_etree_as_dict(sub_element))
            return main_dict
        else:
            return {main_tag: etree.text}

    def authenticate(self):
        
        url = f'{self.base_url}/db/main'

        request = self._build_xml({
            'username': self.username,
            'password': self.password,
            'hours': self.hours,
            'apptoken': self.apptoken,
        })

        response = self._request(url, request, 'Authenticate', 'POST')

        response = self._parse_xml(response, required_fields=['ticket', 'userid'])

        self.ticket = response['ticket']
        self.user_id = response['userid']

    def add_record(self, fields, database=None, ignore_error=True, uploads=None):
        request = {'field': []}
        if ignore_error:
            request['ignoreError'] = '1'
        for field, value in fields.items():
            request['field'].append(({'fid': field}, value))

        if uploads:
            for upload in uploads:
                request['field'].append((
                    {'fid': upload['field'], 'filename': upload['filename']}, 
                    upload['value']
                ))

        response = self._request(
            f'{self.base_url}/db/{database or self.database}',
            self._build_xml(request),
            'AddRecord',
            'POST'
        )
        response = self._parse_xml(response, required_fields=['rid'])
        return int(response.get('rid'))

    def edit_record(self, rid, fields, database=None, uploads=None):
        request = {
            'rid': rid,
            'field': []
        }

        for field, value in fields.items():
            if isinstance(value, tuple):
                part_a = {'fid': field}
                for key, val in value[0].items():
                    part_a[key] = val

                request_field = (part_a, value[1])
            else:
                request_field = ({'fid': field}, value)
            
            request['field'].append(request_field)

        if uploads:
            for upload in uploads:
                request['field'].append((
                    {'fid': upload['field'], 'filename': upload['filename']}, 
                    upload['value']
                ))

        response = self._request(
            f'{self.base_url}/db/{database or self.database}',
            self._build_xml(request),
            'EditRecord',
            'POST'
        )
        response = self._parse_xml(response, required_fields=['rid'])

        return int(response.get('rid'))

    def delete_record(self, rid=None, key=None, database=None):
        if not rid and not key:
            raise TypeError('Must provide a rid or key')
        
        request = {}
        if rid:
            request['rid'] = rid
        elif key:
            request['key'] = key
        
        response = self._request(
            f'{self.base_url}/db/{database or self.database}',
            self._build_xml(request),
            'DeleteRecord',
            'POST'
        )
        return self._parse_xml(response, required_fields=['rid'])

    def purge_records(self, rids=None, query=None, qid=None, database=None):
        request = {}
        if rids:
            rids = [str(rid) for rid in rids]
            query = 'OR'.join(["{3.EX.'%s'}" % rid for rid in rids])
        if query:
            request['query'] = query
        elif qid:
            request['qid'] = qid

        response = self._request(
            f'{self.base_url}/db/{database or self.database}',
            self._build_xml(request),
            'PurgeRecords',
            'POST'
        )
        return self._parse_xml(response)

    def do_query(self, query=None, qid=None, query_params=None, columns=None, sort=None,
                 structured=True, num=None, only_new=False, skip=None, ascending=True,
                 include_rids=False, return_metadata=False, qid_custom_headers=False,
                 database=None):
        if not query_params:
            query_params = {}
        request = {}
        if query:
            request['query'] = query
        elif qid:
            request['qid'] = qid
        else:
            raise TypeError('Must provide a query, qid, or qname')
        
        if columns:
            columns = [str(c) for c in columns]
            request['clist'] = '.'.join(str(c) for c in columns)
        if sort:
            request['slist'] = '.'.join(str(c) for c in sort)
        if structured:
            request['fmt'] = 'structured'

        if query_params:

            for this_key, this_value in query_params.items():
                request[this_key] = this_value

        options = []
        if num is not None:
            options.append('num-{0}'.format(num))
        if only_new:
            options.append('onlynew')
        if skip is not None:
            options.append('skp-{0}'.format(skip))
        if not ascending:
            options.append('sortorder-D')
        if options:
            request['options'] = '.'.join(options)

        if include_rids:
            request['includeRids'] = 1

        if qid_custom_headers and qid:

            headers = self._get_qid_headers(
                qid=qid, database=database or self.database)

        else:
            headers = None

        response = self._request(
            f'{self.base_url}/db/{database or self.database}', self._build_xml(request), 'DoQuery', 'POST')
        
        response = self._parse_xml(response, return_as_dict=False)

        return self._parse_record_data(response, return_metadata, headers)

    def get_schema(self, database=None, required=None, get_xml=False):
        response = self._request(
            f'{self.base_url}/db/{database or self.database}', self._build_xml({}), 'GetSchema', 'POST')

        response = self._parse_xml(response, required_fields=required, return_as_dict=False)

        if get_xml:
            return etree.tostring(response)
        
        return self._parse_schema(response)

    def get_file(self, fname, folder, rid, fid, version=0, database=None):
        url = f'{self.base_url}/up/{database or self.database}/a/r{rid}/e{fid}/v{version}'
        
        response = self._request(url, self._build_xml({}), 'files', 'POST')

        response = base64.b64encode(response)
        
        return response

    def upload_file(self, rid, upload, database=None):
        request = {
            'rid': rid,
            'field': [(
                {'fid': upload['field'], 'filename': upload['filename']},
                upload['value']
            )]
        }

        response = self._request(
            f'{self.base_url}/db/{database or self.database}',
            self._build_xml(request),
            'UploadFile',
            'POST'
        )

        return self._parse_xml(response)

    def import_from_csv(self, records_csv, clist, clist_output=None, skipfirst=False, database=None, required=None,
                        chunk=None):
        # support function to generate import request and return response
        def _run_import(records_csv, clist, clist_output, skipfirst, database, required):
            request = {
                'clist': '.'.join(str(c) for c in clist),
                'records_csv': records_csv,
            }
            if clist_output:
                request['clist_output'] = '.'.join(str(c) for c in clist_output)

            if skipfirst:
                request['skipfirst'] = 1

            response = self._request(
                f'{self.base_url}/db/{database or self.database}', 
                self._build_xml(request), 
                'ImportFromCSV', 
                'POST'
            )
            return self._parse_xml(response, required_fields=required)

        records_list = records_csv.splitlines()

        # confirm that records_csv is not empty and record line count
        line_count = len(records_list)
        if line_count == 0:
            return None

        if chunk:
            print(f'Importing {line_count} records in chunks of {chunk} records')
            chunk_size = chunk
            offset = 0
            while offset < line_count:
                # prevent skipfirst being executed per chunk
                if offset != 0:
                    skipfirst = False

                chunks = records_list[offset:offset + chunk_size]
                offset += chunk_size
                records_csv =  '\n'.join(chunks)
                print(f'Importing records {offset - chunk_size + 1} to {offset} of {line_count} records')
                print(f'Importing {len(chunks)} records')
                response = _run_import(records_csv, clist, clist_output, skipfirst, database, required)
        else:
            response = _run_import(records_csv, clist, clist_output, skipfirst, database, required)

        return response

    def get_user_info(self, email=None, rid=None):
        request = {}
        if email:
            request["email"] = email
        elif rid:
            request["rid"] = rid

        response = self._request(
            f'{self.base_url}/db/main', self._build_xml(request), 'GetUserInfo', 'POST')
        
        response = self._parse_xml(response, return_as_dict=False)
        
        user_info = {}

        user_info["id"] = response.xpath('.//user')[0].attrib["id"]
        user_info["first_name"] = response.xpath('.//firstName')[0].text
        user_info["last_name"] = response.xpath('.//lastName')[0].text
        user_info["login"] = response.xpath('.//login')[0].text
        user_info["email"] = response.xpath('.//email')[0].text
        user_info["screen_name"] = response.xpath('.//screenName')[0].text
        user_info["is_verified"] = response.xpath('.//isVerified')[0].text
        user_info["external_auth"] = response.xpath('.//externalAuth')[0].text

        return user_info

# --------------------------------- deprecated methods (excluding internal) --------------------------------- #

    # def sign_out(self):
    #     response = self.request('SignOut', 'main', {},
    #                             required=['errcode', 'errtext'])
    #     return response

    # def get_user_info(self, email=None, rid=None, database=None):

    #     request = {}
    #     if email:
    #         request["email"] = email
    #     elif rid:
    #         request["rid"] = rid

    #     response = self.request('GetUserInfo', "main", request)
    #     """
    #     <?xml version="1.0" encoding="utf-8" ?>
    #     <qdbapi>
    #         <action>API_GetUserInfo</action>
    #         <errcode>0</errcode>
    #         <errtext>No error</errtext>
    #         <user id="58956622.bmhg">

    #      <firstName>Michael</firstName> <lastName>Geary</lastName> <login>mgeary@sympo.com</login> <email>mgeary@sympo.com</email> <screenName></screenName> <isVerified>1</isVerified>
    #      <externalAuth>0</externalAuth>
    #         </user>
    #     </qdbapi>
    #     """

    #     user_info = {}

    #     user_info["id"] = response.xpath('.//user')[0].attrib["id"]
    #     user_info["first_name"] = response.xpath('.//firstName')[0].text
    #     user_info["last_name"] = response.xpath('.//lastName')[0].text
    #     user_info["login"] = response.xpath('.//login')[0].text
    #     user_info["email"] = response.xpath('.//email')[0].text
    #     user_info["screen_name"] = response.xpath('.//screenName')[0].text
    #     user_info["is_verified"] = response.xpath('.//isVerified')[0].text
    #     user_info["external_auth"] = response.xpath('.//externalAuth')[0].text

    #     return user_info

    # def do_query_count(self, query, database=None):
    #     request = OrderedDict()
    #     request['query'] = query
    #     response = self.request(
    #         'DoQueryCount', database or self.database, request, required=['numMatches'])
    #     return int(response['numMatches'])


    # def set_field_properties(self, fid, settings, database=None):
    #     request = settings
    #     request["fid"] = fid
    #     response = self.request("SetFieldProperties",
    #                             database or self.database, request)
    #     return response

    # def get_db_page(self, page, named=True, database=None):
    #     # Get DB page from a qbase app
    #     request = {}
    #     if named == True:
    #         request['pagename'] = page
    #     else:
    #         request['pageID'] = page
    #     response = self.request(
    #         'GetDBPage', database or self.database, request)
    #     return self._parse_db_page(response)

    # def get_ancestry(self, database=None, required=None, get_xml=False):
    #     """Perform query and return results (list of dicts)."""
    #     request = {}
    #     response = self.request(
    #         'GetAncestorInfo', database or self.database, request, required=required)
    #     if get_xml:
    #         return etree.tostring(response)

    #     return self._parse_schema(response)


    # def granted_dbs(self, adminOnly=0, excludeparents=0, includeancestors=0, withembeddedtables=0, database='main'):
    #     """Perform query and return results (list of dicts)."""
    #     request = {}
    #     if adminOnly:
    #         request['adminOnly'] = adminOnly
    #     if excludeparents:
    #         request['excludeparents'] = excludeparents
    #     if includeancestors:
    #         request['includeancestors'] = includeancestors
    #     if withembeddedtables:
    #         request['withembeddedtables'] = withembeddedtables

    #     response = self.request(
    #         'GrantedDBs', database or self.database, request)
    #     return response

    # def granted_dbs_for_group(self, gid=None, ):

    #     request = {"gid": gid, }
    #     # print request

    #     response = self.request('GrantedDBsForGroup', "main", request)
    #     # print etree.tostring(response)

    #     r = response.xpath('.//dbinfo')
    #     apps = []
    #     for row in r:
    #         my_data = (row.xpath("dbid")[0].text, row.xpath("dbname")[0].text)

    #         apps.append(my_data)

    #     return apps

    # def get_users_in_group(self, gid=None, includeAllMgrs="true", database=None):

    #     request = {"gid": gid, "includeAllMgrs": includeAllMgrs}
    #     response = self.request('GetUsersInGroup', "main", request)
    #     return self._parse_group_users(response)

    # def get_info(self, database=None):

    #     request = {}
    #     response = self.request('GetDBInfo', database, request)

    #     app_info = {}

    #     app_info["dbname"] = response.xpath('.//dbname')[0].text
    #     app_info["lastRecModTime"] = response.xpath(
    #         './/lastRecModTime')[0].text
    #     app_info["lastModifiedTime"] = response.xpath(
    #         './/lastModifiedTime')[0].text
    #     app_info["createdTime"] = response.xpath('.//createdTime')[0].text
    #     app_info["numRecords"] = response.xpath('.//numRecords')[0].text
    #     app_info["mgrID"] = response.xpath('.//mgrID')[0].text
    #     app_info["mgrName"] = response.xpath('.//mgrName')[0].text
    #     app_info["version"] = response.xpath('.//version')[0].text
    #     app_info["time_zone"] = response.xpath('.//time_zone')[0].text

    #     return app_info

    # def create_group(self, name, description, account_id=None):

    #     request = {"name": name, "description": description}

    #     if account_id:
    #         request["accountId"] = account_id

    #     response = self.request('CreateGroup', "main", request)

    #     r = response.xpath('.//group')[0]
    #     return r.attrib["id"]

    #     # print etree.tostring(response)

    # def add_user_to_group(self, gid, userid, allowAdminAccess=False):

    #     request = {"gid": gid, "uid": userid,
    #                "allowAdminAccess": allowAdminAccess}

    #     response = self.request('AddUserToGroup', "main", request)
    #     print(etree.tostring(response))

    #     # r = response.xpath('.//group')[0]
    #     # return r.attrib["id"]

    #     return response

    # def add_group_to_group(self, gid, subgroupid):

    #     request = {"gid": gid, "subgroupid": subgroupid, }

    #     response = self.request('AddSubGroup', "main", request)
    #     print(etree.tostring(response))
    #     return response

    # def get_role_info(self, database=None):

    #     request = {}
    #     response = self.request(
    #         'GetRoleInfo', database or self.database, request)
    #     # print etree.tostring(response)

    #     return self._parse_individual_roles(response)

    # def get_user_role(self, user_id=None, inclgrps=0, database=None):

    #     request = {}
    #     response = self.request(
    #         'GetUserRole', database or self.database, request)
    #     return self._parse_individual_roles(response)

    # def change_user_role(self, user_id=None, old_role_id=None, new_role_id=None, database=None):

    #     request = {"userid": user_id,
    #                "roleid": old_role_id, "newroleid": new_role_id}
    #     print(request)

    #     response = self.request(
    #         'ChangeUserRole', database or self.database, request)
    #     return response

    # def change_manager(self, manager_email=None, database=None):

    #     request = {"newmgr": manager_email}
    #     response = self.request(
    #         'ChangeManager', database or self.database, request)

    #     return response

    # def list_users_and_roles(self, database=None, get_xml=False):

    #     request = {}
    #     response = self.request(
    #         'UserRoles', database or self.database, request)

    #     # print etree.tostring(response)

    #     if get_xml:
    #         return etree.tostring(response)

    #     # print etree.tostring(response)

    #     return self._parse_user_roles(response)

    # def list_db_pages(self, database=None):
    #     request = {}
    #     response = self.request(
    #         'ListDBpages', database or self.database, request)
    #     return self._parse_list_pages(response)

    # def add_group_to_role(self, gid=None, role_id=None, database=None):

    #     request = {}
    #     request['gid'] = gid
    #     request['roleid'] = role_id
    #     response = self.request(
    #         'AddGroupToRole', database or self.database, request)

    #     return response

    # def b64_file(self, url):  # added by Emilio
    #     """ Downloads file given the QB file URL
    #         Returns base64 string representation of file
    #     """
    #     fname = url.split("/")[-1]
    #     headers = {'Cookie': 'ticket=%s' % self.ticket}
    #     r = requests.get(url, headers=headers)
    #     response = r.content

    #     b64 = base64.b64encode(response)

    #     return b64
