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

    [ "one_column", font_size_L, "Large", "The Siniaka-Minia Faunal Reserve was established as an IUCN Category IV area in 1965 covering an area of 4,260 km (1,640 sq mi), due its importance for preserving black rhinoceros. Siniaka-Minia has been managed by the nonprofit conservation organization African Parks since 2017 in partnership with Chad’s government following the success of the African Parks partnership in Zakouma National Park. The reserve is large plain terrain with a backdrop of a massif which rises to a height of 1,613 metres (5,292 ft). It is drained by the Siniaka River and Dorioum River, which are ephemeral in nature; some water holes remain for use during the summer months. Vegetation in the southern part of the reserve is of Sudan savanna while in the north it consists of thorny bushes. The reserve, apart from preserving many threatened species, also contains greater kudu, red-fronted gazelle, oribi, roan antelope, lion and cheetah. Wild animals in the reserve are subject to degree of poaching by well armed hunters which has been difficult to control in view of lack adequate personnel and equipment to carry out effective surveillance operations. It would still need attention as there are sufficient number of mammal species which need to be conserved."],

    [ "one_column", font_size_M, "Medium", "Charles Bachman Moore Jr. (October 28, 1920 – March 2, 2010) was an American physicist, engineer and meteorologist, known for his research on atmospheric physics and his work with gas balloons. He was born in Maryville, Tennessee. Moore attended college at Georgia Institute of Technology in 1940. During World War II, he served as a weather equipment officer for the U.S. Army Air Corps in the China-Burma-India theater, and later in occupied China. Moore returned to Georgia Tech after the war, and received a bachelor’s degree in chemical engineering in 1947. Moore was recruited as a project engineer for Project Mogul in 1947 by New York University geophysicist Athelstan Spilhaus, who headed the Balloon Group within the project. Project Mogul, led by Dr. James Peoples and his assistant Albert P. Crary, made use of Moore’s work in materials science allowing the construction of balloons which could better withstand cold temperatures and safely rise to significantly greater altitudes. A balloon that Moore helped launch in New Mexico on June 4, 1947, was later identified as the source of the debris found on the Foster ranch which led to UFO conspiracy theories and claims surrounding the Roswell incident. In 1953, Moore joined the Arthur D. Little Corporation and worked with Bernard Vonnegut to develop techniques for vaporizing sodium, cesium, and calcium from rockets for high-altitude studies of winds and sodium in the upper atmosphere. They collaborated on over 50 publications related to atmospheric electricity. Moore worked at the General Mills Aeronautical Research Laboratory throughout the 1950s, participating in a number of projects sponsored by the Office of Naval Research aimed at developing both military and intelligence applications for balloons, including attempts to drop anti-Soviet leaflets from balloons and the use of balloons for surveillance purposes. Moore was also known for his 1959 expedition to the stratosphere with Malcolm Ross, in which they performed the first spectrographic analysis of the planet Venus which was free of interference from the Earth’s atmosphere, thereby proving the existence of water on that planet; this expedition involved an ascent to 89,000 feet (27 km, then a record for altitude). In 1969, Moore became the chairman of Langmuir Laboratory for Atmospheric Research and greatly expanded the lab’s facilities. Moore was a professor of atmospheric physics at the New Mexico Institute of Mining and Technology in Socorro for several years, and nominally retired in 1985; however, he continued his research afterward, and his subsequent discoveries led to the first improvement in the design of the lightning rod since that device’s invention by Benjamin Franklin. Moore has received a number of professional and academic honors." ],

    [ "two column", font_size_S, "small", "Hillhead (Scots: Hullheid, Scottish Gaelic: Ceann a’ Chnuic) is an area of Glasgow, Scotland. Situated north of Kelvingrove Park and to the south of the River Kelvin, Hillhead is at the heart of Glasgow’s fashionable West End, with Byres Road forming the western border of the area, the other boundaries being Dumbarton Road to the south and the River Kelvin to the east and north. Hillhead was an independent police burgh from 1869, but as Glasgow grew during the nineteenth century it was first swallowed up physically by the growing city, and then administratively in 1891. Byres Road is a commercially important district to the city of Glasgow, featuring many of the city’s most fashionable and popular independent boutiques. The University of Glasgow is located in the area, having moved from its original site on the High Street to its current Gilmorehill location in 1870. Consequently a great number of students live in the area. Many academics from the University live in the area along with BBC Scotland employees, actors, broadcasters, writers and many students from various universities and teaching hospitals, creating an economically and culturally diverse community. Other features of Hillhead include Ashton Lane, Western Baths, Hillhead High School, Glasgow Academy (a private school), and the Kelvinbridge, which straddles the River Kelvin which used to form an eastern boundary between Hillhead and Glasgow, until Hillhead’s incorporation into the city. The area is served by Hillhead subway station and Kelvinbridge subway station on the Glasgow Subway system. The two stops on either side of those are Kelvinhall in Partick, and St George’s Cross in Woodlands. The neoclassical colonnaded Wellington Church is located on University Avenue, directly opposite the University. The church is a Category A listed building. The archives about Hillhead are maintained by the Archives of the University of Glasgow (GUAS). Jill Schlabach (born 1965 or 1966) is an American diver. She competed in the NCAA Championship and the 1991 Pan American Games. Schlabach hoped to participate in the 1992 Olympics. Schlabach did tumbling in elementary school and did not surviving until she entered high school. She said that she landed right on her face the first time she went off a board. After graduating from Fairfield High School, Schlabach attended the University of Cincinnati as a nursing major. Schlabach was one of the top divers in the Cincinnati Bearcats swimming and diving team. She earned a full athletic scholarship after she won 8th place in the NCAA Championships, where she earned an All-America title in 1986. She was named female diver of the year in 1986 by the Metro Conference and during the same year, she was a finalist in the 1 meter board competition at the U.S. Diving Championships. Schlabach moved to Michigan in December 1989 after meeting University of Michigan coach Dick Kimball at an Olympic Festival. Kimball asked her to join his team and Schlabach found a job at the Michigan Medical Center. Once she improved her diving, she began to work less hours. During days that she worked, Schlabach trained from 4:10 to 6:00 PM, arrive at work by 7:00 PM, stay there till 7:30 AM, and then travel back to the pool to train until 9:30. Schlabach later competed at the FINA Diving World Cup in Canada. Schlabach was a surgical intensive-care nurse at Michigan Medicine at the time she competed in the 1991 Pan American Games. In order to have the time-off to compete, Schlabach worked four days of 12-hour shifts in a row. At the 1991 Pan American Games, Shlabach won the 1 meter springboard and Alison Malsch received second place. Schlabach scored 256.5 points and Maisch received 250.68 points, with Schlabach’s best individual score being 55.08 points. She stated that she hoped to compete in the 3 meter and 10 meter events at the 1992 Olympics." ],

    [ "two_column", font_size_S, "smaller", "The Street family is an Australian dynasty, founded by the 19th-century banker and politician John Street and his wife Susanna, the daughter of Australian explorer and politician William Lawson. Their son Sir Philip Street, grandson Sir Kenneth Street, and great-grandson Sir Laurence Street each served as Chief Justice of the Supreme Court of New South Wales and Lieutenant-Governor of New South Wales. Geoffrey Street served as Minister of Defence in the Second World War, his son Anthony “Tony” Street served as Minister of Foreign Affairs, and Jessie, Lady Street was Australia’s first female delegate to the United Nations. Sir Laurence’s son Alexander “Sandy” Street, daughter Sylvia Emmett (née Street) and son-in-law Arthur Emmett serve as federal judges. John Rendell Street, MLC (1832–1891) was an Australian banker and politician, born to Maria Wood and John Street, JP. His father descended from Baron Sir Thomas Street, an English Chief Justice who presided on the last King’s Bench before the Glorious Revolution of 1688. Both parents were English immigrants to Australia via the 1822 passenger ship Thalia. In 1886, John founded the Perpetual Trustee Company as managing director with fellow trustees Edmund Barton and James Fairfax. He succeeded Edmund Barton, Australia’s 1st Prime Minister, in his New South Wales Legislative Assembly seat of East Sydney. John married Susanna Lawson, the daughter of Australian politician William Lawson, MLC, who along with William Wentworth and Gregory Blaxland pioneered the first settler crossing of the Blue Mountains in 1813. John and Susanna had seven children, including the future Sir Philip and Ernest, who married Emma Browne, the daughter of Australian author Thomas Browne. John was a director of the Colonial Mutual Life Assurance Company (now Commonwealth Bank). His sister Sarah married Thomas Smith, MLC, managing director of the Commercial Banking Company of Sydney (now NAB) and the nephew of CBCS chairman Henry Smith, MLC. Three other Street ancestors via the wives of Sir Kenneth and Sir Laurence were John’s contemporaries, namely John Watt, MLC, a director of the Union Bank of Australia (now ANZ), his father-in-law George Holden, MLC, a trustee of the Bank of New South Wales (now Westpac), and Edward Ogilvie, MLC. Sir Philip Whistler Street, KCMG, KC (1863–1938) was the 8th Chief Justice of the Supreme Court of New South Wales and Lieutenant-Governor of New South Wales. On 11 February 1907, he was made a full judge of the Supreme Court of New South Wales. Sir Philip was made Chief Justice of the Supreme Court on 28 January 1925 and held that office until his 70th birthday in 1933. He was appointed Lieutenant-Governor of New South Wales in 1930, and administered the state in the absence of the Governor of New South Wales from May to October 1934, January to February 1935, and January to August 1936. He died in 1938 and was buried with a state funeral at St Andrew’s Cathedral. He is the second longest-serving judge in New South Wales history. His second son was Laurence, and his eldest was the future Sir Kenneth. Lieutenant Laurence Whistler Street (1894–1915) was 21 years of age when he was killed in action in May 1915 during the Gallipoli campaign. A former student of Sydney Law School, he enlisted in the Australian Army in August 1914, among the first of his generation, and was made an officer of the 3rd Battalion of the 1st Infantry Brigade. Lieutenant Colonel Sir Kenneth Whistler Street, KCMG, KStJ, QC (1890–1972) was the 10th Chief Justice of the Supreme Court of New South Wales and Lieutenant-Governor of New South Wales. He was elevated as a judge of the Supreme Court on 7 October 1931, thus joining the bench of which his father was then Chief Justice. According to Percival Serle, this is the only known case in Australian history of a father and a son sitting together as judges on the same bench. Sir Kenneth was sworn in as Chief Justice of the Supreme Court of New South Wales on 7 February 1950. He was Lieutenant-Governor of New South Wales from 1950 to 1972. Prior to his career as a judge, he served in the First World War, having been commissioned on 29 September 1914 in the Duke of Cornwall’s Light Infantry and sent to France. He ultimately rose to the rank of lieutenant colonel in the Citizens Military Force. Like his father before him, he was buried with a state funeral at St Andrew’s Cathedral, Sydney. Street House at Cranbrook School, Sydney is named in his honour. Sir Kenneth married Jessie Mary Grey Lillingston and named his son Laurence after his brother who died at Gallipoli. Jessie Mary Grey, Lady Street (née Lillingston; 1889–1970) was a leading suffragette. She was the daughter of Charles Alfred Gordon Lillingston, JP and Mabel Harriet Ogilvie, the daughter of Australian politician Edward David Stuart Ogilvie, MLC. Jessie campaigned extensively for peace and human rights. She was dubbed “Red Jessie” by her detractors in the right-wing media for her efforts to promote diplomacy with the USSR and ease tensions during the Cold War. She was a key figure in Australian and international political life for over 50 years, from the women’s suffrage struggle in England to the removal of Australia’s constitutional discrimination against Aboriginal people in 1967. Jessie was Australia’s only female delegate to the establishment of the United Nations conference in San Francisco in 1945, where she played a key role in ensuring that gender was included as a non-discrimination clause, in addition to race and religion, in the United Nations Charter. She is recognised both in Australia and internationally for her activism. The Jessie Street Centre, the Jessie Street Trust, the Jessie Street National Women’s Library and the Jessie Street Gardens exist in her honour. Brigadier Geoffrey Austin Street, MP, MC (1894–1940) was a cousin of Sir Kenneth’s who served as Australia’s Minister of Defence in the First Menzies Government during the Second World War. He was awarded a Military Cross for his courage in serving the Australian Imperial Force during the Gallipoli campaign, where he was wounded before returning to service in France during the First World War. At the request of his friend Robert Menzies, he stood for and won the seat of Corangamite in 1934. He was made Minister of Defence in November 1938 and played a major role in the expansion of the military and munitions prior to the outbreak of the Second World War and pushed the National Registration Act (1939) through parliament despite strong opposition, before dying in the 1940 Canberra air disaster. Commander Sir Laurence Whistler Street, AC, KCMG, KStJ, QC (1926–2018) was the 14th Chief Justice of the Supreme Court of New South Wales and Lieutenant-Governor of New South Wales. He was first made a judge of the Supreme Court of New South Wales in the Equity Division. He was appointed Chief Justice and Lieutenant-Governor in 1974; the youngest since 1844. He had joined the Royal Australian Navy at age 17 to serve in the Second World War and went on to become a commander of the Royal Australian Navy Reserve and an honorary colonel of the Australian Army Reserve. Sir Laurence pioneered the practice of mediation and became the chairman of Fairfax Media and a director of Monte dei Paschi di Siena. Sir Laurence’s sister Philippa “Pip” Street married the Australian Test cricketer and journalist John “Jack” Henry Webb Fingleton, OBE in 1942. He was buried with a state funeral at the Sydney Opera House Concert Hall in July 2018. In an elegy before 700, incumbent Australian Prime Minister Malcolm Turnbull spoke of his mentor: “As a barrister, he was as eloquent as he was erudite, as formidable as he was fashionable […] Laurence had movie star good looks coupled with a charisma, charm and intellect, a humility, a humanity that swept all before him […] His nickname, Lorenzo the Magnificent, was well earned.” Incumbent Chief Justice of Australia Tom Bathurst remembered Sir Laurence as “one of the outstanding jurists of the 20th century.” Susan Gai Watt, AM (born 1932) was the first wife of Sir Laurence Street and the first female chair of the Eastern Sydney Health Service (overseer of hospitals). She is the daughter of Ernest Alexander Stuart Watt (1874–1954), a shipping heir by whom she is the niece of Lieutenant Colonel Walter Oswald Watt, the granddaughter of John Brown Watt, and the great-granddaughter of George Kenyon Holden. Anthony Austin “Tony” Street, MP (born 1926), the son of Geoffrey Austin Street, also represented the seat of Corangamite, from 1966 to 1983. A naval veteran of the Second World War, he was Australia’s Foreign Minister in the Fourth Fraser Ministry, from 1980 until 1983. He had previously served in the Third Fraser Ministry as Minister for Employment and Industrial Relations and Minister for Industrial Relations. Prior to that, he had served in the Second Fraser Ministry as Minister for Employment and Industrial Relations. By his first wife, Susan Gai (née Watt), formerly Lady Street, Sir Laurence had four children: Kenneth, Sylvia, Alexander and Sarah. Kenneth Street is a businessman based in New South Wales. By his wife Sarah Street (née Kinross), he has three children. Judge Sylvia Jane Emmett, AM (née Street) is a judge of the Federal Circuit Court of Australia and a lieutenant commander of the Royal Australian Naval Reserve. She graduated from Sydney Law School (LLB) and is married to Justice Arthur Emmett, a federal judge and Challis Lecturer in Roman Law at Sydney Law School. Arthur became a judge of the New South Wales Court of Appeal in 2013 after 15 years as a judge of the Federal Circuit Court. Judge Alexander “Sandy” Whistler Street, SC is also a judge of the Federal Circuit Court of Australia and a commander of the Royal Australian Naval Reserve. He has four children by two wives. Sarah Whistler Farley (née Street) is a businesswoman and board member of the Prince of Wales Hospital Foundation and the Jessie Street Trust. She graduated from Sydney Law School (LLB) and has four children by her husband, financier Gerard Farley. Jessie Street is Sir Laurence’s only child by his second wife and widow Lady (Penelope; née Ferguson) Street. She holds a Juris Doctor degree from Sydney Law School and is the god-daughter of HRH Charles, Prince of Wales." ],

# Repeat for caps

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
 

    