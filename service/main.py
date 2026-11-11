"""A tiny Pollie helper service: renders a poll announcement from a YAML description."""
import yaml
from jinja2 import Template

import settings

TEMPLATE = Template("Poll '{{ title }}' is open until {{ closes }} ({{ options|length }} options)")


def announce(description: str) -> str:
    poll = yaml.safe_load(description)
    return TEMPLATE.render(title=poll["title"], closes=poll["closes"], options=poll["options"])


def storage_target() -> str:
    return "s3://%s as %s" % (settings.BUCKET, settings.AWS_ACCESS_KEY_ID[:4] + "****")


if __name__ == "__main__":
    print(announce("title: Tabs or spaces?\ncloses: Friday\noptions: [tabs, spaces]"))
