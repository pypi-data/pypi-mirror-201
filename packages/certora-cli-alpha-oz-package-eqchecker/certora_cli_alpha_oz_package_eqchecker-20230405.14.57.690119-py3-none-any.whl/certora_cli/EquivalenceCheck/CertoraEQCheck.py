import argparse
import logging
import sys
import shlex
import os
import glob
import json
from pathlib import Path
from argparse import ArgumentParser
from typing import List, Tuple

scripts_dir_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(scripts_dir_path))
from EVMVerifier.certoraBuild import InputConfig, CertoraBuildGenerator, CertoraVerifyGenerator
from EVMVerifier.certoraContext import get_args
from EVMVerifier.certoraContextClass import CertoraContext
from certoraRun import run_certora

# TODO set these paths to work agnostic to run directory
LOG_PATH = Path('EqCheck_log.log')
SANITY_PATH = Path('sanity.spec')
CERTORA_INTERNAL = Path('.certora_internal')
CONFIG = ".certora_config"
STDOUT = "*.standard.json.stdout"
CERTORA_BUILD = "*.certora_build.json"
INTERNAL = Path('.certora_internal')
DEF_TEMPLATE_PATH = Path('EQ_template.spec')
MC_TEMPLATE_PATH = Path('EQ_mc_template.spec')
DEFAULT_CONF_PATH = Path("EQ_default.conf")

FunctionSig = Tuple[str, List[str], List[str], str]

logger = logging.getLogger('MainLogger')
log_path = Path(__file__).parent.resolve() / LOG_PATH
logging.basicConfig(level=logging.WARNING, filemode='a', filename=log_path,
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')

class EquivalenceChecker:

    def run(self, args: argparse.Namespace) -> None:
        self.path = Path(__file__).parent.resolve()

        # windows handling may come with a later version
        if sys.platform == 'win32':
            logger.error("Windows is not yet supported")
            sys.exit(1)
        if args.debug:
            logger.setLevel(logging.DEBUG)

        self.args = args
        self.contracts = args.contracts
        self.functions = args.functions
        self.conf_mode = args.conf_mode

        if self.conf_mode:
            self.read_input_conf_file()
        else:
            self.files = args.files
            self.solcs = args.solcs

        # setup logging
        root = logging.getLogger()
        root.addHandler(logging.StreamHandler(sys.stdout))

        logger.debug(f'args received: {args}')

        self.build_and_generate_func_sigs()

        # find the signature of functionA and functionB
        self.sigs = list()
        self.sigs.append(grab_func_from_list(self.functions[0], self.funcs[0]))
        self.sigs.append(grab_func_from_list(self.functions[1], self.funcs[1]))

        # validate signatures
        self.validate_signatures()

        # generate spec files from template
        self.is_multicontract = (self.contracts[0] != self.contracts[1]) or (self.files[0] != self.files[1])
        spec = self.generate_spec()
        print(f'Certora spec file generated! Check it out at {spec}')

        conf = self.generate_conf_file(spec)

        run_certora([str(conf)])

        if self.functions[0] == self.functions[1] and self.contracts[0] == self.contracts[1] \
                and self.files[0] == self.files[1]:
            logger.warning("TRIVIAL RUN: You are comparing a function to itself. Please check your arguments \
                           and submit a report to Certora if this is a mistake")
        logger.debug("finished succesfully")
        print("Certora Equivalence Check sucessfully generated!")
        print("Go check the link above to track the progress of your job and see results")
        # optional step: read in the job and print results to terminal

    def read_input_conf_file(self) -> None:
        self.conf_path = Path(args.conf_path).resolve()
        with self.conf_path.open() as conf_file:
            contents = json.load(conf_file)
            files = contents['files']
            self.files = []
            for file in files:
                # if the conf file contains absolute path already then we use it
                if Path(file).exists():
                    self.files.append(file)
                # otherwise append the relative path to the conf file location to create absolute path
                else:
                    self.files.append(resolve_file(self.conf_path.parent / file))
            if len(files) < 2:
                logger.error("ERROR: must provide at least two files for reference")
            if not self.contracts or self.functions:
                # case where either or both of these will be in the conf file
                if not self.functions and 'functions' in contents:
                    # if the user has functions in the conf file but manually inputs different ones
                    # we want to use the ones they input via cli
                    self.functions = contents['functions']
                if not self.contracts and 'contracts' in contents:
                    # same as above for contracts
                    self.contracts = contents['contracts']
                if not self.contracts:
                    logger.error("ERROR: Must provide at least two contracts via conf or CLI. Please use \"contracts\" \
                    in the conf file")
                    sys.exit(1)

                if not self.functions:
                    logger.error("ERROR: Must provide functions via conf or CLI. Please use \"functions\" \
                    in the conf file")
                    sys.exit(1)
                if len(self.contracts) < 2:
                    logger.error("ERROR: not enough contracts provided. Must supply at least 2 contracts")
                    sys.exit(1)
                if len(self.functions) < 2:
                    logger.error("ERROR: Must provide at least 2 seperate functions")
                    sys.exit(1)
            logger.debug(f'files found {self.files}')
            if len(files) < 2:
                logger.error("INPUT ERROR: at least two files must be listed in EQ conf files")
                sys.exit(1)
            if 'solc' in contents:
                self.solcs = [contents['solc'], contents['solc']]
            elif 'solc_map' in contents:
                self.solc_map = contents['solc_map']
            else:
                logger.error("INPUT ERROR: conf file must contain either a solc or solc map")
                sys.exit(1)

    def build_context(self, file: Path, contract: str, solc: str) -> CertoraContext:
        path_to_spec_resolve = self.path / SANITY_PATH
        cmd = f'{file}:{contract} ' \
            f'--verify {contract}:{path_to_spec_resolve} ' \
            f'--solc {solc} ' \
            f'--optimistic_loop ' \
            f'--build_only '
        logger.debug(f'generated command: {cmd}')
        split = shlex.shlex(cmd, posix=True)  # potential for issues on windows
        split.whitespace_split = True
        cmd_list = list(split)
        logger.debug(f'building command: {cmd_list}')
        context, conf_dict = get_args(cmd_list)
        return context

    def build_and_generate_func_sigs(self) -> None:
        """
        Creates a CertoraBuildGenerator and then uses it to first build the given file,
        then extracts function signatures
            @param file: relative path of file being built
            @param contract: name contract being checked
            @param solc: name of solc executable to use for compilation
            @return List of functions as a Tuple in the format [name, inputs, outputs, state mutability]
            """
        self.funcs = list()
        for i in range(2):
            context = self.build_context(self.files[i], self.contracts[i], self.solcs[i])
            config = InputConfig(context)
            cfb = CertoraBuildGenerator(config, context)
            cfb.certora_verify_generator = CertoraVerifyGenerator(cfb)
            cfb.certora_verify_generator.copy_specs()
            cfb.certora_verify_generator.dump()
            logger.debug(f'created CertoraBuildGenerator successfully for {self.files[i]}:{self.contracts[i]}')
            cfb.build(context)
            self.funcs.append(cfb.collect_func_source_code_signatures_source(self.files[i], self.contracts[i],
                                                                             self.solcs[i]))
            logger.debug(f'grabbed functions from {self.contracts[i]}: {self.funcs[i]}')

    # checks the latest internal directory for its .certora_build.json file
    def grab_certora_build(self) -> Path:
        list_of_files = glob.glob(os.path.join(CERTORA_INTERNAL.stem, '*/'))
        latest_dir = os.path.relpath(max(list_of_files, key=os.path.getctime), CERTORA_INTERNAL)
        json_path = Path(CERTORA_INTERNAL / latest_dir).resolve()
        logger.debug(f'looking for build file in {json_path}')
        json_file = next(json_path.glob(CERTORA_BUILD))
        if not json_file:
            raise FileNotFoundError("could not find correlating certora_build file")
        logger.debug(f'found build file {json_file}')
        return json_file

    def generate_spec(self) -> Path:
        """
        Creates the spec to be run from the template
        @param contract_B: name of second contract for the using statement
        @param parameters: inputs of the function signature
        @param outputs: outputs of the function signature
        @param func_A: name of the first function
        @param func_B: name of the second function
        @return: Path to spec built
        """
        output_dir = Path(self.files[0]).parent
        # parameter_list = self.sigs[0][1]
        outputs = self.sigs[0][2]

        # create section declaring output variables
        outputs_dec = ""
        outputs_in_a = ""
        outputs_in_b = ""
        outputs_compare = ""
        index = 0
        functionA = self.functions[0]
        functionB = self.functions[1]
        if functionA == functionB:
            functionB = functionA + "B"
        for var in outputs:
            var_a = f'{functionA}_{var.replace("[]", "")}_out{index}'
            var_b = f'{functionB}_{var.replace("[]", "")}_out{index}'

            outputs_dec += f'{var} {var_a};\n    '
            outputs_dec += f'{var} {var_b};\n    '
            if index == 0:
                outputs_in_a += f'{var_a}'
                outputs_in_b += f'{var_b}'
            else:
                outputs_in_a += f', {var_a}'
                outputs_in_b += f', {var_b}'
            outputs_compare += f'assert({var_a} == {var_b});\n    '
            index += 1

        # read in the template

        if self.is_multicontract:
            temp_path = self.path / MC_TEMPLATE_PATH
        else:
            temp_path = self.path / DEF_TEMPLATE_PATH
        with temp_path.resolve().open('r') as template:
            spec = template.read()

        # fill in the template
        spec = spec.replace("CONTRACTB", self.contracts[1])
        spec = spec.replace("<Fa>", self.functions[0])
        spec = spec.replace("<Fb>", self.functions[1])
        spec = spec.replace("OUTPUTS_DEC", outputs_dec.strip())
        spec = spec.replace("OUTPUTS_IN_A", outputs_in_a)
        spec = spec.replace("OUTPUTS_IN_B", outputs_in_b)
        spec = spec.replace("COMPARE_OUTPUTS", outputs_compare.strip())

        print(spec)
        logger.debug("finished generating spec")

        # save spec as a new file
        spec_file_path = output_dir / (self.functions[0] + "_to_" + self.functions[1] + "_equivalence.spec")
        with spec_file_path.open('w') as spec_file:
            spec_file.write(spec)

        return spec_file_path

    def build_context_from_conf(self, conf_path: Path) -> CertoraContext:
        context = CertoraContext()
        with conf_path.open() as conf_file:
            contents = json.load(conf_file)
            for entry in contents:
                setattr(context, entry, contents[entry])
        logger.debug(f'context loaded: {context}')
        return context

    # check function signature for the proper inputs
    def validate_signatures(self) -> None:
        sig_a = self.sigs[0]
        sig_b = self.sigs[1]
        if sig_a[1] != sig_b[1]:
            logger.error("functions must have the same input parameters")
            sys.exit(1)

        if sig_a[2] != sig_b[2]:
            logger.error("function must have the same output parameters")
            sys.exit(1)

        if (sig_a[3] or sig_b[3]) != ("pure" or "view"):
            logger.error("functions must be pure or view functions for now")
            sys.exit(1)

        if sig_a[3] == "view" and sig_b[3] == "view" and \
           (self.contracts[0] != self.contracts[1] or self.files[0] != self.files[1]):
            logger.error("cannot yet compare two view functions from two seperate contracts")
            sys.exit(1)

    def generate_conf_file(self, spec: Path) -> Path:
        if self.conf_mode:
            # setup the user defined conf file to run
            with self.conf_path.open() as conf_file:
                contents = json.load(conf_file)
                contents['rule_sanity'] = "basic"
                contents['files'] = list()
                for file in self.files:
                    contents['files'].append(str(file))
        else:
            # update default conf_file for running
            with (self.path / DEFAULT_CONF_PATH).open() as conf_file:
                contents = json.load(conf_file)
                for file in self.files:
                    contents['files'].append(str(file))
                if '--bitvector' in args:
                    contents['settings'].append('-useBitVectorTheory')
                if self.solcs[0] == self.solcs[1]:
                    contents['solc'] = self.solcs[0]
                else:
                    contents['solc_map'] = {self.contracts[0]: self.solcs[0], self.contracts[1]: self.solcs[1]}
                contents['msg'] = f'EquivalenceCheck of {self.functions[0]} and {self.functions[1]}'
                if len(contents['settings']) == 0:
                    contents.pop('settings')
        contents['verify'] = [f'{self.contracts[0]}:{spec}']
        logger.debug(f'conf file finished generation: {contents}')

        if 'bitvector_theory' not in contents:
            logger.warning("WARNING: running without bitvector theory when using bitwise operation will result in \
                            innacurate results \n Please run with --bitvector if you are using any of these operation")

        conf_file_path = spec.parent / (spec.stem + '.conf')
        with conf_file_path.open('w') as conf_file:
            json.dump(contents, conf_file, indent=4)
        print(f'Conf file generated: {conf_file_path}')
        return conf_file_path

def grab_func_from_list(target: str, funcs: List[FunctionSig]) -> FunctionSig:
    for func in funcs:
        if func[0] == target:
            logger.debug(f'found sig {func} for {target}')
            return func
    logger.error(f'Could not find function {target}, make sure your function is not internal or in a library')
    sys.exit(1)

# resolve files, raises an error more cleanly if the file is wrong
def resolve_file(file: str) -> Path:
    try:
        out = Path(file).resolve(strict=True)
        return out
    except FileNotFoundError:
        logger.error(f'Could not find file {file}, \
                    make sure you pass the relative path from the directory being run in')
        sys.exit(1)

# splits the colon seperated CLI args into a namespace used by the EquivalenceChecker
def split_args(args: argparse.Namespace) -> argparse.Namespace:
    args.conf_mode = 'conf_path' in args
    if args.conf_mode:
        if args.functionA and args.functionB:
            if ':' in args.functionA and ':' in args.functionB:
                split_a = str(args.functionA).split(':')
                split_b = str(args.functionB).split(':')
                args.contracts = [split_a[0], split_b[0]]
                args.functions = [split_a[1], split_b[1]]
                args.solcs = None
                args.files = None
            elif ':' in args.functionA or ':' in args.functionB:
                logger.error("ERROR: Passed in arguments must be symmetrical")
                sys.exit(1)
            else:
                # set these to None for now and fill them in once we parse the conf file
                args.contracts = None
                args.functions = None
        elif args.functionA or args.functionB:
            logger.error('ERROR: Must give arguments for both contract/functions')
            sys.exit(1)
        else:
            args.contracts = None
            args.functions = None
    else:
        split_a = args.arg_a.split(':')
        split_b = args.arg_b.split(':')
        if len(split_a) < 3:
            logger.error(f'wrong input format given, please use file:contract:function:solc for each function \
                            \n Input: {args.arg_a}')
            sys.exit(1)
        if len(split_b) < 3:
            logger.error(f'wrong input format given, please use file:contract:function:solc for each function \
                            \n Input: {args.arg_b}')
            sys.exit(1)
        if len(split_a) == 4:
            args.file_a, args.contract_a, args.function_a, args.solc_a = split_a
        else:
            args.file_a, args.function_a, args.solc_a = split_a
            args.contract_a = Path(args.file_a).stem

        if len(split_b) == 4:
            args.file_b, args.contract_b, args.function_b, args.solc_b = split_b
        else:
            args.file_b, args.function_b, args.solc_b = split_b
            args.contract_b = Path(args.file_b).stem

        args.files = [resolve_file(args.file_a), resolve_file(args.file_b)]
        args.contracts = [args.contract_a, args.contract_b]
        args.solcs = [args.solc_a, args.solc_b]
        args.functions = [args.function_a, args.function_b]
    return args

if __name__ == '__main__':
    parser = ArgumentParser(
        prog='Certora Equivalence Checker',
        usage='python(3) EqCheck fileA (conf, def)',
        description='A Certora tool for checking the equivalence of two pure or view Solidity functions')

    # setup different modes of entering inputs
    subs = parser.add_subparsers()
    conf_parser = subs.add_parser('conf', help='--conf <path to conf file> <contract>:<functionA> \
                                                <contractB>:<functionB>')
    default_parser = subs.add_parser('def', help='<path to fileA>:<contractA>:<functionA>:<solcA>  \
                                                    <path to fileB>:<contractB>:<functionB>:<solcB>')

    # arguments for --conf
    conf_parser.add_argument('conf_path', help='relative path to your intended conf file')
    # optional positional arguments
    conf_parser.add_argument('functionA', nargs="?", help='usage Contract:Function - name of the first contract and \
                                                           function you are comparing')
    conf_parser.add_argument('functionB', nargs="?", help='usage Contract:Function - name of the second contract and \
                                                           function you are comparing')
    # arguments for --def
    default_parser.add_argument('arg_a', help='Usage: file:contract:function:solc - relative path of the first file \
                                                name of contract, name of function, solc executable name')
    default_parser.add_argument('arg_b', help='Usage: file:contract:function:solc - relative path of the second file \
                                                name of contract, name of function, solc executable name')

    default_parser.add_argument('--bitvector', required=False, help='Use this option for when you are comparing any \
                                                                     functions that use bitwise operations')
    default_parser.add_argument('--debug', required=False, action='store_true')
    conf_parser.add_argument('--debug', required=False, action='store_true')
    args = split_args(parser.parse_args())
    EQCheck = EquivalenceChecker()
    EQCheck.run(args)
