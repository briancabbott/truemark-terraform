
#####################################
# Usage: terraform [global options] <subcommand> [args]
# 
# The available commands for execution are listed below.
# The primary workflow commands are given first, followed by
# less common or more advanced commands.
# 
# Main commands:
#   init          Prepare your working directory for other commands
#   validate      Check whether the configuration is valid
#   plan          Show changes required by the current configuration
#   apply         Create or update infrastructure
#   destroy       Destroy previously-created infrastructure
# 
# All other commands:
#   console       Try Terraform expressions at an interactive command prompt
#   fmt           Reformat your configuration in the standard style
#   force-unlock  Release a stuck lock on the current workspace
#   get           Install or upgrade remote Terraform modules
#   graph         Generate a Graphviz graph of the steps in an operation
#   import        Associate existing infrastructure with a Terraform resource
#   login         Obtain and save credentials for a remote host
#   logout        Remove locally-stored credentials for a remote host
#   output        Show output values from your root module
#   providers     Show the providers required for this configuration
#   refresh       Update the state to match remote systems
#   show          Show the current state or a saved plan
#   state         Advanced state management
#   taint         Mark a resource instance as not fully functional
#   untaint       Remove the 'tainted' state from a resource instance
#   version       Show the current Terraform version
#   workspace     Workspace management
# 
# Global options (use these before the subcommand, if any):
#   -chdir=DIR    Switch to a different working directory before executing the
#                 given subcommand.
#   -help         Show this help output, or the help for a specified subcommand.
#   -version      An alias for the "version" subcommand.

###
## Terraform CLI Module

import argparse
import inspect
import importlib.util
import os
import sys
import subprocess

from truemark_terraform.utils.hcl.hcl_generation_config import HCLGen
# from truemark_terraform.utils.hcl.hcl_utils import to_hcl

from truemark_terraform.driver.terraform import Terraform
from truemark_terraform.driver.operations.terraform_apply_operation import TerraformApplyOperationInput, TerraformApplyOperationOutput
from truemark_terraform.driver.operations.terraform_destroy_operation import TerraformDestroyOperationInput, TerraformDestroyOperationOutput
from truemark_terraform.driver.operations.terraform_init_operation import TerraformInitOperationInput, TerraformInitOperationOutput
from truemark_terraform.driver.operations.terraform_plan_operation import TerraformPlanOperationInput, TerraformPlanOperationOutput
from truemark_terraform.driver.operations.terraform_validate_operation import TerraformValidateOperationInput, TerraformValidateOperationOutput
from truemark_terraform.driver.operations.truemarktf_generate_operation import TruemarkTFGenerateOperationInput, TruemarkTFGenerateOperationOutput

class TerraformCLI():
    def __init__(self) -> None:
        pass

    def get_parser(self):
        parser = argparse.ArgumentParser(prog='truemark-terraform', add_help=True, conflict_handler='resolve')
        parser.description =("Initialize a new or existing Terraform working directory by creating \n"
                            "initial files, loading any remote state, downloading modules, etc. \n"
                            " \n"
                            "This is the first command that should be run for any new or existing \n"
                            "Terraform configuration per machine. This sets up all the local data \n"
                            "necessary to run Terraform that is typically not committed to version \n"
                            "control. \n"
                            " \n"
                            "This command is always safe to run multiple times. Though subsequent runs \n"
                            "may give errors, this command will never delete your configuration or \n"
                            "state. Even so, if you have important information, please back it up prior \n"
                            "to running this command, just in case. \n"
                            " \n"
                            "If no arguments are given, the configuration in this working directory\n"
                            "is initialized. \n")
        # meg = parser.add_mutually_exclusive_group()

        generate_group = parser.add_argument_group('generate')
        generate_group.add_argument('generate', help='generate HCL from the supplied python code file.')
        generate_group.add_argument('--file', type = str)

        # meg.add_argument_group()
        init_group = parser.add_argument_group('init')
        init_group.description = ("Usage: terraform init [options] [DIR]\n"
                        "\n"
                        "  Initialize a new or existing Terraform working directory by creating\n"
                        "  initial files, loading any remote state, downloading modules, etc.\n"
                        "\n"
                        "  This is the first command that should be run for any new or existing\n"
                        "  Terraform configuration per machine. This sets up all the local data\n"
                        "  necessary to run Terraform that is typically not committed to version\n"
                        "  control.\n"
                        "\n"
                        "  This command is always safe to run multiple times. Though subsequent runs\n"
                        "  may give errors, this command will never delete your configuration or\n"
                        "  state. Even so, if you have important information, please back it up prior\n"
                        "  to running this command, just in case.\n"
                        "\n"
                        "  If no arguments are given, the configuration in this working directory\n"
                        "  is initialized.\n")
        init_group.add_argument('-backend',
            help = "Configure the backend for this configuration.", type = bool)
        init_group.add_argument('-backend-config', 
            help = "This can be either a path to an HCL file with key/value assignments (same format as terraform.tfvars)" 
                  " or a 'key=value' format. This is merged with what is in the configuration file. This can be specified " 
                  "multiple times. The backend type must be in the configuration itself.")
        init_group.add_argument('-force-copy',          
            help = "Suppress prompts about copying state data. This is equivalent to providing a \"yes\" to all confirmation prompts.")
        init_group.add_argument('-from-module', 
            help = "Copy the contents of the given module into the target directory before initialization.")
        init_group.add_argument('-get', 
            help = "Download any modules for this configuration.")
        init_group.add_argument('-get-plugins', 
            help = "Download any missing plugins for this configuration. This command is a no-op in Terraform 0.13+: "
                 "use -plugin-dir settings or provider_installation blocks instead.")
        init_group.add_argument('-input', 
            help = "Ask for input if necessary. If false, will error if input was required.")
        init_group.add_argument('-lock', 
            help = "Lock the state file when locking is supported.")
        init_group.add_argument('-lock-timeout',
            help = "Duration to retry a state lock.")
        init_group.add_argument('-no-color', 
            help = "If specified, output won't contain any color.")
        init_group.add_argument('-plugin-dir', 
            help = "Directory containing plugin binaries. This overrides all "
                   "default search paths for plugins, and prevents the automatic installation of plugins. "
                   "This flag can be used multiple times.")
        init_group.add_argument('-reconfigure', 
            help = "Reconfigure the backend, ignoring any saved configuration.")
        init_group.add_argument('-upgrade', 
            help = "If installing modules (-get) or plugins, ignore previously-downloaded objects and install " 
                    "the latest version allowed within configured constraints.")
        init_group.add_argument('-verify-plugins',
            help = "Verify the authenticity and integrity of automatically downloaded plugins.")


        validate_group = parser.add_argument_group('validate')
        validate_group.description = ("Usage: terraform validate [options] [dir] \n"
            "\n"
            "  Validate the configuration files in a directory, referring only to the\n"
            "  configuration and not accessing any remote services such as remote state,\n"
            "  provider APIs, etc.\n"
            "\n"
            "  Validate runs checks that verify whether a configuration is syntactically\n"
            "  valid and internally consistent, regardless of any provided variables or\n"
            "  existing state. It is thus primarily useful for general verification of\n"
            "  reusable modules, including correctness of attribute names and value types.\n"
            "\n"
            "  It is safe to run this command automatically, for example as a post-save\n"
            "  check in a text editor or as a test step for a re-usable module in a CI\n"
            "  system.\n"
            "\n"
            "  Validation requires an initialized working directory with any referenced\n"
            "  plugins and modules installed. To initialize a working directory for\n"
            "  validation without accessing any configured remote backend, use:\n"
            "      terraform init -backend=false\n"
            "\n"
            "  If dir is not specified, then the current directory will be used.\n"
            "\n"
            "  To verify configuration in the context of a particular run (a particular\n"
            "  target workspace, input variable values, etc), use the 'terraform plan'\n"
            "  command instead, which includes an implied validation check.\n")
        validate_group.add_argument('-json', 
            help = "Produce output in a machine-readable JSON format, suitable for use in text "
                   "editor integrations and other automated systems. Always disables color.")
        validate_group.add_argument('-no-color', 
            help = "If specified, output won't contain any color.\n")


        plan_group = parser.add_argument_group('plan')
        plan_group.description = ("Usage: terraform plan [options] [DIR]\n"
                                    "\n"
                                    "  Generates a speculative execution plan, showing what actions Terraform\n"
                                    "  would take to apply the current configuration. This command will not\n"
                                    "  actually perform the planned actions.\n"
                                    "\n"
                                    "  You can optionally save the plan to a file, which you can then pass to\n"
                                    "  the \"apply\" command to perform exactly the actions described in the plan.\n")
        plan_group.add_argument('-compact-warnings', 
            help = "If Terraform produces any warnings that are not accompanied by errors, show them in a more compact form "
                   "that includes only the summary messages. ")
        plan_group.add_argument('-destroy', 
            help = "If set, a plan will be generated to destroy all resources managed by the "
                   "given configuration and state.")
        plan_group.add_argument('-detailed-exitcode', 
            help = "Return detailed exit codes when the command exits. This will change the meaning of exit codes to:"
                      "0 - Succeeded, diff is empty (no changes)"
                      "1 - Errored"
                      "2 - Succeeded, there is a diff")
        plan_group.add_argument('-input', help = "Ask for input for variables if not directly set.")
        plan_group.add_argument('-lock', help = "Lock the state file when locking is supported.")
        plan_group.add_argument('-lock-timeout', help = "Duration to retry a state lock.")
        plan_group.add_argument('-no-color', help = "If specified, output won't contain any color.")
        plan_group.add_argument('-out', help = "Write a plan file to the given path. This can be used as input to the \"apply\" command.")
        plan_group.add_argument('-parallelism', help = "Limit the number of concurrent operations. Defaults to 10.")
        plan_group.add_argument('-refresh', help = "Update state prior to checking for differences.")
        plan_group.add_argument('-state', 
            help = "Path to a Terraform state file to use to look up Terraform-managed resources. By default " 
                   "it will use the state \"terraform.tfstate\" if it exists.")
        plan_group.add_argument('-target', 
            help = "Resource to target. Operation will be limited to this resource and its dependencies. "
                   "This flag can be used multiple times.")
        plan_group.add_argument('-var', 
            help = "Set a variable in the Terraform configuration. This flag can be set multiple times.")
        plan_group.add_argument('-var-file', 
            help = "Set variables in the Terraform configuration from a file. If \"terraform.tfvars\" or any \".auto.tfvars\" "
                   "files are present, they will be automatically loaded.")


        apply_group = parser.add_argument_group('apply')
        apply_group.description = ("Usage: terraform apply [options] [PLAN]\n"
                                    "\n"
                                    "  Creates or updates infrastructure according to Terraform configuration\n"
                                    "  files in the current directory.\n"
                                    "\n"
                                    "  By default, Terraform will generate a new plan and present it for your\n"
                                    "  approval before taking any action. You can optionally provide a plan\n"
                                    "  file created by a previous call to \"terraform plan\", in which case\n"
                                    "  Terraform will take the actions described in that plan without any\n"
                                    "  confirmation prompt.\n")
        apply_group.add_argument('-auto-approve', 
            help = "Skip interactive approval of plan before applying.")
        apply_group.add_argument('-backup', 
            help = "Path to backup the existing state file before modifying. "
                   "Defaults to the \"-state-out\" path with \".backup\" extension. Set to \"-\" to disable backup.")
        apply_group.add_argument('-compact-warnings', 
            help = "If Terraform produces any warnings that are not accompanied by errors, "
                   "show them in a more compact form that includes only the summary messages.")
        apply_group.add_argument('-lock', 
            help = "Lock the state file when locking is supported.")
        apply_group.add_argument('-lock-timeout',  
            help = "Duration to retry a state lock.")
        apply_group.add_argument('-input',  
            help = "Ask for input for variables if not directly set.")
        apply_group.add_argument('-no-color', 
            help = "If specified, output won't contain any color.")
        apply_group.add_argument('-parallelism',  
            help = "Limit the number of parallel resource operations. Defaults to 10.")
        apply_group.add_argument('-refresh',  
            help = "Update state prior to checking for differences. "
                   "This has no effect if a plan file is given to apply.")
        apply_group.add_argument('-state', 
            help = "Path to read and save state (unless state-out is specified). "
                   "Defaults to \"terraform.tfstate\".")
        apply_group.add_argument('-state-out', 
            help = "Path to write state to that is different than \"-state\". "
                   "This can be used to preserve the old state.")
        apply_group.add_argument('-target', 
            help = "Resource to target. Operation will be limited to this resource and its dependencies. "
                   "This flag can be used multiple times.")
        apply_group.add_argument('-var', 
            help = "Set a variable in the Terraform configuration. This flag can be set multiple times.")
        apply_group.add_argument('-var-file', 
            help = "Set variables in the Terraform configuration from a file. If \"terraform.tfvars\" or "
                   "any \".auto.tfvars\" files are present, they will be automatically loaded.")


        destroy_group = parser.add_argument_group('destroy')
        destroy_group.description = ("Usage: terraform destroy [options] [DIR]\n"
                                     "\n"
                                     "  Destroy Terraform-managed infrastructure.\n")
        destroy_group.add_argument('-backup', 
            help = "Path to backup the existing state file before modifying. "
                   "Defaults to the \"-state-out\" path with \".backup\" extension. Set to \"-\" to disable backup.")
        destroy_group.add_argument('-auto-approve', 
            help = "Skip interactive approval before destroying.")
        destroy_group.add_argument('-force', 
            help = "Deprecated: same as auto-approve.")
        destroy_group.add_argument('-lock', 
            help = "Lock the state file when locking is supported.")
        destroy_group.add_argument('-lock-timeout', 
            help = "Duration to retry a state lock.")
        destroy_group.add_argument('-no-color', 
            help = "If specified, output won't contain any color.")
        destroy_group.add_argument('-parallelism', 
            help = "Limit the number of concurrent operations. Defaults to 10.")
        destroy_group.add_argument('-refresh',
            help = "Update state prior to checking for differences. "
                   "This has no effect if a plan file is given to apply.")
        destroy_group.add_argument('-state', 
            help = "Path to read and save state (unless state-out is specified). "
                   "Defaults to \"terraform.tfstate\".")
        destroy_group.add_argument('-state-out', 
            help = "Path to write state to that is different than \"-state\". "
                   "This can be used to preserve the old state.")
        destroy_group.add_argument('-target', 
            help = "Resource to target. Operation will be limited to this resource "
                   "and its dependencies. This flag can be used multiple times.")
        destroy_group.add_argument('-var', 
            help = "Set a variable in the Terraform configuration. This flag can be set multiple times.")
        destroy_group.add_argument('-var-file', 
            help = "Set variables in the Terraform configuration from a file. "
                   "If \"terraform.tfvars\" or any \".auto.tfvars\" files are present, they will be automatically loaded.")
        return parser

    def execute_cli(self):
        p = self.get_parser()
        args = p.parse_args()
        gen = args.generate

        if gen == 'generate':
            self.exec_generate(args.file)
        elif gen == 'init':
            self.exec_init(args.backend, args.backend_config, args.force_copy, args.from_module, args.get, args.get_plugins, args.input, args.lock,
                           args.lock_timeout, args.no_color, args.plugin_dir, args.reconfigure, args.upgrade, args.verify_plugins)
        elif gen == 'validate':
            self.exec_validate(args.json, args.no_color)
        elif gen == 'plan':
            self.exec_plan(args.compact_warnings, args.destroy, args.detailed_exitcode, args.input, args.lock, args.lock_timeout,
                           args.no_color, args.out, args.parallelism, args.refresh, args.state, args.target, args.var, args.var_file)
        elif gen == 'apply':
            self.exec_apply(args.auto_approve, args.backup, args.compact_warnings, args.lock, args.lock_timeout, args.input, args.no_color, 
                            args.parallelism, args.refresh, args.state, args.var, args.state_out, args.target, args.var_file)
        elif gen == 'destroy':
            self.exec_destroy(args.backup, args.auto_approve, args.force, args.lock, args.lock_timeout, args.no_color, 
                              args.parallelism, args.refresh, args.state, args.state_out, args.target, args.var, args.var_file) 
        else:
            print("Unknown directive for TerraForm: {directive}".format(directive = gen))

    def exec_generate(self, file):
        generate_input = TruemarkTFGenerateOperationInput()
        generate_input.py_files = [file]
        generate_output = Terraform().generate(generate_input)
        
        print(generate_output.hcl_contents)

    def exec_init(self, backend, backend_config, force_copy, from_module, get, get_plugins, input, lock, lock_timeout,
                        no_color, plugin_dir, reconfigure, upgrade, verify_plugins):
        init_input = TerraformInitOperationInput(backend = backend,
                                                backend_config = backend_config, 
                                                force_copy = force_copy,
                                                from_module = from_module,
                                                get = get,
                                                get_plugins = get_plugins,
                                                input = input,
                                                lock = lock,
                                                lock_timeout = lock_timeout,
                                                no_color = no_color,
                                                plugin_dir = plugin_dir,
                                                reconfigure = reconfigure,
                                                upgrade = upgrade,
                                                verify_plugins = verify_plugins)
        print(init_input)
        init_output = Terraform().init(init_input)

    def exec_validate(self, json, no_color):
        validate_input = TerraformValidateOperationInput(json = json, no_color = no_color)
        validate_output = Terraform().validate(validate_input)
        

    def exec_plan(self, compact_warnings, destroy, detailed_exitcode, input, lock, lock_timeout, 
                        no_color, out, parallelism, refresh, state, target, var, var_file):
        plan_input = TerraformPlanOperationInput(compact_warnings = compact_warnings,
                                                destroy = destroy,
                                                detailed_exitcode = detailed_exitcode, 
                                                input = input,
                                                lock = lock,
                                                lock_timeout = lock_timeout, 
                                                no_color = no_color,
                                                out = out,
                                                parallelism = parallelism,
                                                refresh = refresh,
                                                state = state,
                                                target = target,
                                                var = var,
                                                var_file = var_file)
        plan_output = Terraform().plan(plan_input)


    def exec_apply(self, auto_approve, backup, compact_warnings, lock, lock_timeout, input, no_color, 
                            parallelism, refresh, state, var, stateout, target, var_file):
        apply_input = TerraformApplyOperationInput(auto_approve = auto_approve,
                                                    backup = backup,
                                                    compact_warnings = compact_warnings,
                                                    lock = lock, 
                                                    lock_timeout = lock_timeout,
                                                    input = input,
                                                    no_color = no_color,
                                                    parallelism = parallelism,
                                                    refresh = refresh, 
                                                    state = state,
                                                    var = var,
                                                    stateout = stateout,
                                                    target = target,
                                                    var_file = var_file)
        apply_output = Terraform().apply(apply_input)
        
    def exec_destroy(self, backup, auto_approve, force, lock, lock_timeout, no_color, 
                              parallelism, refresh, state, state_out, target, var, var_file):
        destroy_input = TerraformDestroyOperationInput(backup = backup,
                                                        auto_approve = auto_approve,
                                                        force = force, 
                                                        lock = lock,
                                                        lock_timeout = lock_timeout, 
                                                        no_color = no_color,
                                                        parallelism = parallelism,
                                                        refresh = refresh, 
                                                        state = state, 
                                                        state_out = state_out, 
                                                        target = target, 
                                                        var = var, 
                                                        var_file = var_file)
        destroy_output = Terraform().destroy(destroy_input)

if __name__ == "__main__":
    TerraformCLI().execute_cli()