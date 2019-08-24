import subprocess


class Kobe(object):
    k8s_objects = [
        "pods",
        "ingress",
        "secret",
        "certificate",
        "statefulset",
    ]

    action_list = [
        "get",
        "describe",
        "edit",
        "exec"
    ]

    package_classify_mapping = {
        "db": ["mongodb", "mysql", ""],
        "cockroach-p": ["cockroach"],
        "cms": ["wordpress", "megento"]
    }

    @property
    def package_type(self):
        return self.stack_name.split("-")[0]

    @property
    def agent_container_name(self):
        return "%s-%s" % (self.package_type, "agent")

    @property
    def pod_name(self):
        return "{namespace}-{classify}-0".format(namespace=self.stack_name, classify=self.package_classify)

    @property
    def package_classify(self):
        print(self.package_classify_mapping, self.package_type)
        for classify, package_types in self.package_classify_mapping.items():
            if self.package_type in package_types:
                return classify
        return None

    def __init__(self, stack_name, action, input):
        self.stack_name = stack_name
        self.action = action
        self.input = input
        self._check()

    def _check(self):
        if not self.package_classify:
            raise Exception("%s 不是一个正确的产品名，如果你确定是一个上线的产品，请联系ethan解决")

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
            choice = input("请输入你要执行命令的序号:")
            command = mapping.get(int(choice))
            subprocess.call(command, shell=True)


kobe = Kobe(stack_name="mysql-1233", action="all", input=1)
kobe.show()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("stack_name", help="stack name")
#     parser.add_argument("-a", "--action", choices=['all', 'get', "describe", "edit", "exec"])
#     parser.add_argument("-s", "--show", help="0 just show ，1 carry out", default=1)
#     args = parser.parse_args()
#     print(args.action)
#     kobe = Kobe(stack_name=args.stack_name, action=args.action, show=show)
