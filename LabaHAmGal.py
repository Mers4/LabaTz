class Resource:
    def __init__(self, name):
        self.name = name
        self.functional_blocks = []

    def add_functional_block(self, fb):
        self.functional_blocks.append(fb)

class FunctionalBlock:
    def __init__(self, name):
        self.name = name
        self.inputs = {}
        self.outputs = {}

    def set_input(self, input_name, value):
        self.inputs[input_name] = value

    def get_output(self, output_name):
        return self.outputs.get(output_name)

class Graph:
    def __init__(self):
        self.resources = {}
        self.functional_blocks = {}

    def add_resource(self, resource):
        self.resources[resource.name] = resource

    def add_functional_block(self, fb):
        self.functional_blocks[fb.name] = fb

class EventProcessor:
    def __init__(self, graph):
        self.graph = graph

    def process_event(self, event):
        # Логика обработки событий в графе
        pass

class FbootLoader:
    def load_configuration(self, file_path):
        # Логика загрузки конфигурации из fboot файла
        pass

class InputOutputViewer:
    def __init__(self, graph):
        self.graph = graph

    def view_inputs_outputs(self, fb_name):
        fb = self.graph.functional_blocks.get(fb_name)
        if fb:
            return fb.inputs, fb.outputs
        return None, None

class IEC61499Parser:
    def parse_command(self, command):
        # Логика парсинга команд в формате IEC 61499
        pass

class FourDiacProtocolHandler:
    def __init__(self, parser):
        self.parser = parser

    def handle_command(self, command):
        parsed_command = self.parser.parse_command(command)
        # Логика обработки команды
        pass

# Пример использования
resource = Resource("Resource1")
fb1 = FunctionalBlock("FB1")
fb2 = FunctionalBlock("FB2")

resource.add_functional_block(fb1)
resource.add_functional_block(fb2)

graph = Graph()
graph.add_resource(resource)
graph.add_functional_block(fb1)
graph.add_functional_block(fb2)

event_processor = EventProcessor(graph)
fboot_loader = FbootLoader()
io_viewer = InputOutputViewer(graph)
parser = IEC61499Parser()
protocol_handler = FourDiacProtocolHandler(parser)

# Пример команды
command = "CREATE_RESOURCE Resource2"
protocol_handler.handle_command(command)