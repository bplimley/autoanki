"""Format data for creating an Anki deck"""

import random
import time


HEADER = """
    PRAGMA foreign_keys=OFF;
    BEGIN TRANSACTION;"""
CREATE_COL = """
    CREATE TABLE col (
        id              integer primary key,
        crt             integer not null,
        mod             integer not null,
        scm             integer not null,
        ver             integer not null,
        dty             integer not null,
        usn             integer not null,
        ls              integer not null,
        conf            text not null,
        models          text not null,
        decks           text not null,
        dconf           text not null,
        tags            text not null
    );"""
INSERT_COL = """
    INSERT INTO col VALUES(1,1332961200,1398130163295,1398130163168,11,0,0,0,'{"nextPos": 1, "estTimes": true, "activeDecks": [1], "sortType": "noteFld", "timeLim": 0, "sortBackwards": false, "addToCur": true, "curDeck": 1, "newBury": true, "newSpread": 0, "dueCounts": true, "curModel": "1398130163168", "collapseTime": 1200}','{"1342697561419": {"vers": [], "name": "Basic", "tags": [], "did": 1398130078204, "usn": -1, "req": [[0, "all", [0]]], "flds": [{"name": "Front", "rtl": false, "sticky": false, "media": [], "ord": 0, "font": "Arial", "size": 12}, {"name": "Back", "rtl": false, "sticky": false, "media": [], "ord": 1, "font": "Arial", "size": 12}], "sortf": 0, "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n", "tmpls": [{"name": "Forward", "qfmt": "Template:Front", "did": null, "bafmt": "", "afmt": "Template:FrontSide\n\n
    <hr id=answer/>\n\n{{Back}}", "ord": 0, "bqfmt": ""}], "latexPost": "\\end{document}", "type": 0, "id": 1342697561419, "css": ".card {\n font-family: arial;\n font-size: 30px;\n text-align: center;\n color: black;\n background-color: white;\n}\n\n.card1 { background-color: #FFFFFF; }", "mod": 1398130117}}','{"1": {"desc": "", "name": "Default", "extendRev": 50, "usn": 0, "collapsed": false, "newToday": [0, 0], "timeToday": [0, 0], "dyn": 0, "extendNew": 10, "conf": 1, "revToday": [0, 0], "lrnToday": [0, 0], "id": 1, "mod": 1398130160}, "1398130078204": {"desc": "", "name": "tatoeba", "extendRev": 50, "usn": -1, "collapsed": false, "newToday": [754, 0], "timeToday": [754, 0], "dyn": 0, "extendNew": 10, "conf": 1, "revToday": [754, 0], "lrnToday": [754, 0], "id": 1398130078204, "mod": 1398130140}}','{"1": {"name": "Default", "replayq": true, "lapse": {"leechFails": 8, "minInt": 1, "delays": [10], "leechAction": 0, "mult": 0}, "rev": {"perDay": 100, "fuzz": 0.05, "ivlFct": 1, "maxIvl": 36500, "ease4": 1.3, "bury": true, "minSpace": 1}, "timer": 0, "maxTaken": 60, "usn": 0, "new": {"perDay": 20, "delays": [1, 10], "separate": true, "ints": [1, 4, 7], "initialFactor": 2500, "bury": true, "order": 1}, "mod": 0, "id": 1, "autoplay": true}}','{}');"""
CREATE_NOTES = """
    CREATE TABLE notes (
        id              integer primary key,   /* 0 */
        guid            text not null,         /* 1 */
        mid             integer not null,      /* 2 */
        mod             integer not null,      /* 3 */
        usn             integer not null,      /* 4 */
        tags            text not null,         /* 5 */
        flds            text not null,         /* 6 */
        sfld            integer not null,      /* 7 */
        csum            integer not null,      /* 8 */
        flags           integer not null,      /* 9 */
        data            text not null          /* 10 */
    );"""
CREATE_CARDS = """
    CREATE TABLE cards (
        id              integer primary key,   /* 0 */
        nid             integer not null,      /* 1 */
        did             integer not null,      /* 2 */
        ord             integer not null,      /* 3 */
        mod             integer not null,      /* 4 */
        usn             integer not null,      /* 5 */
        type            integer not null,      /* 6 */
        queue           integer not null,      /* 7 */
        due             integer not null,      /* 8 */
        ivl             integer not null,      /* 9 */
        factor          integer not null,      /* 10 */
        reps            integer not null,      /* 11 */
        lapses          integer not null,      /* 12 */
        left            integer not null,      /* 13 */
        odue            integer not null,      /* 14 */
        odid            integer not null,      /* 15 */
        flags           integer not null,      /* 16 */
        data            text not null          /* 17 */
    );"""
INSERT_CARDS_EX = """
    INSERT INTO cards VALUES(1398130110964,1398130088495,1398130078204,0,1398130110,-1,0,0,484332854,0,0,0,0,0,0,0,0,);
    INSERT INTO cards VALUES(1398130117922,1398130111274,1398130078204,0,1398130117,-1,0,0,353754516,0,0,0,0,0,0,0,0,);"""
CREATE_REVLOG = """
    CREATE TABLE revlog (
        id              integer primary key,
        cid             integer not null,
        usn             integer not null,
        ease            integer not null,
        ivl             integer not null,
        lastIvl         integer not null,
        factor          integer not null,
        time            integer not null,
        type            integer not null
    );"""
CREATE_GRAVES = """
    CREATE TABLE graves (
        usn             integer not null,
        oid             integer not null,
        type            integer not null
    );"""
FOOTER = """
    ANALYZE sqlite_master;
    INSERT INTO "sqlite_stat1" VALUES('col',NULL,'1');
    CREATE INDEX ix_notes_usn on notes (usn);
    CREATE INDEX ix_cards_usn on cards (usn);
    CREATE INDEX ix_revlog_usn on revlog (usn);
    CREATE INDEX ix_cards_nid on cards (nid);
    CREATE INDEX ix_cards_sched on cards (did, queue, due);
    CREATE INDEX ix_revlog_cid on revlog (cid);
    CREATE INDEX ix_notes_csum on notes (csum);
    COMMIT;
    """

CONF = """{
    "nextPos":1,
    "estTimes":true,
    "activeDecks":[
        1
    ],
    "sortType":"noteFld",
    "timeLim":0,
    "sortBackwards":false,
    "addToCur":true,
    "curDeck":1,
    "newBury":true,
    "newSpread":0,
    "dueCounts":true,
    "curModel":"1398130163168",
    "collapseTime":1200
    }"""
MODELS = """{
    "1342697561419":{
        "vers":[

        ],
        "name":"Basic",
        "tags":[

        ],
        "did":1398130078204,
        "usn":-1,
        "req":[
            [
                0,
                "all",
                [
                    0
                ]
            ]
        ],
        "flds":[
            {
                "name":"Front",
                "rtl":false,
                "sticky":false,
                "media":[

                ],
                "ord":0,
                "font":"Arial",
                "size":12
            },
            {
                "name":"Back",
                "rtl":false,
                "sticky":false,
                "media":[

                ],
                "ord":1,
                "font":"Arial",
                "size":12
            }
        ],
        "sortf":0,
        "latexPre":"\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
        "tmpls":[
            {
                "name":"Forward",
                "qfmt":"{{Front}}",
                "did":null,
                "bafmt":"",
                "afmt":"{{FrontSide}}\n\n
                    <hr id=answer/>\n\n{{Back}}",
                "ord":0,
                "bqfmt":""
            }
        ],
        "latexPost":"\\end{document}",
        "type":0,
        "id":1342697561419,
        "css":".card {\n font-family: arial;\n font-size: 30px;\n text-align: center;\n color: black;\n white;\n}\n\n.card1 { #FFFFFF; }",
        "mod":1398130117
    }
    }"""
DECKS = """{
    "1":{
        "desc":"",
        "name":"Default",
        "extendRev":50,
        "usn":0,
        "collapsed":false,
        "newToday":[
            0,
            0
        ],
        "timeToday":[
            0,
            0
        ],
        "dyn":0,
        "extendNew":10,
        "conf":1,
        "revToday":[
            0,
            0
        ],
        "lrnToday":[
            0,
            0
        ],
        "id":1,
        "mod":1398130160
    },
    "1398130078204":{
        "desc":"",
        "name":"tatoeba",
        "extendRev":50,
        "usn":-1,
        "collapsed":false,
        "newToday":[
            754,
            0
        ],
        "timeToday":[
            754,
            0
        ],
        "dyn":0,
        "extendNew":10,
        "conf":1,
        "revToday":[
            754,
            0
        ],
        "lrnToday":[
            754,
            0
        ],
        "id":1398130078204,
        "mod":1398130140
    }
    }"""
DCONF = """{
    "1":{
        "name":"Default",
        "replayq":true,
        "lapse":{
            "leechFails":8,
            "minInt":1,
            "delays":[
                10
            ],
            "leechAction":0,
            "mult":0
        },
        "rev":{
            "perDay":100,
            "fuzz":0.05,
            "ivlFct":1,
            "maxIvl":36500,
            "ease4":1.3,
            "bury":true,
            "minSpace":1
        },
        "timer":0,
        "maxTaken":60,
        "usn":0,
        "new":{
            "perDay":20,
            "delays":[
                1,
                10
            ],
            "separate":true,
            "ints":[
                1,
                4,
                7
            ],
            "initialFactor":2500,
            "bury":true,
            "order":1
        },
        "mod":0,
        "id":1,
        "autoplay":true
    }
    }"""
SEP = bytes([31])


def random_index():
    """Generate a random integer in the range for Anki indices."""

    # examples at http://decks.wikia.com/wiki/Anki_APKG_format_documentation
    # 1398130088495: 13 digits, ~2^40
    # I will use a 32 bit number here.

    return random.randint(2**32)


def random_guid():
    """Generate a random string appropriate for an Anki GUID."""

    # it is 10 digits long, alphanumberic with symbols

    ascii_list = [random.randint(33, 126) for _ in range(10)]
    return bytes(ascii_list)


def timestamp():
    """Return Unix timestamp, seconds since 1970."""

    ts = int(time.time())
    return ts


def insert_note(model_id, tags, front, back, flags=0):
    """Create a SQL command for a new note."""

    note_id = str(random_index())
    note_guid = random_guid()
    note_mid = str(model_id)
    note_mod = str(timestamp())
    note_usn = '-1'
    note_tags = tags
    note_flds = SEP.join((front, back))
    note_sfld = front
    note_csum = sha1()
    note_flags = str(flags)
    note_data = ''

    note_fields = [
        note_id,
        note_guid,
        note_mid,
        note_mod,
        note_usn,
        note_tags,
        note_flds,
        note_sfld,
        note_csum,
        note_flags,
        note_data
    ]

    cmd = "INSERT INTO notes VALUES({});".format(','.join(note_fields))
    return cmd


def insert_card(note_id, deck_id, note_mod, ):
    """Create a SQL command for a new card."""

    card_id = random_index()
    card_nid = note_id
    card_did = deck_id
    card_ord = '0'
    card_mod = note_mod
    card_usn = '-1'
    card_type = '0'
    card_queue = '0'
    card_due = '484332854'
    card_ivl = '0'
    card_factor = '0'
    card_reps = '0'
    card_lapses = '0'
    card_left = '0'
    card_odue = '0'
    card_odid = '0'
    card_flags = '0'
    card_data = ''

    card_fields = [
        card_id,
        card_nid,
        card_did,
        card_ord,
        card_mod,
        card_usn,
        card_type,
        card_queue,
        card_due,
        card_ivl,
        card_factor,
        card_reps,
        card_lapses,
        card_left,
        card_odue,
        card_odid,
        card_flags,
        card_data
    ]

    cmd = "INSERT INTO cards VALUES({});".format(','.join(card_fields))
    return cmd
