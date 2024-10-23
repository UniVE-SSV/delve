#!/usr/bin/env python3

LISA_DEPENDENCIES_JSON_PATH = "lisa-dependencies.json"
import json
from git import Repo
import os
import shutil
import subprocess

def parse_lisa_dependencies_json(path):
    # Open and read the JSON file
    try:
        with open(path, 'r') as file:
            dependencies = json.load(file)
    except Exception as e:
        raise Exception("Unable to parse file {}".format(path))
    return dependencies

def get_all_src_main_folder(dependency):
    repo_local_path = "lisa-dependencies/{}".format(dependency["name"])
    folders = []
    for root, dirs, _ in os.walk(repo_local_path, topdown=True):
        for dir in dirs:
            full_path = root + "/" + dir
            if full_path.endswith("src/main"):
                folders.append(full_path)
                #print(repo_local_path)
                #print(full_path.removeprefix(repo_local_path))
    return folders

def generate_version_info(dependency):
    repo_local_path = "lisa-dependencies/{}".format(dependency["name"] + "/" + dependency["name"]) # ugly part (the project stays in lisa/lisa) - but this could not be the case for all the FE.
    print("Generating version info")
    command = "cd {} && ./gradlew generateVersionInfo".format(repo_local_path)
    subprocess.run(command, shell=True)

def clone_dependency(dependency):
    repo_local_path = "lisa-dependencies/{}".format(dependency["name"])
    if os.path.exists(repo_local_path):
        # delete the folder
        print("Deleting local folder {}".format(repo_local_path))
        shutil.rmtree(repo_local_path)
    print("Cloning repo {} in {}".format(dependency["repository"], repo_local_path))
    Repo.clone_from(dependency["repository"], repo_local_path)
    print("Switching branch to {}".format(dependency["branch"]))
    command = "cd {} && git checkout -b {} origin/{}".format(repo_local_path, dependency["branch"], dependency["branch"])
    print(command)
    subprocess.run(command, shell=True)

def generate_grammar_source(dependency):
    repo_local_path = "lisa-dependencies/{}".format(dependency["name"])
    if not "generateGrammarSource" in dependency or dependency["generateGrammarSource"] == False:
        print("Skip generateGrammarSource")
        return
    command = "./" + repo_local_path + "/" + dependency["name"] + "/gradlew generateGrammarSource -p " + repo_local_path + "/" + dependency["name"]
    print("Running {}".format(command))
    subprocess.run(command.split(" "))
    command_rsync = "rsync -avh --progress "+ repo_local_path + "/" + dependency["name"] + "/" + dependency["antlrGeneratedSrcBuildRoot"] + "/build/generated-src build"
    print("Copying generated source to delve")
    print(command_rsync)
    subprocess.run(["mkdir", "build"])
    subprocess.run(["mkdir", "build/generated-src"])
    subprocess.run(command_rsync.split(" "))

def get_all_files(folder):
    sources = []
    for root, dirs, files in os.walk(folder, topdown=True):
        for file in files:
            sources.append((root.removeprefix(folder), file))
    return sources

def symlink_sources(dependency):

    folders = get_all_src_main_folder(dependency)
    for folder in folders:
        files = get_all_files(folder)
        _files = ["src/main" + f[0] + "/" + f[1] + "\n" for f in files]
        with open("lisa-dependencies/sym-files.txt", "a") as f:
            f.writelines(_files)
        with open(".git/info/exclude", "a") as f:
            f.writelines(["" + f for f in _files])
        for f in files:
            if "TypeHintAnnotation.java" in f[1]:
                x = 10
            subprocess.run("mkdir -p src/main" + f[0], shell=True)
            subprocess.run("ln -s $(pwd)/{} {}".format(folder + "/" + f[0] + "/" + f[1], "src/main" + f[0] + "/" + f[1]), shell=True)

def delete_links(file):
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            lines = [l[:-1] for l in lines]
            for line in lines:
                subprocess.run("rm {}".format(line), shell=True)
    except Exception as e:
        print(e)
        pass

def main():
    try:
        dependencies = parse_lisa_dependencies_json(LISA_DEPENDENCIES_JSON_PATH)
        # delete old symbolic links
        delete_links("lisa-dependencies/sym-files.txt")
        subprocess.run("rm lisa-dependencies/sym-files.txt", shell=True) # recreate the sym-files.txt
        subprocess.run("rm .git/info/exclude", shell=True) # recreate the info/exclude too
        for dependency in dependencies["dependencies"]:
            # 1. CLONE REPO (and switch branch)
            clone_dependency(dependency)

            if "type" in dependency and dependency["type"] == "lisaCore":
                # we need to call gradle to generate the version info source.
                generate_version_info(dependency)
            # 2. PERFORM generateGrammarSource gradlew task (to compile the antlr grammars)
            #generate_grammar_source(dependency) # no needed (we generated all the necessary files from the delve gradle
            # 3. Symlinks of all the libraries sources (and also add them to a .gitignore)
            symlink_sources(dependency)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()