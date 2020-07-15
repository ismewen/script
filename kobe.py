import argparse
import subprocess

from config import container_name_template_config


class Kobe(object):
    k8s_objects = [
        "pods",
        "ingress",
        "secrets",
        "certificate",
        "statefulset",
        "pv",
        "pvc",
    ]

    action_list = [
        "get",
        "exec",
        "describe",
        "edit",
    ]

    package_classify_mapping = {
        "db": ["mongodb", "mysql", "mariadb", "postgresql"],
        "cockroach-p": ["cockroach"],
        "cms": ["wordpress", "magento", "drupal", "opencart"]
    }

    @property
    def package_type(self):
        package_type = self.stack_name.split("-")[0]
        if package_type == "cockroachdb":
            package_type = "cockroach"
        return package_type

    @property
    def agent_container_name(self):
        return "%s-%s" % (self.package_type, "agent")

    @property
    def pod_name(self):
        return "{namespace}-{classify}-0".format(namespace=self.stack_name, classify=self.package_classify)

    @property
    def package_classify(self):
        for classify, package_types in self.package_classify_mapping.items():
            if self.package_type in package_types:
                return classify
        return None

    def __init__(self, stack_name, action, input):
        self.stack_name = stack_name.lower()
        self.action = action
        self.input = input
        self._check()

    def _check(self):
        if not self.package_classify:
            raise Exception("%s not a valid package classification,please contact ethan to fix this")

    def get_commands(self):
        actions = self.action_list if self.action == "all" else [self.action]
        commands = []
        for action in actions:
            if self.is_exec_action(action):
                commands.extend(self.show_exec_action_commands(action))
            elif self.is_specific_action(action):
                commands.extend(self.show_specific_action_commands(action))
            else:
                commands.extend(self.show_normal_action_commands(action))
        return commands

    @classmethod
    def is_specific_action(self, action):
        return action in ["edit", "describe"]

    @classmethod
    def is_exec_action(cls, action):
        return action == "exec"

    def show_specific_action_commands(self, action):
        template = "kubectl {action} {k8s_object}/{name} -n {namespace}"

        return [template.format(action=action,
                                k8s_object=k8s_object,
                                namespace=self.stack_name,
                                name="name" if k8s_object != "pods" else self.pod_name
                                ) for k8s_object in
                self.k8s_objects]

    def show_exec_action_commands(self, action):
        commands = []
        template = "kubectl exec -it {pod_name} -c {container_name} -n {namespace} bash"
        command = template.format(pod_name=self.pod_name, container_name=self.agent_container_name,
                                  namespace=self.stack_name)
        commands.append(command)
        template = "kubectl exec -it {pod_name} -n {namespace} bash"
        command = template.format(pod_name=self.pod_name, namespace=self.stack_name)
        commands.append(command)
        return commands

    def show_normal_action_commands(self, action):
        template = "kubectl {action} {k8s_object} -n {namespace}"
        return [template.format(action=action, k8s_object=k8s_object, namespace=self.stack_name) for k8s_object in
                self.k8s_objects]

    def show(self):
        commands = self.get_commands()
        mapping = {index: value for index, value in enumerate(commands)}
        for index, value in mapping.items():
            print("%s:%s" % (index, value))
        if self.input:
            choice = input("please input your choice:")
            choice = choice.strip()
            if choice == "exit":
                return
            if choice.startswith("kubectl"):
                subprocess.call(choice)
            else:
                command = mapping.get(int(choice))
                s


class JorDan(object):
    k8s_objects = [
        "pods",
        "ingress",
        "secrets",
        "certificate",
        "statefulset",
    ]

    action_list = [
        "get",
        "exec",
        "describe",
        "edit",
    ]

    def __init__(self, namespace):
        self.namespace = namespace

    def get_container_def_info(self):
        app_name = self.namespace.split("-")[0]
        template = container_name_template_config.get(app_name)
        return {x: y.format(self.namespace) for x, y in template.items()}

    @property
    def agent_name(self):
        return self.get_container_def_info().get("agent_name")

    @property
    def app_name(self):
        return self.get_container_def_info().get("app_name")

    @property
    def sts_name(self):
        return self.get_container_def_info().get("sts_name")

    @property
    def pod_name(self):
        return self.get_container_def_info().get("pod_name")

    def commands(self):
        commands = [
            "kubectl get pods -n %s" % self.namespace,
            "kubectl get ingress -n %s" % self.namespace,
            "kubectl get secrets -n %s" % self.namespace,
            "kubectl get sts -n %s" % self.namespace,
            "kubectl exec -it {pod_name} -c {container_name} -n {namespace}".format(
                pod_name=self.pod_name, container_name=self.app_name, namespace=self.namespace),
            "kubectl exec -it {pod_name} -c {container_name} -n {namespace}".format(
                pod_name=self.pod_name, container_name=self.agent_name, namespace=self.namespace),
            "kubectl describe sts/{sts_name} -n {namespace}".format(sts_name=self.sts_name, namespace=self.namespace),
            "kubectl describe pods/{pod_name} -n {namespace}".format(pod_name=self.pod_name, namespace=self.namespace),
            "kubectl edit sts/{sts_name} -n {namespace}".format(sts_name=self.sts_name, namespace=self.namespace),
            "kubectl edit pods/{pod_name} -n {namespace}".format(pod_name=self.pod_name, namespace=self.namespace),
        ]
        commands_mapping = {str(index): value for index, value in enumerate(commands)}
        for index, command in commands_mapping.items():
            print("%s:%s" % (index, command))
        choice = input("please input your choice:")
        command = commands_mapping.get(str(choice))
        if not command:
            raise Exception("Invalid Choice")
        subprocess.call(command, shell=True)


if __name__ == "__main__":
    ethan = "handsome"
    parser = argparse.ArgumentParser()
    parser.add_argument("namespace", help="stack name")
    # parser.add_argument("-a", "--action", choices=['all', 'get', "describe", "edit", "exec"], default="all")
    # parser.add_argument("-input", "--input", help="", default=1)
    args = parser.parse_args()
    # kobe = Kobe(stack_name=args.namespace, action=args.action, input=args.input)
    # kobe.show()
    jordan = JorDan(args.namespace)
    jordan.commands()