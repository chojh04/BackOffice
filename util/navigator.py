# -*- coding: utf-8 -*-

menuItems = [
        {
            "title": '거래처 관리',
            "icon": 'fa-edit',
            "subMenu": [
                {
                    "title": '대표 거래처 등록',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'merchants.representMerchantReg'
                },
                {
                    "title": '거래처 조회',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'merchants.merchantInq'
                },
            ]
        },
#         {
#             "title": '카드 관리',
#             "icon": 'fa-edit',
#             "subMenu": [
#                 {
#                     "title": '팝카드 상세 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#                 {
#                     "title": '팝카드 사용 내역 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#                 {
#                     "title": 'KPC 카드 상세 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#                 {
#                     "title": 'KPC 카드 상세 내역 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#             ]
#         },
#         {
#             "title": '쿠폰 관리',
#             "icon": 'fa-edit',
#             "subMenu": [
#                 {
#                     "title": '쿠폰 상세 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#                 {
#                     "title": '쿠폰 사용 내역 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#                 {
#                     "title": '쿠폰 상품 등록',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#             ]
#         },
#         {
#             "title": '매출 관리',
#             "icon": 'fa-edit',
#             "subMenu": [
#                 {
#                     "title": '매출 등록',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#                 {
#                     "title": '매출 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#                 {
#                     "title": '매출 통계',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#             ]
#         },
#         {
#             "title": '대사 관리',
#             "icon": 'fa-edit',
#             "subMenu": [
#                 {
#                     "title": '결제 대사 내역 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#                 {
#                     "title": '충전 대사 내역 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#                 {
#                     "title": '판매 대사 내역 조회',
#                     "icon": 'fa-plus-square-o',
#                     "routerLink": 'backofficeindexview.blank',
#                 },
#             ]
#         },
        {
            "title": '정산 내역 관리',
            "icon": 'fa-edit',
            "subMenu": [
                {
                    "title": '결제 정산 내역 조회',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'approvals.payments',
                },
                {
                    "title": '충전 정산 내역 조회',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'approvals.chargements',
                },
                {
                    "title": '판매 정산 내역 조회',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'approvals.salements',
                },
            ]
        },
        {
            "title": '정산 등록 관리',
            "icon": 'fa-edit',
            "subMenu": [
                {
                    "title": '정산 명세서 조회',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'billings.index',
                },
                {
                    "title": '정산 명세서 등록/관리',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'billings.billings',
                },
            ]
        },
        {
            "title": '시스템 관리',
            "icon": 'fa-edit',
            "subMenu": [
                {
                    "title": '사용자 등록/관리',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'systemmng.employees',
                },
                {
                    "title": '사용자 권한 관리',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'systemmng.userMenuMng',
                },
                {
                    "title": '시스템 코드 등록/관리',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'backofficeindexview.blank',
                },
                {
                    "title": '메뉴 관리',
                    "icon": 'fa-plus-square-o',
                    "routerLink": 'systemmng.menusMng',
                },
            ]
        },
    ]