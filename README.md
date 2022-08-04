# letterProofer


## Description
Currently, this script is frankensteined atrocity. 
It only works through the DrawBot extension in Robofont. 
</br> 
</br> 
Made to speed up proofing and prototyping type.
</br> 
Hope to improve upon it when I have the chance.
</br> 
</br> 
It works by collecting every ufo in a designated path labeled 'font_folder' and iterates a loop of text strings for each .ufo
</br>
There is a optional (commented out) snippet to save a PDF in a folder by current output date (YYYY-MM-DD) in a designated path labeled 'proof_folder'
</br> 
- If the folder exists, it will not create one and will only save the PDF
- If the folder doesn't exist, it will create one and then save the PDF
- If the PDF already exists it will NOT overwrite, but number it and save the PDF
</br> 
Each script is a separate proof but has the same general feel.
I tried to automate as much as possible but there are a bunch of variables you can set for your own personal use.
</br> 
</br> 
The script uses AdobeBlank as a fallback so that glyphs not in your font are not displayed. 
You can find AdobeBlank here: https://github.com/adobe-fonts/adobe-blank

## Credits
Special thanks to Connor Davenport, Colin Ford, Ben Kiel for answering python questions.
</br>
</br> 
Spliced together and made possible by the following scripts/resources:
</br> 
DrawBot Proof on Robofont site:
https://robofont.com/documentation/tutorials/making-proofs-with-drawbot/?highlight=proof
</br> 
Proof documents by Dunwich Type:
https://github.com/DunwichType/DTF_Proofs
</br> 
Proof documents by Manic Type
</br> 
Automated Proofs by Matthew Smith:
https://github.com/mttymtt/DrawBot-Sketchbook/tree/master/Proofing/automated_proofs_01
