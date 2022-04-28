# -*- coding: utf-8 -*-
{
    'name': "行事曆展開",
    'version': '15.0.1',
    'depends': ['base', 'calendar'],
    'author': "Taiga Kuroda (mikuroda4402.github.io)",
    'category': 'extand',
    'description': """
    1.透過【行事曆展開】功能，將設定的【行事曆細項】進行展開
    2.展開時，把每個【行事曆細項】所設定的對象類型，在展開時依wizerd上的設定【行事曆展開團隊設定】內容添加到行事曆的與會者
    3.要設計【還原】功能，可以將該次【行事曆展開】動作的行事曆【一鈕刪除】
    """,

    'data': [
        'views/calendar_expand.xml',
        'views/calendar_expand_line.xml',
        'views/calendar_expand_type.xml',
        'views/calendar_handler.xml',

        'security/ir.model.access.csv',
    ],
    # data files containing optionally loaded demonstration data
}