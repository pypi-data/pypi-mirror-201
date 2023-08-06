from syncqb import qb_client
# import qb_client
# from pprint import pprint
# from lxml.etree import _Element

def main():
    # table info:
    # database: bnsucj684
    # values valid for fid 6: 'Misc', '_other'
    # values valid for fid 9: 23
    # fid 3 is the record id, which is auto generated
    # use a value from fid 3 to update or delete a record
    # create a series of tests to test the functionality of each method for both xml and json
    # ONLY MODIFY OR DELETE RECORDS THAT YOU CREATED

    record_data = [
        {
            '6': 'Misc',
            '9': 23.0,
            '3': None
        },
        {
            '6': 'Misc',
            '9': 23.1,
            '3': None
        },
    ]
    record_data_csv = 'Misc,23\nMisc,23\nMisc,23\nMisc,23\nMisc,23\nMisc,23'
    uploads = [
        {
            'field': '19',
            'filename': 'test.txt',
            'value': 'MjM='
        }
    ]

    client = qb_client.get_xml_client()
    client2 = qb_client.get_json_client()

    xml_res = client.do_query(
        # query='{3.EX.128}',
        qid=10, 
        columns=[3, 6, 9], 
        database='bnsucj684', 
        structured=True,
        qid_custom_headers=True
    )
    # xml_res = 'N/A'
    # json_res = client2.get_file(database='bnsucj684', field=19, record=69036)
    json_res = 'N/A'

    print('xml_res:', xml_res)
    print('json_res:', json_res)
    




if __name__ == '__main__':
    main()