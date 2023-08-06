import importlib
import json
import os
import re
import subprocess
import sys
from modulefinder import ModuleFinder
import pandas as pd
from a_pandas_ex_plode_tool import pd_add_explode_tools
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions
from flatten_everything import flatten_everything
from cprinter import TC
from a_pandas_ex_dillpickle import pd_add_dillpickle
from touchtouch import touch
import dill
import pipdeptree,pipreqs
pd_add_dillpickle()
pd_add_apply_ignore_exceptions()
pd_add_explode_tools()


def prepare_ignored_list(ignore_packages):
    ignore_packageslist = (
        list(ignore_packages)
        if not isinstance(ignore_packages, list)
        else ignore_packages
    )
    ignore_packageslist = list(
        flatten_everything(
            [
                [
                    str(x).strip().lower().replace("_", "-"),
                    str(x).strip().lower().replace("-", "_"),
                ]
                for x in ignore_packageslist
            ]
        )
    )
    return ignore_packageslist

def get_pip_tree(ignore_packages=("ipython",)):
    ignore_packageslist=prepare_ignored_list(ignore_packages)
    dep = subprocess.run(r"pipdeptree --json", capture_output=True)
    asj = json.loads(dep.stdout)
    dfs = [pd.Q_AnyNestedIterable_2df(x, unstack=True) for x in asj]

    print('Executing: "pip show ..."_______________________')

    infopip = []
    for df in dfs:
        packna = ""
        try:
            try:
                d = df.loc[
                    (df.level_0 == "package")
                    & ((df.level_1 == "package_name") | (df.level_2 == "package_name"))
                ]
            except Exception as fe:
                d = df.loc[(df.level_0 == "package") & (df.level_1 == "package_name")]
            try:
                try:
                    d2 = df.loc[
                        (df.level_0 == "dependencies")
                        & (df.level_2.isin(["package_name", "required_version"]))
                    ].copy()
                except Exception as fe:
                    d2 = pd.DataFrame(
                        [[pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]],
                        columns=(
                            ["level_0", "level_1", "level_2", "aa_all_keys", "aa_value"]
                        ),
                    )

                d2.aa_all_keys = df.aa_all_keys.ds_apply_ignore(pd.NA, lambda x: x[:2])
            except Exception as fax:
                # print(fax)
                d2 = pd.DataFrame(
                    [[pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]],
                    columns=(
                        ["level_0", "level_1", "level_2", "aa_all_keys", "aa_value"]
                    ),
                )
            packna = d.aa_value.iloc[0]
            if str(packna).strip().lower() in ignore_packageslist:
                print(TC(f"Ignored: {packna}").bg_black.fg_yellow)
                continue

            infopo = [
                g
                for x in subprocess.run(f"pip show {packna}", capture_output=True)
                .stdout.decode("utf-8", "ignore")
                .strip()
                .splitlines()
                if len(g := x.strip().split(":", maxsplit=1)) == 2 and " :: " not in x
            ]

            submopa = []
            try:
                submopa = importlib.util.find_spec(
                    packna.replace("-", "_")
                ).submodule_search_locations
                submopa = [x for x in submopa if os.path.isabs(x)]
                if not (submopa):
                    raise ValueError
            except Exception:
                try:
                    pp = subprocess.run(
                        ["pip", "show", "-f", packna], timeout=30, capture_output=True
                    )
                    # print(pp)
                    allf = [
                        x.strip()
                        for x in pp.stdout.decode("utf-8", "ignore").splitlines()
                    ]
                    allfi = allf[allf.index("Files:") + 1 :]
                    allfi2 = [
                        y
                        for y in set([x.split(os.sep)[0] for x in allfi if os.sep in x])
                        if str(y).isidentifier()
                    ]
                    resa2 = subprocess.run(
                        [
                            sys.executable,
                            "-c",
                            f"import {allfi2[0]};print({allfi2[0]}.__file__)",
                        ],
                        timeout=5,
                        capture_output=True,
                    ).stdout.decode("utf-8", "ignore")
                    if os.path.isabs(resa2):
                        submopa = [os.path.normpath(os.path.dirname(resa2))]
                except Exception as fa:
                    print(fa, packna)
            infopip.append([d, d2, infopo, submopa])
            print(TC(f"Success: {packna}").bg_black.fg_lightgreen)
        except Exception as fe:
            print(TC(f"Error: {packna}\n{fe}").bg_black.fg_lightred)

            continue
    return infopip


def sort_values(infopip):
    collinfos = []
    print("Sorting values _______________________")

    for infop in infopip:
        packna = ""
        try:
            try:
                deps = (
                    infop[1]
                    .loc[infop[1].level_2 == "package_name"]
                    .sort_values(by="aa_all_keys")
                    .aa_value
                )
                depsv = (
                    infop[1]
                    .loc[infop[1].level_2 == "required_version"]
                    .sort_values(by="aa_all_keys")
                    .aa_value
                )
            except Exception as fc:
                deps = []
                depsv = []
            packna = infop[0].aa_value.iloc[0]
            try:
                alldep = tuple((x for x in zip(deps, depsv)))
            except Exception as fe:
                alldep = ()
            try:
                allfo = tuple(infop[3])
            except Exception as fe:
                allfo = ()
            collectedinfos = {
                "package_name": packna,
                "deps": alldep,
                "folders": allfo,
            }
            for okey, oitem in infop[2]:
                collectedinfos[okey] = oitem
            collinfos.append(collectedinfos)

            print(TC(f"Success: {packna}").bg_black.fg_lightgreen)

        except Exception as fe:
            print(TC(f"Error: {packna}\n{fe}").bg_black.fg_lightred)

            continue
    df = pd.DataFrame(collinfos)
    df = df[df.columns[: df.columns.get_indexer(["Required-by"])[0] + 1]].copy()
    return df


def get_data_from_pipreqs(df):
    print('Executing: "pipreqs ..."_______________________')

    def get_pipreqs(x):
        packna = ""
        try:
            packna = x[0]
            resa = tuple(
                (
                    re.findall(r"(^\w+)(.*)", qq.strip())[0]
                    for qq in subprocess.run(
                        [
                            "pipreqs",
                            "--force",
                            "--mode",
                            "gt",
                            "--print",
                            x[0],
                            "--encoding",
                            "utf8",
                        ],
                        capture_output=True,
                    )
                    .stdout.strip()
                    .decode("utf-8", "ignore")
                    .splitlines()
                )
            )
            print(TC(f"Success: {packna}").bg_black.fg_lightgreen)

            return resa
        except Exception as fe:
            print(TC(f"Error: {packna}\n{fe}").bg_black.fg_lightred)
            return pd.NA

    df["pipreqs"] = df.folders.apply(lambda x: get_pipreqs(x))
    df = df.drop(columns="Name")
    df.folders = df.folders.ds_apply_ignore(pd.NA, lambda x: x[0])
    df["import_level"] = -1
    for col in df.columns:
        try:
            if isinstance(df[col][0], str):
                df[col] = df[col].astype("string").str.strip()
        except Exception as fe:
            continue
    return df


def get_module_imports(
    df, pyfile=r"C:\ProgramData\anaconda3\envs\adda\call3xxxxxxxxxxx.py"
):
    pyfile = os.path.normpath(pyfile)

    allmod = []
    try:
        finder = ModuleFinder()
        finder.run_script(pyfile)
        for name, mod in finder.modules.items():
            try:
                allmod.append(name.split(".")[0])
            except Exception:
                pass
        for babb, bab in finder.modules.items():
            try:
                allmod.append(
                    df.loc[
                        (df.folders == os.path.dirname(bab.__file__))
                    ].package_name.iloc[0]
                )
            except Exception:
                continue

    except Exception:
        with open(pyfile, mode="r", encoding="utf-8") as f:
            data = f.read()
        foundstuff = [
            r.replace("_", "-")
            for r in flatten_everything(
                [
                    x.split()
                    for x in set(
                        flatten_everything(
                            [
                                re.findall(
                                    r"""(^\s*\(?\s*\w+\s*\)?\s*$)|(\b(?:from|import).*?[^\s'"()\[\]]\w+[^\s'"^()\[\]]\b)""",
                                    x,
                                )
                                for x in data.splitlines()
                            ]
                        )
                    )
                ]
            )
            if r.isidentifier()
        ]
        allmod.extend(foundstuff)

    allmod = [x.replace("_", "-") for x in set(allmod)]

    allpa = df.loc[
        df.package_name.astype("string")
        .str.strip()
        .str.lower()
        .isin([str(x).strip().lower().replace("_", "-") for x in allmod])
    ].copy()
    allpa["import_level"] = 0
    allpa2sic = allpa.index.copy()
    co = 1
    while True:
        oldlen = len(allpa)
        newlen = oldlen
        allpackages = list(
            flatten_everything(
                allpa.Requires.ds_apply_ignore(
                    pd.NA, lambda x: [q.strip() for q in str(x).split(",")]
                ).to_list()
                + list(flatten_everything(allpa.deps.to_list()))
                + list(flatten_everything(allpa.package_name.to_list()))
                + list(flatten_everything(allpa.pipreqs.to_list()))
                + allmod
            )
        )

        allpa = df.loc[
            df.package_name.astype("string")
            .str.strip()
            .str.lower()
            .isin([str(x).strip().lower().replace("_", "-") for x in allpackages])
            & (df["import_level"] == -1)
        ]
        allpa = allpa.loc[~allpa.package_name.isin(["Ipython", "pip"])]

        df.loc[allpa.index, "import_level"] = co
        co = co + 1
        newlen = len(allpa)
        if newlen == oldlen:
            break

    allimports = df.loc[df.import_level > -1].copy()
    df.loc["import_level"] = -1
    allimports.loc[allpa2sic, "import_level"] = 0
    allimports = allimports.sort_values(by="import_level")
    return df, allimports


#


class ImportFetcher:
    def __init__(self):
        self.df = pd.DataFrame()
        self.ignored_packages = []

    def get_all_modules_in_env(self, ignore_packages=("ipython",)):
        self.ignored_packages = list(ignore_packages) if not isinstance(ignore_packages,list) else ignore_packages
        self.ignored_packages=prepare_ignored_list(self.ignored_packages)
        infopip = get_pip_tree(ignore_packages=ignore_packages)
        dfs = sort_values(infopip)
        self.df = get_data_from_pipreqs(dfs)
        self._formatdf()
        return self

    def save_all_modules_dataframe(self, path):
        path = os.path.normpath(path)
        if not os.path.exists(path):
            touch(path)
        self.df.to_dillpickle(path)
        return self

    def load_all_modules_dataframe(self, path):
        with open(path, mode="rb") as f:
            self.df = dill.loads(f.read())
        self._formatdf()
        return self

    def get_imports_from_py_file(self, pyfile):
        path = os.path.normpath(pyfile)
        _, allimports = get_module_imports(self.df.copy(), pyfile=path)
        return allimports

    def _formatdf(self):
        self.df = self.df.loc[
            ~(
                self.df.Requires.str.strip()
                .str.lower()
                .isin(self.ignored_packages)
                | self.df["Required-by"]
                .str.strip()
                .str.lower()
                .isin(self.ignored_packages)
                | self.df["package_name"]
                .str.strip()
                .str.lower()
                .isin(self.ignored_packages)
            )
        ].reset_index(drop=True)
        self.df.import_level =-1

