# -*- coding: utf-8 -*-

"""Console script for mtawsdoc."""

import click

from mtawsdoc import (AwsHelper, Template)


@click.group()
def main(args=None):
    """Console script for mtawsdoc."""
    pass


@main.command()
def help():
    pass


@main.command(help="Generate Cloudfront Blocks")
def cloudfront():

    ah = AwsHelper()
    t = Template()
    cf = ah.cloudfront()

    template = t.load("cloudfront.md.j2", sites=cf)

    click.echo(template)


if __name__ == "__main__":
    main()
