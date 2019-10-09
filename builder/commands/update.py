import os
from six.moves import configparser
import logging
import sys
import argparse

from cliff.command import Command
from builder.converter.converter import convert_to_xml
from builder.uploader.jenkins_upload import update


class Update(Command):
    """
    Command for updating views on jenkins
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = argparse.ArgumentParser(description="Parser")
        parser.add_argument("--conf",
                            type=str,
                            help="Path to the jenkins config file")
        parser.add_argument("yaml",
                            type=str,
                            nargs="+",
                            help="Path to the view yaml file")
        parser.add_argument("--url",
                            type=str,
                            help="Jenkins url")
        parser.add_argument("--user",
                            type=str,
                            help="Jenkins user")
        parser.add_argument("--password",
                            type=str,
                            help="Jenkins user password")
        return parser

    def read_update(self, config, view_yaml):
        import io
        import six
        with io.open(view_yaml, 'r',encoding='utf-8') as yaml_file:
            _yaml = yaml_file.read()
            self.log.debug(_yaml)
            try:
                xmls = convert_to_xml(_yaml)
            except Exception as e:
                raise(e)

            if isinstance(xmls[0], six.string_types) :
                name, xml = xmls
                self.log.debug(xml)
                update(config, name, xml)
            else:
                for name, xml in xmls:
                    self.log.debug(xml)
                    update(config, name, xml)

    def take_action(self, parsed_args):
        self.log.info("Updating view data in Jenkins")
        if not parsed_args.conf:
            self.get_parser("jenkins-view-builder").print_help()
            sys.exit(1)
        config = self.parse_config(parsed_args)
        for yaml_filename in parsed_args.yaml:

            yaml_file = os.path.join(yaml_filename)

            if os.path.isdir(yaml_file):
                views = [view for view in os.listdir(yaml_file)]
                for view_yaml in views:
                    self.log.debug("View file %s" % view_yaml)
                    self.read_update(config,
                                     os.path.join(yaml_file + '/%s' % view_yaml))
            else:
                self.log.debug("View file %s" % yaml_file)
                self.read_update(config, os.path.join(yaml_file))

    def parse_config(self, parser):
        self.log.debug("Parsing the jenkins config file")
        config = configparser.ConfigParser()
        config.read(parser.conf)
        if parser.user:
            user = parser.user
        else:
            if config.has_option('jenkins', 'user'):
                user = config.get('jenkins', 'user')
            else:
                user = ""
                self.log.info("'user' not set in the config file. Defaulting to \"\"")
        if parser.password:
            password = parser.password
        else:
            if config.has_option('jenkins', 'password'):
                password = config.get('jenkins', 'password')
            else:
                password = ""
                self.log.info("'password' not set in the config file. Defaulting to \"\"")
        if parser.url:
            url = parser.url
        else:
            url = config.get('jenkins', 'url')
        return dict(url=url, user=user, password=password)
