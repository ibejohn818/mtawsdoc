# -*- coding: utf-8 -*-

import os
import sys
import boto3
import jinja2
import jmespath
import json

"""Main module."""


class AwsHelper(object):

    _region = None
    _default_region = 'us-west-2'
    _clients = {}

    def __init__(self, region=None):

        if region is not None:
            AwsHelper._region = region


    @staticmethod
    def getRegion():
        if AwsHelper._region is None:
            if os.environ.get('AWS_DEFAULT_REGION'):
                AwsHelper._region = os.environ.get('AWS_DEFAULT_REGION')
            else:
                AwsHelper._region = AwsHelper._default_region

        return AwsHelper._region

    @staticmethod
    def client(service):
        """ Create and return boto3 client
            clients will be cached """

        if service not in AwsHelper._clients:

            try:
                AwsHelper._clients.update({service: 
                    boto3.client(service, region_name=AwsHelper.getRegion())})
            except:
                raise

        return AwsHelper._clients[service]

    def cloudfront(self):

        cf = self.client("cloudfront")

        try:
            dists = cf.list_distributions()
        except:
            raise

        sites = []

        for d in dists['DistributionList']['Items']:

            try:
                domains = jmespath.search("Aliases.Items[]", d)
            except:
                domains = []

            try:
                origins = jmespath.search("Origins.Items[][DomainName, CustomOriginConfig.OriginProtocolPolicy]", d)
            except:
                origins = []

            try:
                domain = jmespath.search("DomainName", d)
            except:
                domain = None

            sites.append({
                'domains': domains,
                'origins': origins,
                'domain': domain
                })

        return sites


class Template(object):

    def __init__(self):
        self.loader = jinja2.PackageLoader("mtawsdoc","templates")
        self.env = jinja2.Environment(loader=self.loader, trim_blocks=True, lstrip_blocks=True)

    def load(self, template_name, **kwargs):
        temp = self.env.get_template(template_name)
        res = temp.render(**kwargs)
        return res
