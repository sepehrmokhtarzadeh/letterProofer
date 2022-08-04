#
# -*- coding: UTF-8 -*- # ----------------------------------------------------------------------------- #
#
#     letterProofer | Bearings, LC
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
proof_name = "Bearings, LC"

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
    
[ "twelve_column", font_size_XS, "Bearings, LC", "naaan\nnaban\nnacan\nnadan\nnaean\nnafan\nnagan\nnahan\nnaian\nnajan\nnakan\nnalan\nnaman\nnanan\nnaoan\nnapan\nnaqan\nnaran\nnasan\nnatan\nnauan\nnavan\nnawan\nnaxan\nnayan\nnazan\nnbabn\nnbbbn\nnbcbn\nnbdbn\nnbebn\nnbfbn\nnbgbn\nnbhbn\nnbibn\nnbjbn\nnbkbn\nnblbn\nnbmbn\nnbnbn\nnbobn\nnbpbn\nnbqbn\nnbrbn\nnbsbn\nnbtbn\nnbubn\nnbvbn\nnbwbn\nnbxbn\nnbybn\nnbzbn\nncacn\nncbcn\nncccn\nncdcn\nncecn\nncfcn\nncgcn\nnchcn\nncicn\nncjcn\nnckcn\nnclcn\nncmcn\nncncn\nncocn\nncpcn\nncqcn\nncrcn\nncscn\nnctcn\nncucn\nncvcn\nncwcn\nncxcn\nncycn\nnczcn\nndadn\nndbdn\nndcdn\nndddn\nndedn\nndfdn\nndgdn\nndhdn\nndidn\nndjdn\nndkdn\nndldn\nndmdn\nndndn\nndodn\nndpdn\nndqdn\nndrdn\nndsdn\nndtdn\nndudn\nndvdn\nndwdn\nndxdn\nndydn\nndzdn\nneaen\nneben\nnecen\nneden\nneeen\nnefen\nnegen\nnehen\nneien\nnejen\nneken\nnelen\nnemen\nnenen\nneoen\nnepen\nneqen\nneren\nnesen\nneten\nneuen\nneven\nnewen\nnexen\nneyen\nnezen\nnfafn\nnfbfn\nnfcfn\nnfdfn\nnfefn\nnfffn\nnfgfn\nnfhfn\nnfifn\nnfjfn\nnfkfn\nnflfn\nnfmfn\nnfnfn\nnfofn\nnfpfn\nnfqfn\nnfrfn\nnfsfn\nnftfn\nnfufn\nnfvfn\nnfwfn\nnfxfn\nnfyfn\nnfzfn\nngagn\nngbgn\nngcgn\nngdgn\nngegn\nngfgn\nngggn\nnghgn\nngign\nngjgn\nngkgn\nnglgn\nngmgn\nngngn\nngogn\nngpgn\nngqgn\nngrgn\nngsgn\nngtgn\nngugn\nngvgn\nngwgn\nngxgn\nngygn\nngzgn\nnhahn\nnhbhn\nnhchn\nnhdhn\nnhehn\nnhfhn\nnhghn\nnhhhn\nnhihn\nnhjhn\nnhkhn\nnhlhn\nnhmhn\nnhnhn\nnhohn\nnhphn\nnhqhn\nnhrhn\nnhshn\nnhthn\nnhuhn\nnhvhn\nnhwhn\nnhxhn\nnhyhn\nnhzhn\nniain\nnibin\nnicin\nnidin\nniein\nnifin\nnigin\nnihin\nniiin\nnijin\nnikin\nnilin\nnimin\nninin\nnioin\nnipin\nniqin\nnirin\nnisin\nnitin\nniuin\nnivin\nniwin\nnixin\nniyin\nnizin\nnjajn\nnjbjn\nnjcjn\nnjdjn\nnjejn\nnjfjn\nnjgjn\nnjhjn\nnjijn\nnjjjn\nnjkjn\nnjljn\nnjmjn\nnjnjn\nnjojn\nnjpjn\nnjqjn\nnjrjn\nnjsjn\nnjtjn\nnjujn\nnjvjn\nnjwjn\nnjxjn\nnjyjn\nnjzjn\nnkakn\nnkbkn\nnkckn\nnkdkn\nnkekn\nnkfkn\nnkgkn\nnkhkn\nnkikn\nnkjkn\nnkkkn\nnklkn\nnkmkn\nnknkn\nnkokn\nnkpkn\nnkqkn\nnkrkn\nnkskn\nnktkn\nnkukn\nnkvkn\nnkwkn\nnkxkn\nnkykn\nnkzkn\nnlaln\nnlbln\nnlcln\nnldln\nnleln\nnlfln\nnlgln\nnlhln\nnliln\nnljln\nnlkln\nnllln\nnlmln\nnlnln\nnloln\nnlpln\nnlqln\nnlrln\nnlsln\nnltln\nnluln\nnlvln\nnlwln\nnlxln\nnlyln\nnlzln\nnmamn\nnmbmn\nnmcmn\nnmdmn\nnmemn\nnmfmn\nnmgmn\nnmhmn\nnmimn\nnmjmn\nnmkmn\nnmlmn\nnmmmn\nnmnmn\nnmomn\nnmpmn\nnmqmn\nnmrmn\nnmsmn\nnmtmn\nnmumn\nnmvmn\nnmwmn\nnmxmn\nnmymn\nnmzmn\nnnann\nnnbnn\nnncnn\nnndnn\nnnenn\nnnfnn\nnngnn\nnnhnn\nnninn\nnnjnn\nnnknn\nnnlnn\nnnmnn\nnnnnn\nnnonn\nnnpnn\nnnqnn\nnnrnn\nnnsnn\nnntnn\nnnunn\nnnvnn\nnnwnn\nnnxnn\nnnynn\nnnznn\nnoaon\nnobon\nnocon\nnodon\nnoeon\nnofon\nnogon\nnohon\nnoion\nnojon\nnokon\nnolon\nnomon\nnonon\nnooon\nnopon\nnoqon\nnoron\nnoson\nnoton\nnouon\nnovon\nnowon\nnoxon\nnoyon\nnozon\nnpapn\nnpbpn\nnpcpn\nnpdpn\nnpepn\nnpfpn\nnpgpn\nnphpn\nnpipn\nnpjpn\nnpkpn\nnplpn\nnpmpn\nnpnpn\nnpopn\nnpppn\nnpqpn\nnprpn\nnpspn\nnptpn\nnpupn\nnpvpn\nnpwpn\nnpxpn\nnpypn\nnpzpn\nnqaqn\nnqbqn\nnqcqn\nnqdqn\nnqeqn\nnqfqn\nnqgqn\nnqhqn\nnqiqn\nnqjqn\nnqkqn\nnqlqn\nnqmqn\nnqnqn\nnqoqn\nnqpqn\nnqqqn\nnqrqn\nnqsqn\nnqtqn\nnquqn\nnqvqn\nnqwqn\nnqxqn\nnqyqn\nnqzqn\nnrarn\nnrbrn\nnrcrn\nnrdrn\nnrern\nnrfrn\nnrgrn\nnrhrn\nnrirn\nnrjrn\nnrkrn\nnrlrn\nnrmrn\nnrnrn\nnrorn\nnrprn\nnrqrn\nnrrrn\nnrsrn\nnrtrn\nnrurn\nnrvrn\nnrwrn\nnrxrn\nnryrn\nnrzrn\nnsasn\nnsbsn\nnscsn\nnsdsn\nnsesn\nnsfsn\nnsgsn\nnshsn\nnsisn\nnsjsn\nnsksn\nnslsn\nnsmsn\nnsnsn\nnsosn\nnspsn\nnsqsn\nnsrsn\nnsssn\nnstsn\nnsusn\nnsvsn\nnswsn\nnsxsn\nnsysn\nnszsn\nntatn\nntbtn\nntctn\nntdtn\nntetn\nntftn\nntgtn\nnthtn\nntitn\nntjtn\nntktn\nntltn\nntmtn\nntntn\nntotn\nntptn\nntqtn\nntrtn\nntstn\nntttn\nntutn\nntvtn\nntwtn\nntxtn\nntytn\nntztn\nnuaun\nnubun\nnucun\nnudun\nnueun\nnufun\nnugun\nnuhun\nnuiun\nnujun\nnukun\nnulun\nnumun\nnunun\nnuoun\nnupun\nnuqun\nnurun\nnusun\nnutun\nnuuun\nnuvun\nnuwun\nnuxun\nnuyun\nnuzun\nnvavn\nnvbvn\nnvcvn\nnvdvn\nnvevn\nnvfvn\nnvgvn\nnvhvn\nnvivn\nnvjvn\nnvkvn\nnvlvn\nnvmvn\nnvnvn\nnvovn\nnvpvn\nnvqvn\nnvrvn\nnvsvn\nnvtvn\nnvuvn\nnvvvn\nnvwvn\nnvxvn\nnvyvn\nnvzvn\nnwawn\nnwbwn\nnwcwn\nnwdwn\nnwewn\nnwfwn\nnwgwn\nnwhwn\nnwiwn\nnwjwn\nnwkwn\nnwlwn\nnwmwn\nnwnwn\nnwown\nnwpwn\nnwqwn\nnwrwn\nnwswn\nnwtwn\nnwuwn\nnwvwn\nnwwwn\nnwxwn\nnwywn\nnwzwn\nnxaxn\nnxbxn\nnxcxn\nnxdxn\nnxexn\nnxfxn\nnxgxn\nnxhxn\nnxixn\nnxjxn\nnxkxn\nnxlxn\nnxmxn\nnxnxn\nnxoxn\nnxpxn\nnxqxn\nnxrxn\nnxsxn\nnxtxn\nnxuxn\nnxvxn\nnxwxn\nnxxxn\nnxyxn\nnxzxn\nnyayn\nnybyn\nnycyn\nnydyn\nnyeyn\nnyfyn\nnygyn\nnyhyn\nnyiyn\nnyjyn\nnykyn\nnylyn\nnymyn\nnynyn\nnyoyn\nnypyn\nnyqyn\nnyryn\nnysyn\nnytyn\nnyuyn\nnyvyn\nnywyn\nnyxyn\nnyyyn\nnyzyn\nnzazn\nnzbzn\nnzczn\nnzdzn\nnzezn\nnzfzn\nnzgzn\nnzhzn\nnzizn\nnzjzn\nnzkzn\nnzlzn\nnzmzn\nnznzn\nnzozn\nnzpzn\nnzqzn\nnzrzn\nnzszn\nnztzn\nnzuzn\nnzvzn\nnzwzn\nnzxzn\nnzyzn\nnzzzn\noaaao\noabao\noacao\noadao\noaeao\noafao\noagao\noahao\noaiao\noajao\noakao\noalao\noamao\noanao\noaoao\noapao\noaqao\noarao\noasao\noatao\noauao\noavao\noawao\noaxao\noayao\noazao\nobabo\nobbbo\nobcbo\nobdbo\nobebo\nobfbo\nobgbo\nobhbo\nobibo\nobjbo\nobkbo\noblbo\nobmbo\nobnbo\nobobo\nobpbo\nobqbo\nobrbo\nobsbo\nobtbo\nobubo\nobvbo\nobwbo\nobxbo\nobybo\nobzbo\nocaco\nocbco\noccco\nocdco\noceco\nocfco\nocgco\nochco\nocico\nocjco\nockco\noclco\nocmco\nocnco\nococo\nocpco\nocqco\nocrco\nocsco\noctco\nocuco\nocvco\nocwco\nocxco\nocyco\noczco\nodado\nodbdo\nodcdo\nodddo\nodedo\nodfdo\nodgdo\nodhdo\nodido\nodjdo\nodkdo\nodldo\nodmdo\nodndo\nododo\nodpdo\nodqdo\nodrdo\nodsdo\nodtdo\nodudo\nodvdo\nodwdo\nodxdo\nodydo\nodzdo\noeaeo\noebeo\noeceo\noedeo\noeeeo\noefeo\noegeo\noeheo\noeieo\noejeo\noekeo\noeleo\noemeo\noeneo\noeoeo\noepeo\noeqeo\noereo\noeseo\noeteo\noeueo\noeveo\noeweo\noexeo\noeyeo\noezeo\nofafo\nofbfo\nofcfo\nofdfo\nofefo\nofffo\nofgfo\nofhfo\nofifo\nofjfo\nofkfo\noflfo\nofmfo\nofnfo\nofofo\nofpfo\nofqfo\nofrfo\nofsfo\noftfo\nofufo\nofvfo\nofwfo\nofxfo\nofyfo\nofzfo\nogago\nogbgo\nogcgo\nogdgo\nogego\nogfgo\nogggo\noghgo\nogigo\nogjgo\nogkgo\noglgo\nogmgo\nogngo\nogogo\nogpgo\nogqgo\nogrgo\nogsgo\nogtgo\nogugo\nogvgo\nogwgo\nogxgo\nogygo\nogzgo\nohaho\nohbho\nohcho\nohdho\noheho\nohfho\nohgho\nohhho\nohiho\nohjho\nohkho\nohlho\nohmho\nohnho\nohoho\nohpho\nohqho\nohrho\nohsho\nohtho\nohuho\nohvho\nohwho\nohxho\nohyho\nohzho\noiaio\noibio\noicio\noidio\noieio\noifio\noigio\noihio\noiiio\noijio\noikio\noilio\noimio\noinio\noioio\noipio\noiqio\noirio\noisio\noitio\noiuio\noivio\noiwio\noixio\noiyio\noizio\nojajo\nojbjo\nojcjo\nojdjo\nojejo\nojfjo\nojgjo\nojhjo\nojijo\nojjjo\nojkjo\nojljo\nojmjo\nojnjo\nojojo\nojpjo\nojqjo\nojrjo\nojsjo\nojtjo\nojujo\nojvjo\nojwjo\nojxjo\nojyjo\nojzjo\nokako\nokbko\nokcko\nokdko\nokeko\nokfko\nokgko\nokhko\nokiko\nokjko\nokkko\noklko\nokmko\noknko\nokoko\nokpko\nokqko\nokrko\noksko\noktko\nokuko\nokvko\nokwko\nokxko\nokyko\nokzko\nolalo\nolblo\nolclo\noldlo\nolelo\nolflo\nolglo\nolhlo\nolilo\noljlo\nolklo\nolllo\nolmlo\nolnlo\nololo\nolplo\nolqlo\nolrlo\nolslo\noltlo\nolulo\nolvlo\nolwlo\nolxlo\nolylo\nolzlo\nomamo\nombmo\nomcmo\nomdmo\nomemo\nomfmo\nomgmo\nomhmo\nomimo\nomjmo\nomkmo\nomlmo\nommmo\nomnmo\nomomo\nompmo\nomqmo\nomrmo\nomsmo\nomtmo\nomumo\nomvmo\nomwmo\nomxmo\nomymo\nomzmo\nonano\nonbno\noncno\nondno\noneno\nonfno\nongno\nonhno\nonino\nonjno\nonkno\nonlno\nonmno\nonnno\nonono\nonpno\nonqno\nonrno\nonsno\nontno\nonuno\nonvno\nonwno\nonxno\nonyno\nonzno\nooaoo\nooboo\noocoo\noodoo\nooeoo\noofoo\noogoo\noohoo\nooioo\noojoo\nookoo\nooloo\noomoo\noonoo\nooooo\noopoo\nooqoo\nooroo\noosoo\nootoo\noouoo\noovoo\noowoo\nooxoo\nooyoo\noozoo\nopapo\nopbpo\nopcpo\nopdpo\nopepo\nopfpo\nopgpo\nophpo\nopipo\nopjpo\nopkpo\noplpo\nopmpo\nopnpo\nopopo\nopppo\nopqpo\noprpo\nopspo\noptpo\nopupo\nopvpo\nopwpo\nopxpo\nopypo\nopzpo\noqaqo\noqbqo\noqcqo\noqdqo\noqeqo\noqfqo\noqgqo\noqhqo\noqiqo\noqjqo\noqkqo\noqlqo\noqmqo\noqnqo\noqoqo\noqpqo\noqqqo\noqrqo\noqsqo\noqtqo\noquqo\noqvqo\noqwqo\noqxqo\noqyqo\noqzqo\noraro\norbro\norcro\nordro\norero\norfro\norgro\norhro\noriro\norjro\norkro\norlro\normro\nornro\nororo\norpro\norqro\norrro\norsro\nortro\noruro\norvro\norwro\norxro\noryro\norzro\nosaso\nosbso\noscso\nosdso\noseso\nosfso\nosgso\noshso\nosiso\nosjso\noskso\noslso\nosmso\nosnso\nososo\nospso\nosqso\nosrso\nossso\nostso\nosuso\nosvso\noswso\nosxso\nosyso\noszso\notato\notbto\notcto\notdto\noteto\notfto\notgto\nothto\notito\notjto\notkto\notlto\notmto\notnto\nototo\notpto\notqto\notrto\notsto\nottto\notuto\notvto\notwto\notxto\notyto\notzto\nouauo\noubuo\noucuo\nouduo\noueuo\noufuo\nouguo\nouhuo\nouiuo\noujuo\noukuo\nouluo\noumuo\nounuo\nououo\noupuo\nouquo\nouruo\nousuo\noutuo\nouuuo\nouvuo\nouwuo\nouxuo\nouyuo\nouzuo\novavo\novbvo\novcvo\novdvo\novevo\novfvo\novgvo\novhvo\novivo\novjvo\novkvo\novlvo\novmvo\novnvo\novovo\novpvo\novqvo\novrvo\novsvo\novtvo\novuvo\novvvo\novwvo\novxvo\novyvo\novzvo\nowawo\nowbwo\nowcwo\nowdwo\nowewo\nowfwo\nowgwo\nowhwo\nowiwo\nowjwo\nowkwo\nowlwo\nowmwo\nownwo\nowowo\nowpwo\nowqwo\nowrwo\nowswo\nowtwo\nowuwo\nowvwo\nowwwo\nowxwo\nowywo\nowzwo\noxaxo\noxbxo\noxcxo\noxdxo\noxexo\noxfxo\noxgxo\noxhxo\noxixo\noxjxo\noxkxo\noxlxo\noxmxo\noxnxo\noxoxo\noxpxo\noxqxo\noxrxo\noxsxo\noxtxo\noxuxo\noxvxo\noxwxo\noxxxo\noxyxo\noxzxo\noyayo\noybyo\noycyo\noydyo\noyeyo\noyfyo\noygyo\noyhyo\noyiyo\noyjyo\noykyo\noylyo\noymyo\noynyo\noyoyo\noypyo\noyqyo\noyryo\noysyo\noytyo\noyuyo\noyvyo\noywyo\noyxyo\noyyyo\noyzyo\nozazo\nozbzo\nozczo\nozdzo\nozezo\nozfzo\nozgzo\nozhzo\nozizo\nozjzo\nozkzo\nozlzo\nozmzo\noznzo\nozozo\nozpzo\nozqzo\nozrzo\nozszo\noztzo\nozuzo\nozvzo\nozwzo\nozxzo\nozyzo\nozzzo"],

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

# Page template       
def drawNewPage():
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
 

    