# Digital Derge Kangyur

Welcome to the working repository of the ongoing 2014-2018 Esukhia-Barom proofreading project!

The Digital Derge Kangyur you'll find on our repository is based on the UVA-SOAS 2013 eKangyur and is currently undergoing many changes -- use at your own risk!

## The 2013 UVA-SOAS eKangyur

The UVA-SOAS 2013 eKangyur was created by diff-proofreading the previous UVA input against BDRC's OCRed etexts, ACIP's etexts, and Adharsha's early etexts; in a 2013 project overviewed by [UVA](http://www.virginia.edu/) and funded by [SOAS](https://www.soas.ac.uk/) and [KF](https://khyentsefoundation.org/) (for [84000](http://84000.co/)). This version is currently published on UVA, Adharsha, BDRC, and as part of SOAS's ACTIB corpus.

It was intended as an exact representation of the Derge Kangyur edition help by the Library of Congress ([available on BDRC](https://www.tbrc.org/#!rid=W4CZ5369)). As an exact representation it preserved the likes of spelling mistakes, carving mistakes, archaic spellings and mistakes caused by wood-block damage.

## The Esukhia-Barom annotated edition

The current digital version is an attempt at using linguistics and informatics to improve and normalize the digital Kangyur while preserving the spelling of the Derge woodblocks.

For more information on the workflow please refer to:
* [Project Description](https://docs.google.com/document/d/17RGGczT9bZl5Hoy7Z6Avo-xympw6eFDeHlecrdVadkM/edit?usp=sharing)
* [Compared-Proofreading Workflow](https://docs.google.com/document/d/1BobLBqSRvyOCissiYx9kCprbJsU5YDFpKf0NzPkX_Aw/edit?usp=sharing)

## Image Sources

Each time an issue is found, our team checks the [LOC scans](https://www.tbrc.org/#!rid=W4CZ5369) and sometimes falls back on the [edition printed by the 16th Karmapa](https://www.tbrc.org/#!rid=W22084) in case of missing pages or unreadable passages. The Karmapa edition isn't used as a main source because it was retouched with marker pens before printing in Delhi.

LOC scan:
[![c](https://user-images.githubusercontent.com/17675331/43990148-21cbc09a-9d8a-11e8-8543-a9b9bbf17575.png)](http://iiif.bdrc.io/image/v2/bdr:V4CZ5369_I1KG9159::I1KG91590494.jpg/full/full/0/default.jpg)
Karmapa edition:
[![d](https://user-images.githubusercontent.com/17675331/43990149-22e786d0-9d8a-11e8-9ad3-8557a397232f.png)](http://iiif.bdrc.io/image/v2/bdr:V22084_I0918::09180494.tif/full/full/0/default.jpg)

Other interesting differences appear on:
- vol. 83, page 190a (end of the 6th line)
- vol. 75, page 119a (third syllable)
- vol. 33, page 246b (end of first line)

## Format

The texts contain the following structural markup at beginning of lines:

* **[1b]** is _[Page and folio markers]_
* **[1b.1]** is _[Page and folio markers.line number]_

We follow the page numbers indicated in the original, this means that sometimes the page numbers go back to 1a (ex: vol. 31 after p. 256). Pages numbers that appear twice in a row are indicated with an `x`, example in volume 102: `[355xa]`.

They also contain a few error suggestions noted as example. It is far from an exhausted list of the issues found in the original, the staff was actually discouraged to add these.

* **(X,Y)** is _(potential error, correction suggestion)_ , example: `མཁའ་ལ་(མི་,མེ་)ཏོག་དམར་པོ་`

* **[X]** signals obvious errors or highly suspicious spellings (ex: `མཎྜལ་ཐིག་[ལ་]ལྔ་པ་ལ།`), or un-transcribable characters
* **#** signals an unreadable graphical unit
* **{TX}** signals the beginning of the text with Tohoku catalog number **X**. We use the following conventions:
  * when a text is missing from the Tohoku catalog, we indicate it with the preceding number followed by **a**, ex: **T7**, **T7a**, **T8**
  * when a text has subindexes, we separate them with a dash, ex: **T841-1**, **T841-2**, etc. The source of the subindexes are 84000, Adarsha and *The Nyingma Edition of the sDe dGe bKa' 'Gyur and bsTan 'Gyur: Research Catalogue and Bibliography*.

The end of lines sometimes are preceded by a space character (when they end with a shad) so that the result of appending all the lines content is useabletext is correct.

## Encoding

### Unicode

The files are UTF8 with no BOM, in [NFD](http://unicode.org/reports/tr15/). The following representations are used:

 - `\u0F68\u0F7C\u0F7E` (`ཨོཾ`) is used instead of `\u0F00` (`ༀ`)
 - `\u0F62\u0FB1` (`རྱ`) is used instead of `\u0F6A\u0FB1` (`ཪྱ`)
 - `\u0F62\u0F99` (`རྙ`) is used instead of `\u0F6A\u0F99` (`ཪྙ`)
 - `\u0F62\u0FB3` (`རླ`) is used instead of `\u0F6A\u0FB3` (`ཪླ`)
 - `\u0F6A\u0FBB` (`ཪྻ`) is used for the most common form instead of `\u0F62\u0FBB` (`རྻ`)
 - `\u0FB0` is used instead of `\u0F71` in the 3 cases where it precedes yata `\u0FB1`
 - `\u0F74\u0F72` is used instead of `\u0F72\u0F74` in the few cases where both a shabkyu and a gigu are present

### Punctuation

We apply the following normalization without keeping the original in parenthesis:
 - `༄༅། །` at beginning of pages are removed (, )they should be straightforward to reinsert
 - `༄༅། །` are also removed at beginning of volumes when the beginning of a volume is in the middle of a text
 - `༑` are replaced by `།`

We keep the original punctuation in parenthesis (see above) but normalize the following:
 - `༄༅། །` are added at beginning of texts when they're missing
 - `ག། །།` instead of `ག།། །།`, or with any character conforming `[གཀཤ][ོེིུ]?` instead of ག
 - a tshek is inserted between characters conforming `ང[ོེིུ]?` and `།`

## Volume numbers

Each physical volume is one file. We follow the volume order of the Parphud edition ; in the LoC edition, the main difference is that vol. 102 (of Parphud) is before vol. 100 (of Parphud).

## Page numbering issues

- vol. 41, page 33 is duplicated
- vol. 48, page 211 was skipped (both #210 and #211 are written on 210a as ང་ ཉིས་བརྒྱ་ བཅུ་ བཅུ་གཅིག་)
- vol. 77, page 21b, 22a are blank (#22 is written on 22b)
- vol. 77, page 150b, 151a are blank (#151 is written on 151b)
- vol. 77, page 212b, 213a are blank (#213 is written on 213b)
- vol. 86, page 93 is doubled (marked as གོ་གསུམ་གོང་མ་ on 93a/93b and གོ་གསུམ་འོག་མ་ on 93xa/93xb)
- vol. 86, page 261 was skipped (#260 marked as ཉིས་བརྒྱ་དྲུག་ཅུ on 260a and #261 as ཉིས་བརྒྱ་ རེ་གཅིག་ རྒྱུད་འབུམ་ on 260b)
- vol. 90, page 63 was skipped
- vol. 93, page 205 was skipped (#204 marked as ཉིས་བརྒྱ་བཞི་ རྒྱུད་འབུམ་ on 204a and #205 as ཉིས་བརྒྱ་ལྔ་ རྒྱུད་འབུམ་ on 204b)
- vol. 100, page 57 was skipped (#56 marked as ང་དྲུག་ གཟུངས་བསྡུས་ on 56a and #57 as ང་བདུན་ གཟུངས་བསྡུས་ on 56b)

## Completion status

The catalog, volume 103, wasn't digitized as part of this project since it isn't Buddha's words and probably won't be translated by 84,000. Esukhia is hoping to prepare it towards the end of 2018.

## TEI Export

You can find a script in the `scripts/` directory to validate the files and export into a TEI format that can be ingested by BDRC. Other exports should be straightforward taking this script as a template. Note that it exports the volumes in the LoC order.

## Export works

In order to export each work in a different file, run:

        cd scripts/
        python3 export_works.py

The output will be in `scripts/export`.

The volume in which the work is found(the filename) is added on two occasions:
at the beginning of each work and when there is a volume change within a single work.

To get the raw text with no markup, run `python3 export_works.py --clean-content true`.

# Feedback

The files are on Github hoping they'll improve, don't hesitate to signal errors with a pull request!

# How to cite

Use the following statemnent or the [bibtex](https://github.com/Esukhia/derge-kangyur/blob/master/derge-kangyur.bib) file.
    
     ཆོས་ཀྱི་འབྱུང་གནས། [1721–31], བཀའ་འགྱུར་སྡེ་དགེ་པར་མ།, Etexts from UVA, BDRC OCR, ACIP, and Adarsha combined and further proofread by Esukhia, 2012-2018, https://github.com/Esukhia/derge-kangyur

# License

This work is a mechanical reproduction of a Public Domain work, and as such is also in the Public Domain.
