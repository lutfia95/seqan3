#!/usr/bin/env python3
# -----------------------------------------------------------------------------------------------------
# Copyright (c) 2006-2021, Knut Reinert & Freie Universität Berlin
# Copyright (c) 2016-2021, Knut Reinert & MPI für molekulare Genetik
# This file may be used, modified and/or redistributed under the terms of the 3-clause BSD-License
# shipped with this file and also available at: https://github.com/seqan/seqan3/blob/master/LICENSE.md
# -----------------------------------------------------------------------------------------------------
#
# Usage process_compiler_error_log.py <log_file>
#
# Processes a build log and writes a GitHub-Markdown-formatted list of build errors to stdcout.
import re
import sys

# https://regex101.com/r/aE0qX3/1
tokenise_regex = re.compile(r"(\[\s*\d+%\](?:.(?!\[\s*\d+%\]))+(?:error:).*?(?=\[\s*\d+%\]|$))", re.DOTALL)
# Match line containg 'error:', but stop at linebreak, semicolon or parenthesis.
error_regex = re.compile(r"(error:[^(;\n]*)")

with open(sys.argv[1]) as file:
    content = file.read()

counter = 1
log = ''
# One `group` (a string) is all messages in the log associated with one failing compilation
for group in [match.groups()[0] for match in tokenise_regex.finditer(content)]:
    error_message = re.search(error_regex, group).group().rstrip()
    log += '<details><summary>Error {}: <code>{}</code></summary>\n\n```text\n'.format(counter, error_message)
    log += '\n'.join(group.split('\n')[:30]).rstrip() # Only take first 30 lines
    log += '\n```\n</details>\n'
    counter += 1

# Truncate to 65300 to not exceed the limit of GitHub's API
print(log[:65300])
