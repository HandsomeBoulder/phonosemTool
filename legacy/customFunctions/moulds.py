from fuzzywuzzy import fuzz

# фонотипы русского языка
phonotypes = {
    '0' : ('a', 'i', 'o', 'e', 'u', 'ы'),  # voc гласный
    '1' : ('b', 'd', 'g'),  # plos(st) взрывной звонкий
    '2' : ('p', 't', 'k'),  # plos(wk) взрывной глухой
    '3' : ('v', 'z', 'ž', 'j'),  # fric(st) фрикативный звонкий
    '4' : ('f', 's', 'š', 'x'),  # fric(wk) фрикативный глухой
    '5' : ('c', 'č'),  # affr аффриката
    '6' : ('r'),  # R вибрант
    '7' : ('m'),  # son(lab) сонорный губной
    '8' : ('n'),  # son(nas) сонорный носовой
    '9' : ('l'),  # son(lat) сонорный боковой
}

# Шаблоны для русских звукосимволизмов
symbolTemplates = {
    'SHM' : ('k', 'g', 'x'),  # CONS(vel) заднеязычные 
    'CLC' : ('pl', 'kl', 'tl', 'bl', 'dl', 'gl'),  # PLOS + SON(lab)
    'CHW' : ('c', 'č', 'b', 'p', 'm'),  # AFFR, CONS(lab)
    'SCK' : ('b', 'p', 'm', 'f', 's', 'š', 'x'),  # CONS(lab), FRIC(wk)
    'BIT' : ('d', 't', 'z', 's', 'l', 'n', 'c'),  # CONS(den), SON(nas)
    'SPT' : ('b', 'p', 'v', 'f'),  # PLOS(lab), FRIC(lab)
    'GLP' : ('l'),  # SON(lat)
    'CHK' : ('k', 'g', 'x'), # CONS(vel)
    'LCK' : ('l'),  # SON(lat)
    'VMT' : ('k', 'g', 'x'),  # CONS(vel)
    'SMC' : ('b', 'p', 'm'),  # CONS(lab)
    'SLM' : ('p', 't', 'k', 'b', 'd', 'g')  # PLOS
}

# шаблоны для русских звукоподражаний
onomTemplates = {
    # Инстанты
    'I' : [
        {
            # plos/affr + voc + plos/affr
            'blueprint' : ('101', '202', '505', '102', '105', '201', '205', '501', '502'),
            'essentials' : (r'0[125]',),
            'penalty' : ''
        }
    ],
    # Континуанты
    'C' : [
        {
            # plos + voc + plos
            'blueprint' : ('101', '202', '102', '201'),
            'essentials' : '0',
            'penalty' : ''
        },
        {
            # [plos + voc +] fric(wk) [+ voc]
            'blueprint' : ('1040', '2040', '104', '204', '40'),
            'essentials' : ('4',),
            'penalty' : ''
        },
        {
            # [plos +] fric(st) [+ voc + fric(st)]
            'blueprint' : ('1303', '2303', '13', '23', '303'),
            'essentials' : ('3',),
            'penalty' : ''
        }
    ],
    # Фреквентативы
    'F' : [
        {
            # plos + voc + R
            'blueprint' : ('106', '206'),
            'essentials' : ('6',),
            'penalty' : 0.3
        },
        {
            # plos + R
            'blueprint' : ('16', '26'),
            'essentials' : ('6',),
            'penalty' : 0.3
        }
    ],
    # Инстанты-континуанты
    'IC' : [
        {
            # PLOS [+ SON] + VOC + SON
            'blueprint' : ('107', '108', '109', '207', '208', '209', '1707', '1708', '1709', '1807', '1808', '1809', '1907', '1908', '1909', '2707', '2708', '2709', '2807', '2808', '2809', '2907', '2908', '2909'),
            'essentials' : (r'[12].*[789]',),
            'penalty' : 0.5
        },
        {
            # PLOS [+ VOC] + FRIC
            'blueprint' : ('103', '104', '203', '204', '13', '14', '23', '24'),
            'essentials' : (r'[12].*[34]',),
            'penalty' : 0.5
        },
        {
            # FRIC(wk) + SON(lat/lab) + VOC + [FRIC(wk)] + PLOS(wk)
            'blueprint' : ('47042', '49042', '4702', '4902', '042'),
            'essentials' : (r'4[79].*2',),
            'penalty' : ''
        },
        {
            # AFFR + FRIC(wk) + VOC + [FRIC(wk)] + PLOS(wk)
            'blueprint' : ('54042', '5402'),
            'essentials' : (r'54.*2',),
            'penalty' : ''
        },
        {
            # [FRIC(st)] + FRIC(st) + VOC + PLOS(wk)
            'blueprint' : ('3302', '302'),
            'essentials' : (r'3.*2',),
            'penalty' : ''
        },
        {
            # FRIC(wk)/AFFR + SON
            'blueprint' : ('47', '48', '49', '57', '58', '59'),
            'essentials' : (r'[45][789]',),
            'penalty' : ''
        },
        {
            # FRIC(st) + PLOS + VOC + SON(lab)
            'blueprint' : ('3107', '3207'),
            'essentials' : (r'31.*7',),
            'penalty' : ''
        }
    ],
    # Фреквентативы-инстанты
    'FI' : [
        {
            # FRIC + R + VOC [+ FRIC] + PLOS
            'blueprint' : ('36031', '36032', '3601', '3602', '36041', '36042', '46031', '46032', '46041', '46042', '4601', '4602'),
            'essentials' : (r'(?=.*6)(?=.*[12])',),
            'penalty' : 0.5
        },
        {
            # PLOS + R + VOC [+ FRIC] + PLOS
            'blueprint' : ('16031', '16032', '1601', '1602', '16041', '16042', '26031', '26032', '26041', '26042', '2601', '2602'),
            'essentials' : (r'(?=.*6)(?=.*[12])',),
            'penalty' : 0.5
        }
    ],
    # Фреквентативы-континуанты
    'FC' : [
        {
            # PLOS + VOC + R
            'blueprint' : ('106', '206'),
            'essentials' : (r'(?=.*6)(?=.*0)',),
            'penalty' : 0.5
        },
        {
            # FRIC(wk) + VOC + R (+ PLOS); FRIC(st) + VOC + R
            'blueprint' : ('4061', '4062', '306'),
            'essentials' : (r'(?=.*6)(?=.*[34])',),
            'penalty' : 0.5
        }
    ],
    # Фреквентативы-инстанты-континуанты
    'FIC' : [
        {
            # PLOS + R + VOC + SON(lab/nas)
            'blueprint' : ('1607', '1608', '2607', '2608'),
            'essentials' : (r'6.*[78]',),
            'penalty' : 0.5
        },
        {
            # PLOS/FRIC(wk) + R + VOC + FRIC(wk)/AFFR
            'blueprint' : ('1604', '1605', '2604', '2605', '4604', '4605'),
            'essentials' : (r'6.*[45]',),
            'penalty' : 0.5
        },
        {
            # FRIC + VOC + R + PLOS(wk)
            'blueprint' : ('4062', '3062'),
            'essentials' : (r'[45].*6',),
            'penalty' : 0.5
        }
    ]
}