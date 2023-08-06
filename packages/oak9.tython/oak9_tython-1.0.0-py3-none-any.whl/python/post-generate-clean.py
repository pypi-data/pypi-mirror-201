import glob
import os
import re

# The folder structure MUST follow this nesting pattern for many reasons to keep package names proper
# sourceFiles = glob.glob('./oak9/tython/**/*.py', recursive=True)
sourceFiles = glob.glob('./models/**/*.py', recursive=True)
for file in sourceFiles:
    normalized_path = os.path.normpath(file)
    path_components = normalized_path.split(os.sep)
    namespace_order = ["oak9", "tython", "models"]
    kubernetes_namespace = []

    if 'kubernetes' in path_components:
        kubernetes_namespace = namespace_order + path_components[1:-1]

    content_new = []

    with open (file, 'r') as f:
        for line in f:
            if re.search('^(?:from )(!?shared)([^\s]*)', line) != None:
                content_new.append(re.sub('^(?:from )(!?shared)([^\s]*)', 'from ' + '.'.join(namespace_order) + r'.\1', line, flags = re.M))
            elif re.search('^(?:from )(!?gcp)([^\s]*)', line) != None:
                content_new.append(re.sub('^(?:from )(!?gcp)([^\s]*)', 'from ' + '.'.join(namespace_order) + r'.\1', line, flags = re.M))
            elif re.search('^(?:from )(!?kubernetes)([^\s]*)', line) != None:
                content_new.append(re.sub('from kubernetes','from ' + '.'.join(namespace_order) + '.kubernetes', line))
            else:
                content_new.append(line)

    with open(file, 'w'): pass

    with open (file, 'a') as f:
        for line in content_new:
            f.write(line)