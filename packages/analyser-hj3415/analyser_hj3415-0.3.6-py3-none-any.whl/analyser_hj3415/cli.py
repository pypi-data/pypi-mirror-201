import argparse
from util_hj3415 import utils
from .db import chk_db, mongo
from . import eval
from scraper2_hj3415.nfscrapy import run as nfsrun


def db():
    cmd = ['repair', 'sync', 'eval', 'update']
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', help=f"Command - {cmd}")
    parser.add_argument('target', help="Target for scraping (type 6digit code or 'all')")
    parser.add_argument('-d', '--db_path', help="Set mongo database path")

    args = parser.parse_args()

    db_path = args.db_path if args.db_path else "mongodb://192.168.0.173:27017"
    client = mongo.connect_mongo(db_path)

    if args.cmd in cmd:
        if args.cmd == 'repair':
            if args.target == 'all' or utils.is_6digit(args.target):
                need_for_repair_codes = chk_db.chk_integrity_corps(client, args.target)
                # repair dict 예시 - {'343510': ['c106', 'c104', 'c103'], '298000': ['c104'], '091810': ['c104']}
                print(f"Need for repairing codes :{need_for_repair_codes}")
                if need_for_repair_codes:
                    # x = input("Do you want to try to repair db by scraping? (y/N)")
                    # if x == 'y' or x == 'Y':
                        for code, failed_page_list in need_for_repair_codes.items():
                            for page in failed_page_list:
                                if page == 'c101':
                                    nfsrun.c101([code, ], db_path)
                                elif page == 'c103':
                                    nfsrun.c103([code, ], db_path)
                                elif page == 'c104':
                                    nfsrun.c104([code, ], db_path)
                                elif page == 'c106':
                                    nfsrun.c106([code, ], db_path)
                            recheck_result = chk_db.chk_integrity_corps(client, code)
                            if recheck_result:
                                # 다시 스크랩해도 오류가 지속되는 경우
                                print(f"The db integrity failure persists..{recheck_result}")
                                # x = input(f"Do you want to delete {code} on DB? (y/N)")
                                # if x == 'y' or x == 'Y':
                                #    mongo.Corps.del_db(client, code)
                                # else:
                                #    print("Canceled.")
                                mongo.Corps.del_db(client, code)
                    # else:
                    #     print("Done.")
                else:
                    print("Done.")
            else:
                print(f"Invalid target option : {args.target}")
        elif args.cmd == 'update':
            if args.target == 'all' or utils.is_6digit(args.target):
                need_for_update_codes = list(chk_db.chk_modifying_corps(client, args.target).keys())
                # need_for_update_codes 예시 - [codes....]
                print(f"Need for updating codes :{need_for_update_codes}")
                if need_for_update_codes:
                    nfsrun.c103(need_for_update_codes, db_path)
                    nfsrun.c104(need_for_update_codes, db_path)
                    nfsrun.c106(need_for_update_codes, db_path)
            else:
                print(f"Invalid target option : {args.target}")
        elif args.cmd == 'sync':
            if args.target == 'all':
                chk_db.sync_mongo_with_krx(client)
            else:
                print(f"The target should be 'all' in sync command.")
        elif args.cmd == 'eval':
            if args.target == 'all':
                # eval을 평가해서 데이터베이스에 저장한다.
                eval.make_today_eval_df(client, refresh=True)
            else:
                print(f"The target should be 'all' in sync command.")
    else:
        print(f"The command should be in {cmd}")

    client.close()


if __name__ == "__main__":
    db()
