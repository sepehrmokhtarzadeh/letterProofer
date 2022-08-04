#
# -*- coding: UTF-8 -*- # ----------------------------------------------------------------------------- #
#
#     letterProofer | Diacritics, Vietnamese
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
proof_name = "Diacritics, Vietnamese"

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

    [ "one_column", font_size_L, "Vietnamese Diacritics", "Áá Àà Ảả Ãã Ạạ Ăă Ắắ Ằằ Ẳẳ Ẵẵ Ặặ Ââ Ấấ Ầầ Ẩẩ Ẫẫ Ậậ Đđ Éé Èè Ẻẻ Ẽẽ Ẹẹ Êê Ếế Ềề Ểể Ễễ Ệệ Íí Ìì Ỉỉ Ĩĩ Ịị Óó Òò Ỏỏ Õõ Ọọ Ôô Ốố Ồồ Ổổ Ỗỗ Ộộ Ơơ Ớớ Ờờ Ởở Ỡỡ Ợợ Úú Ùù Ủủ Ũũ Ụụ Ưư Ứứ Ừừ Ửử Ữữ Ựự Ýý Ỳỳ Ỷỷ Ỹỹ Ỵỵ" ],

    [ "one_column", font_size_L, "Running text, large", "Chúng ta dùng typography hàng ngày mà không biết rằng đó là typography. Tương tự như những thiết kế nội thất hay thiết kế thời trang, typography cũng là sản phẩm của sự sáng tạo, hòa trộn cả hai mặt khoa học và nghệ thuật, với nguyên liệu là các chữ cái." ],

    [ "one_column", font_size_M, "Running text, medium", "Cha đẻ của typography là một người Đức, Johannes Gutenberg, sáng chế phương pháp in bằng cách sắp xếp những chữ cái rời lên bản in năm 1450. Sự phát triển của ngành công nghệ thông tin giúp công việc thiết kế, chỉnh sửa vị trí và sắp xếp các chữ cái trở nên “dễ như bỡn”. Với kỹ thuật đồ họa tân tiến ngày nay, các “typographer” được trang bị phương tiện để thỏa sức sáng tạo vô vàn kiểu chữ mới.\n\nBan đầu typography chỉ sử dụng cho mục đích truyền thông với các yêu cầu chung như trình bày dễ đọc, dễ hiểu, và phù hợp cho nhiều đối tượng. Nhưng typography ngày nay đã phát triển lên một cấp độ khác với vai trò mới: khơi dậy và kích hoạt những cảm xúc. Nhờ đó ta có thể thưởng thức typography như một tác phẩm nghệ thuật và sáng tạo để nó luôn mới mẻ.\n\nNhiều người từng cảnh báo typography là kỹ thuật “gây nghiện”, bởi sau thời gian bỏ công nghiên cứu, bạn sẽ không còn thờ ơ nhìn vào những bảng quảng cáo, bìa sách, hay quyển tạp chí theo cách cũ. Rồi bạn sẽ bắt đầu chụp ảnh các biển báo trên đường thay vì chụp phong cảnh, chú ý đến cách trình bày thực đơn thay cho các món ăn và dành cả tuần lễ chỉ để tỉ mẩn lựa chọn kiểu chữ cho tiêu đề bài thuyết trình sắp tới. Nhưng bạn sẽ thấy tất cả thật đáng công, bởi nghiên cứu đã chứng minh, kiểu chữ và hình thức trình bày ảnh hưởng rất lớn đến cách ta đọc và những gì ta nhớ." ],

    [ "two_column", font_size_S, "Running text, columns", "Typography là một phần quan trọng của các sản phẩm in ấn như sách, báo, và tạp chí. Sử dụng nhuần nhuyễn kỹ thuật typography giúp ấn phẩm trở nên nổi bật, hấp dẫn và tạo được thương hiệu riêng với độc giả. Một số tạp chí nổi tiếng trên thế giới như The Guardian, The Economist, USA Today, The New York Times đều có người thiết kế typography để sáng tạo kiểu chữ riêng nhắm đến khách hàng mục tiêu của họ.\n\nTờ USA Today mang phong cách táo bạo, đầy màu sắc và tương đối hiện đại nhờ sử dụng một loạt các phông chữ với màu sắc và kích cỡ khác nhau, tên ấn phẩm in hoa trên nền có màu. Trái lại, The New York Times sử dụng phương pháp tiếp cận truyền thống hơn với ít màu, ít kiểu chữ, và nhiều cột.\n\nTrong lĩnh vực quảng cáo, typography tốt giúp xây dựng bản sắc riêng cho sản phẩm, dịch vụ. Sắp xếp kiểu chữ cũng quan trọng như việc chọn lựa màu sắc, hình ảnh khi thiết kế hệ thống nhận diện thương hiệu. Sự khác nhau giữa các kiểu chữ có thể tạo nên hình ảnh tương phản giữa một công ty chuyên nghiệp và không chuyên. Một trong những yếu tố khiến phong cách của Apple luôn được đánh giá cao là nhờ phông chữ Myriad Pro sử dụng thống nhất từ năm 2002 đến nay. Apple thành công với font Myriad Pro. Năm 2006, một thử nghiệm nổi tiếng về typography được thực hiện bởi Phil Renaud một sinh viên ngành thiết kế đại học Windsor (Canada). Trong suốt sáu học kỳ, Renaud thực hiện 52 bài tiểu luận bằng ba phông chữ khác nhau: Times New Roman, Trebuchet MS, và Georgia để gửi cho các giáo sư. Kết quả cho thấy, với cùng nội dung, kiểu chữ ảnh hưởng đáng kể đến điểm số đạt được.\n\nGeorgia cho điểm số tốt nhất. Trebuchet có vẻ thích hợp để viết blog hơn là một bài viết học thuật. Kết quả này cũng phù hợp với một nghiên cứu năm 1998 của Đại học Carnegie Mellon khẳng định, phông Georgia được đánh giá là sắc nét, dễ chịu và dễ đọc hơn cả phông chữ thông dụng Times New Roman.\n\nVận dụng tốt typography không chỉ giúp người đọc tập trung, dễ hiểu, tăng năng suất làm việc, mà còn có thể thuyết phục họ tin vào một thông điệp nào đó. Trái lại, cẩu thả khi trình bày văn bản đôi khi gây hậu quả khó lường, như sự cố Comic Sans vừa xảy ra với các chuyên gia tại Trung tâm Nghiên cứu Hạt nhân châu Âu (CERN) trong năm qua." ]

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
            line_height = font_size * 1.1
            lineHeight(line_height)
            tracking(tracking_amount)
            translate(0, -fontCapHeight())
            baselineShift(-(y_cord["1"]-20))
            textBox(proof_set, (edge_left, y_cord["0"], margin_left_right, margin_top_bottom), align="left")
            
        elif font_size == font_size_M:
            type_style()
            fontSize(font_size)
            line_height = font_size * 1.1
            lineHeight(line_height)
            tracking(tracking_amount)
            translate(0, -(line_height / 4))
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
            fontSize(font_size)
            line_height = 16
            lineHeight(line_height)
            translate(0, -fontCapHeight())
            textBox("Typography là một phần quan trọng của các sản phẩm in ấn như sách, báo, và tạp chí. Sử dụng nhuần nhuyễn kỹ thuật typography giúp ấn phẩm trở nên nổi bật, hấp dẫn và tạo được thương hiệu riêng với độc giả. Một số tạp chí nổi tiếng trên thế giới như The Guardian, The Economist, USA Today, The New York Times đều có người thiết kế typography để sáng tạo kiểu chữ riêng nhắm đến khách hàng mục tiêu của họ.\n\nTờ USA Today mang phong cách táo bạo, đầy màu sắc và tương đối hiện đại nhờ sử dụng một loạt các phông chữ với màu sắc và kích cỡ khác nhau, tên ấn phẩm in hoa trên nền có màu. Trái lại, The New York Times sử dụng phương pháp tiếp cận truyền thống hơn với ít màu, ít kiểu chữ, và nhiều cột.\n\nTrong lĩnh vực quảng cáo, typography tốt giúp xây dựng bản sắc riêng cho sản phẩm, dịch vụ. Sắp xếp kiểu chữ cũng quan trọng như việc chọn lựa màu sắc, hình ảnh khi thiết kế hệ thống nhận diện thương hiệu. Sự khác nhau giữa các kiểu chữ có thể tạo nên hình ảnh tương phản giữa", (((x_cord["1"])-20), (y_cord["5"]), ((x_cord["5"])+30), (y_cord["40"])), align="left")
            
            # Column 2
            textBox("một công ty chuyên nghiệp và không chuyên. Một trong những yếu tố khiến phong cách của Apple luôn được đánh giá cao là nhờ phông chữ Myriad Pro sử dụng thống nhất từ năm 2002 đến nay. Apple thành công với font Myriad Pro. Năm 2006, một thử nghiệm nổi tiếng về typography được thực hiện bởi Phil Renaud một sinh viên ngành thiết kế đại học Windsor (Canada). Trong suốt sáu học kỳ, Renaud thực hiện 52 bài tiểu luận bằng ba phông chữ khác nhau: Times New Roman, Trebuchet MS, và Georgia để gửi cho các giáo sư. Kết quả cho thấy, với cùng nội dung, kiểu chữ ảnh hưởng đáng kể đến điểm số đạt được.\n\nGeorgia cho điểm số tốt nhất. Trebuchet có vẻ thích hợp để viết blog hơn là một bài viết học thuật. Kết quả này cũng phù hợp với một nghiên cứu năm 1998 của Đại học Carnegie Mellon khẳng định, phông Georgia được đánh giá là sắc nét, dễ chịu và dễ đọc hơn cả phông chữ thông dụng Times New Roman.\n\nVận dụng tốt typography không chỉ giúp người đọc tập trung, dễ hiểu, tăng năng suất làm việc, mà còn có thể ", ((x_cord["7"]-20), (y_cord["5"]), ((x_cord["5"])+30), (y_cord["40"])), align="left")
            
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
 

    