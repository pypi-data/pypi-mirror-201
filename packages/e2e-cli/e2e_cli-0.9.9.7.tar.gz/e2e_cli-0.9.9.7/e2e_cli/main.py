import argparse
# import argcomplete working on auto-complete now 

from e2e_cli.commands_routing import CommandsRouting
from e2e_cli.core.error_logs_service import ErrorLogs
from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core import help_messages

PARSING_ERROR_MSG=[]

class Main:
    def __init__(self):
        pass

    def FormatUsage(self, parser, action):
        if(action=="alias"):
            format_string = "e2e_cli" + " alias" + " [-h]" + " {create,delete,list,edit/update} ... "
        else:
            format_string = "e2e_cli" + " --alias"+ " " + action + " [-h]" + " {create,delete,list,edit/update} ... "
        parser.usage = format_string

    def FormatUsageCommand(self, parser, action, command):
        format_string = "e2e_cli" + " alias=" + "<alias_name>"+ " " + action + " [-h] " + command
        parser.usage = format_string

    def alias(self, parser):
        alias_sub_parser = parser.add_subparsers(title="Alias Commands", metavar="", dest="alias_commands")
        alias_add_sub_parser = alias_sub_parser.add_parser("add", help="To add api key and auth token")
        alias_file_sub_parser = alias_sub_parser.add_parser("add_file", help="To add api key and auth token via file")
        alias_delete_sub_parser = alias_sub_parser.add_parser("delete", help="To delete api key and auth token")
        alias_view_sub_parser = alias_sub_parser.add_parser("view", help="To view all alias and credentials")
        alias_set_default_sub_parser = alias_sub_parser.add_parser("set", help="To set default alias for system")
        self.FormatUsageCommand(alias_add_sub_parser, "alias", "add")
        self.FormatUsageCommand(alias_file_sub_parser, "alias", "add_file")
        self.FormatUsageCommand(alias_delete_sub_parser, "alias", "delete")
        self.FormatUsageCommand(alias_view_sub_parser, "alias", "view")
        self.FormatUsageCommand(alias_set_default_sub_parser, "alias", "set")

    def node(self, parser):
        node_sub_parser = parser.add_subparsers(title="Node Commands", metavar="", dest="node_commands")
        node_action=parser.add_argument('--action', help="Type of action to be performed your node")
        node_create_sub_parser = node_sub_parser.add_parser("create", help="To create a new node", formatter_class=help_messages.cli_formatter())
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node", formatter_class=help_messages.cli_formatter())
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes", formatter_class=help_messages.cli_formatter())
        node_get_sub_parser = node_sub_parser.add_parser("get", help="To get a list of all nodes", formatter_class=help_messages.cli_formatter())
        self.FormatUsageCommand(node_action, "node", "actions")
        self.FormatUsageCommand(node_create_sub_parser, "node", "create")
        self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        self.FormatUsageCommand(node_get_sub_parser, "node", "get")

    def image(self, parser):
        image_sub_parser = parser.add_subparsers(title="Image Commands", metavar="", dest="image_commands")
        image_list=parser.add_argument('--list_by', help="attribute/property by which you want to list images")
        image_create_sub_parser = image_sub_parser.add_parser("create", help="To create a new image")
        image_delete_sub_parser = image_sub_parser.add_parser("delete", help="To delete a specific image")
        image_list_sub_parser = image_sub_parser.add_parser("list", help="To get a list of all image")
        image_get_sub_parser = image_sub_parser.add_parser("rename", help="To rename a specific image")
        self.FormatUsageCommand(image_list, "image", "list_by")
        self.FormatUsageCommand(image_create_sub_parser, "image", "create")
        self.FormatUsageCommand(image_delete_sub_parser, "image", "delete")
        self.FormatUsageCommand(image_list_sub_parser, "image", "list")
        self.FormatUsageCommand(image_get_sub_parser, "image", "rename")

    def lb(self, parser):
        node_sub_parser = parser.add_subparsers(title="LB Commands", metavar="", dest="lb_commands")
        node_create_sub_parser = node_sub_parser.add_parser("create", help="To create a new node", formatter_class=help_messages.cli_formatter())
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node", formatter_class=help_messages.cli_formatter())
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes", formatter_class=help_messages.cli_formatter())
        node_edit_sub_parser = node_sub_parser.add_parser("edit", help="To get a list of all nodes", formatter_class=help_messages.cli_formatter())
        self.FormatUsageCommand(node_create_sub_parser, "node", "create")
        self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        self.FormatUsageCommand(node_edit_sub_parser, "node", "edit")

    def bucket(self, parser):
        bucket_sub_parser = parser.add_subparsers(title="Bucket Commands", metavar="", dest="bucket_commands")
        bucket_action=parser.add_argument('--action', help="Type of action to be performed your bucket")
        bucket_create_sub_parser = bucket_sub_parser.add_parser("create", help="To create a new bucket")
        bucket_delete_sub_parser = bucket_sub_parser.add_parser("delete", help="To delete a specific bucket")
        bucket_delete_sub_parser = bucket_sub_parser.add_parser("list", help="To get a list of all buckets")
        self.FormatUsageCommand(bucket_action, "bucket", "actions")
        self.FormatUsageCommand(bucket_create_sub_parser, "bucket", "create")
        self.FormatUsageCommand(bucket_delete_sub_parser, "bucket", "delete")
        self.FormatUsageCommand(bucket_delete_sub_parser, "bucket", "list")    

    def autoscaling(self, parser):
        autoscaling_sub_parser = parser.add_subparsers(title="Autoscaling Commands", metavar="", dest="autoscaling_commands")
        autoscaling_create_sub_parser = autoscaling_sub_parser.add_parser("create", help="To create a new bucket")
        autoscaling_delete_sub_parser = autoscaling_sub_parser.add_parser("delete", help="To delete a specific bucket")
        autoscaling_delete_sub_parser = autoscaling_sub_parser.add_parser("list", help="To get a list of all buckets")
        self.FormatUsageCommand(autoscaling_create_sub_parser, "autoscaling", "create")
        self.FormatUsageCommand(autoscaling_delete_sub_parser, "autoscaling", "delete")
        self.FormatUsageCommand(autoscaling_delete_sub_parser, "autoscaling", "list")

    def vpc(self, parser):
        vpc_sub_parser = parser.add_subparsers(title="VPC Commands", metavar="", dest="vpc_commands")
        vpc_create_sub_parser = vpc_sub_parser.add_parser("create", help="To create a new bucket")
        vpc_delete_sub_parser = vpc_sub_parser.add_parser("delete", help="To delete a specific bucket")
        vpc_delete_sub_parser = vpc_sub_parser.add_parser("list", help="To get a list of all buckets")
        self.FormatUsageCommand(vpc_create_sub_parser, "vpc", "create")
        self.FormatUsageCommand(vpc_delete_sub_parser, "vpc", "delete")
        self.FormatUsageCommand(vpc_delete_sub_parser, "vpc", "list")

    def cdn(self, parser):
        cdn_sub_parser = parser.add_subparsers(title="CDN Commands", metavar="", dest="cdn_commands")
        cdn_action=parser.add_argument('--action', help="Type of action to be performed your cdn")
        cdn_create_sub_parser = cdn_sub_parser.add_parser("create", help="To create a new cdn")
        cdn_delete_sub_parser = cdn_sub_parser.add_parser("delete", help="To delete a specific cdn")
        cdn_delete_sub_parser = cdn_sub_parser.add_parser("list", help="To get a list of all cdn")
        self.FormatUsageCommand(cdn_action, "cdn", "actions")
        self.FormatUsageCommand(cdn_create_sub_parser, "cdn", "create")
        self.FormatUsageCommand(cdn_delete_sub_parser, "cdn", "delete")
        self.FormatUsageCommand(cdn_delete_sub_parser, "cdn", "list")

    def volumes(self, parser):
        volumes_sub_parser = parser.add_subparsers(title="Volumes Commands", metavar="", dest="volumes_commands")
        volumes_action=parser.add_argument('--action', help="Type of action to be performed your volumes")
        volumes_create_sub_parser = volumes_sub_parser.add_parser("create", help="To create a new volumes")
        volumes_delete_sub_parser = volumes_sub_parser.add_parser("delete", help="To delete a specific volumes")
        volumes_delete_sub_parser = volumes_sub_parser.add_parser("list", help="To get a list of all volumes")
        self.FormatUsageCommand(volumes_action, "volumes", "actions")
        self.FormatUsageCommand(volumes_create_sub_parser, "volumes", "create")
        self.FormatUsageCommand(volumes_delete_sub_parser, "volumes", "delete")
        self.FormatUsageCommand(volumes_delete_sub_parser, "volumes", "list")
           
    def dbaas(self, parser):
        dbaas_sub_parser = parser.add_subparsers(title="DBaaS Commands", metavar="", dest="dbaas_commands")
        dbaas_action=parser.add_argument('--action', help="Type of action to be performed your dbaas")
        dbaas_create_sub_parser = dbaas_sub_parser.add_parser("create", help="To launch a new dbaas")
        dbaas_delete_sub_parser = dbaas_sub_parser.add_parser("delete", help="To delete a created dbaas")
        dbaas_list_sub_parser = dbaas_sub_parser.add_parser("list", help="To list all of your dbaas")
        self.FormatUsageCommand(dbaas_action, "dbaas", "actions")
        self.FormatUsageCommand(dbaas_create_sub_parser, "dbaas", "create")
        self.FormatUsageCommand(dbaas_list_sub_parser, "dbaas", "list")
        self.FormatUsageCommand(dbaas_delete_sub_parser, "dbaas", "delete")


class Namespace(argparse._AttributeHolder):
    """Simple object for storing attributes.
    copied and over-written/modified here for getting unrecognised commands/inputs
    """

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__


class ArgPaser(argparse.ArgumentParser):

    # used to collect input values 
    def inputs_list(self, argv):
        inputs=Namespace()
        for element in argv:
            if "=" in element:
                    x=element.split("=")
                    setattr(inputs, x[0], x[1])
            elif(element.startswith('-')):
                    setattr(inputs, element.lstrip('-'), True)
        return inputs        
        
    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = argparse._('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))
        # here args is used for routing to service and inputs as input to service
        return Namespace(args=args, inputs=self.inputs_list(argv))

    def error(self, message):
        args = {'prog': self.prog, 'message': message}
        if("unrecognized arguments" not in args["message"]):
                        PARSING_ERROR_MSG.append( args["message"])


def commanding(parser):
    sub_parsers = parser.add_subparsers(title="Commands", dest="command")
    alias_parser = sub_parsers.add_parser("help", help="To view man doc")
    alias_parser = sub_parsers.add_parser("alias", help="To add delete tokens" )
    node_parser = sub_parsers.add_parser("node", help="To apply crud operations over Nodes")
    lb_parser = sub_parsers.add_parser("lb", help="To apply operations over Load-Balancer")
    bucket_parser = sub_parsers.add_parser("bucket", help="To create/delete/list buckets of the user")
    dbaas_parser = sub_parsers.add_parser("dbaas", help="To perform operations over DBaaS service provided")
    image_parser = sub_parsers.add_parser("image", help="To perform operations over Image service provided")
    autoscaling_parser= sub_parsers.add_parser("autoscaling", help="To create/delete/list autoscaling for the user")
    vpc_parser= sub_parsers.add_parser("vpc", help="To create/delete/list vpc for the user")
    cdn_parser= sub_parsers.add_parser("cdn", help="To create/delete/list cdn for the user")
    volumes_parser= sub_parsers.add_parser("volumes", help="To create/delete/list volume for the user")
    m = Main()
    m.alias(alias_parser)
    m.bucket(bucket_parser)
    m.node(node_parser)
    m.dbaas(dbaas_parser)
    m.lb(lb_parser)
    m.image(image_parser)
    m.autoscaling(autoscaling_parser)
    m.vpc(vpc_parser)
    m.cdn(cdn_parser)
    m.volumes(volumes_parser)

    m.FormatUsage(alias_parser, "alias")
    m.FormatUsage(node_parser, "node")
    m.FormatUsage(lb_parser, "lb")
    m.FormatUsage(bucket_parser, "bucket")
    m.FormatUsage(dbaas_parser, "dbaas")
    m.FormatUsage(autoscaling_parser, "autoscaling")
    m.FormatUsage(vpc_parser, "vpc")
    m.FormatUsage(cdn_parser, "cdn")
    m.FormatUsage(volumes_parser, "volumes")


def run_main_class():
    parser = ArgPaser(description="E2E CLI", formatter_class=help_messages.cli_formatter())

    #version, info, and alias to be taken first else default
    parser.add_argument("-v", "--version", action='store_true', help="To view version Info")
    parser.add_argument( "--info", action='store_true', help="To view package Info")
    parser.add_argument("--alias", default="default", type=str, help="The name of your access credentials valid option")

    # parsing our commands for routing
    commanding(parser)

    # breakpoint()
    args = parser.parse_args()
    commands_route = CommandsRouting(args)
    commands_route.route(PARSING_ERROR_MSG)
   
    

