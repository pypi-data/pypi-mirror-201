#****************************************************************************
#* __main__.py
#*
#* Copyright 2023 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#****************************************************************************
import argparse
from .cmds.cmd_encode import CmdEncode

def getparser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()
    subparsers.required = True

    cmd_enc = subparsers.add_parser("enc", 
            help="Encode a series of PSS files to use obfuscated identifiers")
    cmd_enc.add_argument("-o", "--output", default="scrambled.pss",
            help="Specify the output file. By default, the output is 'scrambled.pss'")
    cmd_enc.add_argument("-c", "--preserve-comments", action="store_true",
            help="Preserve comments from input")
    cmd_enc.add_argument("-s", "--seed", default="0",
            help="Specifies the seed to use in randomly selecting replacement words")
    cmd_enc.add_argument("files", nargs="+",
            help="PSS files to encode")
    cmd_enc.set_defaults(func=CmdEncode())

    return parser

def main():
    parser = getparser()

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
