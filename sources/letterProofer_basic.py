#
# -*- coding: UTF-8 -*- # ----------------------------------------------------------------------------- #
#
#     letterProofer | Words
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
proof_name = "Letterproof"

# Set caption font
caption_font = "Menlo"
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
font_size_S = 18
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

tracking_amount = 15

# --------------------------------------
# -*- Text Strings -*- # 

textStrings = [ 

    # Lowercase alphabet
    [ "one_column", font_size_XXL, "Lowercase alphabet", "abcdefg\nhijklmno\npqrstuv\nwxyz.,"],
    
    # Lowercase Latin
    [ "asymmetric_two_column", font_size_XS, "Lowercase Latin", "proof set elsewhere"],
    
    # Uppercase alphabet
    [ "one_column", font_size_XXL,  "Uppercase alphabet", "ABCDEFG\nHIJKLMNO\nPQRSTUV\nWXYZ&?!"],
    
    # Uppercase Latin
    [ "asymmetric_two_column", font_size_XXS, "Uppercase Latin", "proof set elsehwere"],    

    # Obliques
    [ "one_column", waterfall_L, "Relative weight of obliques", "ikiviwixiyiziIKIVIWIXIYIZI" ],

    # Lowercase & Uppercase alphabet
    [ "one_column", font_size_XL,  "Lowercase & Uppercase alphabet", "Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz"],
    
    # Figures, currency
    [ "one_column", font_size_XL,   "Figures, currency symbols and math characters", ''.join([string.digits, "0§¶$¢ƒ£¥€8°'*\nn-–—o\n", "0−+±×÷=≈#%8" ])],
        
    # Diacritics & Central European
    [ "one_column", font_size_L, "Diacritics and Central European glyphs", "˝`´ˆˇ˘˜˚˙¨¯¸˛\næœąęįųçđðħĸłŋøßŧıȷ\næœāåďťŀľģķòóőôǒŏöõōñ\nÆŒÅĄĘĮŲÇĐÐĦŦŁŊØSS\nÆŒĎŤĿĽĢÒÓŐÔǑŎÖÕŌÑ" ],
    
    # Basic character set
    [ "one_column", font_size_L, "Basic character set overview",  ''.join(["@", string.ascii_lowercase,";:,.\n „“‘l’”", "H?![]{}()/|\ ·-–—[Hq]\n", string.ascii_uppercase, "H&H\n", "©1234567890§¶$¢ƒ£¥€8°'\n 0−+±×÷=≈#%8\n0123456789" ])],


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
            translate(0, -(line_height / 2))
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
        elif font_size == font_size_L:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.1
            lineHeight(line_height)
            translate(0, (line_height - 90))
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, (margin_top_bottom + 20)), align="center")
            
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
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
        elif font_size == font_size_XS:
            type_style()
            fontSize(font_size)
            lineHeight(font_size * 1.4)
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")
            
        elif font_size == font_size_XXS:
            type_style()
            fontSize(font_size)
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="center")

        # Set type for proof, waterfalls 
        if font_size == waterfall_L:
            type_style()
            y_pos_1 = 42
            y_pos_2 = y_pos_1 - 2 
            
            for pts in font_size:
                type_style()
                fontSize(pts)
                translate(0, -fontCapHeight())
                
                if y_pos_1 < 0:
                    continue
                    if y_pos_2 < 0:
                        continue 
                             
                text( proof_set, (x_cord["0"], y_cord[str(y_pos_1)]) )
                
                meta_style()
                text( f"{pts}pt", (x_cord["0"], y_cord[str(y_pos_2)]) )
                y_pos_1 = y_pos_1 - 6
                y_pos_2 = y_pos_2 - 6
                                
        elif font_size == waterfall_M:
            type_style()     
            translate(0, -fontCapHeight())
                
            # Waterfall 1
            fontSize(14)                        
            textBox( proof_set, (x_cord["0"], y_cord["0"], margin_left_right, margin_top_bottom -fontCapHeight()*6) )
            
            # Waterfall 2
            wtr = FormattedString()
            wtr.fontSize(18)
            wtr.font(font_name)
            wtr.fallbackFont("AdobeBlank")
            wtr += proof_set
            textBox( wtr, (x_cord["0"], y_cord["0"], margin_left_right, margin_top_bottom -fontCapHeight()*12) ) 
            
            # Waterfall 3
            wtr = FormattedString()
            wtr.fontSize(24)
            wtr.font(font_name)
            wtr.fallbackFont("AdobeBlank")
            wtr += proof_set
            textBox( wtr, (x_cord["0"], y_cord["0"], margin_left_right, margin_top_bottom -fontCapHeight()*18) ) 

            # Waterfall 4
            wtr = FormattedString()
            wtr.fontSize(36)
            wtr.font(font_name)
            wtr.fallbackFont("AdobeBlank")
            wtr += proof_set
            textBox( wtr, (x_cord["0"], y_cord["0"], margin_left_right, margin_top_bottom -fontCapHeight()*28) ) 
                
        elif font_size == waterfall_S:
            type_style()     
            fontSize(font_size)

            for pts in font_size:
                fontSize(pts)
                translate(0, -fontCapHeight())
                # print(pts)
                # textWidth, textHeight = textSize(proof_set)
                text( proof_set, (x_cord["0"], y_cord[str(y_pos_1)]) )
                meta_style()
                text( f"{pts}pt", (x_cord["0"], y_cord[str(y_pos_2)]) )
                y_pos_1 = y_pos_1 - 6
                y_pos_2 = y_pos_2 - 6


def drawTwoColumnLayout():
    global y_pos_1
    global y_pos_2
    
    with savedState():

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
            
def drawAsymmetricTwoColumnLayout():
    global y_pos_1
    global y_pos_2
    
    with savedState():
        if font_size == font_size_XS:
            type_style()
            
            # Column 1
            fontSize(12)
            line_height = 10 * 1.3
            translate(0, -fontCapHeight())
            textBox("nnanonoaoo	uan\nnnbnonoboo	ubn\nnncnonocoo	ucn\nnndnonodoo	udn\nnnenonoeoo	uen\nnnfnonofoo	ufn\nnngnonogoo	ugn\n nnhonohoo	uhn\nnninonoioo	uin\nnnjnonojoo	ujn\nnnknonokoo	ukn\nnnlnonoloo	uln\nnnmnonomoo	umn\nnnnnononoo	unn\nnnononoooo	uon\nnnpnonopoo	upn\n nnqnonoqoo	uqn\nnnrnonoroo	urn\nnnsnonosoo	usn\nnntnonotoo	utn\nnnunonouoo	uun\n nnvnonovoo	uvn\nnnwnonowoo	uwn\nnnxnonoxoo	uxn\nnnynonoyoo	uyn\nnnznonozoo	uzn\n\nnn.nono.oo	u.n\nnn,nono,oo	u,n\n", (edge_left, -(y_cord["2"]), x_cord["3"], margin_top_bottom), align="left")
            
            # Column 2
            fontSize(12)
            line_height = 12 * 1.3
            translate(0, -fontCapHeight())
            baselineShift(3.75)
            textBox("Angel Adept Blind Bodice Clique Coast Dunce Docile Enact Eosin Furlong Focal Gnome Gondola Human Hoist Inlet Iodine Justin Jocose Knoll Koala Linden Loads Milliner Modal Number Nodule Onset Oddball Pneumo Poncho Quanta Qophs Rhone Roman Snout Sodium Tundra Tocsin Uncle Udder Vulcan Vocal Whale Woman Xmas Xenon Yunnan Young Zloty Zodiac. Angel angel adept for the nuance loads of the arena cocoa and quaalude. Blind blind bodice for the submit oboe of the club snob and abbot. Clique clique coast for the pouch loco of the franc assoc and accede. Dunce dunce docile for the loudness mastodon of the loud statehood and huddle. Enact enact eosin for the quench coed of the pique canoe and bleep. Furlong furlong focal for the genuflect profound of the motif aloof and offers. Gnome gnome gondola for the impugn logos of the unplug analog and smuggle. Human human hoist for the buddhist alcohol of the riyadh caliph and bathhouse. Inlet inlet iodine for the quince champion of the ennui scampi and shiite. Justin justin jocose for the djibouti sojourn of the oranj raj and hajjis. Knoll knoll koala for the banknote lookout of the dybbuk outlook and trekked. Linden linden loads for the ulna monolog of the consul menthol and shallot. Milliner milliner modal for the alumna solomon of the album custom and summon. Number number nodule for the unmade economic of the shotgun bison and tunnel. Onset onset oddball for the abandon podium of the antiquo tempo and moonlit. Pneumo pneumo poncho for the dauphin opossum of the holdup bishop and supplies. Quanta quanta qophs for the inquest sheqel of the cinq coq and suqqu. Rhone rhone roman for the burnt porous of the lemur clamor and carrot. Snout snout sodium for the ensnare bosom of the genus pathos and missing. Tundra tundra tocsin for the nutmeg isotope of the peasant ingot and ottoman. Uncle uncle udder for the dunes cloud of the hindu thou and continuum. Vulcan vulcan vocal for the alluvial ovoid of the yugoslav chekhov and revved. Whale whale woman for the meanwhile blowout of the forepaw meadow and glowworm. Xmas xmas xenon for the bauxite doxology of the tableaux equinox and exxon. Yunnan yunnan young for the dynamo coyote of the obloquy employ and sayyid. Zloty zloty zodiac for the gizmo ozone of the franz laissez and buzzing.", (x_cord["4"], -(y_cord["2"]), x_cord["8"], margin_top_bottom), align="left")
            
            # Type specs
            meta_style()
            translate(0, y_cord["0"])
            text("12pt", (edge_left, (y_cord["48"])))
            text("12pt", (x_cord["4"], (y_cord["48"])))

        if font_size == font_size_XXS:
            type_style()
            
            # Column 1
            fontSize(12)
            line_height = 10 * 1.3
            translate(0, -fontCapHeight())
            textBox("HHAHOHOAOO	HAH\nHHBHOHOBOO	HBH\nHHCHOHOCOO	HCH\nHHDHOHODOO	HDH\nHHEHOHOEOO	HEH\nHHFHOHOFOO	HFH\nHHGHOHOGOO	HGH\nHHHHOHOHOO	HHH\nHHIHOHOIOO	HIH\nHHJHOHOJOO	HJH\nHHKHOHOKOO	HKH\nHHLHOHOLOO	HLH\nHHMHOHOMO	HMH\nHHNHOHONO	HNH\nHHOHOHOOOO	HOH\nHHPHOHOPOO	HPH\nHHQHOHOQOO	HQH\nHHRHOHOROO	HRH\nHHSHOHOSOO	HSH\nHHTHOHOTOO	HTH\nHHUHOHOUOO	HUH\nHHVHOHOVOO	HVH\nHHWHOHOWOO	HWH\nHHXHOHOXOO	HXH\nHHYHOHOYOO	HYH\nHHZHOHOZOO	HZH\n\nHH&HOHO&OO	H&H\nHH?HOHO?OO	H?H\nHH!HOHO!OO	H!H", (edge_left, -(y_cord["2"]), x_cord["3"], margin_top_bottom), align="left")
            
            # Column 2
            fontSize(12)
            line_height = 12 * 1.3
            translate(0, -fontCapHeight())
            baselineShift(3.75)
            textBox("ABIDE ACORN OF THE HABIT DACRON FOR THE BUDDHA GOUDA QUAALUDE. BENCH BOGUS OF THE SCRIBE ROBOT FOR THE APLOMB JACOB RIBBON. CENSUS CORAL OF THE SPICED JOCOSE FOR THE BASIC HAVOC SOCCER. DEMURE DOCILE OF THE TIDBIT LODGER FOR THE CUSPID PERIOD BIDDER. EBBING ECHOING OF THE BUSHED DECAL FOR THE APACHE ANODE NEEDS. FEEDER FOCUS OF THE LIFER BEDFORD FOR THE SERIF PROOF BUFFER. GENDER GOSPEL OF THE PIGEON DOGCART FOR THE SPRIG QUAHOG DIGGER. HERALD HONORS OF THE DIHEDRAL MADHOUSE FOR THE PENH RIYADH BATHHOUSE. IBSEN ICEMAN OF THE APHID NORDIC FOR THE SUSHI SAUDI SHIITE. JENNIES JOGGER OF THE TIJERA ADJOURN FOR THE ORANJ KOWBOJ HAJJIS. KEEPER KOSHER OF THE SHRIKE BOOKCASE FOR THE SHEIK LOGBOOK CHUKKAS. LENDER LOCKER OF THE CHILD GIGOLO FOR THE UNCOIL GAMBOL ENROLLED. MENACE MCCOY OF THE NIMBLE TOMCAT FOR THE DENIM RANDOM SUMMON. NEBULA NOSHED OF THE INBRED BRONCO FOR THE COUSIN CARBON KENNEL. OBSESS OCEAN OF THE PHOBIC DOCKSIDE FOR THE GAUCHO LIBIDO HOODED. PENNIES PODIUM OF THE SNIPER OPCODE FOR THE SCRIP BISHOP HOPPER. QUANTA QOPHS OF THE INQUEST OQOS FOR THE CINQ COQ SUQQU. REDUCE ROGUE OF THE GIRDLE ORCHID FOR THE MEMOIR SENSOR SORREL. SENIOR SCONCE OF THE DISBAR GODSON FOR THE HUBRIS AMENDS LESSEN. TENDON TORQUE OF THE UNITED SCOTCH FOR THE NOUGHT FORGOT BITTERS. UNDER UGLINESS OF THE RHUBARB SEDUCE FOR THE MANCHU HINDU CONTINUUM. VERSED VOUCH OF THE DIVER OVOID FOR THE TELAVIV KARPOV FLIVVER. WENCH WORKER OF THE UNWED SNOWCAP FOR THE ANDREW ESCROW GLOWWORM. XENON XOCHITL OF THE MIXED BOXCAR FOR THE SUFFIX ICEBOX EXXON. YEOMAN YONDER OF THE HYBRID ARROYO FOR THE DINGHY BRANDY SAYYID. ZEBRA ZOMBIE OF THE PRIZED OZONE FOR THE FRANZ ARROZ BUZZING.", (x_cord["4"], -(y_cord["2"]), x_cord["8"], margin_top_bottom), align="left")
            
            # Type specs
            meta_style()
            translate(0, y_cord["0"])
            text("12pt", (edge_left, (y_cord["48"])))
            text("12pt", (x_cord["4"], (y_cord["48"])))

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
                
            # Waterfall type loops
            elif eachString[1] == waterfall_L:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == waterfall_M:
                font_size = eachString[1]
                drawNewPage()
            elif eachString[1] == waterfall_S:
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