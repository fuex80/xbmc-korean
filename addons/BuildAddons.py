import os
import md5
import glob
import zipfile
import shutil
from xml.etree import ElementTree
import Tkinter, tkFileDialog

def main():
    addons_repo = (r"D:\xbmc-korean\xbmc-korea-addons\addons\dharma" )
    #addon_packager(addons_repo)
    generate_addons_xml(addons_repo)
    generate_md5_file(addons_repo)

def addon_packager(addons_repo):
    if (not os.path.exists(addons_repo)):
        print ("Please set Addon Repo path properly")
        # fix:  need to stop script here
    addon_path = addon_selector();
    addon_id=os.path.basename(addon_path)
    add_version =addon_ver(addon_path, addon_id)
    if (not os.path.exists(os.path.join(addons_repo, addon_id))):
        os.mkdir(os.path.join(addons_repo, addon_id))
        print ("Directory for addon in Repo is not exist, Making new one...")
    for filename in glob.glob(os.path.join(addons_repo, addon_id, '*')) :
        os.remove( filename )

    zipper(addon_id, os.path.join(addons_repo, addon_id, addon_id + '-' + add_version + '.zip'))
    shutil.copyfile(os.path.join(addon_id, 'changelog.txt'), os.path.join(addons_repo, addon_id, 'changelog'+ '-' + add_version + '.txt'))
    shutil.copyfile(os.path.join(addon_id, 'icon.png'), os.path.join(addons_repo, addon_id, 'icon.png'))
    print ("Packaged addon is placed in Addon repo\n")

def addon_selector():
    addons_path=os.getcwd()
    addons = os.listdir(addons_path)
    addon_num = 0
    for addon in addons:
        if ( os.path.isdir( addon ) and addon != ".svn" ):
            addon_num = addon_num +1
    addon_lists = ['']*(addon_num+1)
    print("0.Custom Addon Path")
    addon_num = 0
    for addon in addons:
        if ( os.path.isdir( addon ) and addon != ".svn" ):
            addon_num = addon_num +1
            print (str(addon_num) + '.' + addon)
            addon_lists[addon_num] = addon
    addon_selnum = raw_input("Choose an addon: ")
    if (int(addon_selnum)==0):
        root = Tkinter.Tk()
        addon_path=tkFileDialog.askdirectory(parent=root,title='Please select a directory')
        root.withdraw()
        addon_id=os.path.basename(addon_path)
    else:
        addon_id=addon_lists[int(addon_selnum)]
        addon_path=os.path.join(addons_path, addon_id)
    print ("you select " + addon_id + "\n")
    return addon_path

def addon_ver(addon_path, addon_id):
    tree = ElementTree.parse(addon_path + "\\addon.xml")
    add_root = tree.getroot()
    add_version = add_root.attrib['version']
    add_id = add_root.attrib['id']
    if (not add_id == addon_id):
        print (" Addon ID is not matched with addon directory name, please check !")
        # fix:  need to stop script here
    else:
        print ("Processing " + addon_id + " version " + add_version + "\n")
    return add_version

def zipper(dir, zip_file):
    zip = zipfile.ZipFile(zip_file, 'w')
    root_len = len(os.path.abspath(dir))+1
    for root, dirs, files in os.walk(dir):
        if ( not ".svn" in root):
            archive_root = os.path.join(dir, os.path.abspath(root)[root_len:])
            for f in files:
                fullpath = os.path.join(root, f)
                archive_name = os.path.join(archive_root, f)
                zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file

def generate_addons_xml(addons_repo):
    print ("Generating addons.xml from current addon files in repo\n")
    addons = os.listdir(addons_repo)
    addons_root=ElementTree.Element("addons")
    for addon in addons:
        try:
            # skip any file or .svn folder
            if ( not os.path.isdir( os.path.join(addons_repo, addon) ) or addon == ".svn" ): continue
            addon_zfilename = glob.glob(os.path.join( addons_repo, addon, '*.zip' ))
            addon_zfile = zipfile.ZipFile(addon_zfilename[0], "r" )
            zip_addon_xml = addon_zfile.open(addon + '/addon.xml')
            addon_xml = ElementTree.parse(zip_addon_xml).getroot()
            addons_root.append(addon_xml)
        except:
            print ("Problems Found. skipping", addon)
    indent(addons_root)
    addons_xml=ElementTree.ElementTree(addons_root)
    addons_xml.write(os.path.join(addons_repo,'addons.xml'), encoding="UTF-8")

def generate_md5_file(addons_repo):
    # create a new md5 hash
    m = md5.new( open(os.path.join(addons_repo, "addons.xml") ).read() ).hexdigest()
    # save file
    open(os.path.join(addons_repo, 'addons.xml.md5'), "w" ).write(m)

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

if __name__ == '__main__':
    main()
