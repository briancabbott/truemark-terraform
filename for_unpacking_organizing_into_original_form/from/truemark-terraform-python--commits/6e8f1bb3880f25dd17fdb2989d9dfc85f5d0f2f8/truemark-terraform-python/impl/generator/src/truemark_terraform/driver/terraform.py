###
## Primary Python Driver for Terraform. This is where non-model 
## magic happens. The other side of Magic resides within the inner
## structure of the model itself. 
##
##
import os
import inspect
import subprocess
import runpy
import sys
from truemark_terraform.utils.hcl.hcl_generation_config import HCLGen
# from truemark_terraform.utils.hcl.hcl_utils import to_hcl
# from truemark_terraform.utils.hcl.hcl_utils import to_hcl_list
from truemark_terraform.utils.hcl.hcl_utils import new_hcl
from truemark_terraform.model.hashiregistry import HashiReg

from truemark_terraform.driver.operations.terraform_apply_operation import TerraformApplyOperationInput, TerraformApplyOperationOutput
from truemark_terraform.driver.operations.terraform_destroy_operation import TerraformDestroyOperationInput, TerraformDestroyOperationOutput
from truemark_terraform.driver.operations.terraform_init_operation import TerraformInitOperationInput, TerraformInitOperationOutput
from truemark_terraform.driver.operations.terraform_plan_operation import TerraformPlanOperationInput, TerraformPlanOperationOutput
from truemark_terraform.driver.operations.terraform_validate_operation import TerraformValidateOperationInput, TerraformValidateOperationOutput
from truemark_terraform.driver.operations.truemarktf_generate_operation import TruemarkTFGenerateOperationInput, TruemarkTFGenerateOperationOutput

##
# This should be a wrapper around TerraForm as an 'entity', not as a CLI executor.... 
# as an entity-bridge, it should model, the inputs, the outputs, and then call the 
# operations as functions, restructuring the inputs and, capturing and translating 
# the outputs then, abstracting process-execution specific attributes and defaulting 
# command line parameters that arent directly  related to the API operations however, 
# we want this to be callable from our own CLI wrappers so, it should expose control 
# of all TF 'levers' and 'buckets' (levers=parameters, buckets=output strings, error 
# messages, operating files and possibly temp files)  
class Terraform:

    def __init__(self):        
        # argspec = inspect.getfullargspec(self)
        pass

    def generate(self, input: TruemarkTFGenerateOperationInput) -> TruemarkTFGenerateOperationOutput:
        # First, run the python file, registering our python tf object-structure...
        if not input.py_files == None and len(input.py_files) > 0:
            for file in input.py_files:
                runpy.run_path(file)
                
                tf_file = file.replace(".py", "")
                tf_file = tf_file + ".tf"
                hashis = HashiReg.instance().get_hashis()
                hcl_text = new_hcl(hashis)
                with open(tf_file, 'w') as f:
                    f.write(hcl_text)
                    print("wrote: ", tf_file)
                HashiReg.instance().clear_registry()

        # Now, take all Hashi Objects registered and, convert them to HCL, appending them to an overall list and save them to a file.
        # TODO: Note: this is where we will need to enforce order of TF rules (i.e. providers and vars first possibly) -- 
        #       Also, not sure about this - might not need to since currently it invokes it in the same order as it is defined -- 
        #       this implies that a user will define things such as plugins etc first and not after the fact. 
        
        # hashi_hcls = to_hcl_list(hashis)

        # hashi_str = ""
        # for hcl in hashi_hcls:
        #     if hcl: 
        #         hashi_str += hcl.strip() + HCLGen.line

        out = TruemarkTFGenerateOperationOutput(hcl_contents = hcl_text)
        return out

    def init(self, input: TerraformInitOperationOutput) -> TerraformInitOperationOutput:
        cli_args = self.make_cli_args_from_input(input)
        cmd = ['terraform', 'init']
        if cli_args:
           cmd.append(cli_args)
        process = subprocess.run(cmd,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT,
                                  universal_newlines=True)
        print(process)
        print(process.stdout)
        return TerraformInitOperationOutput.from_process(process)

    def plan(self, input: TerraformPlanOperationInput) -> TerraformPlanOperationOutput:
        cli_args = self.make_cli_args_from_input(input)
        cmd = ['terraform', 'plan']
        if cli_args:
            cmd.append(cli_args)
        process = subprocess.run(cmd, 
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, 
                                  universal_newlines=True)
        print(process)
        print(process.stdout)
        return TerraformPlanOperationOutput.from_process(process)

    def apply(self, input: TerraformApplyOperationInput) -> TerraformApplyOperationOutput:
        cli_args = self.make_cli_args_from_input(input)
        cmd = ['terraform', 'apply']
        if cli_args:
            cmd.append(cli_args)
        process = subprocess.Popen(cmd, 
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,  
                                  stdin=subprocess.PIPE,
                                #   shell=True,
                                text=True,
                                  universal_newlines=True)
        process.stdout.flush()
        stdout, stdin = process.communicate(input="yes")
        print(stdout)
        print("done reading")

        print(process.stdout)
        return TerraformApplyOperationOutput.from_process(process)

    def destroy(self, input: TerraformDestroyOperationInput) -> TerraformDestroyOperationOutput: 
        cli_args = self.make_cli_args_from_input(input)
        cmd = ['terraform', 'destroy']
        if cli_args:
            cmd.append(cli_args)
        process = subprocess.run(cmd, 
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, 
                                        universal_newlines=True)
        print(process)
        print(process.stdout)
        return TerraformDestroyOperationOutput.from_process(process)

    def make_cli_args_from_input(self, input_op):
        args = input_op.to_dict()
        cli_args = {}
        for k in args.keys():
            val = args.get(k)
            if val:
                parameter = "-{}".format(k.replace("_", "-"))
                cli_args[parameter] = val
        cli_arg_str = ""
        for k, v in cli_args.items():
            cli_arg_str += " {k} {v} ".format(k = k, v = v)
        return cli_arg_str