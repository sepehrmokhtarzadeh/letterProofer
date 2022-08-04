#
# -*- coding: UTF-8 -*- # ----------------------------------------------------------------------------- #
#
#     letterProofer | Text
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
proof_name = "Running Text"

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
font_size_L = 40
font_size_M = 24
font_size_S = 14
font_size_XS = 12
font_size_S_cap = 14
font_size_XS_cap = 12

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
    
    [ "one_column", font_size_L, "Large", "The Siniaka-Minia Faunal Reserve was established as an IUCN Category IV area in 1965 covering an area of 4,260 km (1,640 sq mi), due its importance for preserving black rhinoceros. Siniaka-Minia has been managed by the nonprofit conservation organization African Parks since 2017 in partnership with Chad’s government following the success of the African Parks partnership in Zakouma National Park. The reserve is large plain terrain with a backdrop of a massif which rises to a height of 1,613 metres (5,292 ft). It is drained by the Siniaka River and Dorioum River, which are ephemeral in nature; some water holes remain for use during the summer months. Vegetation in the southern part of the reserve is of Sudan savanna while in the north it consists of thorny bushes. The reserve, apart from preserving many threatened species, also contains greater kudu, red-fronted gazelle, oribi, roan antelope, lion and cheetah. Wild animals in the reserve are subject to degree of poaching by well armed hunters which has been difficult to control in view of lack adequate personnel and equipment to carry out effective surveillance operations. It would still need attention as there are sufficient number of mammal species which need to be conserved."],

    [ "one_column", font_size_M, "Medium", "Charles Bachman Moore Jr. (October 28, 1920 – March 2, 2010) was an American physicist, engineer and meteorologist, known for his research on atmospheric physics and his work with gas balloons. He was born in Maryville, Tennessee. Moore attended college at Georgia Institute of Technology in 1940. During World War II, he served as a weather equipment officer for the U.S. Army Air Corps in the China-Burma-India theater, and later in occupied China. Moore returned to Georgia Tech after the war, and received a bachelor’s degree in chemical engineering in 1947. Moore was recruited as a project engineer for Project Mogul in 1947 by New York University geophysicist Athelstan Spilhaus, who headed the Balloon Group within the project. Project Mogul, led by Dr. James Peoples and his assistant Albert P. Crary, made use of Moore’s work in materials science allowing the construction of balloons which could better withstand cold temperatures and safely rise to significantly greater altitudes. A balloon that Moore helped launch in New Mexico on June 4, 1947, was later identified as the source of the debris found on the Foster ranch which led to UFO conspiracy theories and claims surrounding the Roswell incident. In 1953, Moore joined the Arthur D. Little Corporation and worked with Bernard Vonnegut to develop techniques for vaporizing sodium, cesium, and calcium from rockets for high-altitude studies of winds and sodium in the upper atmosphere. They collaborated on over 50 publications related to atmospheric electricity. Moore worked at the General Mills Aeronautical Research Laboratory throughout the 1950s, participating in a number of projects sponsored by the Office of Naval Research aimed at developing both military and intelligence applications for balloons, including attempts to drop anti-Soviet leaflets from balloons and the use of balloons for surveillance purposes. Moore was also known for his 1959 expedition to the stratosphere with Malcolm Ross, in which they performed the first spectrographic analysis of the planet Venus which was free of interference from the Earth’s atmosphere, thereby proving the existence of water on that planet; this expedition involved an ascent to 89,000 feet (27 km, then a record for altitude). In 1969, Moore became the chairman of Langmuir Laboratory for Atmospheric Research and greatly expanded the lab’s facilities. Moore was a professor of atmospheric physics at the New Mexico Institute of Mining and Technology in Socorro for several years, and nominally retired in 1985; however, he continued his research afterward, and his subsequent discoveries led to the first improvement in the design of the lightning rod since that device’s invention by Benjamin Franklin. Moore has received a number of professional and academic honors." ],

    [ "two_column", font_size_S, "small", "proof text is elsewhere" ],

    [ "two_column", font_size_XS, "smaller", "proof text is elsewhere" ],

# Repeat for caps
    [ "one_column", font_size_L, "Large", "THE SINIAKA-MINIA FAUNAL RESERVE WAS ESTABLISHED AS AN IUCN CATEGORY IV AREA IN 1965 COVERING AN AREA OF 4,260 KM (1,640 SQ MI), DUE ITS IMPORTANCE FOR PRESERVING BLACK RHINOCEROS. SINIAKA-MINIA HAS BEEN MANAGED BY THE NONPROFIT CONSERVATION ORGANIZATION AFRICAN PARKS SINCE 2017 IN PARTNERSHIP WITH CHAD’S GOVERNMENT FOLLOWING THE SUCCESS OF THE AFRICAN PARKS PARTNERSHIP IN ZAKOUMA NATIONAL PARK. THE RESERVE IS LARGE PLAIN TERRAIN WITH A BACKDROP OF A MASSIF WHICH RISES TO A HEIGHT OF 1,613 METRES (5,292 FT). IT IS DRAINED BY THE SINIAKA RIVER AND DORIOUM RIVER, WHICH ARE EPHEMERAL IN NATURE; SOME WATER HOLES REMAIN FOR USE DURING THE SUMMER MONTHS. VEGETATION IN THE SOUTHERN PART OF THE RESERVE IS OF SUDAN SAVANNA WHILE IN THE NORTH IT CONSISTS OF THORNY BUSHES. THE RESERVE, APART FROM PRESERVING MANY THREATENED SPECIES, ALSO CONTAINS GREATER KUDU, RED-FRONTED GAZELLE, ORIBI, ROAN ANTELOPE, LION AND CHEETAH. WILD ANIMALS IN THE RESERVE ARE SUBJECT TO DEGREE OF POACHING BY WELL ARMED HUNTERS WHICH HAS BEEN DIFFICULT TO CONTROL IN VIEW OF LACK ADEQUATE PERSONNEL AND EQUIPMENT TO CARRY OUT EFFECTIVE SURVEILLANCE OPERATIONS. IT WOULD STILL NEED ATTENTION AS THERE ARE SUFFICIENT NUMBER OF MAMMAL SPECIES WHICH NEED TO BE CONSERVED."],

    [ "one_column", font_size_M, "Medium", "CHARLES BACHMAN MOORE JR. (OCTOBER 28, 1920 – MARCH 2, 2010) WAS AN AMERICAN PHYSICIST, ENGINEER AND METEOROLOGIST, KNOWN FOR HIS RESEARCH ON ATMOSPHERIC PHYSICS AND HIS WORK WITH GAS BALLOONS. HE WAS BORN IN MARYVILLE, TENNESSEE. MOORE ATTENDED COLLEGE AT GEORGIA INSTITUTE OF TECHNOLOGY IN 1940. DURING WORLD WAR II, HE SERVED AS A WEATHER EQUIPMENT OFFICER FOR THE U.S. ARMY AIR CORPS IN THE CHINA-BURMA-INDIA THEATER, AND LATER IN OCCUPIED CHINA. MOORE RETURNED TO GEORGIA TECH AFTER THE WAR, AND RECEIVED A BACHELOR’S DEGREE IN CHEMICAL ENGINEERING IN 1947. MOORE WAS RECRUITED AS A PROJECT ENGINEER FOR PROJECT MOGUL IN 1947 BY NEW YORK UNIVERSITY GEOPHYSICIST ATHELSTAN SPILHAUS, WHO HEADED THE BALLOON GROUP WITHIN THE PROJECT. PROJECT MOGUL, LED BY DR. JAMES PEOPLES AND HIS ASSISTANT ALBERT P. CRARY, MADE USE OF MOORE’S WORK IN MATERIALS SCIENCE ALLOWING THE CONSTRUCTION OF BALLOONS WHICH COULD BETTER WITHSTAND COLD TEMPERATURES AND SAFELY RISE TO SIGNIFICANTLY GREATER ALTITUDES. A BALLOON THAT MOORE HELPED LAUNCH IN NEW MEXICO ON JUNE 4, 1947, WAS LATER IDENTIFIED AS THE SOURCE OF THE DEBRIS FOUND ON THE FOSTER RANCH WHICH LED TO UFO CONSPIRACY THEORIES AND CLAIMS SURROUNDING THE ROSWELL INCIDENT. IN 1953, MOORE JOINED THE ARTHUR D. LITTLE CORPORATION AND WORKED WITH BERNARD VONNEGUT TO DEVELOP TECHNIQUES FOR VAPORIZING SODIUM, CESIUM, AND CALCIUM FROM ROCKETS FOR HIGH-ALTITUDE STUDIES OF WINDS AND SODIUM IN THE UPPER ATMOSPHERE. THEY COLLABORATED ON OVER 50 PUBLICATIONS RELATED TO ATMOSPHERIC ELECTRICITY. MOORE WORKED AT THE GENERAL MILLS AERONAUTICAL RESEARCH LABORATORY THROUGHOUT THE 1950S, PARTICIPATING IN A NUMBER OF PROJECTS SPONSORED BY THE OFFICE OF NAVAL RESEARCH AIMED AT DEVELOPING BOTH MILITARY AND INTELLIGENCE APPLICATIONS FOR BALLOONS, INCLUDING ATTEMPTS TO DROP ANTI-SOVIET LEAFLETS FROM BALLOONS AND THE USE OF BALLOONS FOR SURVEILLANCE PURPOSES. MOORE WAS ALSO KNOWN FOR HIS 1959 EXPEDITION TO THE STRATOSPHERE WITH MALCOLM ROSS, IN WHICH THEY PERFORMED THE FIRST SPECTROGRAPHIC ANALYSIS OF THE PLANET VENUS WHICH WAS FREE OF INTERFERENCE FROM THE EARTH’S ATMOSPHERE, THEREBY PROVING THE EXISTENCE OF WATER ON THAT PLANET; THIS EXPEDITION INVOLVED AN ASCENT TO 89,000 FEET (27 KM, THEN A RECORD FOR ALTITUDE). IN 1969, MOORE BECAME THE CHAIRMAN OF LANGMUIR LABORATORY FOR ATMOSPHERIC RESEARCH AND GREATLY EXPANDED THE LAB’S FACILITIES. MOORE WAS A PROFESSOR OF ATMOSPHERIC PHYSICS AT THE NEW MEXICO INSTITUTE OF MINING AND TECHNOLOGY IN SOCORRO FOR SEVERAL YEARS, AND NOMINALLY RETIRED IN 1985; HOWEVER, HE CONTINUED HIS RESEARCH AFTERWARD, AND HIS SUBSEQUENT DISCOVERIES LED TO THE FIRST IMPROVEMENT IN THE DESIGN OF THE LIGHTNING ROD SINCE THAT DEVICE’S INVENTION BY BENJAMIN FRANKLIN. MOORE HAS RECEIVED A NUMBER OF PROFESSIONAL AND ACADEMIC HONORS." ],

    [ "two_column", font_size_S_cap, "small", "proof text is elsewhere" ],

    [ "two_column", font_size_XS_cap, "smaller", "proof text is elsewhere" ],


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
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="left")
            
        elif font_size == font_size_L:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.1
            lineHeight(line_height)
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            baselineShift(-(y_cord["1"]-20))
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="left")
            
        elif font_size == font_size_M:
            type_style()
            fontSize(font_size)
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="left")
            
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
            fontSize(font_size)
            line_height = 16
            lineHeight(line_height)
            translate(0, -fontCapHeight())
            textBox("Hillhead (Scots: Hullheid, Scottish Gaelic: Ceann a’ Chnuic) is an area of Glasgow, Scotland. Situated north of Kelvingrove Park and to the south of the River Kelvin, Hillhead is at the heart of Glasgow’s fashionable West End, with Byres Road forming the western border of the area, the other boundaries being Dumbarton Road to the south and the River Kelvin to the east and north. Hillhead was an independent police burgh from 1869, but as Glasgow grew during the nineteenth century it was first swallowed up physically by the growing city, and then administratively in 1891. Byres Road is a commercially important district to the city of Glasgow, featuring many of the city’s most fashionable and popular independent boutiques. The University of Glasgow is located in the area, having moved from its original site on the High Street to its current Gilmorehill location in 1870. Consequently a great number of students live in the area. Many academics from the University live in the area along with BBC Scotland employees, actors, broadcasters, writers", (((x_cord["1"])-20), (y_cord["5"]), (x_cord["5"]+30), (y_cord["40"])), align="left")
            
            # Column 2
            fontSize(font_size)
            line_height = 16
            lineHeight(line_height)
            textBox("and many students from various universities and teaching hospitals, creating an economically and culturally diverse community. Other features of Hillhead include Ashton Lane, Western Baths, Hillhead High School, Glasgow Academy (a private school), and the Kelvinbridge, which straddles the River Kelvin which used to form an eastern boundary between Hillhead and Glasgow, until Hillhead’s incorporation into the city. The area is served by Hillhead subway station and Kelvinbridge subway station on the Glasgow Subway system. The two stops on either side of those are Kelvinhall in Partick, and St George’s Cross in Woodlands. The neoclassical colonnaded Wellington Church is located on University Avenue, directly opposite the University. The church is a Category A listed building. The archives about Hillhead are maintained by the Archives of the University of Glasgow (GUAS).\n\nJill Schlabach (born 1965 or 1966) is an American diver. She competed in the NCAA Championship and ", ((x_cord["7"]-20), (y_cord["5"]), ((x_cord["5"])+30), (y_cord["40"])), align="left")
            
            # Type specs
            meta_style()
            translate(0, y_cord["0"])
            text(str(font_size), (edge_left, (y_cord["45"])-8))
            
        elif font_size == font_size_XS:
            type_style()
            
            # Column 1
            fontSize(font_size)
            line_height = 16
            lineHeight(line_height)
            translate(0, -fontCapHeight())
            textBox("The Street family is an Australian dynasty, founded by the 19th-century banker and politician John Street and his wife Susanna, the daughter of Australian explorer and politician William Lawson. Their son Sir Philip Street, grandson Sir Kenneth Street, and great-grandson Sir Laurence Street each served as Chief Justice of the Supreme Court of New South Wales and Lieutenant-Governor of New South Wales. Geoffrey Street served as Minister of Defence in the Second World War, his son Anthony “Tony” Street served as Minister of Foreign Affairs, and Jessie, Lady Street was Australia’s first female delegate to the United Nations. Sir Laurence’s son Alexander “Sandy” Street, daughter Sylvia Emmett (née Street) and son-in-law Arthur Emmett serve as federal judges. John Rendell Street, MLC (1832–1891) was an Australian banker and politician, born to Maria Wood and John Street, JP. His father descended from Baron Sir Thomas Street, an English Chief Justice who presided on the last King’s Bench before the Glorious Revolution of 1688. Both parents were English immigrants to Australia via the 1822 passenger ship Thalia. In 1886, John founded the Perpetual Trustee Company as managing director with fellow trustees Edmund Barton and James Fairfax. He succeeded Edmund Barton, Australia’s 1st Prime Minister, in his New South Wales Legislative Assembly seat of East Sydney. John married Susanna Lawson, the daughter of Australian politician William Lawson, MLC, who along with William Wentworth and Gregory Blaxland pioneered the first settler crossing of the Blue Mountains in 1813. John and Susanna had seven children, including the future Sir Philip and Ernest, who married Emma Browne, the daughter of Australian author Thomas Browne. John was a director of the Colonial Mutual Life Assurance Company (now Commonwealth Bank). His sister Sarah married Thomas Smith, MLC, managing director of the Commercial Banking Company of Sydney (now NAB) and the nephew of CBCS chairman Henry Smith, MLC. Three other Street ancestors via the wives of Sir Kenneth and Sir Laurence were John’s", (((x_cord["1"])-20), (y_cord["5"]), (x_cord["5"]+30), (y_cord["40"])), align="left")
            
            # Column 2
            fontSize(font_size)
            line_height = 16
            lineHeight(line_height)
            textBox("contemporaries, namely John Watt, MLC, a director of the Union Bank of Australia (now ANZ), his father-in-law George Holden, MLC, a trustee of the Bank of New South Wales (now Westpac), and Edward Ogilvie, MLC. Sir Philip Whistler Street, KCMG, KC (1863–1938) was the 8th Chief Justice of the Supreme Court of New South Wales and Lieutenant-Governor of New South Wales. On 11 February 1907, he was made a full judge of the Supreme Court of New South Wales. Sir Philip was made Chief Justice of the Supreme Court on 28 January 1925 and held that office until his 70th birthday in 1933. He was appointed Lieutenant-Governor of New South Wales in 1930, and administered the state in the absence of the Governor of New South Wales from May to October 1934, January to February 1935, and January to August 1936. He died in 1938 and was buried with a state funeral at St Andrew’s Cathedral. He is the second longest-serving judge in New South Wales history. His second son was Laurence, and his eldest was the future Sir Kenneth. Lieutenant Laurence Whistler Street (1894–1915) was 21 years of age when he was killed in action in May 1915 during the Gallipoli campaign. A former student of Sydney Law School, he enlisted in the Australian Army in August 1914, among the first of his generation, and was made an officer of the 3rd Battalion of the 1st Infantry Brigade. Lieutenant Colonel Sir Kenneth Whistler Street, KCMG, KStJ, QC (1890–1972) was the 10th Chief Justice of the Supreme Court of New South Wales and Lieutenant-Governor of New South Wales. He was elevated as a judge of the Supreme Court on 7 October 1931, thus joining the bench of which his father was then Chief Justice. According to Percival Serle, this is the only known case in Australian history of a father and a son sitting together as judges on the same bench. Sir Kenneth was sworn in as Chief Justice of the Supreme Court of New South Wales on 7 February 1950. He was Lieutenant-Governor of New South Wales from 1950 to 1972. Prior to his career as a judge, he served in the First World War, having been commissioned on 29 September 1914 in the Duke of Cornwall’s Light", ((x_cord["7"]-20), (y_cord["5"]), ((x_cord["5"])+30), (y_cord["40"])), align="left")
            
            # Type specs
            meta_style()
            translate(0, y_cord["0"])
            text(str(font_size), (edge_left, (y_cord["45"]-8)))

        elif font_size == font_size_S_cap:
            type_style()
            
            # Column 1
            fontSize(font_size)
            line_height = 16
            lineHeight(line_height)
            translate(0, -fontCapHeight())
            textBox("HILLHEAD (SCOTS: HULLHEID, SCOTTISH GAELIC: CEANN A’ CHNUIC) IS AN AREA OF GLASGOW, SCOTLAND. SITUATED NORTH OF KELVINGROVE PARK AND TO THE SOUTH OF THE RIVER KELVIN, HILLHEAD IS AT THE HEART OF GLASGOW’S FASHIONABLE WEST END, WITH BYRES ROAD FORMING THE WESTERN BORDER OF THE AREA, THE OTHER BOUNDARIES BEING DUMBARTON ROAD TO THE SOUTH AND THE RIVER KELVIN TO THE EAST AND NORTH. HILLHEAD WAS AN INDEPENDENT POLICE BURGH FROM 1869, BUT AS GLASGOW GREW DURING THE NINETEENTH CENTURY IT WAS FIRST SWALLOWED UP PHYSICALLY BY THE GROWING CITY, AND THEN ADMINISTRATIVELY IN 1891. BYRES ROAD IS A COMMERCIALLY IMPORTANT DISTRICT TO THE CITY OF GLASGOW, FEATURING MANY OF THE CITY’S MOST FASHIONABLE AND POPULAR INDEPENDENT BOUTIQUES. THE UNIVERSITY OF GLASGOW IS LOCATED IN THE AREA, HAVING MOVED FROM ITS ORIGINAL SITE ON THE HIGH STREET TO ITS CURRENT GILMOREHILL LOCATION IN 1870. CONSEQUENTLY A GREAT NUMBER OF STUDENTS LIVE IN THE AREA. MANY ACADEMICS FROM THE UNIVERSITY LIVE IN THE AREA ALONG WITH BBC SCOTLAND EMPLOYEES, ACTORS, BROADCASTERS, WRITERS", (((x_cord["1"])-20), (y_cord["5"]), (x_cord["5"]+30), (y_cord["40"])), align="left")
            
            # Column 2
            fontSize(font_size)
            line_height = 16
            lineHeight(line_height)
            textBox("AND MANY STUDENTS FROM VARIOUS UNIVERSITIES AND TEACHING HOSPITALS, CREATING AN ECONOMICALLY AND CULTURALLY DIVERSE COMMUNITY. OTHER FEATURES OF HILLHEAD INCLUDE ASHTON LANE, WESTERN BATHS, HILLHEAD HIGH SCHOOL, GLASGOW ACADEMY (A PRIVATE SCHOOL), AND THE KELVINBRIDGE, WHICH STRADDLES THE RIVER KELVIN WHICH USED TO FORM AN EASTERN BOUNDARY BETWEEN HILLHEAD AND GLASGOW, UNTIL HILLHEAD’S INCORPORATION INTO THE CITY. THE AREA IS SERVED BY HILLHEAD SUBWAY STATION AND KELVINBRIDGE SUBWAY STATION ON THE GLASGOW SUBWAY SYSTEM. THE TWO STOPS ON EITHER SIDE OF THOSE ARE KELVINHALL IN PARTICK, AND ST GEORGE’S CROSS IN WOODLANDS. THE NEOCLASSICAL COLONNADED WELLINGTON CHURCH IS LOCATED ON UNIVERSITY AVENUE, DIRECTLY OPPOSITE THE UNIVERSITY. THE CHURCH IS A CATEGORY A LISTED BUILDING. THE ARCHIVES ABOUT HILLHEAD ARE MAINTAINED BY THE ARCHIVES OF THE UNIVERSITY OF GLASGOW (GUAS).\n\nJILL SCHLABACH (BORN 1965 OR 1966) IS AN AMERICAN DIVER. SHE COMPETED IN THE NCAA CHAMPIONSHIP AND", ((x_cord["7"]-20), (y_cord["5"]), ((x_cord["5"])+30), (y_cord["40"])), align="left")
            
            # Type specs
            meta_style()
            translate(0, y_cord["0"])
            text(str(font_size), (edge_left, (y_cord["45"])-8))
            
        elif font_size == font_size_XS_cap:
            type_style()
            
            # Column 1
            fontSize(font_size)
            line_height = 16
            lineHeight(line_height)
            translate(0, -fontCapHeight())
            textBox("THE STREET FAMILY IS AN AUSTRALIAN DYNASTY, FOUNDED BY THE 19TH-CENTURY BANKER AND POLITICIAN JOHN STREET AND HIS WIFE SUSANNA, THE DAUGHTER OF AUSTRALIAN EXPLORER AND POLITICIAN WILLIAM LAWSON. THEIR SON SIR PHILIP STREET, GRANDSON SIR KENNETH STREET, AND GREAT-GRANDSON SIR LAURENCE STREET EACH SERVED AS CHIEF JUSTICE OF THE SUPREME COURT OF NEW SOUTH WALES AND LIEUTENANT-GOVERNOR OF NEW SOUTH WALES. GEOFFREY STREET SERVED AS MINISTER OF DEFENCE IN THE SECOND WORLD WAR, HIS SON ANTHONY “TONY” STREET SERVED AS MINISTER OF FOREIGN AFFAIRS, AND JESSIE, LADY STREET WAS AUSTRALIA’S FIRST FEMALE DELEGATE TO THE UNITED NATIONS. SIR LAURENCE’S SON ALEXANDER “SANDY” STREET, DAUGHTER SYLVIA EMMETT (NÉE STREET) AND SON-IN-LAW ARTHUR EMMETT SERVE AS FEDERAL JUDGES. JOHN RENDELL STREET, MLC (1832–1891) WAS AN AUSTRALIAN BANKER AND POLITICIAN, BORN TO MARIA WOOD AND JOHN STREET, JP. HIS FATHER DESCENDED FROM BARON SIR THOMAS STREET, AN ENGLISH CHIEF JUSTICE WHO PRESIDED ON THE LAST KING’S BENCH BEFORE THE GLORIOUS REVOLUTION OF 1688. BOTH PARENTS WERE ENGLISH IMMIGRANTS TO AUSTRALIA VIA THE 1822 PASSENGER SHIP THALIA. IN 1886, JOHN FOUNDED THE PERPETUAL TRUSTEE COMPANY AS MANAGING DIRECTOR WITH FELLOW TRUSTEES EDMUND BARTON AND JAMES FAIRFAX. HE SUCCEEDED EDMUND BARTON, AUSTRALIA’S 1ST PRIME MINISTER, IN HIS NEW SOUTH WALES LEGISLATIVE ASSEMBLY SEAT OF EAST SYDNEY. JOHN MARRIED SUSANNA LAWSON, THE DAUGHTER OF AUSTRALIAN POLITICIAN WILLIAM LAWSON, MLC, WHO ALONG WITH WILLIAM WENTWORTH AND GREGORY BLAXLAND PIONEERED THE FIRST SETTLER CROSSING OF THE BLUE MOUNTAINS IN 1813. JOHN AND SUSANNA HAD SEVEN CHILDREN, INCLUDING THE FUTURE SIR PHILIP AND ERNEST, WHO MARRIED EMMA BROWNE, THE DAUGHTER OF AUSTRALIAN AUTHOR THOMAS BROWNE. JOHN WAS A DIRECTOR OF THE COLONIAL MUTUAL LIFE ASSURANCE COMPANY (NOW COMMONWEALTH BANK). HIS SISTER SARAH MARRIED THOMAS SMITH, MLC, MANAGING DIRECTOR OF THE COMMERCIAL BANKING COMPANY OF SYDNEY (NOW NAB) AND THE NEPHEW OF CBCS CHAIRMAN HENRY SMITH, MLC. THREE OTHER STREET ANCESTORS VIA THE WIVES OF SIR KENNETH AND SIR LAURENCE WERE JOHN’S", (((x_cord["1"])-20), (y_cord["5"]), (x_cord["5"]+30), (y_cord["40"])), align="left")
            
            # Column 2
            fontSize(font_size)
            line_height = 16
            lineHeight(line_height)
            textBox("CONTEMPORARIES, NAMELY JOHN WATT, MLC, A DIRECTOR OF THE UNION BANK OF AUSTRALIA (NOW ANZ), HIS FATHER-IN-LAW GEORGE HOLDEN, MLC, A TRUSTEE OF THE BANK OF NEW SOUTH WALES (NOW WESTPAC), AND EDWARD OGILVIE, MLC. SIR PHILIP WHISTLER STREET, KCMG, KC (1863–1938) WAS THE 8TH CHIEF JUSTICE OF THE SUPREME COURT OF NEW SOUTH WALES AND LIEUTENANT-GOVERNOR OF NEW SOUTH WALES. ON 11 FEBRUARY 1907, HE WAS MADE A FULL JUDGE OF THE SUPREME COURT OF NEW SOUTH WALES. SIR PHILIP WAS MADE CHIEF JUSTICE OF THE SUPREME COURT ON 28 JANUARY 1925 AND HELD THAT OFFICE UNTIL HIS 70TH BIRTHDAY IN 1933. HE WAS APPOINTED LIEUTENANT-GOVERNOR OF NEW SOUTH WALES IN 1930, AND ADMINISTERED THE STATE IN THE ABSENCE OF THE GOVERNOR OF NEW SOUTH WALES FROM MAY TO OCTOBER 1934, JANUARY TO FEBRUARY 1935, AND JANUARY TO AUGUST 1936. HE DIED IN 1938 AND WAS BURIED WITH A STATE FUNERAL AT ST ANDREW’S CATHEDRAL. HE IS THE SECOND LONGEST-SERVING JUDGE IN NEW SOUTH WALES HISTORY. HIS SECOND SON WAS LAURENCE, AND HIS ELDEST WAS THE FUTURE SIR KENNETH. LIEUTENANT LAURENCE WHISTLER STREET (1894–1915) WAS 21 YEARS OF AGE WHEN HE WAS KILLED IN ACTION IN MAY 1915 DURING THE GALLIPOLI CAMPAIGN. A FORMER STUDENT OF SYDNEY LAW SCHOOL, HE ENLISTED IN THE AUSTRALIAN ARMY IN AUGUST 1914, AMONG THE FIRST OF HIS GENERATION, AND WAS MADE AN OFFICER OF THE 3RD BATTALION OF THE 1ST INFANTRY BRIGADE. LIEUTENANT COLONEL SIR KENNETH WHISTLER STREET, KCMG, KSTJ, QC (1890–1972) WAS THE 10TH CHIEF JUSTICE OF THE SUPREME COURT OF NEW SOUTH WALES AND LIEUTENANT-GOVERNOR OF NEW SOUTH WALES. HE WAS ELEVATED AS A JUDGE OF THE SUPREME COURT ON 7 OCTOBER 1931, THUS JOINING THE BENCH OF WHICH HIS FATHER WAS THEN CHIEF JUSTICE. ACCORDING TO PERCIVAL SERLE, THIS IS THE ONLY KNOWN CASE IN AUSTRALIAN HISTORY OF A FATHER AND A SON SITTING TOGETHER AS JUDGES ON THE SAME BENCH. SIR KENNETH WAS SWORN IN AS CHIEF JUSTICE OF THE SUPREME COURT OF NEW SOUTH WALES ON 7 FEBRUARY 1950. HE WAS LIEUTENANT-GOVERNOR OF NEW SOUTH WALES FROM 1950 TO 1972. PRIOR TO HIS CAREER AS A JUDGE, HE SERVED IN THE FIRST WORLD WAR, HAVING BEEN COMMISSIONED ON 29 SEPTEMBER 1914 IN THE DUKE OF CORNWALL’S LIGHT", ((x_cord["7"]-20), (y_cord["5"]), ((x_cord["5"])+30), (y_cord["40"])), align="left")
            
            # Type specs
            meta_style()
            translate(0, y_cord["0"])
            text(str(font_size), (edge_left, (y_cord["45"]-8)))


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
 

    