import argparse
import json
import subprocess
import sys


def cmd_outputs(args):
    try:
        result = subprocess.run(
            ["pw-dump"], capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        sinks = []
        for obj in data:
            if obj.get("type") == "PipeWire:Interface:Node":
                info = obj.get("info", {})
                props = info.get("props", {})
                if props.get("media.class") == "Audio/Sink":
                    sinks.append({
                        "id": obj["id"],
                        "name": props.get("node.name", "unknown"),
                        "description": props.get("node.description", "unknown"),
                    })
        if not sinks:
            print("No audio outputs found.")
            return
        for s in sinks:
            print(f"  {s['id']:>6}  {s['name']:<30}  {s['description']}")
    except FileNotFoundError:
        print("error: PipeWire not found — is it installed?", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"error: pw-dump failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_party_create(args):
    print(f"[stub] party create '{args.name}' — will create combined sink")


def cmd_party_add(args):
    print(f"[stub] party add '{args.output}' to '{args.name}'")


def cmd_party_remove(args):
    print(f"[stub] party remove '{args.output}' from '{args.name}'")


def cmd_party_list(args):
    print("[stub] party list — will list all parties")


def cmd_party_destroy(args):
    print(f"[stub] party destroy '{args.name}'")


def main():
    parser = argparse.ArgumentParser(
        prog="yojip",
        description="Join multiple audio outputs into synchronized PipeWire combined sinks",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("outputs", help="list available audio outputs")

    p = sub.add_parser("party", help="manage combined sinks (parties)")
    p.add_argument("action", choices=["create", "add", "remove", "list", "destroy"])
    p.add_argument("name", nargs="?")
    p.add_argument("output", nargs="?")

    args = parser.parse_args()

    if args.command == "outputs":
        cmd_outputs(args)
    elif args.command == "party":
        if args.action == "create" and args.name:
            cmd_party_create(args)
        elif args.action == "add" and args.name and args.output:
            cmd_party_add(args)
        elif args.action == "remove" and args.name and args.output:
            cmd_party_remove(args)
        elif args.action == "list":
            cmd_party_list(args)
        elif args.action == "destroy" and args.name:
            cmd_party_destroy(args)
        else:
            parser.print_help()
            sys.exit(1)


if __name__ == "__main__":
    main()
