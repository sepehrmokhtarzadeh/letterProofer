#
# -*- coding: UTF-8 -*- # ----------------------------------------------------------------------------- #
#
#     letterProofer | Figures
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

font_folder = "Path where fonts are location"
proof_folder = "Path where proofs will be saved"

# To activate saving, uncomment last bit of script below titled "Save"
# This will create a folder in the format "YYYY-MM-DD" and save a PDF in it
# If the folder already exists it should just create the PDF
# If you already saved the file, it will not overwrite but start numbering +1

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
designer_name = "Your Name"
typeface_name = "Your Font Name"
proof_name = "Figures"

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

# --------------------------------------
# -*- Text Strings -*- # 

textStrings = [

    ["one_column", font_size_M, "Numerals, Oldstyle", "7329870978587797219358642839580499304127135734351274062112659782372469939537772177878862212351849746592514739388361831731191325102625591910497885781213188512741970071731425743288340299253716581032974505544226247793823937176799333929072830853294629307453732517333584733968922510473158087292297889012908947721509160261204062365696937003086373659875869281797051905235737527837404463893561116728939755776936576287545872011153763948729946195937343098185452239790103291591481195124187455512472866793579561504708693567067846961019773877249769764723315189874677197977770521807675968545776827588592000823248905191688456428529835355181825678663730679227474393960693934956935877731775528642450235405565755170597711526135662215125098978129995928514518751211643364294116282143873918078177746229828921386213950896023351787261336379941722763749389131045156222888130165407226433670931337210525542943833047327752806892708000569634265379794521729152269111878546361992897387875946820319656396964187020947630880069434061719752073197187962396549500457826988003771095615904830857587198927998450195382548511447854784181850714912600817058876489988567782397708667192072859743053937482571832200150348511666140971945419188890976462582128720228565793727172203527240944963902910889771682794433467110274534811730822882839792894545387707525440186318488021070537525950885547930058904072132258981613339953548745751890617801463910363487862453907182015051898727599789018174778773058426387934711782231352043298110363505589323455628034805155468887918091822085913175384421709058853837237742155890863598915478028499059625971121875982435472127380982968751044926499395800394944382199510993221891593091224516819737477657777970577375385640594620879017174216570116728886345710032735215092526920296845752350275100276921956759608214588440938984716489104332150749268633477176918577199494524977826808173807816534128723607711494949795762525587323157410977956655365091842659816170039300159939471010577809822129456318630279042730965347955372918755935808766286611096197536304600513547254536890599578676517770776073122390991063947701814666069327576528674996825350232135905319517381109559318027018357651770782927519187522333551739930609493619434482785432116737149254577748682007611151669104193135705677079941156358477611642741066074406546349379510878168327239953042375534899471130827227865020965951957963212293857200425270202861297621893762895052393958608614286967728115275265811107168212138682387632036373603821951019920259638529856403930039608719538771569941903286886875948570918286118012800957340110669072700613191589723454367071714055970835258755729304767776726573103848482597704840685156827952059789870410973623603753992446784310072757949800138896391794814609024887181556742025689432246793262235260069932185252771332817097062691270955225259381890391376296557270955430775622885428527562683376057937675987519455180757566911148002067589446098628573989834783718786283961670503353791779591872349803965750762310165780335612652809503976175539281291127196709781790250536502979327682531154731274999538237630075177223796741171093766331211150184198129264213308771703271782510757170136411553890747643561575132059798365914900257378792994112572784069427616982801572005597803947482119753123704765272444205121370171368346767191061221752691954495717795371105081780482501251267141957951594463839216304779396392638390865596969834718076905439652759239885546223395182090091185409636714791458226058951777715014324259803446349809356567641374967707605072984460757509229517395485579558707332355999919360497232821030380015096679934974797626114798333830591960961776807724864201615730791398996051889667150660447158122013594511181415749045808687139127607913565188092681043848071157688153919032541593715322405997812114070039717096781034497765856073155896170786052355653630635788421261210799024513712309977061290119116669437670791181239832489974884814598401881332618835963729857757359637701937007888505402499344912149114909596463072206744127728157955580628567859779636719483181585556547189665809065738040783665458042074311181273902336244575501219155155117113879540845893675721234130779847541796594623438330771842005172748847027150179496879104173710640362681095070533135667759836338057375920766375715979382993110933121207808965689865659388469858263976870889035532715787874093936745569477552220958770886282311947550099772841629725901186153233971477423128307829918565480320057067754051892846375809506025953559565129261117031956876625455611966829274527037134675872993891574078867078923294514924617941096732371056352890717167470113755938324715750824111822435138902549009316059017190265179123407397701323604255729275769800998895124884815975068771917924777415547379069187427953735967363583121432799012816317662008605388366281164703397744200245603731157711197286853882355092585381480402303555818719855505471320142410820139771660627019219474096030099787722978246229325497726255313490315533461800419330882839921539933635799620279126783620205070999365827638957224582186615555137358322548751948297273769983627141052709803840363270654736937582343389510614382026511450443494258907171048871266857954808537965793071613157371188584367306435254252079566774439732926544206290230495325642237516134479586597678800130625016440519428532658859899528677965951391599781329123101996572815505448786808722595041058478709527545633573571947518474923763894725431165715958311344005785778290592576750370359748719087487267010578567771933691815289427706685976619053601304562970570357245719526616431332658406637821767482661609397272958399481429650250240124049068115641575590666872079235571529377713563721185719912531228788269816937338527167291793738216524483817537720139477155500342305220216335794794783229834284037045442295857614927640570212012052655599341735377350485042131769777982719851723997374417271947708655417257982071450319595957711625965020789357534742276599951074307763792090485825187866809435061112154017480729137100935337350467392056100929597706515359878234023303465958863834296609820685993154588519195765486220427311666491931053451471999117916800451669158452098707503374514110681206417476564143886731248417662817713527921805095670186906505526127913345965253062626862119901286285374510709328373585025466861626599270086487050572115057597882003598245272582195276883705822579095997916048337856866690585017399513729722655485375587529975731091736192062137729935769068790907633769432447577524451758713130815533454021325598137120867252378531702282189802481293971744868819784548667386191724519770335373857970477421837907906311335219572874808308594204951685707152876995987111561244967866434859765179536238715149353155517854211501786885118816101739876912281573173329363974974787579583725925885537767742258177177970912054735467591323731811899959723511377863711029169730892323961030579337309996125754986377153761261529828109799278827727706225240882857095170725578275910321766291538142485800841897515908751302099731024405503077477220929627293303849479902498916756906721491825459673830766436033077302994683173183094377783735130381999149807917591717711613538917371596708844232859974638624982803476001997413608551104253257170657135686973095961172558883149573552745251422743127880074520245072709989954492796465121919562697365309912821142508872669370402198172326231329751129787981712038774589772267020513369525617828287522050058179084085294914653844117073535614291551763572133007890640152669428610773672112956258167308512979129206670366176846182790584297798675119788851351597544764473742217703248177938609251842831039137734856098772730123813390803371908856552494172155663783995493105970568423583028600893215388611994126517129793489339779120006277932257023997768317627903974282573031167605653787177319212987439266070191995073971593182157837924260046550994023027107811768814735177433939787039552541759829395017679727865554785355419981991695854924331730505505379435800130436038134355495039315516796970898551732184181891193540193171920826125840957359207348366708096174237463004401488780353980651721941955671485443587095236575087036374900227388023487785167228220805568486005185690993568935815937839730448147732971172965889177815517928626983762734254167942037916448873059020257250715557917338208222349161744682570032859821931692725458045133639785991935592900606755093965422137975221739056293565704521897661316827731674470839767279497001732126013849861984240560428230377949112768171389522340383703190447469840969321984769079999522793002024761263220287938406410184775205603904221089617747331181916258057461976318479568722678715302276520285784770294417070544505825837919195587971753023556907052581578819177473457757539264535735857036590852473311029349337087123007359756921537079247232072520745831902851869507618049235203994232804692723741918973942875902071229030423236558241345875479847571566515252473276430122639806551571536287650897156789838789859277024250341532649516928090156306714623559509249739289119419876976264317539274686352453502549362972987176592710484507023695687696770802662972902784448530989147837016330251447401262877759317712695483897599357149708769612923351507541437400847207690123368002693502965611677714674815480739904762546038529499059063787150533770926849653201879704120519933028108314730397255158403464525470600609680527717199157582953381030178637659500785948559572330384175047504940260013791553776183483780631330475655200275872080274086045787191972468373555708722717974276477173954109673828188867771112707792523826883094332710273213812577171777507398913526037333561162636314546534474297615495733950298977748274545241611119489059226237898095651181138311685995048297330772663139192223915517452814799883977302891990765707879185648182620762629522600057715174816328541094896831839027449764873275107305479053990520566555231854875100984209188172590616909734195978048397957984693711407779155627707410863625456025625936537388525277626236870249872864259577346081373994615909522040010146150207487248097191944640394892859830717335871943157942239504151270086321757327180977716780374388831300842709596851901625790472357719"],
    
    [ "two-six_columns", font_size_XS, "Side bearings - Oldstyle", "0,00\n0,10\n0,20\n0,30\n0,40\n0,50\n0,60\n0,70\n0,80\n0,90\n\n1,01\n1,11\n1,21\n1,31\n1,41\n1,51\n1,61\n1,71\n1,81\n1,91\n\n2,02\n2,12\n2,22\n2,32\n2,42\n2,52\n2,62\n2,72\n2,82\n2,92\n\n3,03\n3,13\n3,23\n3,33\n3,43\n3,53\n3,63\n3,73\n3,83\n3,93\n\n4,04\n4,14\n4,24\n4,34\n4,44\n4,54\n4,64\n4,74\n4,84\n4,94\n\n5,05\n5,15\n5,25\n5,35\n5,45\n5,55\n5,65\n5,75\n5,85\n5,95\n\n6,06\n6,16\n6,26\n6,36\n6,46\n6,56\n6,66\n6,76\n6,86\n6,96\n\n7,07\n7,17\n7,27\n7,37\n7,47\n7,57\n7,67\n7,77\n7,87\n7,97\n\n8,08\n8,18\n8,28\n8,38\n8,48\n8,58\n8,68\n8,78\n8,88\n8,98\n\n9,09\n9,19\n9,29\n9,39\n9,49\n9,59\n9,69\n9,79\n9,89\n9,99\n\n0:00\n0:10\n0:20\n0:30\n0:40\n0:50\n0:60\n0:70\n0:80\n0:90\n\n1:01\n1:11\n1:21\n1:31\n1:41\n1:51\n1:61\n1:71\n1:81\n1:91\n\n2:02\n2:12\n2:22\n2:32\n2:42\n2:52\n2:62\n2:72\n2:82\n2:92\n\n3:03\n3:13\n3:23\n3:33\n3:43\n3:53\n3:63\n3:73\n3:83\n3:93\n\n4:04\n4:14\n4:24\n4:34\n4:44\n4:54\n4:64\n4:74\n4:84\n4:94\n\n5:05\n5:15\n5:25\n5:35\n5:45\n5:55\n5:65\n5:75\n5:85\n5:95\n\n6:06\n6:16\n6:26\n6:36\n6:46\n6:56\n6:66\n6:76\n6:86\n6:96\n\n7:07\n7:17\n7:27\n7:37\n7:47\n7:57\n7:67\n7:77\n7:87\n7:97\n\n8:08\n8:18\n8:28\n8:38\n8:48\n8:58\n8:68\n8:78\n8:88\n8:98\n\n9:09\n9:19\n9:29\n9:39\n9:49\n9:59\n9:69\n9:79\n9:89\n9:99"],
    
    [ "two-six_columns", font_size_XXS, "Side bearings - Lining", "0,00\n0,10\n0,20\n0,30\n0,40\n0,50\n0,60\n0,70\n0,80\n0,90\n\n1,01\n1,11\n1,21\n1,31\n1,41\n1,51\n1,61\n1,71\n1,81\n1,91\n\n2,02\n2,12\n2,22\n2,32\n2,42\n2,52\n2,62\n2,72\n2,82\n2,92\n\n3,03\n3,13\n3,23\n3,33\n3,43\n3,53\n3,63\n3,73\n3,83\n3,93\n\n4,04\n4,14\n4,24\n4,34\n4,44\n4,54\n4,64\n4,74\n4,84\n4,94\n\n5,05\n5,15\n5,25\n5,35\n5,45\n5,55\n5,65\n5,75\n5,85\n5,95\n\n6,06\n6,16\n6,26\n6,36\n6,46\n6,56\n6,66\n6,76\n6,86\n6,96\n\n7,07\n7,17\n7,27\n7,37\n7,47\n7,57\n7,67\n7,77\n7,87\n7,97\n\n8,08\n8,18\n8,28\n8,38\n8,48\n8,58\n8,68\n8,78\n8,88\n8,98\n\n9,09\n9,19\n9,29\n9,39\n9,49\n9,59\n9,69\n9,79\n9,89\n9,99\n\n0:00\n0:10\n0:20\n0:30\n0:40\n0:50\n0:60\n0:70\n0:80\n0:90\n\n1:01\n1:11\n1:21\n1:31\n1:41\n1:51\n1:61\n1:71\n1:81\n1:91\n\n2:02\n2:12\n2:22\n2:32\n2:42\n2:52\n2:62\n2:72\n2:82\n2:92\n\n3:03\n3:13\n3:23\n3:33\n3:43\n3:53\n3:63\n3:73\n3:83\n3:93\n\n4:04\n4:14\n4:24\n4:34\n4:44\n4:54\n4:64\n4:74\n4:84\n4:94\n\n5:05\n5:15\n5:25\n5:35\n5:45\n5:55\n5:65\n5:75\n5:85\n5:95\n\n6:06\n6:16\n6:26\n6:36\n6:46\n6:56\n6:66\n6:76\n6:86\n6:96\n\n7:07\n7:17\n7:27\n7:37\n7:47\n7:57\n7:67\n7:77\n7:87\n7:97\n\n8:08\n8:18\n8:28\n8:38\n8:48\n8:58\n8:68\n8:78\n8:88\n8:98\n\n9:09\n9:19\n9:29\n9:39\n9:49\n9:59\n9:69\n9:79\n9:89\n9:99"]

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
        
        if font_size == font_size_XL:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.2
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
        
        elif font_size == font_size_M:
            
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.2
            translate(0, -fontCapHeight())
            openTypeFeatures(lnum=False)
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")

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

# Draws title page
def drawTitlePage(section=""):
    with savedState():
        translate(margin, margin)
        with savedState():
            translate(0, fontCapHeight() * 2)
            meta_style()
            # text(designer_name, (x_cord["0"], y_cord["48"]))
            # text(typeface_name, (x_cord["0"], y_cord["46"]))
            text((''.join(postscriptFontName + " " + font_version + " " + proof_name)), (edge_right, edge_top + 5), align = "right")
            openTypeFeatures(tnum=True)
            text((''.join(current_date + " , " + current_time)), (edge_right, edge_top - 7), align = "right")
        
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
        font_version = ''.join('v.' + str(f.info.versionMajor) + '.' + str(f.info.versionMinor))
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

# -!- ALWAYS KEEP AT BOTTOM OF CODE -!-
# --------------------------------------
# -*- Page Numbers -*- # 

# Get all pages
allPages = pages()

page_number = 0

for page in allPages:
    
    # With each loop, add 1 to page number
    page_number += 1
    
    # Set first page as current context
    if page_number == 1:
        
        # Style first page
        with page:
            grid()
            drawTitlePage("")
    else:
        
        # Set next page as current context & add page number
        with page:
            meta_style()
            translate(0, -fontCapHeight())
            text(str(page_number), (edge_right, edge_bottom - 10), align="right")

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
 

    