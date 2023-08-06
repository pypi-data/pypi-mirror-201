import re
from xpinyin import Pinyin
from lxml import etree

p = Pinyin()


def tbxpath(tb_xpath=None, p='S', text=None, lable='th'):
    tblist = []
    tree = text
    _tr_label = []
    obj = tree.xpath(tb_xpath)
    if obj:
        obj = obj[0]
        if p == 'H':
            tr = obj.xpath('.//tr')
            for _tr in tr:
                th = _tr.xpath('.//th//text()')
                td = _tr.xpath('.//td//text()')
                td = excute_tb_td(td)
                th = excute_tb_th(th)
                if len(td) == len(th) and len(td) > 0 and len(th) > 0:
                    for i in enumerate(th):
                        tbdict = {}
                        tbdict[th[i[0]]] = td[i[0]]
                        tblist.append(tbdict)

        if p == 'S':
            tr = obj.xpath('.//tr')
            # print(tr)
            for _tr in enumerate(tr):
                tbdict = {}
                _tr_num = _tr[0]
                _tr_tree = _tr[1]
                if _tr_num == 0:
                    _tr_label = th_tree(_tr_tree, lable)
                    # print(_tr_label)
                else:
                    _tr_str = td_tree(_tr_tree)
                    # print(_tr_str)
                    if len(_tr_str) == len(_tr_label) and len(_tr_label) > 0 and len(_tr_str) > 0:
                        for i in enumerate(_tr_label):
                            tbdict[_tr_label[i[0]]] = _tr_str[i[0]]
                        tblist.append(tbdict)
        return tblist, len(tblist)

    else:
        return None


def td_tree(td):
    td_list = []
    _td_tree = td.xpath('.//td')
    for _td in _td_tree:
        _td_text = _td.xpath('.//text()')
        _td_text = excute_tb_td(_td_text)
        _td_text = ''.join(_td_text)
        td_list.append(_td_text)
    return td_list


def th_tree(td, lable):
    td_list = []
    _td_tree = td.xpath('.//%s' % lable)
    for _td in _td_tree:
        _td_text = _td.xpath('.//text()')
        _td_text = excute_tb_th(_td_text)
        _td_text = ''.join(_td_text)
        td_list.append(_td_text)
    return td_list


def excute_tb_td(tb):
    tb = [relp_tb_td(i) for i in tb]
    return tb


def excute_tb_th(tb):
    tb = [relp_tb_th(i) for i in tb]
    tb = [i for i in tb if i != '']
    return tb


def relp_tb_td(tb):
    tb = re.sub(r'(\r|\n|\t|\xa0)', lambda x: '', tb).replace(' ', '')
    return tb


def relp_tb_th(tb):
    th_str = re.sub("([^\u0030-\u0039\u0041-\u007a\u4e00-\u9fa5])", '', tb)
    result1 = p.get_initials(th_str, '')
    return result1


if __name__ == '__main__':
    d = ''
    # print(tbxpath("//table", p='S', text=a, lable='td'))
    # print(tbxpath("//table", p='S', text=b))
    # print(tbxpath("//table[@class='project_table']", p='S', text=c))
    print(tbxpath("//table[@class='table table-bordered table-condensed table-hover table-striped']", p='S', text=d,
                  lable='th'))
