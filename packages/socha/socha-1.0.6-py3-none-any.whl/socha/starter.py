"""
This is the main entry point for the SoCha application.
"""
import argparse
import datetime
import logging

import pkg_resources
import urllib.request
import json

from socha.api.networking.game_client import GameClient, IClientHandler
from socha.utils.package_builder import SochaPackageBuilder


class Starter:
    """
    When this is called, the client will try to connect to the server and join a game.
    When successful, the client will start the loop and call the on_update and calculate_move methods,
    if the server sends updates.
    """

    def __init__(self, logic: IClientHandler, host: str = "localhost", port: int = 13050, reservation: str = None,
                 room_id: str = None, survive: bool = False, auto_reconnect: bool = False,
                 log: bool = False, verbose: bool = False, build: str = None):
        """
        All these arguments can be overwritten, when parsed via start arguments,
        or you initialize this class with the desired values.

        :param logic: Your logic the client will call, if moves are requested.
        :param host: The host that the client should connect to.
        :param port: The port of the host.
        :param reservation: Reservation code for a prepared game.
        :param room_id: Room Id the client will try to connect.
        :param survive: If True the client will keep running, even if the connection to the server is terminated.
        :param log: If True the client will write a log file to the current directory.
        :param verbose: Verbose option for logging.
        """
        args = self._handle_start_args()

        self.write_log: bool = args.log or log
        self.verbose = args.verbose or verbose
        self._setup_debugger(self.verbose)

        self.check_socha_version()

        self.build: str = args.build or build
        if self.build:
            builder = SochaPackageBuilder(self.build)
            builder.build_package()
            exit(0)

        self.host: str = args.host or host
        self.port: int = args.port or port
        self.reservation: str = args.reservation or reservation
        self.room_id: str = args.room or room_id
        self.survive: bool = args.survive or survive
        self.auto_reconnect: bool = args.auto_reconnect or auto_reconnect

        self.client = GameClient(host=self.host, port=self.port, handler=logic, reservation=self.reservation,
                                 room_id=room_id, auto_reconnect=self.auto_reconnect, survive=self.survive)

        self.client.join()

        self.client.start()

    def _setup_debugger(self, verbose: bool):
        if verbose:
            level: int = logging.DEBUG
        else:
            level: int = logging.INFO

        if self.write_log:
            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            logging.basicConfig(filename=f"log{now}", level=level,
                                format="%(asctime)s: %(levelname)s - %(message)s")
            logging.getLogger().addHandler(logging.StreamHandler())
        else:
            logging.basicConfig(level=level, format="%(asctime)s: %(levelname)s - %(message)s")
        logging.info("Starting...")
        logging.critical("\nDiese Version von SoCha hat einige Änderungen.\n"
                         "Deshalb wird Code welcher mit 1.0.0 und niedriger geschrieben wurde ein paar Fehler haben.\n"
                         "Hilfe, um seinen Code anzupassen kann man unter: \n"
                         "https://github.com/FalconsSky/socha-python-client/blob/master/changes.md\n"
                         "finden, oder mir eine E-Mail oder Nachricht auf Discord schreiben.")

    @staticmethod
    def check_socha_version():
        package_name = 'socha'
        try:
            installed_version = pkg_resources.get_distribution(package_name).version
            response = urllib.request.urlopen(f"https://pypi.org/pypi/{package_name}/json")
            json_data = json.loads(response.read())
            latest_version = json_data['info']['version']
            if installed_version != latest_version:
                logging.warning(
                    f"A newer version ({latest_version}) of {package_name} is available. You have version "
                    f"{installed_version}.")
        except pkg_resources.DistributionNotFound:
            logging.error(f"{package_name} is not installed.")
        except urllib.error.URLError as e:
            logging.warning(
                f"Could not check the latest version of {package_name} due to {type(e).__name__}: {e}")

    @staticmethod
    def _handle_start_args():
        parser = argparse.ArgumentParser(description='All arguments are optional.', add_help=False,
                                         epilog='Please make sure that the server is already running, '
                                                'before you start your player.')
        parser.add_argument('--help', action='help', help='Prints this help message.')
        parser.add_argument('-h', '--host', help='The host to connect to. The default is \'localhost\'.')
        parser.add_argument('-p', '--port', help='The port of the host. The default is 13050.', type=int)
        parser.add_argument('-r', '--reservation', help='Reservation code for a prepared game.', type=str)
        parser.add_argument('-R', '--room', help='Room Id the client will try to connect.', type=str)
        parser.add_argument('-s', '--survive', action='store_true',
                            help='If present the client will keep running, even if the connection to the server is '
                                 'terminated.')
        parser.add_argument('-l', '--log', action='store_true',
                            help='If present the client will write a log file to the current directory.')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose option for logging.')
        parser.add_argument('--auto-reconnect', action='store_true',
                            help='Automatically reconnect to the server if the connection is lost.')
        parser.add_argument('-b', '--build', help='Builds the this script into a package with all its dependencies.')
        return parser.parse_args()
