from elasticsearch7 import Elasticsearch
from sshtunnel import SSHTunnelForwarder
import json
from faker import Faker
from random import random
from datetime import datetime


class ElasticsearchIndexManager:
    def __init__(self, es_version, path_mapping, path_template, path_setting, remote_address, es_port):
        self.es_version = es_version
        self.path_mapping = path_mapping
        self.path_template = path_template
        self.path_setting = path_setting
        self.remote_address = remote_address
        self.es_port = es_port

        self.index_pattern_list = []
        self.index_template_list = []
        self.index_name_list = []
        self.mapping_data = {}
        self.setting_data = {}
        self.template_data = {}
        self.data_dic = {}

    def connect_ssh_tunnel(self):
        ssh_tunnel = SSHTunnelForwarder(
            ssh_address_or_host=("wny.iptime.org", 18022),
            ssh_username="won21yuk",
            ssh_pkey="C:/Users/by_wh/.ssh/datalab-bastion.pem",
            ssh_private_key_password="wnytech",
            remote_bind_address=(self.remote_address, self.es_port)
        )
        return ssh_tunnel

    def connect_elasticsearch(self, hosts):
        es = Elasticsearch(hosts)
        return es

    def delete_index_has_template(self, index_list):
        dummy_list = index_list[:]
        index_list_not_template = index_list
        for index in dummy_list:
            for pattern in self.index_pattern_list:
                if index.startswith(pattern) is True:
                    index_list_not_template.remove(index)
                    print(index + ' has been removed.')

        return index_list_not_template

    def create_index_template(self, es):
        for template in self.index_template_list:
            template_nm = template
            if es.indices.exists_template(name=template_nm):
                print(f'Index template {template_nm} already exists.')
            else:
                template_body = self.template_data[template_nm]
                es.indices.put_template(name=template_nm, body=template_body)
                print(f'Created index template {template_nm}.')

    def create_index_body(self, index):
        mapping = self.mapping_data[index]
        setting = self.setting_data[index]
        setting.update(mapping)
        return setting

    def create_index(self, es, index_list):
        index_list_not_template = self.delete_index_has_template(index_list)
        for index in index_list_not_template:
            body = self.create_index_body(index)
            if es.indices.exists(index=index):
                print(f"Index {index} already exists.")
            else:
                es.index(index=index, doc_type="doc", body=body)
                print(f"Created index {index}.")

    def load_data_from_files(self):
        with open(self.path_mapping, 'r', encoding='utf-8') as f:
            self.mapping_data = json.load(f)
            self.index_name_list = [index for index in self.mapping_data if index.find('.') == -1]
            self.index_type_list = [list((self.mapping_data[index]['mappings'].keys()))[0] for index in
                                    self.index_name_list]
        with open(self.path_setting, 'r', encoding='utf-8') as f:
            self.setting_data = json.load(f)

        with open(self.path_template, 'r', encoding='utf-8') as f:
            self.template_data = json.load(f)
            self.index_template_list = [template for template in self.template_data if template.find('.') == -1]
            for i in range(len(self.index_template_list)):
                template_name = self.index_template_list[i]
                template = self.template_data[template_name]
                index_pattern = template['index_patterns'][0].split('*')[0]
                self.index_pattern_list.append(index_pattern)

    def execution(self):
        ssh_server = self.connect_ssh_tunnel()
        with ssh_server as server:
            elasticsearch_hosts = ["http://localhost:{}".format(server.local_bind_port)]
            es = self.connect_elasticsearch(elasticsearch_hosts)
            self.create_index_template(es)
            self.create_index(es, self.index_name_list)

    def bulk_data_generator(self, count):
        numeric = ['long', 'integer', 'short', 'byte', 'double', 'float', 'half_float', 'scaled_float', 'unsigned_long']
        string = ['keyword', 'text']
        faker = Faker()
        loop = 0
        self.load_data_from_files()
        # 1000개 쌓일 때 마다 벌크 인덱싱
        for i in range(len(self.index_name_list)):
            cnt = 0
            bulk_data = ''
            while cnt < int(count):
                parsed_properties = self.mapping_data[self.index_name_list[i]]['mappings'][self.index_type_list[i]]['properties']
                for k, v in parsed_properties.items():
                    chk_subfield = list(v.keys())
                    # 서브 필드가 존재한다면, 서브 필드들의 필드명과 타입을 가져오기
                    if "properties" in chk_subfield:
                        parsed_subfields = parsed_properties[k]['properties']
                        dict_ms_field = {}
                        dict_dummy = {}
                        for sb_key, sb_value in parsed_subfields.items():
                            subfield_nm = sb_key
                            subfield_type = parsed_subfields[sb_key]['type']
                            dict_s_field = {}
                            if subfield_type in numeric:
                                # if subfield_nm == 'timestamp':
                                #     dict_s_field = {
                                #         subfield_nm: faker.date_time_between(start_date=datetime(2019, 1, 1)).strftime(
                                #             "%Y-%m-%d %H:%M:%S")}
                                # else:
                                dict_s_field = {subfield_nm: faker.pyint(min_value=1, max_value=1000)}
                            elif subfield_type in string:
                                # if subfield_nm == 'timestamp':
                                #     dict_s_field = {
                                #         subfield_nm: faker.date_time_between(start_date=datetime(2019, 1, 1)).strftime(
                                #             "%Y-%m-%d %H:%M:%S")}
                                # else:
                                dict_s_field = {subfield_nm: faker.text(20).replace(".", "")}
                            elif subfield_type == "date":
                                dict_s_field = {
                                    subfield_nm: faker.date_time_between(start_date=datetime(2019, 1, 1)).strftime(
                                        "%Y-%m-%d %H:%M:%S")}
                            elif subfield_type == "boolean":
                                dict_s_field = {subfield_nm: random.choice([True, False])}
                            elif subfield_type == "object":
                                dict_s_field[k] = {"name": faker.name(), "age": faker.pyint(min_value=20, max_value=70)}
                            else:
                                dict_s_field[k] = {subfield_nm: faker.text(20)}
                            dict_dummy.update(dict_s_field)
                        dict_ms_field[k] = dict_dummy
                        self.data_dic.update(dict_ms_field)

                    # 서브필드가 없다면, 바로 해당 필드들의 필드명과 타입을 가져오기 (현재 : 멀티필드는 고려 x)
                    else:
                        field_type = parsed_properties[k]['type']
                        dict_m_field = {}
                        if field_type in numeric:
                            # if k == 'timestamp':
                            #     dict_m_field[k] = faker.date_time_between(start_date=datetime(2019, 1, 1)).strftime(
                            #         "%Y-%m-%d %H:%M:%S")
                            # else:
                            dict_m_field[k] = faker.pyint(min_value=1, max_value=1000)
                        elif field_type in string:
                            # if k == 'timestamp':
                            #     dict_m_field[k] = faker.date_time_between(start_date=datetime(2019, 1, 1)).strftime(
                            #         "%Y-%m-%d %H:%M:%S")
                            # else:
                            dict_m_field[k] = faker.text(20).replace(".", "")
                        elif field_type == "date":
                            dict_m_field[k] = faker.date_time_between(start_date=datetime(2019, 1, 1)).strftime(
                                "%Y-%m-%d %H:%M:%S")
                        elif field_type == "boolean":
                            dict_m_field[k] = random.choice([True, False])
                        elif field_type == "object":
                            dict_m_field[k] = {"name": faker.name(), "age": faker.pyint(min_value=20, max_value=70)}
                        else:
                            dict_m_field[k] = faker.text(20)

                        self.data_dic.update(dict_m_field)

                # 8버전에서는 type지정 x
                # Elasticsearch Bulk API에서 사용할 수 있는 NDJSON 형태의 데이터를 생성
                index_line = {
                    "index": {
                        "_index": self.index_name_list[i],
                        "_type": self.index_type_list[i]
                    }
                }
                data_line = json.dumps(self.data_dic)
                bulk_data += f"{json.dumps(index_line)}\n{data_line}\n"
                cnt += 1
            loop += 1
            ssh_server = self.connect_ssh_tunnel()
            with ssh_server as server:
                elasticsearch_hosts = ["http://localhost:{}".format(server.local_bind_port)]
                es = self.connect_elasticsearch(elasticsearch_hosts)

                es.bulk(body=bulk_data)
                print(f"{bulk_data}\n{loop}번 루프\n")


# if __name__=='__main__':
#     es_manager = ElasticsearchIndexManager(
#         es_version=6,
#         es_port=9200,
#         path_mapping='/diagnostics/mapping.json',
#         path_setting='/diagnostics/settings.json',
#         path_template='/diagnostics/templates.json',
#         remote_address='192.168.121.1'
#     )
#
#     es_manager.load_data_from_files()
#     es_manager.execution()
#
#     for _ in range(10):
#         es_manager.bulk_data_generator(10)

