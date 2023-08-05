import os
import re
from tronpytool import Paths
from . import REC, ITEM, ITEMLINK, ITEM_CP_LOCAL, ITEM_TRANSPILE_GO, TRANS_LOCAL, ITEM_TRANSPILE_PYTHON, \
    ITEM_TRANSPILE_TS, PRE_HEAD, SUB_FOOTER, FORGE_BUILD

REG = r"(.+?)([A-Z])"


def snake(match):
    return match.group(1).lower() + "_" + match.group(2).lower()


def filter_file_name(y: str) -> str:
    classNameNew = y
    if y.startswith("TRC"):
        classNameNew = y.lower()
    elif y.startswith("ERC20"):
        classNameNew = y.upper()
    else:
        classNameNew = re.sub(REG, snake, y, 0)
    print(classNameNew)
    return classNameNew


def compileItem1(tar: Paths, k0: str) -> str:
    """
    list the item content
    :param tar:
    :param k0:
    :return:
    """
    return ITEM.format(
        SOLCPATH=tar.SOLCPATH,
        COMPILE_COIN=k0,
        SOLVER=tar.SOLC_VER,
        EVMVERSION=tar.EVM_VERSION
    )


def compileItem2(tar: Paths, k0: str, link_lib_conf: str) -> str:
    """

    :param tar:
    :param k0:
    :param link:
    :return:
    """

    return ITEMLINK.format(
        SOLCPATH=tar.SOLCPATH,
        COMPILE_COIN=k0,
        FILES_CONFIG=link_lib_conf,
        SOLVER=tar.SOLC_VER,
    )


def buildCmdTsUpdate(p: Paths, pathName: str) -> str:
    nameClass = filter_file_name(os.path.basename(pathName)).replace('.sol', '')
    fromp = "{}/codec/gen_ts/{}.ts".format(p.BUILDPATH, nameClass)
    top = "{}/{}/src/api/abi/{}.ts".format(p.BUILDPATH, p.WEB_DAPP_SRC, nameClass)
    return ITEM_CP_LOCAL.format(
        fromlocation=fromp,
        tolocation=top
    )


def moveTsFiles(p: Paths, pathName: str) -> str:
    nameClass = filter_file_name(os.path.basename(pathName)).replace('.sol', '')
    fromp = "{}/codec/gen_ts/{}.ts".format(p.BUILDPATH, nameClass)
    top = "{}/{}/src/api/abi/{}.ts".format(p.BUILDPATH, p.WEB_DAPP_SRC, nameClass)
    return ITEM_CP_LOCAL.format(
        fromlocation=fromp,
        tolocation=top
    )


def abiPath_v1(p: Paths, pathName: str) -> str:
    return f"{p.BUILDPATH}/build/{os.path.basename(pathName).replace('.sol', '')}.abi"


def abiPath_v2(p: Paths, pathName: str) -> str:
    file_name = os.path.basename(pathName)
    return f"{p.BUILDPATH}/build/{file_name}/{file_name.replace('.sol', '')}.abi"


def buildCmdPy(p: Paths, pathName: str) -> str:
    return ITEM_TRANSPILE_PYTHON.format(
        outputfolder=f"{p.BUILDPATH}/codec/gen_py",
        target_abi=abiPath_v1(p, pathName),
        BUILDPATH=p.BUILDPATH
    )


def buildCmdPy2(p: Paths, pathName: str) -> str:
    return ITEM_TRANSPILE_PYTHON.format(
        outputfolder=f"{p.BUILDPATH}/codec/gen_py",
        target_abi=abiPath_v2(p, pathName),
        BUILDPATH=p.BUILDPATH
    )


def buildCmdTs(p: Paths, pathName: str) -> str:
    return ITEM_TRANSPILE_TS.format(
        outputfolder=f"{p.BUILDPATH}/codec/gen_ts",
        target_abi=abiPath_v1(p, pathName),
        BUILDPATH=p.BUILDPATH
    )


def buildCmdTs2(p: Paths, pathName: str) -> str:
    return ITEM_TRANSPILE_TS.format(
        outputfolder=f"{p.BUILDPATH}/codec/gen_ts",
        target_abi=abiPath_v2(p, pathName),
        BUILDPATH=p.BUILDPATH
    )


def buildCmdGo(p: Paths, pathName: str) -> str:
    based_name = os.path.basename(pathName)
    class_name = filter_file_name(based_name).replace('.sol', '')
    return ITEM_TRANSPILE_GO.format(
        outputfolder=f"{p.BUILDPATH}/codec/gen_go",
        target_abi=abiPath_v1(p, pathName),
        BUILDPATH=p.BUILDPATH,
        classname=class_name
    )


def buildCmdGo2(p: Paths, pathName: str) -> str:
    based_name = os.path.basename(pathName)
    class_name = filter_file_name(based_name).replace('.sol', '')
    return ITEM_TRANSPILE_GO.format(
        outputfolder=f"{p.BUILDPATH}/codec/gen_go/{class_name}",
        target_abi=abiPath_v2(p, pathName),
        BUILDPATH=p.BUILDPATH,
        classname=class_name
    )


def wrapContentTranspile(tar: Paths, compile_list: list) -> str:
    """
    wrap content
    :param tar:
    :param compile_list:
    :return:
    """
    return TRANS_LOCAL.format(
        LISTP="\n".join(compile_list),
        TARGET_LOC=tar.TARGET_LOC,
        COMPRESSED_NAME=tar.COMPRESSED_NAME,
        SOLVER=tar.SOLC_VER,
        PRE_HEAD=wrapHeadTranspile(tar),
        FOOTER=SUB_FOOTER
    )


def wrapHeadTranspile(p: Paths) -> str:
    return PRE_HEAD.format(
        FACTORY=p.FACTORY_PATH,
        BUILDPATH=p.BUILDPATH
    )


def wrapContentCompile(tar: Paths, compile_list: list) -> str:
    """
    wrap content
    :param tar:
    :param compile_list:
    :return:
    """
    return REC.format(
        LISTP="\n".join(compile_list),
        TARGET_LOC=tar.TARGET_LOC,
        COMPRESSED_NAME=tar.COMPRESSED_NAME,
        SOLVER=tar.SOLC_VER
    )


def wrapForgeCompile(tar: Paths) -> str:
    return FORGE_BUILD.format(
        SRC=tar.SOURCE_PATH,
        BUILD=tar.FORGE_BUILD,
        RUNS=100000
    )
