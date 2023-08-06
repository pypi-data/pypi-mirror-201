from datetime import datetime


def query_response_handle(marketdatas):

    if marketdatas:
        # etf
        if marketdatas[0].get('mdETFBasicInfo'):
            result = get_etf_info_handle(marketdatas)
            return result
        # 静态信息
        if marketdatas[0].get('mdConstant'):
            result = get_basic_info_handle(marketdatas)
            return result


def get_etf_info_handle(marketdatas):
    etf_map = {
        'htsc_code': 'HTSCSecurityID', 'name': 'Symbol', 'creation_name': 'CreationSymbol', 'creation_id': 'CreationID',
        'redemption_id': 'RedemptionID', 'redemption_name': 'RedemptionSymbol',
        'creation_redemption_capital_id': 'CreationRedemptionCapitalID',
        'creation_redemption_capital_name': 'CreationRedemptionCapitalSymbol',
        'cross_source_capital_id': 'CrossSourceCapitalID', 'cross_source_capital_name': 'CrossSourceCapitalSymbol',
        'min_pr_units': 'CreationRedemptionUnit', 'esti_cash': 'EstimateCashComponent', 'con_num': 'RecordNum',
        'trading_day': 'TradingDay', 'cash_dif': 'CashComponent', 'min_pr_aset': 'NAVperCU', 'net_asset': 'NAV',
        'cross_market': 'CrossMarket',
        'fund_company': 'FundManagementCompany', 'underlying_id': 'UnderlyingSecurityID',
        'underlying_exchange': 'UnderlyingSecurityIDSource', 'purchase_cap': 'CreationLimit',
        'redemption_cap': 'RedemptionLimit',
        'purchase_cap_per_user': 'CreationLimitPerUser', 'redemption_cap_per_user': 'RedemptionLimitPerUser',
        'net_purchase_cap': 'NetCreationLimit', 'net_redemption_cap': 'NetRedemptionLimit',
        'net_purchase_cap_per_user': 'NetCreationLimitPerUser',
        'net_redemption_cap_per_user': 'NetRedemptionLimitPerUser',

    }

    exchange_code_map = {101: 'XSHG', 102: 'XSHE'}
    security_type_map = {
        1: 'index',
        2: 'stock',
        3: 'fund',
        4: 'bond',
        7: 'option',
        8: 'future',
    }

    result = []
    for marketdata in marketdatas:
        etf_data = marketdata['mdETFBasicInfo']
        md_time = datetime.strptime(str(etf_data['MDDate']) + str(etf_data['MDTime']), '%Y%m%d%H%M%S%f')
        md_time = datetime.strftime(md_time, '%Y-%m-%d %H:%M:%S.%f')
        exchange = exchange_code_map.get(etf_data.get("securityIDSource"))
        security_type = security_type_map.get(etf_data.get('securityType'))
        cash_sub_up_limit = etf_data['MaxCashRatio'] * 100

        if etf_data.get('IsPublish'):
            is_iopv = 1
        else:
            is_iopv = 0

        if etf_data.get('IsAllowCreation'):
            isallowcreation = True
        else:
            isallowcreation = False

        if etf_data.get('IsAllowRedemption'):
            isallowredemption = True
        else:
            isallowredemption = False

        if isallowcreation and isallowredemption:
            pr_permit = "1"
        elif isallowcreation and not isallowredemption:
            pr_permit = "2"
        elif not isallowcreation and isallowredemption:
            pr_permit = "3"
        else:
            pr_permit = "0"

        etf_result = None
        if exchange == 'XSHG':
            etf_result = {'htsc_code': '', 'name': '', 'time': '', 'exchange': '', 'security_type': '',
                          'creation_id': '', 'creation_name': '', 'redemption_id': '', 'redemption_name': '',
                          'creation_redemption_capital_id': '', 'creation_redemption_capital_name': '',
                          'cross_source_capital_id': '', 'cross_source_capital_name': '', 'min_pr_units': '',
                          'esti_cash': '', 'cash_sub_up_limit': '', 'is_iopv': '', 'pr_permit': '', 'con_num': '',
                          'trading_day': '', 'cash_dif': '', 'min_pr_aset': '', 'net_asset': '', 'cross_market': ''}

        elif exchange == 'XSHE':
            etf_result = {'htsc_code': '', 'name': '', 'time': '', 'exchange': '', 'security_type': '',
                          'fund_company': '', 'underlying_id': '', 'underlying_exchange': '', 'min_pr_units': '',
                          'esti_cash': '', 'cash_sub_up_limit': '', 'is_iopv': '', 'pr_permit': '', 'con_num': '',
                          'trading_day': '', 'cash_dif': '', 'min_pr_aset': '', 'net_asset': '', 'purchase_cap': '',
                          'redemption_cap': '', 'purchase_cap_per_user': '', 'redemption_cap_per_user': '',
                          'net_purchase_cap': '', 'net_redemption_cap': '', 'net_purchase_cap_per_user': '',
                          'net_redemption_cap_per_user': '', 'cross_market': ''}

        etf_result['time'] = md_time
        etf_result['exchange'] = exchange
        etf_result['security_type'] = security_type
        etf_result['cash_sub_up_limit'] = cash_sub_up_limit
        etf_result['is_iopv'] = is_iopv
        etf_result['pr_permit'] = pr_permit

        for key in list(etf_result.keys()):

            if not etf_result[key]:
                value = etf_data.get(etf_map.get(key))
                if key == 'trading_day' and value:
                    etf_result[key] = '{}-{}-{}'.format(str(value)[:4], str(value)[4:6], str(value)[6:])
                else:
                    etf_result[key] = value

        result.append(etf_result)

    return result


def get_basic_info_handle(marketdatas):

    basic_info_map = {
        # 指数
        'htsc_code': 'HTSCSecurityID', 'name': 'Symbol', 'prev_close': 'PreClosePx',
        # 股票
        'security_sub_type': 'SecuritySubType', 'listing_date': 'ListDate', 'total_share': 'OutstandingShare',
        'listed_share': 'PublicFloatShareQuantity', 'trading_phase': 'TradingPhaseCode',
         'max': 'MaxPx', 'min': 'MinPx', 'lot_size': 'LotSize', 'tick_size': 'TickSize',
        'buy_qty_unit': 'BuyQtyUnit', 'sell_qty_unit': 'SellQtyUnit',
        'hk_spread_table_code': 'HKSpreadTableCode', 'sh_hk_connect': 'ShHkConnect', 'sz_hk_connect': 'SzHkConnect',
        'is_vcm': 'VCMFlag', 'is_cas': 'CASFlag', 'is_pos': 'POSFlag',
        'buy_qty_upper_limit': 'BuyQtyUpperLimit', 'sell_qty_upper_limit': 'SellQtyUpperLimit',
        # 基金
        'buy_qty_lower_limit': 'BuyQtyLowerLimit', 'sell_qty_lower_limit': 'SellQtyLowerLimit',
        # 债券
        'expire_date': 'ExpireDate', 'base_contract_id': 'BaseContractID'
    }

    exchange_code_map = {
                            101: 'XSHG',  # 上交所
                            102: 'XSHE',  # 深交所
                            703: 'CSI',  # 中证指数
                            702: 'CNI',  # 国证指数
                            106: 'XBSE',  # 北交所
                            204: 'HKSC',  # 港股通
                            205: 'HGHQ',  # H股全流通
                        }

    security_type_map = {
                            1: 'index',
                            2: 'stock',
                            3: 'fund',
                            4: 'bond',
                        }

    security_sub_type_map = {1001: '交易所指数', 1002: '亚洲指数', 1003: '国际指数', 1004: '系统分类指数', 1005: '用户分类指数', 1006: '期货指数', 1007: '指数现货', 1101: '申万一级行业指数', 1102: '申万二级行业指数', 1103: '申万三级行业指数', 1201: '自定义指数 - 概念股指数', 1202: '自定义指数 - 行业指数', 1203: '自定义指数 - 策略指数', 2001: 'A股（主板）', 2002: '中小板股', 2003: '创业板股', 2004: 'B股', 2005: '国际板', 2006: '战略新兴板', 2007: '新三板', 2008: '港股主板', 2009: '港股创业板', 2010: '香港上市NASD股票', 2011: '香港扩展板块股票', 2012: '美股', 2013: '美国存托凭证ADR', 2014: '英股', 2016: '两网公司及退市公司A股（股转系统）', 2017: '两网公司及退市公司B股（股转系统）', 2018: '股转系统挂牌公司股票', 2019: 'B转H股/H股全流通', 2020: '主板、中小板存托凭证', 2021: '创业板存托凭证', 2022: '北交所（精选层）', 2023: '股转系统基础层', 2024: '股转系统创新层', 2100: '优先股', 2200: '科创板', 3001: '基金（封闭式）', 3002: '未上市开放基金（仅申赎）', 3003: '上市开放基金LOF', 3004: '交易型开放式指数基金ETF', 3005: '分级子基金', 3006: '扩展板块基金（港）', 3007: '仅申赎基金', 4001: '政府债券（国债）', 4002: '企业债券', 4003: '金融债券', 4004: '公司债', 4005: '可转债券', 4006: '私募债', 4007: '可交换私募债', 4008: '证券公司次级债', 4009: '证券公司短期债', 4010: '可交换公司债', 4011: '债券预发行', 4012: '固收平台特定债券', 5001: '质押式国债回购', 5002: '质押式企债回购', 5003: '买断式债券回购', 5004: '报价回购', 5005: '质押式协议回购', 5006: '三方回购', 6001: '企业发行权证', 6002: '备兑权证', 6003: '牛证（moo-cow）', 6004: '熊证（bear）', 7001: '个股期权', 7002: 'ETF期权', 8001: '指数期货', 8002: '商品期货', 8003: '股票期货', 8004: '债券期货', 8005: '同业拆借利率期货', 8006: 'Exchange Fund Note Futures外汇基金票据期货', 8007: 'Exchange For Physicals期货转现货', 8009: 'Exchange of Futures For Swaps', 8010: '指数期货连线CX', 8011: '指数期货连线CC', 8012: '商品期货连线CX', 8013: '商品期货连线CC', 8014: '股票期货连线CX', 8015: '股票期货连线CC', 8016: '期现差价线', 8017: '跨期差价线', 8018: '外汇期货', 8019: '贵金属期货', 8100: '上海国际能源交易中心（INE）', 9000: '汇率', 10000: '利率', 11000: '贵金属', 12001: '国债（银行间市场TB）', 12002: '政策性金融债（银行间市场PFB）', 12003: '央行票据（银行间市场CBB）', 12004: '政府支持机构债券（银行间市场GBAB）', 12005: '短期融资券（银行间市场CP）', 12006: '中期票据（银行间市场MTN）', 12007: '企业债（银行间市场CORP）', 12008: '同业存单（银行间市场CD）', 12009: '超短期融资券（银行间市场SCP）', 12010: '资产支持证券（银行间市场ABS）', 12999: '其它（银行间市场Other）', 13002: '商品现货', 13018: '外汇现货', 13019: '贵金属期货', 99001: 'A股新股申购', 99002: 'A股增发', 99010: '集合资产管理计划', 99020: '资产支持证券', 99030: '资金前端控制'}

    trading_phase_map = {'0': '开盘前，启动', '1': '开盘集合竞价', '2': '开盘集合竞价阶段结束到连续竞价阶段开始之前', '3': '连续竞价', '4': '中午休市', '5': '收盘集合竞价', '6': '已闭市', '7': '盘后交易', '8': '临时停牌', '9': '波动性中断', '10': '竞价交易收盘至盘后固定价格交易之前', '11': '盘后固定价格交易'}

    # 需要除的键
    divisor_list = ['prev_close', 'max', 'min']

    result = []
    for marketdata in marketdatas:
        constant_data = marketdata['mdConstant']

        divisor = pow(10, int(constant_data.get("DataMultiplePowerOf10")))  # 除数

        md_time = datetime.strptime(str(constant_data['MDDate']), '%Y%m%d')
        md_time = datetime.strftime(md_time, '%Y-%m-%d')
        exchange = exchange_code_map.get(constant_data.get("securityIDSource"))
        security_type = security_type_map.get(constant_data.get('securityType'))

        constant_result = None
        if security_type =='index':
            constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'time': '', 'prev_close': ''}

        elif security_type == 'stock':
            if exchange == 'XBSE':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listing_date': '', 'total_share': '', 'listed_share': '', 'time': '', 'trading_phase': '', 'prev_close': '', 'max': '', 'min': '', 'lot_size': '', 'tick_size': '', 'buy_qty_unit': '', 'sell_qty_unit': ''}

            elif exchange == 'HKSC':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listing_date': '', 'time': '', 'prev_close': '', 'max': '', 'min': '', 'lot_size': '', 'hk_spread_table_code': '', 'sh_hk_connect': '', 'sz_hk_connect': '', 'is_vcm': '', 'is_cas': '', 'is_pos': ''}

            elif exchange == 'HGHQ':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listed_share': '', 'time': '', 'max': '', 'min': '', 'lot_size': '', 'tick_size': '', 'buy_qty_unit': '', 'sell_qty_unit': '', 'buy_qty_upper_limit': '', 'sell_qty_upper_limit': ''}

            elif exchange == 'XSHG':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listing_date': '', 'listed_share': '', 'time': '', 'trading_phase': '', 'prev_close': '', 'max': '', 'min': '', 'buy_qty_unit': '', 'sell_qty_unit': '', 'buy_qty_upper_limit': '', 'sell_qty_upper_limit': '', 'buy_qty_lower_limit': '', 'sell_qty_lower_limit': ''}

            elif exchange == 'XSHE':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listing_date': '', 'total_share': '', 'listed_share': '', 'time': '', 'trading_phase': '', 'prev_close': '', 'max': '', 'min': '', 'buy_qty_unit': '', 'sell_qty_unit': '', 'buy_qty_upper_limit': '', 'sell_qty_upper_limit': ''}

        elif security_type == 'fund':
            if exchange == 'XSHG':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listing_date': '', 'time': '', 'trading_phase': '', 'prev_close': '', 'max': '', 'min': '', 'buy_qty_unit': '', 'sell_qty_unit': '', 'buy_qty_upper_limit': '', 'sell_qty_upper_limit': '', 'buy_qty_lower_limit': '', 'sell_qty_lower_limit': ''}

            elif exchange == 'XSHE':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listing_date': '', 'total_share': '', 'listed_share': '', 'time': '', 'trading_phase': '', 'prev_close': '', 'max': '', 'min': '', 'buy_qty_unit': '', 'sell_qty_unit': '', 'buy_qty_upper_limit': '', 'sell_qty_upper_limit': ''}

        elif security_type == 'bond':
            if exchange == 'XSHG':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listing_date': '', 'time': '', 'trading_phase': '', 'prev_close': '', 'max': '', 'min': '', 'buy_qty_unit': '', 'sell_qty_unit': '', 'buy_qty_upper_limit': '', 'sell_qty_upper_limit': '', 'buy_qty_lower_limit': '', 'sell_qty_lower_limit': ''}

            elif exchange == 'XSHE':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listing_date': '', 'total_share': '', 'listed_share': '', 'time': '', 'trading_phase': '', 'prev_close': '', 'max': '', 'min': '', 'tick_size': '', 'expire_date': '', 'buy_qty_unit': '', 'sell_qty_unit': '', 'buy_qty_upper_limit': '', 'sell_qty_upper_limit': '', 'buy_qty_lower_limit': '', 'sell_qty_lower_limit': ''}

            elif exchange == 'XBSE':
                constant_result = {'htsc_code': '', 'name': '', 'exchange': '', 'security_type': '', 'security_sub_type': '', 'listing_date': '', 'total_share': '', 'listed_share': '', 'time': '', 'trading_phase': '', 'prev_close': '', 'max': '', 'lot_size': '', 'tick_size': '', 'buy_qty_unit': '', 'sell_qty_unit': '', 'base_contract_id': ''}

        security_sub_type = constant_data.get('SecuritySubType')
        if security_sub_type:
            security_sub_type = security_sub_type_map.get(int(security_sub_type))
            if security_sub_type:
                constant_result['security_sub_type'] = security_sub_type

        trading_phase = constant_data.get('TradingPhaseCode')
        if trading_phase and 'trading_phase'in constant_result:
            constant_result['trading_phase'] = trading_phase_map.get(trading_phase)

        constant_result['time'] = md_time
        constant_result['exchange'] = exchange
        constant_result['security_type'] = security_type
        for key in list(constant_result.keys()):

            if not constant_result[key]:
                value = constant_data.get(basic_info_map.get(key))
                if key in divisor_list and value:
                    value = value / divisor
                if key in ['listing_date', 'expire_date'] and value:
                    constant_result[key] = '{}-{}-{}'.format(str(value)[:4], str(value)[4:6], str(value)[6:])
                else:
                    constant_result[key] = value

        result.append(constant_result)

    return result



















