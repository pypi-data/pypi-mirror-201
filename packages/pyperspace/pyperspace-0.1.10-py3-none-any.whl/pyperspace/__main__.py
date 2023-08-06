from pyperspace.rest_api import generate_api
from pyperspace.config import get_config, Config
from uvicorn.main import run
from argparse import ArgumentParser

def _get_arg_parser():
    argparser = ArgumentParser(description='Pyperspace Daemon')
    argparser.add_argument('-c', '--config', metavar='<file>', help='configuration file', required=True)
    argparser.add_argument('--data-dir', metavar='<dir>', help='overrides data directory', default=None)
    argparser.add_argument('--host', metavar='<IP>', help='overrides HTTP listener IP', default='0.0.0.0')
    argparser.add_argument('-p', '--port', metavar='<int>', type=int, help='overrides HTTP listener port', default=None)
    return argparser

def _parse_config(cfg_file: str, args) -> Config:
    cfg = get_config(cfg_file)
    if args.data_dir is not None: cfg.data_dir = args.data_dir
    if args.host is not None: cfg.http.host = args.host
    if args.port is not None: cfg.http.port = args.port
    return cfg

def main():
    args = _get_arg_parser().parse_args()
    cfg = _parse_config(args.config, args)
    run(generate_api(cfg), host=cfg.http.host, port=cfg.http.port, workers=1)
    return 0
