# -*- coding: utf-8 -*-
import mojimoji

a = mojimoji.zen_to_han(unicode("ＨＩＶ感染", 'utf-8'), kana=False)
print a.lower()
