import argparse
import json
from pathlib import Path

from .engine import assess, lead_report, read_env, read_json, render_contact_message, validate


def main():
    parser = argparse.ArgumentParser(description="Prepare evidence-led leads locally; never sends messages")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("validate")
    check.add_argument("file")
    check.add_argument("--schema", default="schemas/opportunity.schema.json")
    for command in ("assess", "report"):
        p = sub.add_parser(command)
        p.add_argument("lead")
        p.add_argument("--profile", default="private/founder_profile.local.json")
        if command == "report":
            p.add_argument("--output", required=True)
    contact = sub.add_parser("contact-draft")
    contact.add_argument("lead")
    contact.add_argument("template")
    contact.add_argument("--approval", required=True)
    contact.add_argument("--env", default=".env.local")
    contact.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.command == "validate":
        validate(read_json(args.file), args.schema)
        print("Valid")
    elif args.command == "assess":
        print(json.dumps(assess(read_json(args.lead), read_json(args.profile)), indent=2))
    else:
        output = Path(args.output).resolve()
        private_root = Path("private").resolve()
        if not output.is_relative_to(private_root):
            parser.error("Reports and rendered contacts must stay under private/")
        if args.command == "report":
            result = lead_report(read_json(args.lead), read_json(args.profile))
        else:
            result = render_contact_message(Path(args.template).read_text(encoding="utf-8"),
                                            read_json(args.approval), read_env(args.env),
                                            read_json(args.lead))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result, encoding="utf-8")
        print("Saved private draft; not sent")


if __name__ == "__main__":
    main()
