import json

from prettytable import PrettyTable


from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.request_service import Request
from e2e_cli.core.alias_service import AliasServices
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL
from e2e_cli.node.node_crud.node import NodeCrud


class LBServices:
    def __init__(self, alias):
        self.alias = alias
        self.alias_service_object = AliasServices(alias)

    def choice_nodes(self, nodes_assigned_to_lb, node_list_dict):
        node_list = []
        for node_instance in nodes_assigned_to_lb:
            node_list.append(node_instance["backend_name"])
        table = PrettyTable(["Node ID", "Node Name", "Node Status",
                             "Price"])
        for node_count in node_list_dict.keys():
            if node_list_dict[node_count]["name"] in node_list:
                pass
            else:
                table.add_row([node_count, node_list_dict[node_count]["name"],
                               node_list_dict[node_count]["status"],
                               node_list_dict[node_count]["plan"]])

        if table.rowcount == 0:
            return "/"
        Py_version_manager.py_print(table)
        node_choice = Py_version_manager.py_input("Enter the Node ID: ")
        while( not Checks.is_int(node_choice) or not int(node_choice) in node_list_dict): 
            node_choice = Py_version_manager.py_input("Enter a valid Node ID: ")
        return int(node_choice)

    def assign_nodes(self, nodes_assigned_to_lb, api_key, auth_token):
        node_class_object = NodeCrud(alias=self.alias,
                                      api_key=api_key,
                                      auth_token=auth_token)
        node_dict_list = node_class_object.list_node(parameter=1)
        node_list_dict = dict()
        node_count = 1
        for node_instance in node_dict_list:
            node_list_dict[node_count] = node_instance
            node_count += 1
        node_choice = self.choice_nodes(nodes_assigned_to_lb, node_list_dict)
        if node_choice == '/':
            return nodes_assigned_to_lb
        Py_version_manager.py_print("Node name: ", node_list_dict[node_choice]["name"])
        Py_version_manager.py_print("Node ip: ", node_list_dict[node_choice]["public_ip_address"])
        node_port = Py_version_manager.py_input("Enter the Node Port: ")
        while(not Checks.is_int(node_port)):
            node_port = Py_version_manager.py_input("Enter the Node Port: ")
        nodes_assigned_to_lb.append(
            {"backend_name": node_list_dict[node_choice]["name"],
             "backend_ip": node_list_dict[node_choice]["private_ip_address"], "backend_port": node_port})
        want_to_go_further = Py_version_manager.py_input("Enter y/n to add more nodes: ")
        while want_to_go_further.lower() == 'y':
            node_choice = self.choice_nodes(nodes_assigned_to_lb, node_list_dict)
            if node_choice == '/':
                break
            Py_version_manager.py_print("Node name: ", node_list_dict[node_choice]["name"])
            Py_version_manager.py_print("Node ip: ", node_list_dict[node_choice]["private_ip_address"])
            node_port = Py_version_manager.py_input("Enter the Node Port: ")
            while(not Checks.is_int(node_port)):
                node_port = Py_version_manager.py_input("Enter the Node Port: ")
            nodes_assigned_to_lb.append(
                {"backend_name": node_list_dict[node_choice]["name"],
                 "backend_ip": node_list_dict[node_choice]["private_ip_address"], 
                 "backend_port": node_port})
            want_to_go_further = Py_version_manager.py_input("Enter y/n to add more nodes: ")
        return nodes_assigned_to_lb

    def classic_lb_creation(self, api_key, auth_token, nodes_assigned_to_lb, plan_assigned_to_lb):
        Py_version_manager.py_print("(Note: All the fields having a important ahead of them can't be skipped)")
        name_assigned_to_lb = Py_version_manager.py_input("Name of your lb(important): ")
        while(name_assigned_to_lb=="" or " " in name_assigned_to_lb):
            name_assigned_to_lb = Py_version_manager.py_input("Name of your lb(important): ") 
        Py_version_manager.py_print("Load Balancing Property: ")
        lb_balancing_property = {"1": "source",
                                 "2": "roundrobin"}
        Py_version_manager.py_print("1. Source IP Hash")
        Py_version_manager.py_print("2. Round Robin")
        lb_balancing_property_choice = Py_version_manager.py_input(": ")
        while(not lb_balancing_property_choice in lb_balancing_property):
            lb_balancing_property_choice = Py_version_manager.py_input("Please select from given choices only: ")
        balancing_property_assigned_to_lb = lb_balancing_property[lb_balancing_property_choice]

        nodes_assigned_to_lb = self.assign_nodes(nodes_assigned_to_lb, api_key, auth_token)
        payload = json.dumps({
            "acl_list": [],
            "acl_map": [],
            "backends": [
                {
                    "balance": balancing_property_assigned_to_lb,
                    "check_url": "/",
                    "domain_name": "localhost",
                    "http_check": False,
                    "servers": nodes_assigned_to_lb
                }
            ],
            "enable_bitninja": False,
            "host_target": "",
            "lb_mode": "HTTP",
            "lb_name": name_assigned_to_lb,
            "lb_port": 80,
            "lb_reserve_ip": "",
            "lb_type": "External",
            "node_list_type": "S",
            "plan_name": plan_assigned_to_lb,
            "scaler_id": "",
            "scaler_port": "",
            "ssl_certificate_id": "",
            "ssl_context": {
                "redirect_to_https": False
            },
            "vpc_list": []
        })
        return payload

    def acl_condition_path(self):
        table = PrettyTable(["ID", "Conditions"])
        table.add_row(["1", "Exact Match"])
        table.add_row(["2", "Prefix Match"])
        table.add_row(["3", "Suffix Match"])
        table.add_row(["4", "Regex Match"])
        table.add_row(["5", "Exact Match(Case-Sensitive)"])
        table.add_row(["6", "Prefix Match(Case-Sensitive)"])
        table.add_row(["7", "Suffix Match(Case-Sensitive)"])
        table.add_row(["8", "Regex Match(Case-Sensitive)"])

        Py_version_manager.py_print(table)
        acl_conditions = []
        acl_condition_choice = Py_version_manager.py_input(": ")
        if acl_condition_choice == "1":
            acl_conditions.append("path -i")
        elif acl_condition_choice == "2":
            acl_conditions.append("path_beg -i")
        elif acl_condition_choice == "3":
            acl_conditions.append("path_end -i")
        elif acl_condition_choice == "4":
            acl_conditions.append("path_reg -i")
        elif acl_condition_choice == "5":
            acl_conditions.append("path")
        elif acl_condition_choice == "6":
            acl_conditions.append("path_beg")
        elif acl_condition_choice == "7":
            acl_conditions.append("path_end")
        elif acl_condition_choice == "8":
            acl_conditions.append("path_reg")
        else:
            self.acl_condition_path()
        path = Py_version_manager.py_input("Enter the value to be matched for previous option : ")
        val_choice = Py_version_manager.py_input("Want to enter more values for the key(y/n): ")
        while val_choice.lower() == 'y':
            path = path + " " + Py_version_manager.py_input("Enter value")
            val_choice = Py_version_manager.py_input("Want to enter more values for the key(y/n): ")
        acl_conditions.append(path)
        return acl_conditions

    def acl_condition_host(self):
        table = PrettyTable(["ID", "Conditions"])
        table.add_row(["1", "Exact Match"])
        table.add_row(["2", "Prefix Match"])
        table.add_row(["3", "Suffix Match"])
        table.add_row(["4", "Regex Match"])

        Py_version_manager.py_print(table)
        acl_condition_choice = Py_version_manager.py_input(": ")
        acl_conditions = []
        if acl_condition_choice == "1":
            acl_conditions.append("hdr(host) -i")
        elif acl_condition_choice == "2":
            acl_conditions.append("hdr_beg(host) -i")
        elif acl_condition_choice == "3":
            acl_conditions.append("hdr_end(host) -i")
        elif acl_condition_choice == "4":
            acl_conditions.append("hdr_reg(host) -i")
        else:
            self.acl_condition_host()
        path = Py_version_manager.py_input("Enter value: ")
        val_choice = Py_version_manager.py_input("Want to enter more values for the key(y/n): ")
        while val_choice.lower() == 'y':
            path = path + " " + Py_version_manager.py_input("Enter value")
            val_choice = Py_version_manager.py_input("Want to enter more values for the key(y/n): ")
        acl_conditions.append(path)
        return acl_conditions

    def acl_condition_qpm(self):
        table = PrettyTable(["ID", "Conditions"])
        table.add_row(["1", "Exact Match"])
        table.add_row(["2", "Prefix Match"])
        table.add_row(["3", "Suffix Match"])
        table.add_row(["4", "Regex Match"])
        table.add_row(["5", "Exact Match(Case-Sensitive)"])
        table.add_row(["6", "Prefix Match(Case-Sensitive)"])
        table.add_row(["7", "Suffix Match(Case-Sensitive)"])
        table.add_row(["8", "Regex Match(Case-Sensitive)"])

        Py_version_manager.py_print(table)
        acl_conditions = []
        acl_condition_choice = Py_version_manager.py_input(": ")
        if acl_condition_choice == "1":
            key = Py_version_manager.py_input("Key: ")
            acl_conditions.append("urlp(" + key + ") -i")
        elif acl_condition_choice == "2":
            key = Py_version_manager.py_input("Key: ")
            acl_conditions.append("urlp_beg(" + key + ") -i")
        elif acl_condition_choice == "3":
            key = Py_version_manager.py_input("Key: ")
            acl_conditions.append("urlp_end(" + key + ") -i")
        elif acl_condition_choice == "4":
            key = Py_version_manager.py_input("Key: ")
            acl_conditions.append("urlp_reg(" + key + ")")
        elif acl_condition_choice == "5":
            key = Py_version_manager.py_input("Key: ")
            acl_conditions.append("urlp(" + key + ")")
        elif acl_condition_choice == "6":
            key = Py_version_manager.py_input("Key: ")
            acl_conditions.append("urlp_beg(" + key + ")")
        elif acl_condition_choice == "7":
            key = Py_version_manager.py_input("Key: ")
            acl_conditions.append("urlp_end(" + key + ")")
        elif acl_condition_choice == "8":
            key = Py_version_manager.py_input("Key: ")
            acl_conditions.append("urlp_reg(" + key + ")")
        else:
            self.acl_condition_qpm()
        path = Py_version_manager.py_input("Enter value: ")
        val_choice = Py_version_manager.py_input("Want to enter more values for the key(y/n): ")
        while val_choice.lower() == 'y':
            path = path + " " + Py_version_manager.py_input("Enter value")
            val_choice = Py_version_manager.py_input("Want to enter more values for the key(y/n): ")
        acl_conditions.append(path)
        return acl_conditions

    def acl_condition_http(self):
        table = PrettyTable(["ID", "METHODS"])
        table.add_row(["1", "HEAD"])
        table.add_row(["2", "OPTIONS"])
        table.add_row(["3", "GET"])
        table.add_row(["4", "POST"])
        table.add_row(["5", "PUT"])
        table.add_row(["6", "DELETE"])
        table.add_row(["7", "CONNECT"])
        table.add_row(["8", "TRACE"])

        Py_version_manager.py_print(table)
        acl_conditions = []
        acl_conditions.append("method")
        acl_condition_choice = Py_version_manager.py_input(": ")
        if acl_condition_choice == "1":
            acl_conditions.append("HEAD")
        elif acl_condition_choice == "2":
            acl_conditions.append("OPTIONS")
        elif acl_condition_choice == "3":
            acl_conditions.append("GET")
        elif acl_condition_choice == "4":
            acl_conditions.append("POST")
        elif acl_condition_choice == "5":
            acl_conditions.append("PUT")
        elif acl_condition_choice == "6":
            acl_conditions.append("DELETE")
        elif acl_condition_choice == "7":
            acl_conditions.append("CONNECT")
        elif acl_condition_choice == "8":
            acl_conditions.append("TRACE")
        else: 
            self.acl_condition_http()
        return acl_conditions

    def acl_condition_sip(self):
        acl_conditions = ["src"]
        path = Py_version_manager.py_input("Enter Source IP: ")
        while(path=="" or " "in path):
            path = Py_version_manager.py_input("Enter a valid Source IP: ")
        val_choice = Py_version_manager.py_input("Want to enter more values for the key(y/n): ")
        while val_choice.lower() == 'y':
            path = path + " " + Py_version_manager.py_input("Enter value")
            val_choice = Py_version_manager.py_input("Want to enter more values for the key(y/n): ")
        acl_conditions.append(path)
        return acl_conditions

    def set_acl_rules(self, rule_count):
        Py_version_manager.py_print(" ACL Rules")
        acl_instance = dict()
        acl_instance["acl_name"] = "rule-" + str(rule_count)
        Py_version_manager.py_print("Name     " + acl_instance["acl_name"])
        Py_version_manager.py_print("Condition ")
        table = PrettyTable(["ID", "CONDITIONS"])
        table.add_row(["1", "PATH BASED"])
        table.add_row(["2", "HOST BASED"])
        table.add_row(["3", "QUERY PARAMETERS BASED"])
        table.add_row(["4", "HTTP METHODS BASED"])
        table.add_row(["5", "SOURCE IP BASED"])

        Py_version_manager.py_print(table)
        condition_choice = Py_version_manager.py_input(": ")
        if condition_choice == "1":
            condition_acl_list = self.acl_condition_path()
            acl_instance["acl_condition"] = condition_acl_list[0]
            acl_instance["acl_matching_path"] = condition_acl_list[1]
        elif condition_choice == "2":
            condition_acl_list = self.acl_condition_host()
            acl_instance["acl_condition"] = condition_acl_list[0]
            acl_instance["acl_matching_path"] = condition_acl_list[1]
        elif condition_choice == "3":
            condition_acl_list = self.acl_condition_qpm()
            acl_instance["acl_condition"] = condition_acl_list[0]
            acl_instance["acl_matching_path"] = condition_acl_list[1]
        elif condition_choice == "4":
            condition_acl_list = self.acl_condition_http()
            acl_instance["acl_condition"] = condition_acl_list[0]
            acl_instance["acl_matching_path"] = condition_acl_list[1]
        elif condition_choice == "5":
            condition_acl_list = self.acl_condition_sip()
            acl_instance["acl_condition"] = condition_acl_list[0]
            acl_instance["acl_matching_path"] = condition_acl_list[1]
        else:
            Py_version_manager.py_print("please select out of the given choices only")
            self.set_acl_rules(rule_count)
        return acl_instance

    def acl_rules(self, acl_rules_assigned):
        rule_count = 1
        acl_rules_assigned.append(self.set_acl_rules(rule_count))
        add_more_rules = Py_version_manager.py_input("Want to add more rules(y/n): ")
        while add_more_rules.lower() == 'y':
            rule_count += 1
            acl_rules_assigned.append(self.set_acl_rules(rule_count))
            add_more_rules = Py_version_manager.py_input("Want to add more rules(y/n): ")
        return acl_rules_assigned

    def backends(self, api_key, auth_token, backends_assigned_to_lb, nodes_assigned_to_backend):
        Py_version_manager.py_print("Load Balancing Property: ")
        lb_balancing_property = {"1": "source",
                                 "2": "roundrobin"}
        Py_version_manager.py_print("1. Source IP Hash")
        Py_version_manager.py_print("2. Round Robin")
        prev_len = len(backends_assigned_to_lb)
        lb_balancing_property_choice = Py_version_manager.py_input(": ")
        backends_assigned_to_lb.append({"balance": lb_balancing_property[lb_balancing_property_choice],
                                        "check_url": "/",
                                        "checkbox_enable": "null",
                                        "domain_name": "localhost",
                                        "http_check": "false",
                                        "name": "backend-server-" + str(prev_len + 1),
                                        "servers": self.assign_nodes(nodes_assigned_to_backend,
                                                                     api_key, auth_token)
                                        })
        return backends_assigned_to_lb

    def create_rules_objects(self, acl_rules):
        rules_object_list = []
        rules_object = {}
        for acl_rule_index in range(0, len(acl_rules)):
            rules_object["rule"] = "rule-" + str(acl_rule_index + 1)
            acl_rule_type = acl_rules[acl_rule_index]["acl_condition"]
            condition = ""
            match_type = ""
            if "path" in acl_rule_type:
                condition = "Path"
                if "beg" in acl_rule_type:
                    if "-i" in acl_rule_type:
                        match_type = "Prefix Match"
                    else:
                        match_type = "Prefix Match(Case-Sensitive)"
                elif "end" in acl_rule_type:
                    if "-i" in acl_rule_type:
                        match_type = "Suffix Match"
                    else:
                        match_type = "Suffix Match(Case-Sensitive)"
                elif "reg" in acl_rule_type:
                    if "-i" in acl_rule_type:
                        match_type = "Regex Match"
                    else:
                        match_type = "Regex Match(Case-Sensitive)"
                else:
                    if "-i" in acl_rule_type:
                        match_type = "Exact Match"
                    else:
                        match_type = "Exact Match(Case-Sensitive)"

            elif "hdr" in acl_rule_type:
                condition = "Host"
                if "beg" in acl_rule_type:
                    match_type = "Prefix Match"
                elif "end" in acl_rule_type:
                    match_type = "Suffix Match"
                elif "reg" in acl_rule_type:
                    match_type = "Regex Match"
                else:
                    match_type = "Exact Match"

            elif "urlp" in acl_rule_type:
                condition = "Query Parameters Matching"
                if "beg" in acl_rule_type:
                    if "-i" in acl_rule_type:
                        match_type = "Prefix Match"
                    else:
                        match_type = "Prefix Match(Case-Sensitive)"
                elif "end" in acl_rule_type:
                    if "-i" in acl_rule_type:
                        match_type = "Suffix Match"
                    else:
                        match_type = "Suffix Match(Case-Sensitive)"
                elif "reg" in acl_rule_type:
                    if "-i" in acl_rule_type:
                        match_type = "Regex Match"
                    else:
                        match_type = "Regex Match(Case-Sensitive)"
                else:
                    if "-i" in acl_rule_type:
                        match_type = "Exact Match"
                    else:
                        match_type = "Exact Match(Case-Sensitive)"

            elif "method" in acl_rule_type:
                condition = "HTTP Methods"

            else:
                condition = "Source IP"

            rules_object["rule_type"] = condition + " " + match_type
            rules_object_list.append(rules_object)
        return rules_object_list

    def set_backends(self, backend_server_list, backends_assigned_to_rule):
        table = PrettyTable(["Backend Server ID", "Backend Server"])
        for backend_instance in backend_server_list:
            if backend_instance["backend_name"] in backends_assigned_to_rule:
                pass
            else:
                table.add_row([backend_instance["backend_id"], backend_instance["backend_name"]])
        if table.rowcount == 0:
            return "/"
        Py_version_manager.py_print(table)
        backend_choice = Py_version_manager.py_input(": ")
        return backend_choice

    def select_rules(self, acl_rules):
        Py_version_manager.py_print("Choose a rule ")
        rules_object_list = self.create_rules_objects(acl_rules)
        table = PrettyTable(["ID", "ACL RULE", "ACL RULE TYPE"])
        rule_id = 1
        for rule_instance in rules_object_list:
            table.add_row([rule_id, rule_instance["rule"], rule_instance["rule_type"]])
            rule_id += 1
        Py_version_manager.py_print(table)
        rule_choice = Py_version_manager.py_input(": ")
        return rules_object_list[int(rule_choice) - 1]["rule"]

    def acl_maps(self, acl_maps_list, acl_rules, backends):
        your_rule_choice = self.select_rules(acl_rules)
        backend_server_list = []
        rules_to_backends = dict()
        rules_to_backends[your_rule_choice] = []
        for backend_index in range(0, len(backends)):
            backend_server_list.append(
                {"backend_id": str(backend_index + 1),
                 "backend_name": "backend-server-" + str(backend_index + 1)
                 }
            )
        backend_choice = self.set_backends(backend_server_list, rules_to_backends[your_rule_choice])
        condition_state_choice = Py_version_manager.py_input("Enter ACL Condition State(T/F): ")
        if condition_state_choice.lower() == 't':
            condition_state_choice = "true"
        else:
            condition_state_choice = "false"
        rules_to_backends[your_rule_choice].append(backend_server_list[int(backend_choice) - 1]["backend_name"])
        acl_maps_list.append({"acl_backend": backend_server_list[int(backend_choice) - 1]["backend_name"],
                              "acl_condition_state": condition_state_choice,
                              "acl_name": your_rule_choice})
        add_more_choice = Py_version_manager.py_input("Want to add more(y/n): ")
        while add_more_choice.lower() == 'y':
            your_rule_choice = self.select_rules(acl_rules)
            backend_server_list = []
            for backend_index in range(0, len(backends)):
                backend_server_list.append(
                    {"backend_id": str(backend_index + 1),
                     "backend_name": "backend-server-" + str(backend_index + 1)
                     }
                )
            backend_choice = self.set_backends(backend_server_list, rules_to_backends[your_rule_choice])
            if backend_choice == '/':
                break
            condition_state_choice = Py_version_manager.py_input("Enter ACL Condition State(T/F): ")
            if condition_state_choice.lower() == 't':
                condition_state_choice = "true"
            else:
                condition_state_choice = "false"
            rules_to_backends[your_rule_choice].append(backend_server_list[int(backend_choice) - 1]["backend_name"])
            acl_maps_list.append({"acl_backend": backend_server_list[int(backend_choice) - 1]["backend_name"],
                                  "acl_condition_state": condition_state_choice,
                                  "acl_name": your_rule_choice})
            add_more_choice = Py_version_manager.py_input("Want to add more(y/n): ")
        return acl_maps_list

    def advance_lb_creation(self, api_key, auth_token, acl_rules_assigned_to_lb, acl_maps_to_backends,
                            backends_assigned_to_lb, plan_assigned_to_lb):
        Py_version_manager.py_print("(Note: All the fields having a important ahead of them can't be skipped)")
        name_assigned_to_lb = Py_version_manager.py_input("Name of your lb(important): ")
        while(name_assigned_to_lb=="" or " " in name_assigned_to_lb):
            name_assigned_to_lb = Py_version_manager.py_input("Name of your lb(important): ") 
        Py_version_manager.py_print("Load Balancing Property: ")
        acl_rules_assigned_to_lb = self.acl_rules(acl_rules_assigned_to_lb)
        if not backends_assigned_to_lb:
            backends_assigned_to_lb = self.backends(api_key, auth_token, backends_assigned_to_lb, [])
            add_more_backend = Py_version_manager.py_input("Want to add more backend(y/n): ")
            while add_more_backend.lower() == 'y':
                backends_assigned_to_lb = self.backends(api_key, auth_token, backends_assigned_to_lb, [])
                add_more_backend = Py_version_manager.py_input("Want to add more backend(y/n): ")
        else:
            Py_version_manager.py_print("Choose Backend you want to edit")
            table = PrettyTable(["Backend Server"])
            for backend_instance in backends_assigned_to_lb:
                table.add_row(backend_instance["name"])
            Py_version_manager.py_print(table)
            backend_choice = Py_version_manager.py_input(": ")
            backends_assigned_to_lb = self.backends(api_key, auth_token, backends_assigned_to_lb,
                                                    backends_assigned_to_lb[int(backend_choice)]["servers"])
        acl_maps_to_backends = self.acl_maps(acl_maps_to_backends, acl_rules_assigned_to_lb, backends_assigned_to_lb)
        payloads = {
            "acl_list": acl_rules_assigned_to_lb,
            "acl_map": acl_maps_to_backends,
            "backends": backends_assigned_to_lb,
            "checkbox_enable": "",
            "default_backend": "",
            "enable_bitninja": "false",
            "lb_mode": "HTTP",
            "lb_name": name_assigned_to_lb,
            "lb_port": "80",
            "lb_reserve_ip": "",
            "lb_type": "External",
            "node_list_type": "S",
            "plan_name": plan_assigned_to_lb,
            "ssl_certificate_id": "",
            "ssl_context": {"redirect_to_https": "false"},
            "vpc_list": []
        }
        return json.dumps(payloads)

    def all_lb(self):
        api_key_credentials_object = self.alias_service_object.get_api_credentials()
        if api_key_credentials_object["message"] == "Invalid alias provided":
            return api_key_credentials_object
        else:
            url =  BASE_URL+"myaccount/api/v1/appliances/?location=Delhi&apikey=" + \
                  api_key_credentials_object["api_credentials"]["api_key"]
            payload = {}
            method = "GET"
            response_object = Request(req=method, url=url, 
                Auth_Token=api_key_credentials_object["api_credentials"]["api_auth_token"],
                payload=payload)
            return {"lb_api_response": response_object.response.json(),
                    "message": api_key_credentials_object["message"]}

    def get_lb_by_id(self, lb_id):
        if(Checks.is_int(lb_id)):
            lb_list = self.all_lb()["lb_api_response"]["data"]
            found_dict = next((d for d in lb_list if d['id'] == int(lb_id)), None)
        else:
            found_dict=None
        return found_dict

    def add_lb(self):
        api_key_credentials_object = self.alias_service_object.get_api_credentials()
        if api_key_credentials_object["message"] == "Invalid alias provided":
            return api_key_credentials_object
        else:
            Py_version_manager.py_print("Fill in the details required")
            Py_version_manager.py_print("Choose the type of Load Balancer you want to use: ")
            Py_version_manager.py_print("1. Classic Load Balancer")
            Py_version_manager.py_print("2. Advanced Load Balancer")
            choice_of_lb = Py_version_manager.py_input(": ")
            while (not Checks.is_int(choice_of_lb) or not 0<int(choice_of_lb)<=2):
                Py_version_manager.py_print("please select out of the given choices only")
                choice_of_lb = Py_version_manager.py_input(": ")
            choice_of_lb=int(choice_of_lb)
            lb_plans = [
                {
                    "ID": 1,
                    "Plan": "E2E-LB-1",
                    "Specs": "2 vCPU 3 GB RAM 10GB SSD",
                    "Price": "Rs1 /hour or  Rs730 /mo"
                },
                {
                    "ID": 2,
                    "Plan": "E2E-LB-2",
                    "Specs": "4 vCPU 6 GB RAM 10GB SSD",
                    "Price": "Rs2 /hour or  Rs1460 /mo"
                },
                {
                    "ID": 3,
                    "Plan": "E2E-LB-3",
                    "Specs": "8 vCPU 12 GB RAM 10GB SSD",
                    "Price": "Rs4 /hour or  Rs2920 /mo"
                },
                {
                    "ID": 4,
                    "Plan": "E2E-LB-4",
                    "Specs": "12 vCPU 24 GB RAM 10GB SSD",
                    "Price": " Rs8 /hour or  Rs5840 /mo"
                },
                {
                    "ID": 5,
                    "Plan": "E2E-LB-5",
                    "Specs": "24 vCPU 48 GB RAM 10GB SSD",
                    "Price": " Rs16 /hour or  Rs11680 /mo"
                }
            ]
            Py_version_manager.py_print("Plans for load-balancers")
            table = PrettyTable(["ID", "Plan", "Specs", "Price"])
            for plan_instance in lb_plans:
                table.add_row([plan_instance["ID"], plan_instance["Plan"],
                               plan_instance["Specs"], plan_instance["Price"]])
            Py_version_manager.py_print(table)
            plan_choice = Py_version_manager.py_input(": ")
            while (not Checks.is_int(plan_choice) or not 0<int(plan_choice)<=len(lb_plans)):
                Py_version_manager.py_print("please select out of the given choices only")
                plan_choice = Py_version_manager.py_input(": ")
            plan_choice=int(plan_choice)
            plan_assigned_to_lb = lb_plans[plan_choice-1]["Plan"]
            if int(choice_of_lb) == 1:
                payload = self.classic_lb_creation(api_key_credentials_object["api_credentials"]["api_key"],
                                                   api_key_credentials_object["api_credentials"]["api_auth_token"], [],
                                                   plan_assigned_to_lb)
                url =  BASE_URL+"myaccount/api/v1/appliances/load-balancers/" \
                      "?apikey=" + api_key_credentials_object["api_credentials"]["api_key"]
                response_object = Request(req="POST", url=url, 
                Auth_Token=api_key_credentials_object["api_credentials"]["api_auth_token"],
                payload=payload)
                return {"lb_api_response": response_object.response.json(),
                        "message": api_key_credentials_object["message"]}
            elif int(choice_of_lb) == 2:
                payload = self.advance_lb_creation(api_key_credentials_object["api_credentials"]["api_key"],
                                                   api_key_credentials_object["api_credentials"]["api_auth_token"], [],
                                                   [], [], plan_assigned_to_lb)
                url =  BASE_URL+"myaccount/api/v1/appliances/load-balancers/" \
                      "?apikey=" + api_key_credentials_object["api_credentials"]["api_key"]
                response_object = Request(req="POST", url=url, 
                Auth_Token=api_key_credentials_object["api_credentials"]["api_auth_token"],
                payload=payload)
                return {"lb_api_response": response_object.response.json(),
                        "message": api_key_credentials_object["message"]}

    def delete_lb_sevice(self):
        lb_id = Py_version_manager.py_input("Enter the id of the lb: ")
        all_lb_in_list = self.get_lb_by_id(lb_id)
        while (all_lb_in_list is None or not Checks.is_int(lb_id)):
            Py_version_manager.py_print("Please choose a valid load-balancer id: ")
            lb_id = Py_version_manager.py_input("Enter the id of the lb: ")
            all_lb_in_list = self.get_lb_by_id(lb_id)
        Py_version_manager.py_print("Deleting this lb instance can cause loss!")
        choice = Py_version_manager.py_input("Do you still want to continue?(Y/N)")
        if choice.upper() == "Y":
            api_key_credentials_object = self.alias_service_object.get_api_credentials()
            if api_key_credentials_object["message"] == "Invalid alias provided":
                return api_key_credentials_object
            else:

                url =  BASE_URL+"myaccount/api/v1/appliances/" + lb_id + "/?apikey=" + \
                      api_key_credentials_object["api_credentials"]["api_key"]

                payload = {}
                response_object = Request(req="DELETE", url=url, 
                Auth_Token=api_key_credentials_object["api_credentials"]["api_auth_token"],
                payload=payload)
                return {"lb_api_response": response_object.response.json(),
                        "message": api_key_credentials_object["message"]}
        else:
            return {"message": "Aborted"}

    def change_lb_name(self):
        lb_name = Py_version_manager.py_input(" Enter Load-Balancer Name: ")
        payload = {"name": lb_name,
                   "type": "rename"}

        return json.dumps(payload)

    def select_backend(self, backend_assigned):
        table = PrettyTable(["Backend ID", "Backend Name"])
        for backend_index in range(0, len(backend_assigned)):
            table.add_row([str(backend_index + 1), "backend-server-" + str(backend_index + 1)])
        Py_version_manager.py_print(table)
        backend_choice = Py_version_manager.py_input(": ")
        return backend_choice

    def select_node(self, nodes_assigned):
        table = PrettyTable(["Node ID", "Node Name"])
        for node_index in range(0, len(nodes_assigned)):
            table.add_row([str(node_index + 1), nodes_assigned[node_index]["backend_name"]])
        Py_version_manager.py_print(table)
        node_choice = Py_version_manager.py_input(": ")
        return node_choice

    def change_port_node(self, appliances):
        appliances_assigned = appliances[0]
        backend_assigned = appliances_assigned["context"]["backends"]
        backend_choice = self.select_backend(backend_assigned)
        nodes_assigned = backend_assigned[int(backend_choice) - 1]["servers"]
        Py_version_manager.py_print(" ")
        node_choice = self.select_node(nodes_assigned)
        node_port = Py_version_manager.py_input(" Node Port: ")
        nodes_assigned[int(node_choice) - 1]["backend_port"] = node_port
        change_choice = Py_version_manager.py_input("Want to change more(y/n): ")
        while change_choice.lower() == 'y':
            backend_assigned = appliances_assigned["context"]["backends"]
            backend_choice = self.select_backend(backend_assigned)
            nodes_assigned = backend_assigned[int(backend_choice) - 1]["servers"]
            Py_version_manager.py_print(" ")
            node_choice = self.select_node(nodes_assigned)
            node_port = Py_version_manager.py_input(" Node Port: ")
            nodes_assigned[int(node_choice) - 1]["backend_port"] = node_port
            change_choice = Py_version_manager.py_input("Want to change more(y/n): ")
        payloads = {
            "acl_list": appliances_assigned["context"]["acl_list"],
            "acl_map": appliances_assigned["context"]["acl_map"],
            "backends": backend_assigned,
            "checkbox_enable": "",
            "default_backend": "",
            "enable_bitninja": "false",
            "lb_mode": appliances_assigned["context"]["lb_mode"],
            "lb_name": appliances_assigned["context"]["lb_name"],
            "lb_port": appliances_assigned["context"]["lb_port"],
            "lb_reserve_ip": appliances_assigned["context"]["lb_reserve_ip"],
            "lb_type": appliances_assigned["context"]["lb_type"],
            "node_list_type": appliances_assigned["context"]["node_list_type"],
            "plan_name": appliances_assigned["context"]["plan_name"],
            "ssl_certificate_id": appliances_assigned["context"]["ssl_context"]["ssl_certificate_id"],
            "ssl_context": {"redirect_to_https": appliances_assigned["context"]["ssl_context"]["redirect_to_https"]},
            "vpc_list": appliances_assigned["context"]["vpc_list"]
        }
        return json.dumps(payloads)

    def add_new_node(self, appliances, api_credentials_object):
        appliances_assigned = appliances[0]
        backend_assigned = appliances_assigned["context"]["backends"]
        backend_choice = self.select_backend(backend_assigned)
        nodes_assigned = backend_assigned[int(backend_choice) - 1]["servers"]
        Py_version_manager.py_print(" ")
        nodes_assigned = self.assign_nodes(nodes_assigned, api_credentials_object["api_credentials"]["api_key"],
                                           api_credentials_object["api_credentials"]["api_auth_token"])
        change_choice = Py_version_manager.py_input("Want to change more(y/n): ")
        while change_choice.lower() == 'y':
            backend_assigned = appliances_assigned["context"]["backends"]
            backend_choice = self.select_backend(backend_assigned)
            nodes_assigned = backend_assigned[int(backend_choice) - 1]["servers"]
            Py_version_manager.py_print(" ")
            nodes_assigned = self.assign_nodes(nodes_assigned, api_credentials_object["api_credentials"]["api_key"],
                                               api_credentials_object["api_credentials"]["api_auth_token"])
            change_choice = Py_version_manager.py_input("Want to change more(y/n): ")
        payloads = {
            "acl_list": appliances_assigned["context"]["acl_list"],
            "acl_map": appliances_assigned["context"]["acl_map"],
            "backends": backend_assigned,
            "checkbox_enable": "",
            "default_backend": "",
            "enable_bitninja": "false",
            "lb_mode": appliances_assigned["context"]["lb_mode"],
            "lb_name": appliances_assigned["context"]["lb_name"],
            "lb_port": appliances_assigned["context"]["lb_port"],
            "lb_reserve_ip": appliances_assigned["context"]["lb_reserve_ip"],
            "lb_type": appliances_assigned["context"]["lb_type"],
            "node_list_type": appliances_assigned["context"]["node_list_type"],
            "plan_name": appliances_assigned["context"]["plan_name"],
            "ssl_certificate_id": appliances_assigned["context"]["ssl_context"]["ssl_certificate_id"],
            "ssl_context": {"redirect_to_https": appliances_assigned["context"]["ssl_context"]["redirect_to_https"]},
            "vpc_list": appliances_assigned["context"]["vpc_list"]
        }
        return json.dumps(payloads)

    def edit_lb(self):
        api_key_credentials_object = self.alias_service_object.get_api_credentials()
        if api_key_credentials_object["message"] == "Invalid alias provided":
            return api_key_credentials_object
        else:
            lb_id = Py_version_manager.py_input("Enter the id of the lb: ")
            all_lb_in_list = self.get_lb_by_id(lb_id)
            while(all_lb_in_list is None):
                Py_version_manager.py_print("Please choose a valid load-balancer id: ")
                lb_id = Py_version_manager.py_input("Enter the id of the lb: ")
                all_lb_in_list = self.get_lb_by_id(lb_id)
            Py_version_manager.py_print("  Please Make a Choice ")
            Py_version_manager.py_print("1.  Change LoadBalancer Name")
            Py_version_manager.py_print("2.  Change a Port of a Node")
            Py_version_manager.py_print("3.  Add a new Port")
            edit_choice = Py_version_manager.py_input(": ")
            if edit_choice == str(1):
                json_payload = self.change_lb_name()
                url =  BASE_URL+"myaccount/api/v1/appliances/load-balancers/" + \
                      lb_id + "/actions/?apikey=" + api_key_credentials_object["api_credentials"]["api_key"]
                response_obj = Request(req="PUT", url=url, 
                Auth_Token=api_key_credentials_object["api_credentials"]["api_auth_token"],
                payload=json_payload)
                return {"lb_api_response": response_obj.response.json(),
                        "message": api_key_credentials_object["message"]}
            elif edit_choice == str(2):
                json_payload = self.change_port_node(all_lb_in_list["appliance_instance"])
                url =  BASE_URL+"myaccount/api/v1/appliances/load-balancers/" + \
                      lb_id + "/?apikey=" + api_key_credentials_object["api_credentials"]["api_key"]
                response_obj = Request(req="PUT", url=url, 
                Auth_Token=api_key_credentials_object["api_credentials"]["api_auth_token"],
                payload=json_payload)
                return {"lb_api_response": response_obj.response,
                        "message": api_key_credentials_object["message"]}

            elif edit_choice == str(3):
                json_payload = self.add_new_node(all_lb_in_list["appliance_instance"], api_key_credentials_object)
                url =  BASE_URL+"myaccount/api/v1/appliances/load-balancers/" + \
                      lb_id + "/?apikey=" + api_key_credentials_object["api_credentials"]["api_key"]
                response_obj = Request(req="PUT", url=url, 
                Auth_Token=api_key_credentials_object["api_credentials"]["api_auth_token"],
                payload=json_payload)
                return {"lb_api_response": response_obj.response.json(),
                        "message": api_key_credentials_object["message"]}

            else:
                return { "code" : "" ,"message": "Failure"}