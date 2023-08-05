from trojsdk.core import client_utils
from python_hosts import Hosts, HostsEntry
import webbrowser
import sys


def run(args):
    import subprocess

    with subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ) as process:
        for line in process.stdout:
            print(line.decode("utf8"), end="")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="trojsdk", description="Troj sdk command line utils"
    )
    parser.add_argument(
        "-config", metavar="-c", type=str, help="Path to the config file"
    )
    parser.add_argument("-query_mongo", metavar="-qm", help="Pass an arbitrary dict to query the mongodb")
    parser.add_argument("-endpoint", metavar="-e", help="The end point where your cluster is located")

    parser.add_argument(
        "-test", action="store_true", help="Run tests with TrojAI supplied configs."
    )
    parser.add_argument("-gp", action="store_true", help="Get pods")
    parser.add_argument("-gpw", action="store_true", help="Get pods watch")
    parser.add_argument("-nossl", action="store_true", help="No ssl flag")
    parser.add_argument(
        "-minio",
        nargs="?",
        const="127.0.0.1",
        metavar="IP ADDRESS",
        type=str,
        help=argparse.SUPPRESS,
        # help="Install the host entry and open the MinIO dashboard for the local cluster. Default value of 127.0.0.1.",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if args.gp:
        import subprocess

        # open kubectl get pods -n=trojai
        process = run(["kubectl", "get", "pods", "-n=trojai"])

    if args.gpw:
        # open kubectl get pods -n=trojai -w
        try: 
            process = run(["kubectl", "get", "pods", "-n=trojai", "-w"])
        except KeyboardInterrupt:
            print("Exiting watch...")

    if args.config:
        client_utils.submit_evaluation(path_to_config=args.config, nossl=args.nossl)

    if args.minio:
        address = args.minio
        name = "trojai.minio"
        comment = "Trojai MinIO host"

        hosts = Hosts()
        hosts.remove_all_matching(comment=comment)

        try:
            host_entry = HostsEntry(
                entry_type="ipv4", address=address, names=[name], comment=comment
            )
        except Exception as e:
            try:
                host_entry = HostsEntry(
                    entry_type="ipv6", address=address, names=[name], comment=comment
                )
            except Exception as e2:
                raise e from e2

        hosts.add([host_entry])
        hosts.write()
        webbrowser.open_new_tab("http://" + name)

    if args.query_mongo is not None and args.endpoint is not None:
        pass


if __name__ == "__main__":
    main()
