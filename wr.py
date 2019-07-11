#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import json


def write_results(results):
    res = open('results.json', 'w', encoding='utf-8')
    writer = res.write
    writer(json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False))


def read_results():
    res = open('results.json', 'r', encoding='utf-8')
    reader = res.read()
    return json.loads(reader)


def clear(id):
    results = read_results()
    results.pop(id)
    write_results(results)


def read_problems():
    pr = open('problems/problems.json', 'r', encoding='utf-8')
    reader = pr.read()
    return json.loads(reader)


def write_problems(problems):
    res = open('problems/problems.json', 'w', encoding='utf-8')
    writer = res.write
    writer(json.dumps(problems, indent=2, ensure_ascii=False))


def read_feedback():
    fb = open('feedback.json', 'r', encoding='utf-8')
    reader = fb.read()
    return json.loads(reader)


def write_feedback(feedback):
    fb = open('feedback.json', 'w', encoding='utf-8')
    writer = fb.write
    writer(json.dumps(feedback, ensure_ascii=False))


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def read_admins():
    fb = open('admins.json', 'r', encoding='utf-8')
    reader = fb.read()
    return json.loads(reader)


def write_admins(admins):
    fb = open('admins.json', 'w', encoding='utf-8')
    writer = fb.write
    writer(json.dumps(admins, ensure_ascii=False))


def group_consecutives(vals, step=1):
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    for part in result:
        try:
            if len(part) == 2:
                i = result.index(part)
                result[i] = part[0]
                result.insert(i+1, part[1])
            elif len(part) == 1:
                i = result.index(part)
                result[i] = part[0]
        except TypeError:
            pass
    return result
