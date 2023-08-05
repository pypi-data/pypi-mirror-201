import copy
import os
from os import PathLike
from collections import OrderedDict
from typing import List
from xml.etree.ElementTree import Element, ElementTree


class Object:
    def __init__(self, object_element: Element) -> None:
        self.object_element = object_element
        self.tag = object_element.tag
        self.id = object_element.get('id')

    def __str__(self) -> str:
        return f'Object: tag={self.tag}, id={self.id}'

    def set_fill_color(self, color: str) -> str:
        style = self.object_element.attrib['style']
        style_dict = OrderedDict(item.split(':') for item in style.split(';'))
        style_dict['fill'] = color
        self.object_element.attrib['style'] = ';'.join([f'{key}:{value}' for key, value in style_dict.items()])


class Layer:

    def __init__(self, layer_element: Element, parent_layer_path: str):
        self.layer_element: Element = layer_element
        self.layer_name: str = layer_element.get('{http://www.inkscape.org/namespaces/inkscape}label')
        self.layer_path: str = f'/{self.layer_name}' if parent_layer_path == '/' else '/'.join([parent_layer_path, self.layer_name])
        self.layers: OrderedDict[str, Layer] = self.parse_layers()
        self.objects: OrderedDict[str, Object] = self.parse_objects()

    def __str__(self):
        return f'Layer: name={self.layer_name}'

    def parse_layers(self) -> OrderedDict[str, 'Layer']:
        layer_dict: OrderedDict[str, Layer] = OrderedDict()

        for layer_element in self.layer_element.findall('{http://www.w3.org/2000/svg}g'):
            layer = Layer(layer_element, self.layer_path)
            layer_dict[layer.layer_name] = layer

        return layer_dict

    def parse_objects(self) -> OrderedDict[str, Object]:
        object_dict: OrderedDict[str, Object] = OrderedDict()

        for element in self.layer_element:
            if not element.tag == '{http://www.w3.org/2000/svg}g':
                object = Object(element)
                object_dict[object.id] = object

        return object_dict

    def print_structure(self, level=1):
        for object in self.objects.values():
            print(f'{" " * level * 2}{object}')
        for layer in self.layers.values():
            print(f'{" " * level * 2}{layer}')
            layer.print_structure(level+1)

    def find_first_layer_by_name(self, layer_name: str) -> 'Layer':
        expected_layer = self.layers.get(layer_name)

        if expected_layer is not None:
            return expected_layer
        else:
            for layer in self.layers.values():
                expected_layer = layer.find_first_layer_by_name(layer_name)
                if expected_layer:
                    return expected_layer

    def get_layer_by_path(self, path: str):
        if path == '/':
            return self
        else:
            layer_names = path[1:].split('/')
            current_layer = self
            for layer_name in layer_names:
                current_layer = current_layer.layers[layer_name]
                if current_layer is None:
                    break
            return current_layer

    def get_all_layer_paths(self) -> List[str]:
        # return get_all_layer_paths(self)
        layer_paths: List[str] = [self.layer_path]
        for layer in self.layers.values():
            layer_paths.extend(layer.get_all_layer_paths())
        return layer_paths

    def fill_all_objects(self, color: str) -> str:
        for object in self.objects.values():
            object.set_fill_color(color)


class Image(Layer):

    def __init__(self, element_tree: ElementTree) -> None:
        self.element_tree: ElementTree = element_tree
        self.layer_element: Element = self.element_tree.getroot()
        self.layer_name: str = '/'
        self.layer_path: str = '/'
        self.layers: OrderedDict[str, Layer] = self.parse_layers()
        self.objects: OrderedDict[str, Object] = self.parse_objects()

    def extract_layer(self, path: str) -> 'Image':
        if path == '/':
            return copy.deepcopy(self)
        else:
            return self.extract_layers([path])

    def extract_layers(self, paths: List[str]) -> 'Image':
        new_image = copy.deepcopy(self)

        layers_to_extract: List[Layer] = []
        for path in paths:
            layers_to_extract.append(copy.deepcopy(new_image.get_layer_by_path(path)))

        for layer in new_image.layers.values():
            new_image.layer_element.remove(layer.layer_element)
        new_image.layers.clear()

        for layer_to_extract in layers_to_extract:
            new_image.layers[layer_to_extract.layer_name] = layer_to_extract
            new_image.layer_element.append(layer_to_extract.layer_element)
        return new_image

    def tear_apart(self) -> dict[str, 'Image']:
        layer_path_list = self.get_all_layer_paths()
        return dict((layer_path, self.extract_layer(layer_path)) for layer_path in layer_path_list)

    def tear_apart_to_file(self, output_dir: PathLike, base_name: str) -> None:
        extracted_images = self.tear_apart()
        for layer_path, extracted_image in extracted_images.items():
            if layer_path == '/':
                extracted_image.save(os.path.join(output_dir, f'{base_name}.svg'))
            else:
                extracted_image.save(os.path.join(output_dir, f'{base_name}{layer_path.replace("/", "_")}.svg'))

    def save(self, path: PathLike) -> None:
        self.element_tree.write(path)
