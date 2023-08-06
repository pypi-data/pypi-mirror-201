#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Gary
# Datetime: 2022/12/8 16:05
# IDE: PyCharm
"""
    Functions:
        - update_action_send_users()
          - get users by "media" name
          - get "operations" and "send to users" by "action" name
          - merge "media" users and "send to users"
          - update "action"
        - main(): main function
"""
import argparse
import logging


def update_action_send_users(zapi, media_name: str, action_name: str):
    """
        根据 Action 名称更新 operations 的 "send to users" 列表：
            1. 首先根据 Media 名称获取这个 Media 下的所有用户信息（即哪些用户配置了这个 Media）；
            2. 然后，根据 Action 名称获取 Operations 信息；
            3. 其次，获取此 Operation 原有的 "send to users" 列表；
            4. 再比对 "send to users" 列表和根据 Media 名称获取的用户列表；
            5. 最后追加不在原有 "send to users" 列表里的用户信息;
            6. 【action.update() 方法要求更新原有 Action 所有参数字段，否则会清空没有更新到的参数的值】。
    :param zapi:
    :param media_name:
    :param action_name:
    :return:
    """
    media = zapi.mediatype.get(
        {
            "filter": {"description": media_name},
            "selectUsers": ["userid"],
            "output": ["users"]
        }
    )
    action = zapi.action.get(
        {
            "output": "extend",
            "selectOperations": "extend",
            "filter": {"name": action_name}
        }
    )
    usr_groups = zapi.usergroup.get(
        {
            "output": ["usrgrpid", "name", "users"],
            "selectUsers": ["userid"],
            # "0" 表示处于开启状态
            "status": 0,
            "filter": {"name": ["Zabbix administrators", "Disabled"]}
        }
    )
    if not media or not action:
        logging.info(f"update None! Action -> ['{action_name}']")
    if media and action:
        media_users = media[0].get("users")
        operations = action[0].get("operations")
        usrgrp_users = []
        for grp in usr_groups:
            usrgrp_users.extend(grp.get("users"))
        for operation in operations:
            # 排除在 "Zabbix administrators"、"Disabled" 这两个用户组中的用户
            media_users = [user for user in media_users if user not in usrgrp_users]
            for user in media_users:
                user.update({"operationid": operation.get("operationid")})
            ops_users = operation.get("opmessage_usr")
            ops_users.extend(media_users)
            operation["opmessage_usr"] = ops_users
        zapi.action.update(
            {
                "actionid": action[0].get("actionid"),
                "operations": operations
            }
        )
        logging.info(f"update success! Action -> [{action[0].get('name')!r}]")


def main(args):
    """Main Function"""
    update_action_send_users(
        zapi=args.zapi,
        media_name=args.media,
        action_name=args.action
    )


parser = argparse.ArgumentParser(
    description="Automatically search for the media type configured by the user,"
                "and then configure it as action"
)
parser.add_argument(
    "--media",
    required=True,
    type=str,
    help="user configured media type"
)
parser.add_argument(
    "--action",
    required=True,
    type=str,
    help="the alarm action"
)
parser.set_defaults(handler=main)
