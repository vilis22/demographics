import xml.etree.ElementTree as ET

tree = ET.parse('tbl_district.xml')
root = tree.getroot()

for district in root.findall('.//tbl_district'):
    print(f"{district.find('district').text}. {district.find('name_district').text}")
    