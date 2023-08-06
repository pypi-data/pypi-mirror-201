import os
from functools import reduce
from string import printable
import regex as re
import io
import pandas as pd
from tolerant_isinstance import isinstance_tolerant
import requests
from collections import defaultdict

allsi = [x.encode() for x in printable[:-4].replace('"', "").replace("'", "")]


def convert_to_normal_dict(di):
    if isinstance_tolerant(di, defaultdict):
        di = {k: convert_to_normal_dict(v) for k, v in di.items()}
    return di


def groupBy(key, seq, continue_on_exceptions=True, withindex=True, withvalue=True):
    indexcounter = -1

    def execute_f(k, v):
        nonlocal indexcounter
        indexcounter += 1
        try:
            return k(v)
        except Exception as fa:
            if continue_on_exceptions:
                return "EXCEPTION: " + str(fa)
            else:
                raise fa

    # based on https://stackoverflow.com/a/60282640/15096247
    if withvalue:
        return convert_to_normal_dict(
            reduce(
                lambda grp, val: grp[execute_f(key, val)].append(
                    val if not withindex else (indexcounter, val)
                )
                or grp,
                seq,
                defaultdict(list),
            )
        )
    return convert_to_normal_dict(
        reduce(
            lambda grp, val: grp[execute_f(key, val)].append(indexcounter) or grp,
            seq,
            defaultdict(list),
        )
    )


def group_values_in_flattened_nested_iter_and_count(
    seq, continue_on_exceptions=True, withindex=False, withvalue=True
):
    li = groupBy(
        key=lambda x: x,
        seq=seq,
        continue_on_exceptions=continue_on_exceptions,
        withindex=withindex,
        withvalue=withvalue,
    )
    for key, item in li.copy().items():
        li[key] = len(item)
    return li


def get_csv_sep(file):
    data = _openfile(file)

    probsep = defaultdict(list)
    for d in data.splitlines():
        for a in allsi:
            allco = d.count(a)
            if allco != 0:
                probsep[a].append(allco)
    alltoga = []

    for key, item in probsep.items():
        sora = group_values_in_flattened_nested_iter_and_count(item)
        sora = tuple(sorted([x[1] for x in sora.items()]))[-1]
        alltoga.append((sora, key))
    pros = tuple(sorted(alltoga))[-1][1]
    return pros


def _openfile(key):

    if os.path.exists(key):
        try:
            with open(key, mode="rb") as f:
                data = f.read()
            return data
        except Exception as fe:
            print(fe)
            return data
    else:
        try:
            with requests.get(url=key) as response:
                data = response.content
        except Exception as fe:
            pass
    return data


def read_balky_csv_files(
    csvfiles,
    encoding="utf-8",
    sep=None,
    regexremove=(rb"^\s*#\s+.*$",),
    filepathcolumn="file",
    regex_flags=None,
    *args,
    **kwargs,
):
    linesplit = b"\n"

    alldfs = []
    oldsep = sep
    if not isinstance_tolerant(csvfiles, list):
        try:
            csvfiles = [csvfiles]
        except Exception:
            pass
    if not isinstance_tolerant(sep, (None, bytes)):
        try:
            sep = sep.encode()
        except Exception:
            pass
    regexremove2 = []
    if regexremove:
        for r in regexremove:
            if not isinstance_tolerant(r, bytes):
                r = r.encode()
            if regex_flags:
                regexremove2.append(re.compile(r, flags=regex_flags))
            else:
                regexremove2.append(re.compile(r))
        regexremove = regexremove2.copy()
    foax = b""
    for key in csvfiles:
        if isinstance_tolerant(oldsep, None):
            sep = get_csv_sep(key)
        alllength = defaultdict(list)
        alldaxa = []
        try:
            data = _openfile(key)
            for q in data.splitlines():
                g = len(q.strip().split(sep))
                if g < 2:

                    continue

                if regexremove:
                    for regx in regexremove:
                        q = regx.sub(b"", q).strip()
                        if q != b"":
                            alllength[g].append(q)
                else:
                    alllength[g].append(q)
            alldaxa = list(sorted(alllength.items(), key=lambda x: len(x[1])))[-1][1]
            foax = linesplit.join(alldaxa)
            foax2 = io.BytesIO(foax)
            df = pd.read_table(
                foax2,
                encoding=encoding,
                header=None,
                skip_blank_lines=True,
                sep=sep.decode(),
                *args,
                **kwargs,
            )
            df[filepathcolumn] = key
            alldfs.append(df.copy())
        except Exception as fe:
            try:
                bline = int(str(fe).strip().split()[-1])
            except Exception as bux:

                continue
            if foax:
                while alldaxa:
                    try:
                        del alldaxa[bline - 1]
                        foax = linesplit.join(alldaxa)
                        foax2 = io.BytesIO(foax)
                        df = pd.read_table(
                            foax2,
                            encoding=encoding,
                            header=None,
                            skip_blank_lines=True,
                            sep=sep.decode(),
                            *args,
                            **kwargs,
                        )
                        df[filepathcolumn] = key
                        alldfs.append(df.copy())
                        break
                    except Exception as fea:
                        try:
                            bline = int(str(fea).strip().split()[-1])
                            continue
                        except Exception as feax:
                            break

    if len(alldfs) > 1:
        return pd.concat(alldfs, ignore_index=True).dropna().reset_index(drop=True)
    else:
        return alldfs[0]
