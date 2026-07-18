# -*- coding: utf-8 -*-
"""
教务管理系统 - 程序入口
运行方式：python main.py
"""

from admin_system import AdminSystem


def main():
    print("正在启动教务管理系统...")
    try:
        system = AdminSystem()
        system.run()
    except Exception as e:
        print(f"系统启动失败：{e}")
        print("请检查 MySQL 服务是否启动，以及 db_config.py 中的配置是否正确。")


if __name__ == '__main__':
    main()
