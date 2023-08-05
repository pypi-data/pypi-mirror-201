import argparse
import ast
import logging
import re
import sys
from dataclasses import dataclass, field
from enum import unique, auto
from pathlib import Path
from typing import Optional, Dict, Any, Callable, List

from EVMVerifier import certoraValidateFuncs as Vf
from Shared import certoraUtils as Util

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))


# logger for issues regarding context
context_logger = logging.getLogger("context")


def validate_prover_ext(value: str) -> str:
    strings = value.split()
    for arg in ContextAttribute:
        if arg.value.jar_flag is None:
            continue
        for string in strings:
            if string == arg.value.jar_flag:
                raise argparse.ArgumentTypeError(f"the flag {string} should be set using {arg.get_flag()}"
                                                 "and not by the --prover_ext flag")
    return value


def parse_struct_link(link: str) -> str:
    search_res = re.search(r'^\w+:([^:=]+)=\w+$', link)
    # We do not require firm form of slot number so we can give more informative warnings
    if search_res is None:
        raise argparse.ArgumentTypeError(f"Struct link argument {link} must be of the form contractA:<field>=contractB")
    if search_res[1].isidentifier():
        return link
    try:
        parsed_int = int(search_res[1], 0)  # an integer or a hexadecimal
        if parsed_int < 0:
            raise argparse.ArgumentTypeError(f"struct link slot number negative at {link}")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Struct link argument {link} must be of the form contractA:number=contractB"
                                         f" or contractA:fieldName=contractB")
    return link


def parse_solc_args(list_as_string: str) -> List[str]:
    """
    parse the argument as a list
    """
    if Util.is_new_api():
        type_deprecated(list_as_string, ContextAttribute.SOLC_ARGS)
    v = ast.literal_eval(list_as_string)
    if type(v) is not list:
        raise argparse.ArgumentTypeError(f'--solc_args: "{list_as_string}" is not a list')
    return v


APPEND = 'append'
STORE_TRUE = 'store_true'
STORE_FALSE = 'store_false'
VERSION = 'version'
SINGLE_OR_NONE_OCCURRENCES = '?'
MULTIPLE_OCCURRENCES = '*'
ONE_OR_MORE_OCCURRENCES = '+'


class AttrArgType(Util.NoValEnum):
    STRING = auto()
    BOOLEAN = auto()
    LIST_OF_STRINGS = auto()
    USER_DEFINED = auto()

class ArgStatus(Util.NoValEnum):
    REGULAR = auto()
    NEW = auto()
    DEPRECATED = auto()


class ArgGroups(Util.NoValEnum):
    # The order of the groups is the order we want to show the groups in argParse's help
    MODE = "Mode of operation. Please choose one, unless using a .conf or .tac file"
    USEFUL = "Most frequently used options"
    RUN = "Options affecting the type of verification run"
    SOLIDITY = "Options that control the Solidity compiler"
    LOOP = "Options regarding source code loops"
    HASHING = "Options regarding handling of unbounded hashing"
    RUN_TIME = "Options that help reduce running time"
    LINKAGE = "Options to set addresses and link contracts"
    CREATION = "Options to model contract creation"
    INFO = "Debugging options"
    JAVA = "Arguments passed to the .jar file"
    PARTIAL = "These arguments run only specific parts of the tool, or skip parts"
    CLOUD = "Fine cloud control arguments"
    MISC_HIDDEN = "Miscellaneous hidden arguments"
    ENV = ""


@dataclass
class CertoraArgument:
    flag: Optional[str] = None  # override the 'default': option name
    group: Optional[ArgGroups] = None  # name of the arg parse (see ArgGroups above)
    attr_validation_func: Optional[Callable] = None  # TODO more precise
    arg_status: ArgStatus = ArgStatus.REGULAR
    deprecation_msg: Optional[str] = None
    jar_flag: Optional[str] = None  # the flag that is sent to the jar (if attr is sent to the jar)
    jar_no_value: Optional[bool] = False  # if true, flag is sent with no value
    help_msg: str = argparse.SUPPRESS

    # args for argparse's add_attribute passed as is
    argparse_args: Dict[str, Any] = field(default_factory=dict)
    arg_type: AttrArgType = AttrArgType.STRING

    def get_dest(self) -> Optional[str]:
        return self.argparse_args.get('dest')


class UniqueStore(argparse.Action):
    """
    This class makes the argparser throw an error for a given flag if it was inserted more than once
    """

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: Any,  # type: ignore
                 option_string: str) -> None:
        if getattr(namespace, self.dest, self.default) is not self.default:
            parser.error(f"{option_string} appears several times.")
        setattr(namespace, self.dest, values)


@unique
class ContextAttribute(Util.NoValEnum):
    """
    This enum class must be unique. If 2 args have the same value we add the 'flag' attribute to make sure the hash
    value is not going to be the same

    The order of the attributes is the order we want to show the attributes in argParse's help

    """
    FILES = CertoraArgument(
        attr_validation_func=Vf.validate_input_file,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="[contract.sol[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac",
        flag='files',
        argparse_args={
            'nargs': MULTIPLE_OCCURRENCES
        }
    )

    VERIFY = CertoraArgument(
        group=ArgGroups.MODE,
        attr_validation_func=Vf.validate_verify_attr,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="Matches specification files to contracts. For example: --verify [contractName:specName.spec ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    ASSERT_CONTRACTS_DEPRECATED = CertoraArgument(
        group=ArgGroups.MODE,
        arg_status=ArgStatus.DEPRECATED,
        attr_validation_func=Vf.validate_assert_contract,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        deprecation_msg="--assert is deprecated; use --assert_contracts instead",
        flag='--assert',
        help_msg="The list of contracts to assert. Usage: --assert [contractName ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'dest': 'assert_contracts_deprecated' if Util.is_new_api() else 'assert_contracts',
            'action': APPEND
        }
    )

    ASSERT_CONTRACTS = CertoraArgument(
        group=ArgGroups.MODE,
        arg_status=ArgStatus.NEW,
        attr_validation_func=Vf.validate_assert_contract,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="The list of contracts to assert. Usage: --assert_contracts [contractName ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND,
        }
    )

    BYTECODE_JSONS_DEPRECATED = CertoraArgument(
        group=ArgGroups.MODE,
        arg_status=ArgStatus.DEPRECATED,
        attr_validation_func=Vf.validate_json_file,
        flag='--bytecode',
        deprecation_msg="--bytecode is deprecated; use --bytecode_jsons instead",
        arg_type=AttrArgType.LIST_OF_STRINGS,
        jar_flag='-bytecode',
        help_msg="List of EVM bytecode json descriptors. Usage: --bytecode [bytecode1.json ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'dest': 'bytecode_jsons_deprecated' if Util.is_new_api() else 'bytecode_jsons',
            'action': APPEND
        }
    )
    BYTECODE_JSONS = CertoraArgument(
        group=ArgGroups.MODE,
        arg_status=ArgStatus.NEW,
        attr_validation_func=Vf.validate_json_file,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        jar_flag='-bytecode',
        help_msg="List of EVM bytecode json descriptors. Usage: --bytecode_jsons [bytecode1.json ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    BYTECODE_SPEC = CertoraArgument(
        group=ArgGroups.MODE,
        attr_validation_func=Vf.validate_readable_file,
        jar_flag='-spec',
        help_msg="Spec to use for the provided bytecodes. Usage: --bytecode_spec myspec.spec",
        argparse_args={
            'action': UniqueStore
        }
    )

    MSG = CertoraArgument(
        group=ArgGroups.USEFUL,
        help_msg="Add a message description (alphanumeric string) to your run.",
        argparse_args={
            'action': UniqueStore
        }
    )

    #  RULE option is for both --rule and --rules
    RULE = CertoraArgument(
        group=ArgGroups.USEFUL,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        jar_flag='-rule',
        help_msg="List of specific properties (rules or invariants) you want to verify. "
                 "Usage: --rule [rule1 rule2 ...] or --rules [rule1 rule2 ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    MULTI_ASSERT_CHECK = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        jar_no_value=True,
        jar_flag='-multiAssertCheck',
        help_msg="Check each assertion separately by decomposing every rule "
                 "into multiple sub-rules, each of which checks one assertion while it assumes all "
                 "preceding assertions",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    INCLUDE_EMPTY_FALLBACK = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-includeEmptyFallback',
        help_msg="check the fallback method, even if it always reverts",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    RULE_SANITY = CertoraArgument(
        group=ArgGroups.RUN,
        attr_validation_func=Vf.validate_sanity_value,
        help_msg="Sanity checks for all the rules",
        jar_flag='-ruleSanityChecks',
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'default': None,  # 'default': when no --rule_sanity given, may take from --settings
            'const': Vf.RuleSanityValue.BASIC.name.lower()  # 'default': when empty --rule_sanity is given
        }
    )

    MULTI_EXAMPLE = CertoraArgument(
        group=ArgGroups.RUN,
        attr_validation_func=Vf.validate_multi_example_value,
        help_msg="produce multi-examples",
        jar_flag='-multipleCEX',
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'default': None,  # 'default': when no --multi_example given, may take from --settings
            'const': Vf.MultiExampleValues.BASIC.name.lower()
        }
    )

    SHORT_OUTPUT = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-ciMode',
        help_msg="Reduces verbosity. It is recommended to use this option in continuous integration",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    NO_CALLTRACE_STORAGE_INFORMATION = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-noCalltraceStorageInformation',
        help_msg="Avoid adding storage information to CallTrace report.",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    TYPECHECK_ONLY = CertoraArgument(
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="Stop after typechecking",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    SEND_ONLY = CertoraArgument(   # --send_only also implies --short_output.
        group=ArgGroups.RUN,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="Do not wait for verifications results",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    SOLC = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_exec_file,
        help_msg="Path to the Solidity compiler executable file",
        argparse_args={
            'action': UniqueStore
        }
    )

    SOLC_ARGS = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        arg_status=ArgStatus.DEPRECATED,
        deprecation_msg="--solc_args is deprecated; use --optimize, --via_ir, or --evm_version instead",
        help_msg="List of string arguments to pass for the Solidity compiler, for example: "
                 "\"['--optimize', '--evm-version', 'istanbul', '--via-ir']\"",
        argparse_args={
            'action': UniqueStore,
            'type': parse_solc_args
        }
    )

    VIA_IR = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        arg_status=ArgStatus.NEW,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="instruct the solidity compiler to use intermediate representation instead of EVM opcode",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    EVM_VERSION = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        arg_status=ArgStatus.NEW,
        help_msg="instruct the Solidity compiler to use a specific EVM version",
        argparse_args={
            'action': UniqueStore
        }
    )

    SOLC_MAP = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_solc_map,
        arg_type=AttrArgType.USER_DEFINED,
        help_msg="Matches each Solidity file with a Solidity compiler executable. "
                 "Usage: <sol_file_1>=<solc_1>,<sol_file_2>=<solc_2>[,...] ",
        argparse_args={
            'action': UniqueStore,
            'type': lambda value: Vf.parse_dict('solc_map', value)
        }
    )
    PATH = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        arg_status=ArgStatus.DEPRECATED,
        attr_validation_func=Vf.validate_dir,
        help_msg="Use the given path as the root of the source tree instead of the root of the "
                 "filesystem. Default: $PWD/contracts if exists, else $PWD",
        argparse_args={
            'action': UniqueStore
        }
    )

    SOLC_ALLOW_PATH = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        arg_status=ArgStatus.NEW,
        attr_validation_func=Vf.validate_dir,
        deprecation_msg="--path is deprecated; use --solc_allow_path instead",
        help_msg="Use the given path as the root of the source tree instead of the root of the "
                 "filesystem. Default: $PWD/contracts if exists, else $PWD",
        argparse_args={
            'action': UniqueStore
        }
    )

    OPTIMIZE = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_non_negative_integer,
        help_msg="Tells the Solidity compiler to optimize the gas costs of the contract for a given number of runs."
                 "If the value is not specified the solc default is used",
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'action': UniqueStore,
            'const': -1
        }
    )

    OPTIMIZE_MAP = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_optimize_map,
        arg_type=AttrArgType.USER_DEFINED,
        help_msg="Matches each Solidity source file with a number of runs to optimize for. "
                 "Usage: <sol_file_1>=<num_runs_1>,<sol_file_2>=<num_runs_2>[,...]",
        argparse_args={
            'action': UniqueStore,
            'type': lambda value: Vf.parse_dict('optimize_map', value)
        }
    )

    PACKAGES_PATH = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_dir,
        help_msg="Path to a directory including the Solidity packages ('default':: $NODE_PATH)",
        argparse_args={
            'action': UniqueStore
        }
    )

    PACKAGES = CertoraArgument(
        group=ArgGroups.SOLIDITY,
        attr_validation_func=Vf.validate_packages,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="A mapping [package_name=path, ...]",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    OPTIMISTIC_LOOP = CertoraArgument(
        group=ArgGroups.LOOP,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-assumeUnwindCond',
        jar_no_value=True,
        help_msg="After unrolling loops, assume the loop halt conditions hold",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    LOOP_ITER = CertoraArgument(
        group=ArgGroups.LOOP,
        attr_validation_func=Vf.validate_non_negative_integer,
        jar_flag='-b',
        help_msg="The maximal number of loop iterations we verify for. Default: 1",
        argparse_args={
            'action': UniqueStore
        }
    )

    OPTIMISTIC_HASHING = CertoraArgument(
        group=ArgGroups.HASHING,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="When hashing data of potentially unbounded length, assume that its length is bounded by the "
                 "value set through the `--hashing_length_bound` option. If this is not set, and the length "
                 "can be exceeded by the input program, the prover reports an assertion violation.",
        jar_flag='-optimisticUnboundedHashing',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    HASHING_LENGTH_BOUND = CertoraArgument(
        group=ArgGroups.HASHING,
        attr_validation_func=Vf.validate_non_negative_integer,
        jar_flag='-hashingLengthBound',
        help_msg="Constraint on the maximal length of otherwise unbounded data chunks that are being hashed. "
                 "In bytes. Default: 224, which corresponds to 7 machine words (since 7 * 32 = 224)",
        argparse_args={
            'action': UniqueStore
        }
    )

    METHOD = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        attr_validation_func=Vf.validate_method,
        jar_flag='-method',
        help_msg="Parametric rules will only verify given method. Usage: --method 'fun(uint256,bool)'",
        argparse_args={
            'action': UniqueStore
        }
    )

    CACHE = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        help_msg='name of the cache to use',
        argparse_args={

            'action': UniqueStore
        }
    )

    SMT_TIMEOUT = CertoraArgument(
        group=ArgGroups.RUN_TIME,
        attr_validation_func=Vf.validate_positive_integer,
        jar_flag='-t',
        help_msg="Set max timeout for all SMT solvers in seconds, 'default': is 600",
        argparse_args={
            'action': UniqueStore
        }
    )

    LINK = CertoraArgument(
        group=ArgGroups.LINKAGE,
        attr_validation_func=Vf.validate_link_attr,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="Links a slot in a contract with another contract. Usage: ContractA:slot=ContractB",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    ADDRESS = CertoraArgument(
        group=ArgGroups.LINKAGE,
        attr_validation_func=Vf.validate_address,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="Set a contract's address to be the given address Format: <contractName>:<number>",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    STRUCT_LINK = CertoraArgument(
        group=ArgGroups.LINKAGE,
        attr_validation_func=Vf.validate_struct_link,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        flag=None if Util.is_new_api() else '--structLink',
        help_msg="Linking to a struct field, <contractName>:<number>=<contractName>",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND,
            'dest': None if Util.is_new_api() else 'struct_link'
        }
    )

    PROTOTYPE = CertoraArgument(
        group=ArgGroups.CREATION,
        attr_validation_func=Vf.validate_prototype_attr,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="Execution of constructor bytecode with the given prefix should yield a unique instance of the "
                 "given contract",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    DYNAMIC_BOUND = CertoraArgument(
        group=ArgGroups.CREATION,
        attr_validation_func=Vf.validate_non_negative_integer,
        jar_flag='-dynamicCreationBound',
        help_msg="Maximum number of instances of a contract that can be created "
                 "with the CREATE opcode; if 0, CREATE havocs ('default':: 0)",
        argparse_args={
            'action': UniqueStore
        }
    )

    DYNAMIC_DISPATCH = CertoraArgument(
        group=ArgGroups.CREATION,
        arg_type=AttrArgType.BOOLEAN,
        jar_flag='-dispatchOnCreated',
        help_msg="If set, on a best effort basis automatically use dispatcher summaries for external"
                 " calls on contract instances generated by CREATE",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    DEBUG = CertoraArgument(
        group=ArgGroups.INFO,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="Use this flag to see debug statements",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    SHOW_DEBUG_TOPICS = CertoraArgument(
        group=ArgGroups.INFO,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="Include topic names in debug messages",
        argparse_args={
            'action': STORE_TRUE
        }
    )

    DEBUG_TOPICS = CertoraArgument(
        group=ArgGroups.INFO,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        help_msg="list of logger topics to show when using '--debug'",
        argparse_args={
            'nargs': ONE_OR_MORE_OCCURRENCES,
            'action': APPEND
        }
    )

    VERSION = CertoraArgument(
        group=ArgGroups.INFO,
        arg_type=AttrArgType.BOOLEAN,
        help_msg="Show the tool version",
        argparse_args={
            'action': VERSION,
            'version': 'This message should never be reached'
        }
    )

    JAR = CertoraArgument(
        group=ArgGroups.JAVA,
        attr_validation_func=Vf.validate_jar,
        argparse_args={
            'action': UniqueStore
        }
    )

    JAVA_ARGS_DEPRECATED = CertoraArgument(
        group=ArgGroups.JAVA,
        attr_validation_func=Vf.validate_java_args,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        arg_status=ArgStatus.DEPRECATED,
        deprecation_msg="--javaArgs is deprecated; use --java_args instead",
        flag="--javaArgs",
        argparse_args={
            'action': APPEND,
            'dest': 'javaArgs' if Util.is_new_api() else 'java_args',
            'type': lambda value: type_deprecated(value, ContextAttribute.JAVA_ARGS_DEPRECATED)
        }
    )

    JAVA_ARGS = CertoraArgument(
        group=ArgGroups.JAVA,
        arg_status=ArgStatus.NEW,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        argparse_args={
            'action': APPEND,
        }
    )

    CHECK_ARGS = CertoraArgument(
        group=ArgGroups.PARTIAL,
        arg_type=AttrArgType.BOOLEAN,
        flag='--check_args',  # added to prevent dup with DISABLE_LOCAL_TYPECHECKING
        argparse_args={
            'action': STORE_TRUE
        }
    )

    BUILD_ONLY = CertoraArgument(
        group=ArgGroups.PARTIAL,
        arg_type=AttrArgType.BOOLEAN,
        flag='--build_only',  # added to prevent dup with CHECK_ARGS
        argparse_args={
            'action': STORE_TRUE
        }
    )

    BUILD_DIR = CertoraArgument(
        group=ArgGroups.PARTIAL,
        attr_validation_func=Vf.validate_build_dir,
        help_msg="Path to the build directory",
        argparse_args={
            'action': UniqueStore
        }
    )

    DISABLE_LOCAL_TYPECHECKING = CertoraArgument(
        group=ArgGroups.PARTIAL,
        arg_type=AttrArgType.BOOLEAN,
        flag=None if Util.is_new_api() else '--disableLocalTypeChecking',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    NO_COMPARE = CertoraArgument(
        group=ArgGroups.PARTIAL,
        arg_type=AttrArgType.BOOLEAN,
        flag='--no_compare',  # added to prevent dup with CHECK_ARGS
        argparse_args={
            'action': STORE_TRUE
        }
    )

    EXPECTED_FILE = CertoraArgument(
        group=ArgGroups.PARTIAL,
        attr_validation_func=Vf.validate_optional_readable_file,
        help_msg="JSON file to use as expected results for comparing the output",
        argparse_args={
            'action': UniqueStore
        }
    )

    QUEUE_WAIT_MINUTES = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--queue_wait_minutes',  # added to prevent dup with MAX_POLL_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    MAX_POLL_MINUTES = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--max_poll_minutes',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    LOG_QUERY_FREQUENCY_SECONDS = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--log_query_frequency_seconds',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    MAX_ATTEMPTS_TO_FETCH_OUTPUT = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--max_attempts_to_fetch_output',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    DELAY_FETCH_OUTPUT_SECONDS = CertoraArgument(
        group=ArgGroups.CLOUD,
        attr_validation_func=Vf.validate_non_negative_integer,
        flag='--delay_fetch_output_seconds',  # added to prevent dup with QUEUE_WAIT_MINUTES
        argparse_args={
            'action': UniqueStore
        }
    )

    PROCESS = CertoraArgument(
        group=ArgGroups.CLOUD,
        argparse_args={
            'action': UniqueStore,
            'default': 'emv'
        }
    )

    SETTINGS = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        arg_type=AttrArgType.LIST_OF_STRINGS,
        attr_validation_func=Vf.validate_settings_attr,
        arg_status=ArgStatus.DEPRECATED,
        argparse_args={
            'action': APPEND
        }
    )
    """
    The content of prover_ext is added as is to the jar command without any flag. If jar_flag was set to None, this
    attribute would have been skipped altogether. setting jar_flag to empty string ensures that the value will be added
    to the jar as is
    """
    PROVER_EXT = CertoraArgument(

        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=validate_prover_ext,
        arg_status=ArgStatus.NEW,
        jar_flag='',
        help_msg="send flags directly to the prover",
        argparse_args={
            'action': UniqueStore,
        }
    )

    LOG_BRANCH = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        flag='--log_branch',
        argparse_args={
            'action': UniqueStore
        }
    )

    COMMIT_SHA1 = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_git_hash,
        argparse_args={
            'action': UniqueStore
        }
    )
    DISABLE_AUTO_CACHE_KEY_GEN = CertoraArgument(
        flag='--disable_auto_cache_key_gen',  # added to prevent dup with SKIP_PAYABLE_ENVFREE_CHECK
        group=ArgGroups.MISC_HIDDEN,
        arg_type=AttrArgType.BOOLEAN,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    MAX_GRAPH_DEPTH = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_non_negative_integer,
        jar_flag='-graphDrawLimit',
        argparse_args={
            'action': UniqueStore
        }
    )

    TOOL_OUTPUT = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        arg_status=ArgStatus.NEW,
        attr_validation_func=Vf.validate_tool_output_path,
        jar_flag='json',
        argparse_args={
            'action': UniqueStore,
        }
    )

    TOOL_OUTPUT_DEPRECATED = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        arg_status=ArgStatus.DEPRECATED,
        attr_validation_func=Vf.validate_tool_output_path,
        jar_flag='json',
        flag='--toolOutput',
        argparse_args={
            'action': UniqueStore,
            'dest': 'tool_output_deprecated' if Util.is_new_api() else 'tool_output'
        }
    )

    INTERNAL_FUNCS = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_json_file,
        argparse_args={
            'action': UniqueStore
        }
    )

    COINBASE_MODE = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        arg_type=AttrArgType.BOOLEAN,
        flag='--coinbaseMode',
        jar_flag='-coinbaseFeaturesMode',
        argparse_args={
            'action': STORE_TRUE
        }
    )

    GET_CONF = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        arg_status=ArgStatus.DEPRECATED,
        deprecation_msg="--get_conf is deprecated; use --conf_file instead",
        attr_validation_func=Vf.validate_conf_file,
        argparse_args={
            'action': UniqueStore,
            'type': lambda value: type_deprecated(value, ContextAttribute.GET_CONF)
        }
    )

    CONF_OUTPUT_FILE = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        arg_status=ArgStatus.NEW,
        argparse_args={
            'action': UniqueStore
        }
    )

    SKIP_PAYABLE_ENVFREE_CHECK = CertoraArgument(
        flag='--skip_payable_envfree_check',  # added to prevent dup with DISABLE_AUTO_CACHE_KEY_GEN
        group=ArgGroups.MISC_HIDDEN,
        jar_flag='-skipPayableEnvfreeCheck',
        arg_type=AttrArgType.BOOLEAN,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    RUN_SOURCE = CertoraArgument(
        group=ArgGroups.MISC_HIDDEN,
        attr_validation_func=Vf.validate_run_source,
        argparse_args={
            'action': UniqueStore
        }
    )

    ASSERT_AUTOFINDERS_SUCCESS = CertoraArgument(
        flag="--assert_autofinder_success",
        group=ArgGroups.MISC_HIDDEN,
        arg_type=AttrArgType.BOOLEAN,
        argparse_args={
            'action': STORE_TRUE
        }
    )

    STAGING = CertoraArgument(
        group=ArgGroups.ENV,
        flag='--staging',  # added to prevent dup with CLOUD
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'default': None,
            'const': "",
            'action': UniqueStore
        }
    )

    CLOUD = CertoraArgument(
        group=ArgGroups.ENV,
        flag='--cloud',  # added to prevent dup with STAGING
        argparse_args={
            'nargs': SINGLE_OR_NONE_OCCURRENCES,
            'default': None,
            'const': "",
            'action': UniqueStore
        }
    )

    def validate_value(self, value: str) -> None:
        if self.value.attr_validation_func is not None:
            self.value.attr_validation_func(value)

    def get_flag(self) -> str:
        return self.value.flag if self.value.flag is not None else '--' + self.name.lower()


def type_deprecated(value: str, attr: ContextAttribute) -> str:
    if Util.is_new_api():
        raise argparse.ArgumentTypeError(attr.value.deprecation_msg)
    return value
