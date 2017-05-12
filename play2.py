#!/usr/bin/env python

import json
import subprocess
import operator
import argparse

class EC2(object):
    def instance_description(self, instance_id):
        if not hasattr(self, '_instances'):
            self._instances = json.loads(self.aws_describe_instance(instance_id))
        return self._instances

    def aws_describe_instance(self, instance_id):
        return subprocess.check_output(["aws", "ec2", "describe-instances", "--instance-ids",  instance_id])

    def ec2_gropus(self, instance_id):
        def get_instances(reservation): return reservation['Instances']

        def get_group_names(instance): return instance['SecurityGroups']

        list = self.instance_description(instance_id)

        instances = reduce(operator.add, map(get_instances, list['Reservations']))

        names = map(get_group_names, instances)

        return names


def parse_args():
    parser = argparse.ArgumentParser(description='Permission management of EC2 instances.')
    parser.add_argument('--i', action='store', help='The instance id to discover/update.')
    parser.add_argument('--list_sg', action='store_true', help='List security groups of an instance.')
    parser.add_argument('--update_sg', action='store_true', help='Change security group of an instance.')
    parser.add_argument('--get_role', action='store_true', help='Display IAM role name of an instance.')
    parser.add_argument('--update_role', action='store_true', help='Update IAM role of an instance.')

    args = parser.parse_args()
    if not args.list_sg:
        parser.print_help()
    return args


def print_json(text):
    print json.dumps(text, indent=2, sort_keys=True)


def main():
    args = parse_args()

    if args.list_sg:
        print_json(EC2().ec2_gropus(args.i))


if __name__ == '__main__':
    main()
