#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time
import logging
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from elasticsearch import RequestError, NotFoundError

parser = argparse.ArgumentParser('Gather zabbix host informations and create es index')
parser.add_argument('--es_url', required=True, help="ElasticSearch server ip")
parser.add_argument('--es_user', default='', help="ElasticSearch server login user")
parser.add_argument('--es_passwd', default='', help="ElasticSearch server login password")
parser.add_argument('--es_tpl', required=True, help="ElasticSearch index template name")
parser.set_defaults(handler=lambda args: main(args))

body = {
    "order": "500",
    "index_patterns": [
        "zabbix-raw-host-info-*"
    ],
    "mappings": {
        "properties": {
            "hostid": {
                "type": "integer"
            },
            "proxy_hostid": {
                "type": "integer"
            },
            "status": {
                "type": "byte"
            },
            "disable_until": {
                "type": "date"
            },
            "available": {
                "type": "byte"
            },
            "errors_from": {
                "type": "date"
            },
            "lastaccess": {
                "type": "byte"
            },
            "ipmi_authtype": {
                "type": "byte"
            },
            "ipmi_privilege": {
                "type": "byte"
            },
            "ipmi_disable_until": {
                "type": "date"
            },
            "ipmi_available": {
                "type": "byte"
            },
            "snmp_disable_until": {
                "type": "date"
            },
            "snmp_available": {
                "type": "byte"
            },
            "maintenanceid": {
                "type": "integer"
            },
            "maintenance_status": {
                "type": "byte"
            },
            "maintenance_type": {
                "type": "byte"
            },
            "maintenance_from": {
                "type": "date"
            },
            "ipmi_errors_from": {
                "type": "date"
            },
            "snmp_errors_from": {
                "type": "date"
            },
            "jmx_disable_until": {
                "type": "date"
            },
            "jmx_available": {
                "type": "byte"
            },
            "jmx_errors_from": {
                "type": "date"
            },
            "flags": {
                "type": "byte"
            },
            "templateid": {
                "type": "integer"
            },
            "tls_connect": {
                "type": "byte"
            },
            "tls_accept": {
                "type": "byte"
            },
            "auto_compress": {
                "type": "byte"
            },
            "groups": {
                "properties": {
                    "groupid": {
                        "type": "integer"
                    },
                    "internal": {
                        "type": "byte"
                    },
                    "flags": {
                        "type": "byte"
                    },
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            },
            "interfaces": {
                "properties": {
                    "ip": {
                        "type": "ip"
                    },
                    "interfaceid": {
                        "type": "integer"
                    },
                    "hostid": {
                        "type": "integer"
                    },
                    "main": {
                        "type": "byte"
                    },
                    "type": {
                        "type": "byte"
                    },
                    "useip": {
                        "type": "byte"
                    },
                    "port": {
                        "type": "integer"
                    },
                    "bulk": {
                        "type": "byte"
                    }
                }
            },
            "inventory": {
                "properties": {
                    "hostid": {
                        "type": "integer"
                    },
                    "inventory_mode": {
                        "type": "byte"
                    },
                    "alias": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "asset_tag": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "chassis": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "host_netmask": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "host_networks": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "hw_arch": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "location": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "macaddress_a": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "macaddress_b": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "model": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "oob_ip": {
                        "type": "text"
                    },
                    "os": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "os_full": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "os_short": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "poc_1_name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "poc_2_name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "serialno_a": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "site_rack": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "tag": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "type": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "type_full": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "vendor": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            },
            "主机组": {
                "type": "alias",
                "path": "groups.name"
            },
            "接口地址": {
                "type": "alias",
                "path": "interfaces.ip"
            },
            "主机别名": {
                "type": "alias",
                "path": "inventory.alias"
            },
            "资产标签": {
                "type": "alias",
                "path": "inventory.asset_tag"
            },
            "机架": {
                "type": "alias",
                "path": "inventory.chassis"
            },
            "子网掩码": {
                "type": "alias",
                "path": "inventory.host_netmask"
            },
            "主机网络": {
                "type": "alias",
                "path": "inventory.host_networks"
            },
            "硬件架构": {
                "type": "alias",
                "path": "inventory.hw_arch"
            },
            "机房": {
                "type": "alias",
                "path": "inventory.location"
            },
            "MAC_A": {
                "type": "alias",
                "path": "inventory.macaddress_a"
            },
            "MAC_B": {
                "type": "alias",
                "path": "inventory.macaddress_b"
            },
            "型号": {
                "type": "alias",
                "path": "inventory.model"
            },
            "主机名称": {
                "type": "alias",
                "path": "inventory.name"
            },
            "管理IP": {
                "type": "alias",
                "path": "inventory.oob_ip"
            },
            "OS": {
                "type": "alias",
                "path": "inventory.os"
            },
            "OS_FULL": {
                "type": "alias",
                "path": "inventory.os_full"
            },
            "OS_SHORT": {
                "type": "alias",
                "path": "inventory.os_short"
            },
            "主负责人": {
                "type": "alias",
                "path": "inventory.poc_1_name"
            },
            "次负责人": {
                "type": "alias",
                "path": "inventory.poc_2_name"
            },
            "序列号": {
                "type": "alias",
                "path": "inventory.serialno_a"
            },
            "机柜": {
                "type": "alias",
                "path": "inventory.site_rack"
            },
            "标签": {
                "type": "alias",
                "path": "inventory.tag"
            },
            "类型": {
                "type": "alias",
                "path": "inventory.type"
            },
            "具体类型": {
                "type": "alias",
                "path": "inventory.type_full"
            },
            "供应商": {
                "type": "alias",
                "path": "inventory.vendor"
            }
        }
    }
}


def get_es_tpl(es, tpl_name: str):
    try:
        tpl = es.indices.get_template(name=tpl_name)
        if tpl:
            return tpl.get(tpl_name)
    except (RequestError, NotFoundError) as err:
        logging.error(msg="\033[31m" + str(err) + "\033[0m")


def get_hosts(zapi, es, tpl_name):
    body_datas = []
    hosts = zapi.host.get({
        'output': 'extend',
        'selectGroups': 'extend',
        'selectInterfaces': 'extend',
        'selectInventory': 'extend'
    })
    dt = time.strftime('%Y.%m.%d', time.localtime())
    for host in hosts:
        host['@timestamp'] = datetime.utcfromtimestamp(time.time())
        body_datas.append({
            '_id': host['hostid'],
            '主机名称': host['inventory'].get('name', host['host']),
            '主机别名': host['inventory'].get('alias', host['host']),
            '接口地址': [aif['ip'] for aif in host['interfaces']],
            '主机组': [grp['name'] for grp in host['groups']],
            'OS': host['inventory'].get('os'),
            'OS_FULL': host['inventory'].get('os_full'),
            'OS_SHORT': host['inventory'].get('os_short'),
            '资产标签': host['inventory'].get('asset_tag'),
            '主负责人': host['inventory'].get('poc_1_name'),
            '次负责人': host['inventory'].get('poc_2_name'),
            '机架': host['inventory'].get('chassis'),
            '子网掩码': host['inventory'].get('host_netmask'),
            '主机网络': host['inventory'].get('host_networks'),
            '机房': host['inventory'].get('location'),
            '机柜': host['inventory'].get('site_rack'),
            '序列号': host['inventory'].get('serialno_a'),
            '管理IP': host['inventory'].get('oob_ip'),
            'MAC_A': host['inventory'].get('macaddress_a'),
            'MAC_B': host['inventory'].get('macaddress_b'),
            '硬件架构': host['inventory'].get('hw_arch'),
            '标签': host['inventory'].get('tag'),
            '类型': host['inventory'].get('type'),
            '具体类型': host['inventory'].get('type_full'),
            '型号': host['inventory'].get('model'),
            '供应商': host['inventory'].get('vendor'),
            '@timestamp': datetime.utcfromtimestamp(time.time())
        })

    tpl = get_es_tpl(es=es, tpl_name=tpl_name)
    # 当指定的模板存在时，则 Merge 以上的 mappings 到指定的模板
    tpl.update(body) if tpl else None
    es.indices.put_template(
        name=tpl_name,
        body=tpl if tpl else body,
        # "create" 设置为 False 时，如果不存在这个模板则创建，如果存在则更新
        create=False
    )

    for host in hosts:
        host['_id'] = host['hostid']
    helpers.bulk(es, hosts, index='zabbix-raw-host-info-' + dt, raise_on_error=True)
    helpers.bulk(es, body_datas, index='zabbix-host-info-' + dt, raise_on_error=True)


def main(args):
    es = Elasticsearch(
        args.es_url,
        http_auth=(args.es_user, args.es_passwd)
    )
    get_hosts(args.zapi, es, args.es_tpl)
