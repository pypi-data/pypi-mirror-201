# This is a sample Python script.
import os.path
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import logging
import getpass
import argparse
from nvos import login, run

# 创建全局记录器
# 配置日志格式化信息
logging.basicConfig(filename=os.path.expanduser(os.path.join("~", "logger.log")), level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser(description="Script Description")

    subparsers = parser.add_subparsers(title="NVOS Script Command", dest='subcommand')
    subparsers.add_parser('login', help='The login command is the first command that must be executed.')

    subparsers.add_parser('init', help='The Init command is used to initialize the workspace. Please execute the '
                                      'command in your workspace directory')
    subparsers.add_parser('async', help='The async command automatically synchronizes the data you modify from the cloud and to push addtion file to cloud')
    subparsers.add_parser('pull', help='The pull command pulls the data you modify from the cloud')
    subparsers.add_parser('push', help='The push command is used upload local new files or folders to the cloud')
    subparsers.add_parser('version', help='The version command will tell you this script really version')
    subparsers.add_parser('path', help='The path command will return windows service register script path, so you can '
                                       'install this script for windows like async command.You need execute "pythonw '
                                       'win_auto_script.py" and script is this command return path content')
    args = parser.parse_args()

    if args.subcommand == "login":
        username = input("email：")
        password = getpass.getpass("password：")
        status = login.login_user_check(username, password)
        print(status)
        run.login_init_data()
    elif args.subcommand == "init":
        run.command_init()
    elif args.subcommand == "async":
        run.command_async()
    elif args.subcommand == "pull":
        run.command_pull()
    elif args.subcommand == "push":
        run.command_push()
    elif args.subcommand == "version":
        print("1.1.0")
    elif args.subcommand == "path":
        current_file_path = os.path.abspath(__file__)
        current_file_dir = os.path.dirname(current_file_path)
        current_file_dir = os.path.dirname(current_file_dir)
        win_path = os.path.join(current_file_dir, 'win', 'win_auto_script.py')
        print(win_path)
    else:
        parser.print_help()
        print(
            "\n\t if you still have many things you don't understand,you can take a look as https://nio.feishu.cn/wiki/wikcn9L7Di4ILQKaNmDDTrmpLqg ")


if __name__ == '__main__':
    main()
    # flag = utils.check_subdirectory_workspace_exist("/Users/andre.zhao/Documents/test")
    # print(flag)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
