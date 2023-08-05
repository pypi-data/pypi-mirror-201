import oyaml as yaml


class MyDumper(yaml.Dumper):

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def dump(data, stream=None):
    yaml.dump(data, stream, allow_unicode=True,
              Dumper=MyDumper, default_flow_style=False)
