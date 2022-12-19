python3 -m src.db_proxy.app  > db_proxy.log  2> db_proxy.log &
python3 -m src.gateway.app   > gateway.log   2> gateway.log &
python3 -m src.translate.app > translate.log 2> translate.log &