# XML to CSV converter, XML generated from Promax Ranger Neo Signal Coverage tool
Converts xml files generated by Promax Ranger Neo Signal coverage tool to csv file.

Although users of Promax Ranger Neo are offered to convert xml files at their website https://www.promax.es/tools/kml-generator/settings/ I decided to create my own CSV converter.

One reason is that I want to extract some of the data parameters that the website does not. Second I could easily convert xml files offline and finally I can convert multiple files at once.

I am using lxml to parse the data and pandas to convert it to csv.

I added a code to generate a 10 random XML files stored in test_xml folder to test the converter.

I also have the different csv output for the different configuration of the converter.