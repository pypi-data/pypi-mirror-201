import itertools
from pathlib import Path
from typing import Dict, Any, Set, List, Tuple
import json
import subprocess
from abc import ABC, abstractmethod

from EVMVerifier.Compiler.CompilerCollector import CompilerCollector, CompilerLang
from Shared.certoraUtils import Singleton
from Shared.certoraUtils import print_failed_to_run


class CompilerLangVy(CompilerLang, metaclass=Singleton):
    """
    [CompilerLang] for Vyper.
    """
    _compiler_name: str = "vyper"

    @property
    def name(self) -> str:
        return "Vyper"

    @property
    def compiler_name(self) -> str:
        return self._compiler_name

    @staticmethod
    def normalize_func_hash(func_hash: str) -> str:
        try:
            return hex(int(func_hash, 16))
        except ValueError:
            raise Exception(f'{func_hash} is not convertible to hexadecimal')

    @staticmethod
    def normalize_file_compiler_path_name(file_abs_path: str) -> str:
        if not file_abs_path.startswith('/'):
            return '/' + file_abs_path
        return file_abs_path

    @staticmethod
    def normalize_deployed_bytecode(deployed_bytecode: str) -> str:
        assert deployed_bytecode.startswith("0x"), f'expected {deployed_bytecode} to have hexadecimal prefix'
        return deployed_bytecode[2:]

    @staticmethod
    def get_contract_def_node_ref(contract_file_ast: Dict[int, Any], contract_file: str, contract_name: str) -> \
            int:
        # in vyper, "ContractDefinition" is "Module"
        denormalized_contract_file = contract_file[1:] if contract_file.startswith('/') else contract_file
        contract_def_refs = list(filter(
            lambda node_id: contract_file_ast[node_id].get("ast_type") == "Module" and
            (contract_file_ast[node_id].get("name") == contract_file, contract_file_ast) or
            contract_file_ast[node_id].get("name") == denormalized_contract_file, contract_file_ast))
        assert len(contract_def_refs) != 0, \
            f'Failed to find a "Module" ast node id for the file {contract_file}'
        assert len(contract_def_refs) == 1, f'Found multiple "Module" ast node ids for the same file' \
            f'{contract_file}: {contract_def_refs}'
        return contract_def_refs[0]

    @staticmethod
    def compilation_output_path(sdc_name: str, config_path: Path) -> Path:
        return config_path / f"{sdc_name}"

    # Todo - add this for Vyper too and make it a CompilerLang class method one day
    @staticmethod
    def compilation_error_path(sdc_name: str, config_path: Path) -> Path:
        return config_path / f"{sdc_name}.standard.json.stderr"

    @staticmethod
    def all_compilation_artifacts(sdc_name: str, config_path: Path) -> Set[Path]:
        """
        Returns the set of paths for all files generated after compilation.
        """
        return {CompilerLangVy.compilation_output_path(sdc_name, config_path),
                CompilerLangVy.compilation_error_path(sdc_name, config_path)}

    class VyperType(ABC):
        uniqueId: int = 0

        @classmethod
        def get_unique_id(cls) -> int:
            r = cls.uniqueId
            cls.uniqueId += 1
            return r

        @abstractmethod
        def size_in_bytes(self) -> int:
            pass

        @abstractmethod
        def generate_types_field(self) -> Dict[str, Any]:
            pass

        @abstractmethod
        def get_canonical_vyper_name(self) -> str:
            pass

        @abstractmethod
        def get_used_types(self) -> List[Any]:
            pass

        def resolve_forward_declared_types(self, resolution_dict: Dict[str, Any]) -> Any:
            return self

    class VyperTypeNameReference(VyperType):
        def __init__(self, name: str):
            self.name = name

        def size_in_bytes(self) -> int:
            raise NotImplementedError

        def generate_types_field(self) -> Dict[str, Any]:
            raise NotImplementedError

        def get_canonical_vyper_name(self) -> str:
            return self.name

        def get_used_types(self) -> List[Any]:
            raise NotImplementedError

        def resolve_forward_declared_types(self, resolution_dict: Dict[str, Any]) -> Any:
            if self.name in resolution_dict:
                return resolution_dict[self.name]
            return self

    class VyperTypeStaticArray(VyperType):
        def __init__(self, element_type: Any, max_num_elements: int):
            self.element_type = element_type
            self.max_num_elements = max_num_elements

        def size_in_bytes(self) -> int:
            return self.element_type.size_in_bytes() * self.max_num_elements

        def generate_types_field(self) -> Dict[str, Any]:
            return {
                'label': self.element_type.get_canonical_vyper_name() + '[' + str(self.max_num_elements) + ']',
                'encoding': 'inplace',
                'base': self.element_type.get_canonical_vyper_name(),
                'numberOfBytes': str(self.size_in_bytes())
            }

        def get_canonical_vyper_name(self) -> str:
            return self.element_type.get_canonical_vyper_name() + '[' + str(self.max_num_elements) + ']'

        def resolve_forward_declared_types(self, resolution_dict: Dict[str, Any]) -> Any:
            self.element_type = self.element_type.resolve_forward_declared_types(resolution_dict)
            return self

        def get_used_types(self) -> List[Any]:
            return [self] + [self.element_type]

    class VyperTypeDynArray(VyperType):
        def __init__(self, element_type: Any, max_num_elements: int):
            self.array_type = CompilerLangVy.VyperTypeStaticArray(element_type, int(max_num_elements))
            self.id = self.get_unique_id()

        def size_in_bytes(self) -> int:
            return self.array_type.size_in_bytes() + 32

        def generate_types_field(self) -> Dict[str, Any]:
            return {
                'label': self.get_canonical_vyper_name(),
                'encoding': 'inplace',
                'members': [
                    {
                        'label': 'count',
                        'offset': 0,
                        'slot': '0',
                        'type': 'uint256'
                    },
                    {
                        'label': 'data',
                        'offset': 0,
                        'slot': '1',
                        'type': self.array_type.get_canonical_vyper_name()
                    }
                ],
                'numberOfBytes': str(self.size_in_bytes())
            }

        def get_canonical_vyper_name(self) -> str:
            return 'DynArray[' + self.array_type.element_type.get_canonical_vyper_name() + ', ' \
                + str(self.array_type.max_num_elements) + ']'

        def resolve_forward_declared_types(self, resolution_dict: Dict[str, Any]) -> Any:
            self.array_type = self.array_type.resolve_forward_declared_types(resolution_dict)
            return self

        def get_used_types(self) -> List[Any]:
            return [self] + self.array_type.get_used_types()

    class VyperTypeString(VyperTypeDynArray):
        def __init__(self, max_num_elements: int):
            super().__init__(CompilerLangVy.primitive_types['uint8'], max_num_elements)

        def get_canonical_vyper_name(self) -> str:
            return 'String[' + str(self.array_type.max_num_elements) + ']'

        def resolve_forward_declared_types(self, resolution_dict: Dict[str, Any]) -> Any:
            return self

    class VyperTypeHashMap(VyperType):
        def __init__(self, key_type: Any, value_type: Any):
            self.key_type = key_type
            self.value_type = value_type

        def size_in_bytes(self) -> int:
            return 32

        def generate_types_field(self) -> Dict[str, Any]:
            return {
                'label': self.get_canonical_vyper_name(),
                'encoding': 'mapping',
                'key': self.key_type.get_canonical_vyper_name(),
                'value': self.value_type.get_canonical_vyper_name(),
                'numberOfBytes': '32'
            }

        def get_canonical_vyper_name(self) -> str:
            return 'HashMap[' + self.key_type.get_canonical_vyper_name() + ', ' + \
                self.value_type.get_canonical_vyper_name() + ']'

        def resolve_forward_declared_types(self, resolution_dict: Dict[str, Any]) -> Any:
            self.key_type = self.key_type.resolve_forward_declared_types(resolution_dict)
            self.value_type = self.value_type.resolve_forward_declared_types(resolution_dict)
            return self

        def get_used_types(self) -> List[Any]:
            return [self] + [self.key_type] + [self.value_type]

    class VyperTypeStruct(VyperType):
        def __init__(self, name: str, fields: List[Tuple[str, Any]]):
            self.name = name
            self.fields = fields
            self.id = self.get_unique_id()

        def size_in_bytes(self) -> int:
            return sum([f[1].size_in_bytes() for f in self.fields])

        def generate_types_field(self) -> Dict[str, Any]:
            bytes_so_far_rounded_up = 0
            slots = {}
            for n, t in self.fields:
                slots.update({n: bytes_so_far_rounded_up // 32})
                bytes_so_far_rounded_up += (t.size_in_bytes() + 31) & ~31
            members_field = [
                {
                    'label': n,
                    'slot': str(slots[n]),
                    'offset': 0,
                    'type': t.get_canonical_vyper_name()
                }
                for (n, t) in self.fields]
            return {
                'label': self.get_canonical_vyper_name(),
                'encoding': 'inplace',
                'members': members_field,
                'numberOfBytes': str(self.size_in_bytes())
            }

        def get_canonical_vyper_name(self) -> str:
            return self.name

        def resolve_forward_declared_types(self, resolution_dict: Dict[str, Any]) -> Any:
            self.fields = [(f[0], f[1].resolve_forward_declared_types(resolution_dict)) for f in self.fields]
            return self

        def get_used_types(self) -> List[Any]:
            return [self] + list(itertools.chain.from_iterable([t.get_used_types() for _, t in self.fields]))

    class VyperTypePrimitive(VyperType):
        def __init__(self, name: str, size: int):
            self.name = name
            self.size = size

        def size_in_bytes(self) -> int:
            return self.size

        def generate_types_field(self) -> Dict[str, Any]:
            return {
                'label': self.get_canonical_vyper_name(),
                'encoding': 'inplace',
                'numberOfBytes': str(self.size_in_bytes())
            }

        def get_canonical_vyper_name(self) -> str:
            return self.name

        def get_used_types(self) -> List[Any]:
            return [self]

    primitive_types = {
        'address': VyperTypePrimitive('address', 32),
        'bool': VyperTypePrimitive('bool', 1),
        'byte': VyperTypePrimitive('byte', 1),
        'decimal': VyperTypePrimitive('decimal', 32),
        'int8': VyperTypePrimitive('int8', 1),
        'int16': VyperTypePrimitive('int16', 2),
        'int32': VyperTypePrimitive('int32', 4),
        'int64': VyperTypePrimitive('int64', 8),
        'int128': VyperTypePrimitive('int128', 16),
        'int256': VyperTypePrimitive('int256', 32),
        'uint8': VyperTypePrimitive('uint8', 1),
        'uint16': VyperTypePrimitive('uint16', 2),
        'uint32': VyperTypePrimitive('uint32', 4),
        'uint64': VyperTypePrimitive('uint64', 8),
        'uint128': VyperTypePrimitive('uint128', 16),
        'uint256': VyperTypePrimitive('uint256', 32),
        'nonreentrant lock': VyperTypePrimitive('nonreentrant lock', 32),
        'ERC20': VyperTypePrimitive('ERC20', 32),
        'ERC721': VyperTypePrimitive('ERC721', 32),
        'bytes4': VyperTypePrimitive('bytes4', 32 + 4),
        'bytes8': VyperTypePrimitive('bytes8', 32 + 8),
        'bytes16': VyperTypePrimitive('bytes16', 32 + 16),
        'bytes32': VyperTypePrimitive('bytes32', 32 + 32)
    }

    @staticmethod
    def collect_storage_layout_info(file_abs_path: str,
                                    config_path: Path,
                                    compiler_cmd: str,
                                    data: Dict[str, Any]) -> Dict[str, Any]:
        def extract_type_from_subscript_node(ast_subscript_node: Dict[str, Any],
                                             named_constants: Dict[str, int]) -> CompilerLangVy.VyperType:
            value_id = ast_subscript_node['value']['id']
            if value_id == 'String':
                max_bytes = ast_subscript_node['slice']['value']['value']
                return CompilerLangVy.VyperTypeString(max_bytes)
            elif value_id == 'DynArray':
                elem_type = extract_type_from_type_annotation_node(ast_subscript_node['slice']['value']['elements'][0],
                                                                   named_constants)
                max_elements = ast_subscript_node['slice']['value']['elements'][1]['value']
                if max_elements in named_constants:
                    return CompilerLangVy.VyperTypeDynArray(elem_type, named_constants[max_elements])
                else:
                    return CompilerLangVy.VyperTypeDynArray(elem_type, max_elements)
            elif value_id == 'HashMap':
                elements_node = ast_subscript_node['slice']['value']['elements']
                key_type = extract_type_from_type_annotation_node(elements_node[0], named_constants)
                value_type = extract_type_from_type_annotation_node(elements_node[1], named_constants)
                return CompilerLangVy.VyperTypeHashMap(key_type, value_type)
            else:  # StaticArray
                key_type = CompilerLangVy.primitive_types[value_id] if value_id in CompilerLangVy.primitive_types \
                    else extract_type_from_type_annotation_node(value_id, named_constants)
                max_elements_node = ast_subscript_node['slice']['value']
                if 'id' in max_elements_node and max_elements_node['id'] in named_constants:
                    return CompilerLangVy.VyperTypeStaticArray(key_type, named_constants[max_elements_node['id']])
                else:
                    return CompilerLangVy.VyperTypeStaticArray(key_type, max_elements_node['value'])

        def extract_type_from_type_annotation_node(ast_type_annotation: Dict[str, Any],
                                                   named_constants: Dict[str, int]) -> CompilerLangVy.VyperType:
            if ast_type_annotation['ast_type'] == 'Subscript':
                return extract_type_from_subscript_node(ast_type_annotation, named_constants)
            elif ast_type_annotation['id'] in CompilerLangVy.primitive_types:
                return CompilerLangVy.primitive_types[ast_type_annotation['id']]
            elif 'value' in ast_type_annotation:
                value_id = ast_type_annotation['value']['id']
                return CompilerLangVy.VyperTypeNameReference(value_id)
            else:
                return CompilerLangVy.VyperTypeNameReference(ast_type_annotation['id'])

        def extract_type_from_variable_decl(ast_vardecl_node: Dict[str, Any],
                                            named_constants: Dict[str, int]) -> CompilerLangVy.VyperType:
            return extract_type_from_type_annotation_node(ast_vardecl_node['annotation'], named_constants)

        def extract_type_from_struct_def(ast_structdef_node: Dict[str, Any],
                                         named_constants: Dict[str, int]) -> CompilerLangVy.VyperType:
            fields = [(n['target']['id'], extract_type_from_type_annotation_node(n['annotation'], named_constants))
                      for n in ast_structdef_node['body']]
            return CompilerLangVy.VyperTypeStruct(ast_structdef_node['name'], fields)

        def resolve_extracted_types(extracted_types: List[CompilerLangVy.VyperType]) -> List[CompilerLangVy.VyperType]:
            real_types = [t for t in extracted_types if not isinstance(t, CompilerLangVy.VyperTypeNameReference)]
            name_resolution_dict = {t.get_canonical_vyper_name(): t for t in real_types}
            return [t.resolve_forward_declared_types(name_resolution_dict) for t in real_types]

        def extract_ast_types(ast_body_nodes: List[Dict[str, Any]]) -> List[CompilerLangVy.VyperType]:
            result = []
            named_constants: Dict[str, int] = {}
            for ast_node in ast_body_nodes:
                if ast_node['ast_type'] == 'VariableDecl':
                    result.append(extract_type_from_variable_decl(ast_node, named_constants))
                    if ast_node['is_constant'] and (ast_node['value'] is not None) and \
                            (ast_node['value']['ast_type'] == 'Int'):
                        named_constants.update({ast_node['target']['id']: int(ast_node['value']['value'])})
                elif ast_node['ast_type'] == 'StructDef':
                    result.append(extract_type_from_struct_def(ast_node, named_constants))
            return result

        storage_layout_output_file_name = f'{config_path}.storage.layout'
        storage_layout_stdout_name = storage_layout_output_file_name + '.stdout'
        storage_layout_stderr_name = storage_layout_output_file_name + '.stderr'
        args = [compiler_cmd, '-f', 'layout', '-o', storage_layout_output_file_name, file_abs_path]
        with Path(storage_layout_stdout_name).open('w+') as stdout:
            with Path(storage_layout_stderr_name).open('w+') as stderr:
                try:
                    subprocess.run(args, stdout=stdout, stderr=stderr)
                    with Path(storage_layout_output_file_name).open('r') as output_file:
                        storage_layout_dict = json.load(output_file)
                except Exception as e:
                    print(f'Error: {e}')
                    print_failed_to_run(compiler_cmd)
                    raise
        ast_output_file_name = f'{config_path}.ast'
        ast_stdout_name = storage_layout_output_file_name + '.stdout'
        ast_stderr_name = storage_layout_output_file_name + '.stderr'
        args = [compiler_cmd, '-f', 'ast', '-o', ast_output_file_name, file_abs_path]
        with Path(ast_stdout_name).open('w+') as stdout:
            with Path(ast_stderr_name).open('w+') as stderr:
                try:
                    subprocess.run(args, stdout=stdout, stderr=stderr)
                    with Path(ast_output_file_name).open('r') as output_file:
                        ast_dict = json.load(output_file)
                except Exception as e:
                    print(f'Error: {e}')
                    print_failed_to_run(compiler_cmd)
                    raise

        extracted_types = extract_ast_types(ast_dict['ast']['body'])
        resolved_types = resolve_extracted_types(extracted_types)
        all_used_types = list(itertools.chain.from_iterable([e.get_used_types() for e in resolved_types])) + \
            list(CompilerLangVy.primitive_types.values())
        types_field = {i.get_canonical_vyper_name(): i.generate_types_field() for i in all_used_types}
        storage_field = [{
            'label': v,
            'slot': str(storage_layout_dict['storage_layout'][v]['slot']),
            'offset': 0,
            'type': storage_layout_dict['storage_layout'][v]['type']
        } for v in storage_layout_dict['storage_layout'].keys()]

        contract_name = list(data['contracts'][file_abs_path].keys())[0]
        data['contracts'][file_abs_path][contract_name]['storageLayout'] = {
            'storage': storage_field,
            'types': types_field,
            'storageHashArgsReversed': True
        }
        data['contracts'][file_abs_path][contract_name]['storageHashArgsReversed'] = True
        return data

    @staticmethod
    def get_supports_imports() -> bool:
        return False


class CompilerCollectorVy(CompilerCollector):

    @property
    def compiler_name(self) -> str:
        return self.smart_contract_lang.compiler_name

    @property
    def smart_contract_lang(self) -> CompilerLangVy:
        return CompilerLangVy()

    @property
    def compiler_version(self) -> str:
        return "vyper"  # TODO implement to return a valid version
