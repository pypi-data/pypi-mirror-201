from . import SUB_FOOTER
from .commoncompile import *


def BuildRemoteLinuxCommand(p: Paths, list_files: list = None, linked: dict = None) -> None:
    """
    building the remote linux command line
    :param p:
    :param list_files:
    :return:
    """
    k = list()
    # ==================================================
    if list_files is not None:
        for v in list_files:
            k.append(compileItem1(p, v))
    # ==================================================
    if linked is not None:
        for c in linked:
            if "compile" in c and "libraries" in c:
                compile_file = c["compile"]
                lib_cmds = list()
                """
                solc before v0.8.1

                example: link = {
                    "filepath.sol:CLASS:0x0930193019391093012930209099302129"
                }

                solc --optimize --bin MetaCoin.sol | solc --link --libraries TestLib:<address>

                """
                for b in c["libraries"]:
                    if "class" in b and "address" in b:
                        source_line = "{}:{}".format(b["class"], b["address"])
                        if "src" in b:
                            source_line = "{}:{}:{}".format(b["src"], b["class"], b["address"])
                        lib_cmds.append(source_line)
                library_link_cmd = " ".join(lib_cmds)
                k.append(compileItem2(p, compile_file, library_link_cmd))
    # ==================================================
    with open(p.workspaceFilename("remotesolc"), 'w') as f:
        f.write(wrapContentCompile(p, k))
        f.close()
    # ==================================================


def BuildLang(p: Paths, list_class_names: list) -> None:
    """

    :param p:
    :param list_class_names:
    :return:
    """
    k = list()
    # ==================================================
    for v in list_class_names:
        k.append(buildCmdPy(p, v))
        k.append(buildCmdTs(p, v))
        k.append(buildCmdTsUpdate(p, v))
    # ==================================================
    with open(p.workspaceFilename("localpile"), 'w') as f:
        f.write(wrapContentTranspile(p, k))
        f.close()


def BuildLangForge(p: Paths, list_class_names: list) -> None:
    """

    :param p: path in string
    :param list_class_names: the class name
    :return:
    """
    k = list()
    # ==================================================
    for v in list_class_names:
        k.append(buildCmdPy2(p, v))
        k.append(buildCmdTs2(p, v))
        k.append(buildCmdGo2(p, v))
        if p.WEB_DAPP_SRC is not None:
            if os.path.isdir(p.WEB_DAPP_SRC):
                k.append(moveTsFiles(p, v))
            else:
                print(f"app path for implementation {p.WEB_DAPP_SRC} is not exist. file move is stopped.")
    # ==================================================
    with open(p.workspaceFilename("localpile"), 'w') as f:
        f.write(wrapContentTranspile(p, k))
        f.close()


def BuildForgeLinuxBuildCommand(p: Paths) -> None:
    with open(p.workspaceFilename("buildforgebin"), 'w') as f:
        f.write(wrapForgeCompile(p))
        f.close()
