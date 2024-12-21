import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
import socket
import struct

# Класс для представления функционального блока
class FunctionalBlock:
    def __init__(self, name):
        self.name = name
        self.inputs = {}
        self.outputs = {}
        self.connections = []

    def add_input(self, input_name, value=None):
        self.inputs[input_name] = value

    def add_output(self, output_name, value=None):
        self.outputs[output_name] = value

    def connect(self, output_name, target_block, input_name):
        self.connections.append((output_name, target_block, input_name))

    def process(self):
        # Простой пример обработки: передача значения из входа на выход
        for input_name, value in self.inputs.items():
            if value is not None:
                for output_name in self.outputs:
                    self.outputs[output_name] = value
                    for conn in self.connections:
                        if conn[0] == output_name:
                            conn[1].inputs[conn[2]] = value

# Класс для представления ресурса
class Resource:
    def __init__(self, name):
        self.name = name
        self.functional_blocks = {}

    def add_functional_block(self, block):
        self.functional_blocks[block.name] = block

    def process_all(self):
        for block in self.functional_blocks.values():
            block.process()

# Функция для загрузки проекта из XML-файла
def load_project(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    resource = Resource(root.attrib['name'])

    for block_elem in root.findall('functional_block'):
        block = FunctionalBlock(block_elem.attrib['name'])
        for input_elem in block_elem.findall('input'):
            block.add_input(input_elem.attrib['name'], input_elem.attrib.get('value'))
        for output_elem in block_elem.findall('output'):
            block.add_output(output_elem.attrib['name'])
        resource.add_functional_block(block)

    for conn_elem in root.findall('connection'):
        source_block = resource.functional_blocks[conn_elem.attrib['source_block']]
        target_block = resource.functional_blocks[conn_elem.attrib['target_block']]
        source_block.connect(conn_elem.attrib['source_output'], target_block, conn_elem.attrib['target_input'])

    return resource

# Функция для отображения графа связей функциональных блоков
def display_graph(resource):
    graph = nx.DiGraph()

    for block in resource.functional_blocks.values():
        graph.add_node(block.name)
        for conn in block.connections:
            graph.add_edge(block.name, conn[1].name, label=f"{conn[0]} -> {conn[2]}")

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=15, font_weight="bold")
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')

    # Сохранение графика в файл
    plt.savefig("graph.png")
    print("Граф сохранен в файл graph.png")

    # Отображение графика
    plt.show(block=True)

# Функция для отправки команды и получения ответа
def send_command(host, port, resource_name, command_xml):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Формирование заголовка
        resource_name_len = len(resource_name)
        command_xml_len = len(command_xml)
        header = struct.pack('!B H', 0x50, resource_name_len) + resource_name.encode() + struct.pack('!B H', 0x50, command_xml_len)

        # Отправка заголовка и команды
        s.sendall(header + command_xml.encode())

        # Получение ответа
        response_header = s.recv(3)
        response_len = struct.unpack('!H', response_header[1:3])[0]
        response_xml = s.recv(response_len).decode()

        return response_xml

# Функция для загрузки проекта в среду исполнения по TCP
def load_project_to_execution(resource, host, port):
    for block in resource.functional_blocks.values():
        for input_name, value in block.inputs.items():
            command_xml = f'<Request ID="1" Action="SET"><{block.name}.{input_name}>{value}</{block.name}.{input_name}></Request>'
            response = send_command(host, port, resource.name, command_xml)
            print(f"Response: {response}")

        for output_name in block.outputs:
            command_xml = f'<Request ID="2" Action="GET"><{block.name}.{output_name}></{block.name}.{output_name}></Request>'
            response = send_command(host, port, resource.name, command_xml)
            print(f"Response: {response}")

# Функция для чтения значений переменных по TCP
def read_variables(host, port, resource_name):
    command_xml = '<Request ID="3" Action="READ_ALL"></Request>'
    response = send_command(host, port, resource_name, command_xml)
    print(f"Response: {response}")

# Пример использования
if __name__ == "__main__":
    # Загрузка проекта из XML-файла
    resource = load_project("app.sys")

    # Отображение графа связей функциональных блоков
    display_graph(resource)

    # Загрузка проекта в среду исполнения по TCP
    load_project_to_execution(resource, "localhost", 12345)

    # Чтение значений переменных по TCP
    read_variables("localhost", 12345, resource.name)