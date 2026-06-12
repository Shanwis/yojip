import argparse
import json
import subprocess
import sys

PARTY_NAME = "yojip_party"

def _pw_dump():
    try:
        result = subprocess.run(
            ["pw-dump"], capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except FileNotFoundError:
        print("error: PipeWire not found — is it installed?", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"error: pw-dump failed: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"error: pw-dump returned invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def _real_sinks(data):
    sinks = []
    for obj in data:
        if obj.get("type") != "PipeWire:Interface:Node":
            continue
        props = obj.get("info", {}).get("props", {})
        if props.get("media.class") == "Audio/Sink" and not props.get("node.virtual", False):
            sinks.append({
                "id": obj["id"],
                "name": props.get("node.name", "unknown"),
                "description": props.get("node.description", "unknown"),
            })
    return sinks


def _party_ids(data):
    ids = []
    for obj in data:
        if obj.get("type") != "PipeWire:Interface:Node":
            continue
        props = obj.get("info", {}).get("props", {})
        if props.get("node.name") == PARTY_NAME:
            ids.append(obj["id"])
    return ids


def cmd_outputs(args):
    data = _pw_dump()
    sinks = _real_sinks(data)
    if not sinks:
        print("No audio outputs found.")
        return
    for s in sinks:
        print(f"  {s['id']:>6}  {s['name']:<30}  {s['description']}")


def cmd_party(args):
    data = _pw_dump()

    if args.action == "delete":
        ids = _party_ids(data)
        if not ids:
            print("error: no party exists", file=sys.stderr)
            sys.exit(1)
        for node_id in ids:
            subprocess.run(["pw-cli", "destroy", str(node_id)], capture_output=True, check=True)
        print("Party deleted")
        return

    if _party_ids(data):
        print("error: a party already exists", file=sys.stderr)
        sys.exit(1)

    sinks = _real_sinks(data)
    if not sinks:
        print("error: no audio outputs found", file=sys.stderr)
        sys.exit(1)

    slave_names = ",".join(s["name"] for s in sinks)
    try:
        subprocess.run(
            ["pactl", "load-module", "module-combine-sink",
             f"sink_name={PARTY_NAME}",
             f"slaves={slave_names}",
             "latency_compensate=true"],
            capture_output=True, text=True, check=True,
        )
    except FileNotFoundError:
        print("error: pactl not found — is pipewire-pulse installed?", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"error: pactl failed: {e}", file=sys.stderr)
        if e.stderr:
            print(e.stderr.strip(), file=sys.stderr)
        sys.exit(1)

    try:
        subprocess.run(
            ["pactl", "set-default-sink", PARTY_NAME],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"error: failed to set default sink: {e}", file=sys.stderr)
        sys.exit(1)

    print("Party created")


def main():
    parser = argparse.ArgumentParser(
        prog="yojip",
        description="Join multiple audio outputs into synchronized PipeWire combined sinks",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("outputs", help="list available audio outputs")

    p = sub.add_parser("party", help="manage combined sinks (parties)")
    p.add_argument("action", nargs="?", choices=["create", "delete"], default="create")

    args = parser.parse_args()

    if args.command == "outputs":
        cmd_outputs(args)
    elif args.command == "party":
        cmd_party(args)


if __name__ == "__main__":
    main()
