#
# -*- coding: UTF-8 -*- # ----------------------------------------------------------------------------- #
#
#     letterProofer | Kerning
#     Version: 0.002
#
#     Still working on this. Needs to be optimized and restructured.
#     Extra page is drawn—need to figure this out when I have more time

#     
#
#     07/29/2022
#

# --------------------------------------
# -*- Imports -*- # 

import os
import time
import string
import numpy
import json
import tempfile
from datetime import date
from glob import glob
from os import listdir
from os.path import join, isfile
from pathlib import Path
from operator import itemgetter, attrgetter, methodcaller
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from drawBot import fill, stroke, rect, font, text, openTypeFeatures, height, newPage, textBox
from drawBot import installFont, pages, pageCount, saveImage
from fontTools.ttLib.ttFont import TTFont
from itertools import islice

# --------------------------------------
# -*- Set paths to directories -*- # 

font_folder = "/Users/smokh/S3P0/000-999/400-499 Creative/402 Type Design/02 Oldb/402.02.03 Fonts/2022-08-03"
proof_folder = "/Users/smokh/S3P0/000-999/400-499 Creative/402 Type Design/03 Leitmotiv/402.03.06 Proofs"

# --------------------------------------
# -*- Date & Time -*- # 

today = date.today()
now = time.localtime()
current_date = today.strftime ("%d/%m/%y")
current_year = today.strftime("%Y")
current_time = time.strftime("%H:%M", now)

# --------------------------------------
# -*- Settings -*- # 

# Set your information
designer_name = "Sepehr Mokhtarzadeh"
typeface_name = "Leitmotif"

# Set caption font
caption_font = "AndaleMono"
caption_size = 7
caption_color = 0

# --------------------------------------
# -*- Type Sizes -*- # 

# Set type scale
font_size_XXXL = 120
font_size_XXL = 96
font_size_XL = 80
font_size_L = 50
font_size_M = 24
font_size_S = 16
font_size_XS = 12
font_size_XXS = 9

# Set type waterfall sizes
waterfall_L = (24, 36, 48, 60)
waterfall_M = (12, 18, 24, 32)
waterfall_S = (12, 18, 28)

# Waterfall modifier
modifier = 8
y_pos_1 = 40
y_pos_2 = y_pos_1 - 2

tracking_amount = False

# --------------------------------------
# -*- Text Strings -*- # 

textStrings = [

    [ "one_column", font_size_XS, "UC kerning proof – every glyph between every glyph",
    ''.join(['%s%s%s\n' % (c, c.join(list(ascii_uppercase)), c) for c in ascii_uppercase if c == "A" or c == "B" or c == "C" or c == "D" or c == "E" or c == "F" or c == "G" or c == "H" or c == "I" or c == "J" or c == "K" or c == "L" or c == "M" or c == "N" or c == "O" or c == "P" or c == "Q" or c == "R" or c == "S" or c == "T" or c == "U" or c == "V" or c == "W" or c == "X" or c == "Y" or c == "Z" ])],

    [ "one_column", font_size_XS, "LC kerning proof – every glyph between every glyph",
    ''.join(['%s%s%s\n' % (c, c.join(list(ascii_lowercase)), c) for c in ascii_lowercase if c == "a" or c == "b" or c == "c" or c == "d" or c == "e" or c == "f" or c == "g" or c == "h" or c == "i" or c == "j" or c == "k" or c == "l" or c == "m" or c == "n" or c == "o" or c == "p" or c == "q" or c == "r" or c == "s" or c == "t" or c == "u" or c == "v" or c == "w" or c == "x" or c == "y" or c == "z" ])],

    [ "one_column", font_size_XS, "UC sets of three", "Aar Abo Act Adj Aer Aft Aga Ahe Aie Aji Ake Alm Amo Ano Aoa App Aqu Art Ass Att Aug Ave Awa Axe Aye Azo Bal Bbn Bcc Bdj Ber Bfd Bga Bhu Bie Bji Bkl Bli Bmo Bni Boa Bpi Bqu Brt Bss Btl But Bve Bwa Bxl Bye Bzo Cal Cbn Ccn Cdj Cer Cfi Cga Che Cie Cjn Ckl Cle Cmo Cnl Coa Cpl Cqu Crl Css Ctl Cul Cvl Cwl Cxl Cyi Czo Dal Dbn Dci Ddj Der Dfl Dga Dhr Die Dji Dkl Dli Dmo Dnu Don Dpi Dqu Dri Dsl Dtl Dul Dvl Dwl Dxl Dya Dzn Ear Ebe Ech Edw Een Efo Ega Ehr Eit Ejo Ekn Eld Emp Ens Eob Epa Equ Ero Est Eth Euc Evo Ewa Exe Eyo Eze Fal Fbo Fci Fdj Fer Ffu Fgn Fhi Fil Fjo Fkl Fli Fmi Fnl Fol Fpi Fqu Fra Fst Fto Ful Fvl Fwl Fxi Fyi Fzi Gal Gbo Gch Gdj Ger Gfl Ggl Ghi Gil Gjl Gke Gli Gmo Gnl Gol Gpi Gqu Gra Gst Gto Gut Gve Gwl Gxi Gyn Gzn Har Hbo Hct Hdj Her Hfl Hga Hhe Hie Hji Hke Hlm Hmo Hno Hon Hpl Hqu Hrt Hss Htt Hue Hve Hwa Hxe Hyu Hzi Jap Jbo Jct Jdj Jer Jfn Jgu Jhe Jie Jjl Jkl Jlm Jmo Jno Jon Jpl Jqu Jrt Jss Jtt Jut Jve Jwa Jxe Jyn Jzt Kan Kbo Kci Kdj Ker Kfn Kga Khe Kie Kjl Kkn Klm Kmo Kno Kon Kpl Kqu Krt Kss Kti Kui Kve Kwa Kxe Kye Kzo Lam Lbo Lct Ldj Len Lft Lga Lhe Lie Lju Lke Llm Lmo Lno Lon Lpl Lqu Lrt Lss Ltt Luc Lve Lwa Lxe Lye Lzt Oan Obu Oct Odj Oer Ofa Oga Ohe Oie Oja Oke Olf Omi Onu Oon Opl Oqu Ort Oss Ott Out Ovl Owa Oxe Oye Ozo Par Pbl Pct Pdj Per Pfe Pgs Phi Pie Pji Pki Pla Pml Pnu Pon Ppl Pqu Prt Psa Pts Pul Pvc Pwi Pxl Pyn Pzl Qal Qie Qoa Qui Qwa Rad Rbi Rct Rdj Ren Rfe Rgs Rha Ria Rji Rkl Rli Rms Rni Roa Rpi Rqu Rrt Rsi Rtd Rut Rvi Rwl Rxi Ryn Rzi Sar Sbo Sct Sdl Ser Sfo Sgi She Sie Sja Ski Slo Smi Sno Sol Spe Squ Srt Sst Stt Sut Sve Swa Sxe Syl Szo Tar Tba Tcm Tdi Ter Tfl Tgi The Tie Tji Tke Tlm Tmo Tno Tol Tpi Tqu Trt Tsi Tti Tut Tvl Twl Txl Tyl Tzo Ual Ubi Uct Udj Uer Ufc Uga Uhi Uie Uji Uke Ulm Umo Uno Uol Upp Uqu Urt Uss Utl Uui Uvl Uwl Uxe Uye Uzo Val Vbo Vct Vdj Ver Vft Vga Vhe Vie Vjl Vki Vlm Vmo Vno Vol Vpi Vqu Vrl Vsi Vtt Vut Vvl Vwl Vxl Vyl Vzi Wal Wbo Wcl Wdj Wer Wfi Wga Whe Wie Wjl Wke Wlm Wmo Wno Wol Wpi Wqu Wrl Wsi Wtt Wut Wvl Wwl Wxl Wya Wzl Xal Xbo Xce Xdj Xer Xft Xga Xhe Xie Xjl Xki Xlm Xmo Xno Xol Xpi Xqu Xrl Xsi Xtt Xut Xvl Xwl Xxl Xye Xzi Yal Ybo Yci Ydj Yer Yfl Yga Yhe Yie Yjo Ykl Yli Ymo Yno Yol Ypi Yqu Yrl Ysi Ytt Yut Yvl Ywl Yxl Yyl Yzi Zan Zbr Zco Zdj Zer Zfl Zga Zhe Zie Zji Zke Zlm Zmo Zno Zol Zpi Zqu Zro Zsn Zti Zut Zvl Zwl Zxl Zyl Zzl" ],

    [ "one_column", font_size_XS, "UC & LC kern pairs", "AaAbAcAdAeAfAgAhAiAjAkAlAmAnAoApAqArAsAtAuAvAwAxAyAzA\nSaSbScSdSeSfSgShSiSjSkSlSmSnSoSpSqSrSsStSuSvSwSxSySzS\nTaTbTcTdTeTfTgThTiTjTkTlTmTnToTpTqTrTsTtTuTvTwTxTyTzT\nUaUbUcUdUeUfUgUhUiUjUkUlUmUnUoUpUqUrUsUtUuUvUwUxUyUzU\nVaVbVcVdVeVfVgVhViVjVkVlVmVnVoVpVqVrVsVtVuVvVwVxVyVzV\nWaWbWcWdWeWfWgWhWiWjWkWlW\nWmWnWoWpWqWrWsWtWuWvWwWxWyWzW\nXaXbXcXdXeXfXgXhXiXjXkXlXmXnXoXpXqXrXsXtXuXvXwXxXyXzX\nYaYbYcYdYeYfYgYhYiYjYkYlYmYnYoYpYqYrYsYtYuYvYwYxYyYzY\nZaZbZcZdZeZfZgZhZiZjZkZlZmZnZoZpZqZrZsZtZuZvZwZxZyZzZ" ],

    [ "one_column", font_size_XS, "Punctuation kern", """H‘–’H’–‘H'–'H–?H‘.H.’H’.H.‘H',H,'H“,H,”H”‚H„“H",H,"H\nH"¿H?"H“¿H?”H“¡H!”H"¡H!"HH?“H!“H…?H?…H\nh–a–b–c–d–e–f–g–h–i–j–k–l–m–n–o–p–q–r–s–t–u–v–w–x–y–z–þ–æ–ð–\nH–A–B–C–D–E–F–G–H–I–J–K–L–M–N–O–P–Q–R–S–T–U–V–W–X–Y–Z–Þ–Æ–Ð–\nh.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.x.y.z.ð.h\nh,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,ð,h\nH.A.B.C.D.E.F.G.H.I.J.K.L.M.N.O.P.Q.R.S.T.U.V.H.W.X.Y.Z.Þ.H.Æ.H\nH,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,H,W,X,Y,Z,Þ,H,Æ,H\na; b; c; d; e; f; g; h; i; j; k; l; m; n; o; p; q; r; s; t; u; v; w; x; y; z;\nA; B; C; D; E; F; G; H; I; J; K; L; M; N; O; P; Q; R; S; T; U; V; W; X; Y; Z;\n n//a//b//c//d//e//f//g//h//i//ĩ//j//k//l//m//\n//n//o//p//q//r//s//t//u//v//w//y//z//n\nH//A//B//C//D//E//F//G//H//I//J//K//L//M//\n//N//O//P//Q//R//S//T//U//V//W//X//Y//Z//Þ//Æ//H\n¿A? ¿B? ¿C? ¿D? ¿E? ¿F? ¿G? ¿H? ¿I? ¿J? ¿K? ¿L? ¿M? ¿N? ¿O? ¿P? ¿Q? ¿R? ¿S? ¿T? ¿U? ¿V? ¿W? ¿X? ¿Y? ¿Z?\n¿a? ¿b? ¿c? ¿d? ¿e? ¿f? ¿g? ¿h? ¿i? ¿j? ¿k? ¿l? ¿m? ¿n? ¿o? ¿p? ¿q? ¿r? ¿s? ¿t? ¿u? ¿v? ¿w? ¿x? ¿y? ¿z? ¿þ? ¿æ? ¿ð? HH–?HH¿–HH\n¡a! ¡b! ¡c! ¡d! ¡e! ¡f! ¡g! ¡h! ¡i! ¡j! ¡k! ¡l! ¡m! ¡n! ¡o! ¡p! ¡q! ¡r! ¡s! ¡t! ¡u! ¡v! ¡w! ¡x! ¡y! ¡z!\n¡A! ¡B! ¡C! ¡D! ¡E! ¡F! ¡G! ¡H! ¡I! ¡J! ¡K! ¡L! ¡M! ¡N! ¡O! ¡P! ¡Q! ¡R! ¡S! ¡T! ¡U! ¡V! ¡W! ¡X! ¡Y! ¡Z!\nH’A’C’D’E’F’G’H’I’J’K’L’M’N’O’P’Q’R’S’T’U’V’W’X’Y’Z’H’Æ\nH"A"C"D"E"F"G"H"I"J"K"L"M"N"O"P"Q"R"S"T"U"V"W"X"Y"Z"H"Æ""" ],

    [ "one_column", font_size_XS, "Quotation", """nd“n”bd’nhn“   nd“o”bd’oho“   nd“þ”bd’þhþ“   nd“a”bd’aha“   nd“b”bd’bhb“   nd“c”bd’chc“   nd“d”bd’dhd“   nd“e”bd’ehe“   nd“f”bd’fhf“   nd“g”bd’ghg“   nd“h”bd’hhh“   nd“i”bd’ihi“  nd“j”bd’jhj“   nd“k”bd’khk“   nd“l”bd’lhl“   nd“m”bd’mhm“   nd“p”bd’php“   nd“q”bd’qhq“   nd“r”bd’rhr“   nd“s”bd’shs“   nd“t”bd’tht“   nd“u”bd’uhu“   nd“v”bd’vhv“   nd“w”bd’whw“   nd“x”bd’xhx“   nd“y”bd’yhy“   nd“z”bd’zhz“   nd“æ”bd’æhæ“   nd“œ”bd’œhœ“   nd“ð”hð“   nd“ß”hß“\nnd"n"bd'nh nd"o"bd'oh nd"þ"bd'þh nd"a"bd'ab nd"b"bd'btb nd"c"bd'ch nd"d"bd'dh nd"e"bd'eh nd"f"bd'fh nd"g"bd'gh nd"h"bd'hh nd"i"bd'ih nd"j"bd'jh nd"k"bd'kh nd"l"bd'lh nd"m"bd'mh nd"p"bd'ph nd"q"bd'qh nd"r"bd'rh nd"s"bd'sh nd"t"bd'th nd"u"bd'uh nd"v"bd'vh nd"w"bd'wh nd"x"bd'xh nd"y"bd'yh nd"z"bd'zh nd"æ"bd'æh nd"œ"bd'œh nd"ð"bd ndß"bd\nHH“N”BD’NHN“   HH“O”BD’OHO“   HH“Þ”BD’ÞHÞ“   HH“A”BD’AHA“   HH“B”BD’HB“   HH“C”BD’CHC“   HH“D”BD’DHH“   HH“E”BD’EHE“   HH“F”BD’FHF“   HH“G”BD’GHG“   HH“H”BD’HHH“   HH“I”BD’IHI“  HH“J”BD’JHJ“   HH“K”BD’KHK“   HH“L”BD’LHL“   HH“M”BD’MHM“   HH“P”BD’PHP“   HH“Q”BD’QHQ“   HH“R”BD’RHR“   HH“S”BD’SHS“   HH“T”BD’THT“   HH“U”BD’UHU“   HH“V”BD’VHV“   HH“W”BD’WHW“   HH“X”BD’XHX“   HH“Y”BD’YHY“   HH“Z”BD’ZHZ“   HH“Æ”BD’ÆHÆ“   HH“Œ”BD’ŒHŒ“   HH“Ð”BD’ÐHÐ“\nHH"N"HD'NH HH"O"HD'OH HH"A"HD'AH HH"B"HD'BH HH"C"HD'CH HH"D"HD'DH HH"E"HD'EH HH"F"HD'FH HH"G"HD'GH HH"H"HD'HH HH"I"HD'IH HH"J"HD'JH HH"K"HD'KH HH"L"HD'LH HH"M"HD'MH HH"P"HD'PH HH"Q"HD'QH HH"R"HD'RH HH"S"HD'SH HH"T"HD'TH HH"U"HD'UH HH"V"HD'VH HH"W"HD'WH HH"X"HD'XH HH"Y"HD'YH HH"Z"HD'ZH HH"Æ"HD'ÆH HH"Œ"HD'ŒH HH"Ð"HD'ÐH HH"Þ"HD'ÞH""" ],

    [ "one_column", font_size_XS, "Symbols", "«A» «B» «C» «E» «F» «J» «K» «L» «P» «R» «T» «V» «W» «X» «Y» «Z»\n»A« »B« »C« »E« »F« »J« »K« »L« »P« »R« »T« »V« »W« »X« »Y« »Z«\n«c» «f» «j» «k» «o» «t» «v» «w» «x» «z»\n»c« »f« »j« »k« »o« »t« »v« »w« »x« »z«\n«0» «1» «2» «3» «4» «5» «6» «7» «8» «9»\n»0« »1« »2« »3« »4« »5« »6« »7« »8« »9«\n«.».«:»:«?»?«–»–« H(«)H(»)H\n\nh@a@b@c@d@e@f@g@h@i@j@k@l@m@h\nh@n@o@p@q@r@s@t@u@v@w@x@y@z@h\nH@A@B@C@D@E@F@G@H@I@J@K@L@M@H\nH@N@O@P@Q@R@S@T@U@V@W@X@Y@Z@Æ@Þ@H\n\nHH HH A HH HH T HH HH V HH HH Y HH HH X HH HH\nHH HH W HH HH F HH HH J HH HH\nHOH HOF AOA AOA JOA HOW WOV VOY YOY HOT TOH\nhn hn v hn hn w hn hn f hn hn r hn hn" ],

    [ "one_column", font_size_XS, "UC Variants", "H–A–B–C–D–E–F–G–H–I–J–K–L–M–N–O–P–Q–R–S–T–U–V–W–X–Y–Z–Þ–Æ–Ð–\n¿AH ¿BH ¿CH ¿DH ¿EH ¿FH ¿GH ¿HH ¿IH ¿JH ¿KH ¿LH ¿MH ¿NH ¿OH ¿PH ¿QH ¿RH ¿SH ¿TH ¿UH ¿VH ¿WH ¿XH ¿YH ¿ZH\n¡A! ¡B! ¡C! ¡D! ¡E! ¡F! ¡G! ¡H! ¡I! ¡J! ¡K! ¡L! ¡M! ¡N! ¡O! ¡P! ¡Q! ¡R! ¡S! ¡T! ¡U! ¡V! ¡W! ¡X! ¡Y! ¡Z!\n«A» «B» «C» «E» «F» «J» «K» «L» «P» «T» «V» «W» «X» «Y» «Z»\n»A« »B« »C« »E« »F« »J« »K« »L« »R« »T« »V« »W« »X« »Y« »Z«\n–0–1–2–3–4–5–6–7–8–9\n¿00 ¿10 ¿20 ¿30 ¿40 ¿50 ¿60 ¿70 ¿80 ¿90    ¡00 ¡10 ¡20 ¡30 ¡40 ¡50 ¡60 ¡70 ¡80 ¡90\n«0» «1» «2» «3» «4» «5» «6» «7» «8» «9»\n»0« »1« »2« »3« »4« »5« »6« »7« »8« »9«\nH@A@B@C@D@E@F@G@H@I@J@K@L@M@H\nH@N@O@P@Q@R@S@T@U@V@W@X@Y@Z@Æ@Þ@H" ],

    [ "one_column", font_size_XL, "Diacritics", "ÆaÆbÆcÆdÆeÆfÆgÆhÆiÆjÆkÆlÆm\nÆnÆoÆpÆqÆrÆsÆtÆuÆvÆwÆxÆyÆ\nðAðBðCðDðEðFðGðHðIðJðKðLðMðNðOðRðSðTðUð\nŦAŦBŦCŦDŦEŦFŦGŦHŦIŦJŦKŦLŦ\nŦMŦNŦOŦPŦQŦRŦSŦTŦUŦVŦWŦXŦYŦZ\n\næabæcædæeæfægæhæiæjækælæmænæoæpæqæræsætæuævæwæxæyæzæ\nþabþcþdþeþfþgþhþiþjþkþlþmþnþoþpþqþrþsþtþuþvþwþxþyþzþ\nðabðcðdðeðfðgðhðiðjðkðlðmðnðoðpðqðrðsðtðuðvðwðyð\nĩAĩBĩCĩDĩEĩFĩGĩHĩIĩJĩKĩLĩMĩNĩOĩPĩQĩRĩSĩTĩUĩVĩWĩXĩYĩZĩ\n\nąj ąg ąy ći éî fâ fā fă fã få fä fè fë fē fì fî fj fö fü fð gj gy îè ît íč íň íř íš íž ïf įj įg įy ši šī št tă tã tu’ĩ úř ųj ųg ųy žī\nFä Få Fā Fă Fã Fè Fë Fê Fē Fì Fî Fö Kā Kä Kå Kī Kö Kř Kū Pä På Pā Pă Pã Pè Pë Pē Pě Pì Pî Pï Pī Pň Pö Př Pū Pž Ţâ Tâ Tä Tå Tā Tă Tã Tè Tê Të Tē Tĕ Tě Tī Tö Tō Tř Tš Tū Tž Vå Vä Vā Vă Vã Vë Vē Vě Vî Vī Vö Vš Vž Wå Wä Wā Wè Wö Yā Yã Yū" ],

    [ "one_column", font_size_XL, "Figures", """01020304050607080900 91929394959697989909\n81828384858687889808 71727374757677879707\n61626364656676869606 51525354556575859505\n41424344546474849404 31323343536373839303\n21223242526272829202 11213141516171819101\n\n$12 $23 $34 $45 $56 $67 $78 $89 $90 $01\n€12 €23 €34 €45 €56 €67 €78 €89 €90 €01\n£12 £23 £34 £45 £56 £67 £78 £89 £90 £01\n¥12 ¥23 ¥34 ¥45 ¥56 ¥67 ¥78 ¥89 ¥90 ¥01\n₺12 ₺23 ₺34 ₺45 ₺56 ₺67 ₺78 ₺89 ₺90 ₺01\n₹12 ₹23 ₹34 ₹45 ₹56 ₹67 ₹78 ₹89 ₹90 ₹01v12¢ 23¢ 34¢ 45¢ 56¢ 67¢ 78¢ 89¢ 90¢ 01¢\n\n“$0 “£0 “€0 “¥0 “₹0¢” 99%” 99%"\n"0" "1" "2" "3" "4" "5" "6" "7" "8" "9"\n“0” “1” “2” “3” “4” “5” “6” “7” “8” “9”\n.1.2.3.4.5.6.7.8.9.0.0 ,1,2,3,4,5,6,7,8,9,0,0\n¿1? ¿2? ¿3? ¿4? ¿5? ¿6? ¿7? ¿8? ¿9? ¿0?\n-1-2-3-4-5-6-7-8-9-0- –1–2–3–4–5–6–7–8–9–0\n0//0//1//2//3//4//5//6//7//8//9""" ],


]
 
     
# --------------------------------------
# -*- Page Info -*- # 

show_document_grid = False
show_grid = False
show_labels = False

# Metrics
mmmm = 2.834627813
inch = 72

# Margins
margin = (1/2) * inch
number_of_columns = 13
number_of_rows = 49

# Dimensions
page_dimensions = 'LetterLandscape'
newPage(page_dimensions)

# Document Grid
subdivisions = 8
grid_unit = inch / subdivisions

page_width = width() / inch
page_height = height() / inch

number_of_x_gridlines = float(grid_unit * page_width)
number_of_y_gridlines = float(grid_unit * page_height)

# Document Margins
margin_left_right = width() - (margin * 2)
margin_top_bottom = height() - (margin * 2)

col_width = margin_left_right / number_of_columns
row_height = margin_top_bottom / number_of_rows

# Coordinate helpers
edge_left = 0
edge_right = margin_left_right
edge_top = margin_top_bottom
edge_bottom = 0

# --------------------------------------
# -*- Functions, Style  -*- # 

def meta_style():
    fill(caption_color)
    font(caption_font, caption_size)
    
def type_style():
    fallbackFont("AdobeBlank")
    font(postscriptFontName)

# --------------------------------------
# -*- Functions, Components -*- # 

def drawHeaderFooter():
    with savedState():
        translate(margin,margin)
        with savedState():
            meta_style()
        
            translate(0, fontCapHeight() * 2)
        
            # Definitions
            leftHeader = ' '.join([typeface_name, "©", current_year, "copyright by designed by", designer_name])
            rightHeader = ' '.join(["output made on:", current_date, ",", current_time])
            rightFooter = ' '.join([postscriptFontName, font_version])
        
            # Draw
            text(leftHeader, (edge_left, edge_top + 5), align="left" )
            text(rightHeader, (edge_right, edge_top + 5), align="right")
        
            # Draw line below Header
            with savedState():
                stroke(0)
                strokeWidth(0.25)
                line((edge_left, y_cord["48"] + 5), (edge_right, y_cord["48"] + 5))
        
            # Draw Footer
            translate(0, -(fontCapHeight() * 3.25))
            text(rightFooter, (edge_left, edge_bottom - 10), align="left")
            
# --------------------------------------
# -*- Functions, Page Layouts -*- # 

def drawOneColumnLayout():
    global y_pos_1
    global y_pos_2
    
    with savedState():
        
        # # Set type for page title
        # if font_size == waterfall_L or font_size == waterfall_M or font_size == waterfall_S:
        #     font(caption_font, 14)
        #     text(section, (edge_left, y_cord["45"]))
        # else:
        #     font(caption_font, 14)
        #     text(' '.join([str(font_size), "pt.", section]),(edge_left, y_cord["45"]))
        
        # Set type for proof, single type size
        if font_size == font_size_XXXL:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.2
            tracking(tracking_amount)
            translate(0, -(line_height / 2))
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
        elif font_size == font_size_XXL:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.2
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
        elif font_size == font_size_XL:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.2
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
        elif font_size == font_size_L:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.6
            lineHeight(line_height)
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            baselineShift(-(y_cord["1"]/2))
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
        elif font_size == font_size_M:
            type_style()
            fontSize(font_size)
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
        elif font_size == font_size_S:
            type_style()
            fontSize(font_size)
            lineHeight(32)
            tracking(tracking_amount)
            translate(0, -fontCapHeight()*4)
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="left")
            
        elif font_size == font_size_XS:
            type_style()
            fontSize(font_size)
            lineHeight(font_size * 1.4)
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="left")
            
        elif font_size == font_size_XXS:
            type_style()
            fontSize(font_size)
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
def drawTwoColumnLayout():
    global y_pos_1
    global y_pos_2
    
    with savedState():
            
        # # Set type for page title
        # if font_size == waterfall_L or font_size == waterfall_M or font_size == waterfall_S or font_size == font_size_S or font_size == font_size_XS or font_size == font_size_XXS:
        #     font(caption_font, 14)
        #     text(section, (edge_left, y_cord["45"]))
        # else:
        #     font(caption_font, 14)
        #     text(' '.join([str(font_size), "pt.", section]),(edge_left, y_cord["45"]))
        
        # Set type for proof, single type size
        if font_size == font_size_XXL:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.2
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
        if font_size == font_size_S:
            type_style()
            
            # Column 1
            fontSize(14)
            line_height = 14 * 1.3
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, -(y_cord["6"]), (x_cord["6"]-20), margin_top_bottom), align="left")
            
            # Column 2
            fontSize(16)
            line_height = 16 * 1.3
            translate(0, -fontCapHeight())
            baselineShift(3.75)
            textBox(proof_set, (x_cord["6"], -(y_cord["6"]), x_cord["6"], margin_top_bottom), align="left")
            
            # Type specs
            meta_style()
            translate(0, y_cord["0"])
            text("14pt", (edge_left, (y_cord["43"])))
            text("16pt", (x_cord["6"], (y_cord["43"])))
        
        if font_size == font_size_XS:
            type_style()
            
            # Column 1
            fontSize(12)
            line_height = 10 * 1.3
            translate(0, -fontCapHeight())
            textBox("Angel Adept Blind Bodice Clique Coast Dunce Docile Enact Eosin Furlong Focal Gnome Gondola Human Hoist Inlet Iodine Justin Jocose Knoll Koala Linden Loads Milliner Modal Number Nodule Onset Oddball Pneumo Poncho Quanta Qophs Rhone Roman Snout Sodium Tundra Tocsin Uncle Udder Vulcan Vocal Whale Woman Xmas Xenon Yunnan Young Zloty Zodiac. Angel angel adept for the nuance loads of the arena cocoa and quaalude. Blind blind bodice for the submit oboe of the club snob and abbot. Clique clique coast for the pouch loco of the franc assoc and accede. Dunce dunce docile for the loudness mastodon of the loud statehood and huddle. Enact enact eosin for the quench coed of the pique canoe and bleep. Furlong furlong focal for the genuflect profound of the motif aloof and offers. Gnome gnome gondola for the impugn logos of the unplug analog and smuggle. Human human hoist for the buddhist alcohol of the riyadh caliph and bathhouse. Inlet inlet iodine for the quince champion of the ennui scampi and shiite. Justin justin jocose for the djibouti sojourn of the oranj raj and hajjis. Knoll knoll koala for the banknote lookout of the dybbuk outlook and trekked. Linden linden loads for the ulna monolog of the consul menthol and shallot. Milliner milliner modal for the alumna solomon of the album custom and summon. Number number nodule for the unmade economic of the shotgun bison and tunnel. ", (edge_left, -(y_cord["2"]), x_cord["5"], margin_top_bottom), align="left")
            
            # Column 2
            fontSize(12)
            line_height = 12 * 1.3
            translate(0, -fontCapHeight())
            baselineShift(3.75)
            textBox("Onset onset oddball for the abandon podium of the antiquo tempo and moonlit. Pneumo pneumo poncho for the dauphin opossum of the holdup bishop and supplies. Quanta quanta qophs for the inquest sheqel of the cinq coq and suqqu. Rhone rhone roman for the burnt porous of the lemur clamor and carrot. Snout snout sodium for the ensnare bosom of the genus pathos and missing. Tundra tundra tocsin for the nutmeg isotope of the peasant ingot and ottoman. Uncle uncle udder for the dunes cloud of the hindu thou and continuum. Vulcan vulcan vocal for the alluvial ovoid of the yugoslav chekhov and revved. Whale whale woman for the meanwhile blowout of the forepaw meadow and glowworm. Xmas xmas xenon for the bauxite doxology of the tableaux equinox and exxon. Yunnan yunnan young for the dynamo coyote of the obloquy employ and sayyid. Zloty zloty zodiac for the gizmo ozone of the franz laissez and buzzing.", (x_cord["6"], -(y_cord["2"]), x_cord["5"], margin_top_bottom), align="left")
            
            # Type specs
            meta_style()
            translate(0, y_cord["0"])
            text("12pt", (edge_left, (y_cord["47"])))
            text("12pt", (x_cord["6"], (y_cord["47"])))
            
        if font_size == font_size_XXS:
            type_style()
            
            # Column 1
            fontSize(12)
            line_height = 10 * 1.3
            translate(0, -fontCapHeight())
            textBox("ABIDE ACORN OF THE HABIT DACRON FOR THE BUDDHA GOUDA QUAALUDE. BENCH BOGUS OF THE SCRIBE ROBOT FOR THE APLOMB JACOB RIBBON. CENSUS CORAL OF THE SPICED JOCOSE FOR THE BASIC HAVOC SOCCER. DEMURE DOCILE OF THE TIDBIT LODGER FOR THE CUSPID PERIOD BIDDER. EBBING ECHOING OF THE BUSHED DECAL FOR THE APACHE ANODE NEEDS. FEEDER FOCUS OF THE LIFER BEDFORD FOR THE SERIF PROOF BUFFER. GENDER GOSPEL OF THE PIGEON DOGCART FOR THE SPRIG QUAHOG DIGGER. HERALD HONORS OF THE DIHEDRAL MADHOUSE FOR THE PENH RIYADH BATHHOUSE. IBSEN ICEMAN OF THE APHID NORDIC FOR THE SUSHI SAUDI SHIITE. JENNIES JOGGER OF THE TIJERA ADJOURN FOR THE ORANJ KOWBOJ HAJJIS. KEEPER KOSHER OF THE SHRIKE BOOKCASE FOR THE SHEIK LOGBOOK CHUKKAS. LENDER LOCKER OF THE CHILD GIGOLO FOR THE UNCOIL GAMBOL ENROLLED. MENACE MCCOY OF THE NIMBLE TOMCAT FOR THE DENIM RANDOM SUMMON. NEBULA NOSHED OF THE INBRED BRONCO FOR THE COUSIN CARBON KENNEL. ", (edge_left, -(y_cord["2"]), x_cord["5"], margin_top_bottom), align="left")
            
            # Column 2
            fontSize(12)
            line_height = 12 * 1.3
            translate(0, -fontCapHeight())
            baselineShift(3.75)
            textBox("OBSESS OCEAN OF THE PHOBIC DOCKSIDE FOR THE GAUCHO LIBIDO HOODED. PENNIES PODIUM OF THE SNIPER OPCODE FOR THE SCRIP BISHOP HOPPER. QUANTA QOPHS OF THE INQUEST OQOS FOR THE CINQ COQ SUQQU. REDUCE ROGUE OF THE GIRDLE ORCHID FOR THE MEMOIR SENSOR SORREL. SENIOR SCONCE OF THE DISBAR GODSON FOR THE HUBRIS AMENDS LESSEN. TENDON TORQUE OF THE UNITED SCOTCH FOR THE NOUGHT FORGOT BITTERS. UNDER UGLINESS OF THE RHUBARB SEDUCE FOR THE MANCHU HINDU CONTINUUM. VERSED VOUCH OF THE DIVER OVOID FOR THE TELAVIV KARPOV FLIVVER. WENCH WORKER OF THE UNWED SNOWCAP FOR THE ANDREW ESCROW GLOWWORM. XENON XOCHITL OF THE MIXED BOXCAR FOR THE SUFFIX ICEBOX EXXON. YEOMAN YONDER OF THE HYBRID ARROYO FOR THE DINGHY BRANDY SAYYID. ZEBRA ZOMBIE OF THE PRIZED OZONE FOR THE FRANZ ARROZ BUZZING.", (x_cord["6"], -(y_cord["2"]), x_cord["5"], margin_top_bottom), align="left")
            
            # Type specs
            meta_style()
            translate(0, y_cord["0"])
            text("12pt", (edge_left, (y_cord["47"])))
            text("12pt", (x_cord["6"], (y_cord["47"])))

        # Set type for proof, waterfalls
        if font_size == waterfall_L:

            for pts in font_size:
                type_style()
                fontSize(pts)
                translate(0, -fontCapHeight())
                textWidth, textHeight = textSize(proof_set)
                
                # Ends loop to prevent TypeError
                if y_pos_1 < 0:
                    continue
                    if y_pos_2 < 0:
                        continue 
                                    
                text( proof_set, (x_cord["0"], y_cord[str(y_pos_1)]) )
                meta_style()
                text( f"{pts}pt", (x_cord["0"], y_cord[str(y_pos_2)]) )
                y_pos_1 = y_pos_1 - 6
                y_pos_2 = y_pos_2 - 6
                
        if font_size == waterfall_M:     
            y_pos_1 = 40
            y_pos_2 = y_pos_1 - 2 

            for pts in font_size:
                type_style()
                fontSize(pts)
                translate(0, -fontCapHeight())
                textWidth, textHeight = textSize(proof_set)
                
                # Ends loop to prevent TypeError
                if y_pos_1 < 0:
                    continue
                    if y_pos_2 < 0:
                        continue 
                
                # Creates text            
                text( proof_set, ((x_cord["6"] -margin), y_cord[str(y_pos_1)]), align="right" )
                text( proof_set.upper(), ((x_cord["7"] -margin), y_cord[str(y_pos_1)]), align="left" )
                
                meta_style()
                text( f"{pts}pt", ((x_cord["6"] -margin), y_cord[str(y_pos_2)]), align="right" )
                text( f"{pts}pt", ((x_cord["7"] -margin), y_cord[str(y_pos_2)]), align="left" )
                y_pos_1 = y_pos_1 - 6
                y_pos_2 = y_pos_2 - 6

def drawTwelveColumnLayout():
    global y_pos_1
    global y_pos_2

    # Set type for proof, single type size
    if font_size == font_size_XS:
        type_style()
        fontSize(font_size)
        line_height = font_size * 1.3
        translate(0, -fontCapHeight())

        # Page 1 columns
        textBox(proof_set[:227], (edge_left, -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[228:], (x_cord["1"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[462:], (x_cord["2"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[690:], (x_cord["3"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[918:], (x_cord["4"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[1146:], (x_cord["5"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[1374:], (x_cord["6"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[1602:], (x_cord["7"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[1830:], (x_cord["8"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[2058:], (x_cord["9"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[2286:], (x_cord["10"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[2514:], (x_cord["11"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        textBox(proof_set[2742:], (x_cord["12"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
    
        # Add new page if textString is too long
        if len(proof_set) >= 2742:
        
            newPage(page_dimensions)
            grid()
            drawHeaderFooter()
            translate(margin,margin)
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.3
            translate(0, -fontCapHeight())
        
            # Page 2 columns
            textBox(proof_set[2970:], (edge_left, -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[3198:], (x_cord["1"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[3426:], (x_cord["2"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[3654:], (x_cord["3"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[3882:], (x_cord["4"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[4110:], (x_cord["5"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[4338:], (x_cord["6"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[4566:], (x_cord["7"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[4794:], (x_cord["8"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[5022:], (x_cord["9"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[5250:], (x_cord["10"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[5478:], (x_cord["11"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[5706:], (x_cord["12"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        
            # Add new page if textString is too long
            if len(proof_set) >= 5928:
                
                newPage(page_dimensions)
                grid()
                drawHeaderFooter()
                translate(margin,margin)
                type_style()
                fontSize(font_size)
                line_height = font_size * 1.3
                translate(0, -fontCapHeight())
        
                # Page 2 columns
            
                textBox(proof_set[5934:], (edge_left, -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[6162:], (x_cord["1"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[6390:], (x_cord["2"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[6618:], (x_cord["3"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[6846:], (x_cord["4"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7074:], (x_cord["5"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7302:], (x_cord["6"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7530:], (x_cord["7"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7758:], (x_cord["8"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[7986:], (x_cord["9"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[8214:], (x_cord["10"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[8442:], (x_cord["11"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                textBox(proof_set[8670:], (x_cord["12"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
                
def drawTwoSixColumnLayout():
    global y_pos_1
    global y_pos_2
    
    with savedState():
        
        # Set type for proof, single type size
        if font_size == font_size_XS:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.3
            translate(0, -fontCapHeight())

            # Column Set 1
            textBox(proof_set[:227], (edge_left, -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[178:], (x_cord["1"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[357:], (x_cord["2"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[535:], (x_cord["3"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[714:], (x_cord["4"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[892:], (x_cord["5"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        
            # Column Set 2
            openTypeFeatures(tnum=False)
            textBox(proof_set[:227], (x_cord["7"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[178:], (x_cord["8"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[357:], (x_cord["9"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[535:], (x_cord["10"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[714:], (x_cord["11"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[892:], (x_cord["12"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")

        if font_size == font_size_XXS:
            type_style()
            fontSize(12)
            line_height = font_size * 1.3
            translate(0, -fontCapHeight())

            # Column Set 1
            openTypeFeatures(lnum=False)
            openTypeFeatures(tnum=False)
            textBox(proof_set[:227], (edge_left, -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[178:], (x_cord["1"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[357:], (x_cord["2"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[535:], (x_cord["3"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[714:], (x_cord["4"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[892:], (x_cord["5"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
        
            # Column Set 2
            openTypeFeatures(lnum=False)
            openTypeFeatures(tnum=False)
            textBox(proof_set[:227], (x_cord["7"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[178:], (x_cord["8"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[357:], (x_cord["9"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[535:], (x_cord["10"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[714:], (x_cord["11"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")
            textBox(proof_set[892:], (x_cord["12"], -(y_cord["0"]), (x_cord["1"]), margin_top_bottom), align="left")


# Page template       
def drawNewPage():
    newPage(page_dimensions)
    grid()
    drawHeaderFooter()

    translate(margin,margin)
    if layout == "one_column":
        drawOneColumnLayout()
    elif layout == "two_column":
        drawTwoColumnLayout()
    elif layout == "asymmetric_two_column":
        drawAsymmetricTwoColumnLayout()
    elif layout == "three_column":
        drawThreeColumnLayout()
    elif layout == "four_column":
        drawOneColumnLayout()
    elif layout == "twelve_column":
        drawTwelveColumnLayout()
    elif layout == "two-six_columns":
        drawTwoSixColumnLayout()
            
# Defines on/off button for grid and labels
def grid():
    if show_grid:
        drawGrid()     
    if show_labels:
        drawGridLabels()
# --------------------------------------
# -*- Coordinates -*- # 

x_cord_name_list = list()
x_cord_num_list = list()

y_cord_name_list = list()
y_cord_num_list = list()

x_cord_dict = dict(zip(x_cord_name_list, x_cord_num_list))
zip_x_cords = zip(x_cord_name_list, x_cord_num_list)

y_cord_dict = dict(zip(y_cord_name_list, y_cord_num_list))
zip_y_cords = zip(y_cord_name_list,  y_cord_num_list)

with savedState():
    for x in range(number_of_columns + 1):
        
        col_name = str(x)
        x_cord = str(x * col_width)
        
        x_cord_name_list.append(col_name)
        x_cord_num_list.append(float(x_cord))
        
        for y in range(number_of_rows + 1):
            
            row_name = str(y)
            y_cord = str(y * row_height)
            
            y_cord_name_list.append(row_name)
            y_cord_num_list.append(float(y_cord))

# Create dictionary from zip object
x_cord = dict(zip_x_cords)
y_cord = dict(zip_y_cords)

# --------------------------------------
# -*- Grid -*- # 

# Draws grid
def drawGrid():
    with savedState():
        translate(margin, margin)
        for x in numpy.arange(number_of_columns):
            for y in range(number_of_rows):
                with savedState():
                    fill(None)
                    stroke(1, 0, 0, 0.1)
                    strokeWidth(0.25)
                    rect(x * col_width, y * row_height, col_width, row_height)

# Draws grid labels        
def drawGridLabels():
    with savedState():
        translate(margin, margin)
    
        fill(1, 0, 0, 0.5)
        font(caption_font, 6)
    
        for x in range(number_of_columns + 1):
            text(str(x), (x_cord[str(x)], margin / -2), align="center")
        
        translate(0, (-fontCapHeight() / 2))
        for y in range(number_of_rows + 1):
            text(str(y), (margin / -2, y_cord[str(y)]), align="center")

# --------------------------------------

# def collectFilesPaths(folder, extension=''):
#     """hidden files (starting with a dot) are filtered out"""
#     paths = []
#     for eachFileName in [nn for nn in listdir(folder) if not nn.startswith('.')]:
#         eachPath = join(folder, eachFileName)
#         if isfile(eachPath) and eachPath.endswith(extension):
#             paths.append(eachPath)
#             print(paths)
#         else:
#             print(paths)
#         return paths

                    
# def getFont(folder, extension=''):
    
#     fonts = []
#     for eachFont in folder:
#         eachPath = join(folder, eachFont)
#         if isfile(eachPath) and eachPath.endswith(extension):
#             f = OpenFont(eachFontPath, showInterface = False)
#             fonts.append(f)
#             print(f)
        
# --------------------------------------
# -*- Instructions -*- # 

ufos = glob(os.path.join(font_folder, "*.ufo"))   
allFonts = ufos

if __name__ == '__main__':
    
    # Iterate over all fonts
    for eachFontPath in allFonts:
        
        # Definitions
        f = OpenFont(eachFontPath, showInterface = False)
        f.testInstall
        postscriptFontName = '%s-%s' % (f.info.familyName, f.info.styleName)
        font_version = ''.join(str(f.info.versionMajor) + '.' + str(f.info.versionMinor))
        print(font_version)
        print(postscriptFontName)
        
        # Draws pages
        for eachString in textStrings:
            
            # Definitions
            layout = eachString[0]
            section = eachString[2]
            proof_set = eachString[3]
            
            # Loop de loops
            if eachString[1] == font_size_XXXL:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_XXL:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_XL:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_L:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_M:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_S:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_XS:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == font_size_XXS:
                font_size = eachString[1]
                drawNewPage()

# --------------------------------------
# -*- Save -*- # 

# time_stamp = today.strftime ("%Y-%m-%d")
# path = Path(proof_folder + "/" + time_stamp)


# file_name = (str(path) + "/" + '-'.join(postscriptFontName.split()) + "_proof_" + '-'.join(proof_name.split()))
# file_version = 0


# if (os.path.exists(path)):
#     print("Folder Exists!")
#     while (os.path.exists(file_name + "_" + str(file_version) + ".pdf")):
#         print("File already exists, saved with a numerator")
#         file_version += 1
        
#     saveImage(file_name + "_" + str(file_version) + ".pdf")
#     print("File saved!")
# else:
#     print("Folder does not exist")
#     while (os.path.exists(file_name + "_" + str(file_version) + ".pdf")):
#         print("File already exists, saved with a numerator")
#         file_version += 1
#     path.mkdir(parents=True, exist_ok=True)
#     saveImage(file_name + "_" + str(file_version) + ".pdf")
 

    